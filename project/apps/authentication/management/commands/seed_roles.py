from django.core.management.base import BaseCommand

from apps.authentication.models import Role


class Command(BaseCommand):

    help = "Seed default roles"

    def handle(self, *args, **kwargs):

        roles = [

            ("Administrator", "System Administrator"),

            ("HR Manager", "HR Dashboard"),

            ("Sales Manager", "Sales Dashboard"),

            ("Content Manager", "Content Dashboard"),

            ("Technical Support", "Support Dashboard"),

        ]

        for name, description in roles:

            Role.objects.get_or_create(

                name=name,

                defaults={

                    "description": description

                }

            )

        self.stdout.write(

            self.style.SUCCESS(

                "Roles seeded successfully."

            )

        )