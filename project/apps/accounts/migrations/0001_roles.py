"""Create the five NexForge roles (Django Groups) and grant model permissions.

Roles are runtime-editable via the admin; this migration just seeds sensible
defaults aligned with the SRS access matrix. Re-runnable and reversible.
"""

from django.db import migrations

# role -> list of (app_label, model) it may fully manage (add/change/delete/view)
ROLE_MODELS = {
    "Administrator": "__all__",
    "Content Manager": [
        ("projects", "project"),
        ("projects", "projectgallery"),
        ("projects", "projectvideo"),
        ("projects", "projectdeliverable"),
        ("services", "service"),
        ("services", "servicebenefit"),
        ("services", "servicedeliverable"),
        ("blog", "blogpost"),
        ("blog", "blogcategory"),
        ("content", "faq"),
        ("content", "galleryitem"),
        ("content", "award"),
        ("content", "download"),
        ("content", "testimonial"),
        ("core", "industry"),
        ("core", "technology"),
        ("core", "client"),
    ],
    "Sales Manager": [("contact", "enquiry")],
    "Technical Support": [("contact", "enquiry")],
    "HR Manager": [],
}


def create_roles(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    for role, models in ROLE_MODELS.items():
        group, _ = Group.objects.get_or_create(name=role)
        if models == "__all__":
            group.permissions.set(Permission.objects.all())
            continue
        perms = []
        for app_label, model in models:
            perms.extend(
                Permission.objects.filter(
                    content_type__app_label=app_label,
                    content_type__model=model,
                )
            )
        if perms:
            group.permissions.set(perms)


def remove_roles(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=ROLE_MODELS).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("projects", "0001_initial"),
        ("services", "0001_initial"),
        ("blog", "0001_initial"),
        ("content", "0001_initial"),
        ("contact", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_roles, remove_roles)]
