# NexForge - Full Database Schema (live dump)

Generated from the live PostgreSQL (Supabase) database.

```
TOTAL TABLES: 36
auth_group, auth_group_permissions, auth_permission, auth_user, auth_user_groups, auth_user_user_permissions, authtoken_token, blog_blogcategory, blog_blogpost, careers_jobapplication, careers_jobopening, contact_enquiry, content_award, content_download, content_faq, content_galleryitem, content_testimonial, core_client, core_industry, core_technology, django_admin_log, django_content_type, django_migrations, django_session, projects_beforeaftergallery, projects_project, projects_project_technologies, projects_projectdeliverable, projects_projectgallery, projects_projectmilestone, projects_projectvideo, services_service, services_service_industries, services_service_technologies, services_servicebenefit, services_servicedeliverable

==================================================================
TABLE: auth_group
------------------------------------------------------------------
  id                         integer                  NOT NULL
  name                       character varying(150)   NOT NULL
  PK: id

==================================================================
TABLE: auth_group_permissions
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  group_id                   integer                  NOT NULL
  permission_id              integer                  NOT NULL
  FK: permission_id -> auth_permission.id
  FK: group_id -> auth_group.id
  PK: id

==================================================================
TABLE: auth_permission
------------------------------------------------------------------
  id                         integer                  NOT NULL
  name                       character varying(255)   NOT NULL
  content_type_id            integer                  NOT NULL
  codename                   character varying(100)   NOT NULL
  FK: content_type_id -> django_content_type.id
  PK: id

==================================================================
TABLE: auth_user
------------------------------------------------------------------
  id                         integer                  NOT NULL
  password                   character varying(128)   NOT NULL
  last_login                 timestamp with time zone NULL
  is_superuser               boolean                  NOT NULL
  username                   character varying(150)   NOT NULL
  first_name                 character varying(150)   NOT NULL
  last_name                  character varying(150)   NOT NULL
  email                      character varying(254)   NOT NULL
  is_staff                   boolean                  NOT NULL
  is_active                  boolean                  NOT NULL
  date_joined                timestamp with time zone NOT NULL
  PK: id

==================================================================
TABLE: auth_user_groups
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  user_id                    integer                  NOT NULL
  group_id                   integer                  NOT NULL
  FK: group_id -> auth_group.id
  FK: user_id -> auth_user.id
  PK: id

==================================================================
TABLE: auth_user_user_permissions
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  user_id                    integer                  NOT NULL
  permission_id              integer                  NOT NULL
  FK: permission_id -> auth_permission.id
  FK: user_id -> auth_user.id
  PK: id

==================================================================
TABLE: authtoken_token
------------------------------------------------------------------
  key                        character varying(40)    NOT NULL
  created                    timestamp with time zone NOT NULL
  user_id                    integer                  NOT NULL
  FK: user_id -> auth_user.id
  PK: key

==================================================================
TABLE: blog_blogcategory
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(120)   NOT NULL
  slug                       character varying(50)    NOT NULL
  PK: id

==================================================================
TABLE: blog_blogpost
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  created_at                 timestamp with time zone NOT NULL
  updated_at                 timestamp with time zone NOT NULL
  title                      character varying(200)   NOT NULL
  slug                       character varying(50)    NOT NULL
  summary                    text                     NOT NULL
  body                       text                     NOT NULL
  featured_image             character varying(100)   NULL
  is_featured                boolean                  NOT NULL
  published_at               timestamp with time zone NULL
  author_id                  integer                  NULL
  category_id                bigint                   NOT NULL
  FK: author_id -> auth_user.id
  FK: category_id -> blog_blogcategory.id
  PK: id

==================================================================
TABLE: careers_jobapplication
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(150)   NOT NULL
  email                      character varying(254)   NOT NULL
  phone                      character varying(20)    NOT NULL
  resume                     character varying(100)   NOT NULL
  cover_letter               text                     NOT NULL
  status                     character varying(20)    NOT NULL
  created_at                 timestamp with time zone NOT NULL
  reviewed_by_id             integer                  NULL
  opening_id                 bigint                   NOT NULL
  FK: opening_id -> careers_jobopening.id
  FK: reviewed_by_id -> auth_user.id
  PK: id

==================================================================
TABLE: careers_jobopening
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(200)   NOT NULL
  slug                       character varying(50)    NOT NULL
  department                 character varying(120)   NOT NULL
  location                   character varying(150)   NOT NULL
  employment_type            character varying(20)    NOT NULL
  experience                 character varying(80)    NOT NULL
  description                text                     NOT NULL
  responsibilities           text                     NOT NULL
  requirements               text                     NOT NULL
  is_open                    boolean                  NOT NULL
  posted_at                  timestamp with time zone NOT NULL
  PK: id

==================================================================
TABLE: contact_enquiry
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(150)   NOT NULL
  email                      character varying(254)   NOT NULL
  phone                      character varying(20)    NOT NULL
  message                    text                     NOT NULL
  status                     character varying(20)    NOT NULL
  created_at                 timestamp with time zone NOT NULL
  assigned_to_id             integer                  NULL
  FK: assigned_to_id -> auth_user.id
  PK: id

==================================================================
TABLE: content_award
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(200)   NOT NULL
  year                       integer                  NOT NULL
  description                text                     NOT NULL
  image                      character varying(100)   NULL
  PK: id

==================================================================
TABLE: content_download
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(200)   NOT NULL
  file                       character varying(100)   NOT NULL
  type                       character varying(20)    NOT NULL
  created_at                 timestamp with time zone NOT NULL
  PK: id

==================================================================
TABLE: content_faq
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  question                   character varying(255)   NOT NULL
  answer                     text                     NOT NULL
  category                   character varying(20)    NOT NULL
  order                      integer                  NOT NULL
  is_active                  boolean                  NOT NULL
  PK: id

==================================================================
TABLE: content_galleryitem
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(180)   NOT NULL
  category                   character varying(80)    NOT NULL
  image                      character varying(100)   NOT NULL
  order                      integer                  NOT NULL
  PK: id

==================================================================
TABLE: content_testimonial
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  author_name                character varying(120)   NOT NULL
  designation                character varying(120)   NOT NULL
  quote                      text                     NOT NULL
  is_active                  boolean                  NOT NULL
  client_id                  bigint                   NULL
  FK: client_id -> core_client.id
  PK: id

==================================================================
TABLE: core_client
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(180)   NOT NULL
  slug                       character varying(50)    NOT NULL
  logo                       character varying(100)   NULL
  website                    character varying(200)   NOT NULL
  industry_id                bigint                   NULL
  FK: industry_id -> core_industry.id
  PK: id

==================================================================
TABLE: core_industry
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(120)   NOT NULL
  slug                       character varying(50)    NOT NULL
  icon                       character varying(100)   NULL
  PK: id

==================================================================
TABLE: core_technology
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  name                       character varying(120)   NOT NULL
  category                   character varying(80)    NOT NULL
  icon                       character varying(100)   NULL
  PK: id

==================================================================
TABLE: django_admin_log
------------------------------------------------------------------
  id                         integer                  NOT NULL
  action_time                timestamp with time zone NOT NULL
  object_id                  text                     NULL
  object_repr                character varying(200)   NOT NULL
  action_flag                smallint                 NOT NULL
  change_message             text                     NOT NULL
  content_type_id            integer                  NULL
  user_id                    integer                  NOT NULL
  FK: content_type_id -> django_content_type.id
  FK: user_id -> auth_user.id
  PK: id

==================================================================
TABLE: django_content_type
------------------------------------------------------------------
  id                         integer                  NOT NULL
  app_label                  character varying(100)   NOT NULL
  model                      character varying(100)   NOT NULL
  PK: id

==================================================================
TABLE: django_migrations
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  app                        character varying(255)   NOT NULL
  name                       character varying(255)   NOT NULL
  applied                    timestamp with time zone NOT NULL
  PK: id

==================================================================
TABLE: django_session
------------------------------------------------------------------
  session_key                character varying(40)    NOT NULL
  session_data               text                     NOT NULL
  expire_date                timestamp with time zone NOT NULL
  PK: session_key

==================================================================
TABLE: projects_beforeaftergallery
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  before_image               character varying(100)   NOT NULL
  after_image                character varying(100)   NOT NULL
  caption                    character varying(180)   NOT NULL
  order                      integer                  NOT NULL
  project_id                 bigint                   NOT NULL
  FK: project_id -> projects_project.id
  PK: id

==================================================================
TABLE: projects_project
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  created_at                 timestamp with time zone NOT NULL
  updated_at                 timestamp with time zone NOT NULL
  title                      character varying(200)   NOT NULL
  slug                       character varying(50)    NOT NULL
  status                     character varying(20)    NOT NULL
  location                   character varying(150)   NOT NULL
  project_value              character varying(80)    NOT NULL
  duration                   character varying(60)    NOT NULL
  team_size                  integer                  NULL
  overview                   text                     NOT NULL
  challenges                 text                     NOT NULL
  solution                   text                     NOT NULL
  thumbnail                  character varying(100)   NULL
  is_featured                boolean                  NOT NULL
  order                      integer                  NOT NULL
  client_id                  bigint                   NULL
  industry_id                bigint                   NOT NULL
  FK: client_id -> core_client.id
  FK: industry_id -> core_industry.id
  PK: id

==================================================================
TABLE: projects_project_technologies
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  project_id                 bigint                   NOT NULL
  technology_id              bigint                   NOT NULL
  FK: project_id -> projects_project.id
  FK: technology_id -> core_technology.id
  PK: id

==================================================================
TABLE: projects_projectdeliverable
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(180)   NOT NULL
  project_id                 bigint                   NOT NULL
  FK: project_id -> projects_project.id
  PK: id

==================================================================
TABLE: projects_projectgallery
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  image                      character varying(100)   NOT NULL
  caption                    character varying(180)   NOT NULL
  order                      integer                  NOT NULL
  project_id                 bigint                   NOT NULL
  FK: project_id -> projects_project.id
  PK: id

==================================================================
TABLE: projects_projectmilestone
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(200)   NOT NULL
  description                text                     NOT NULL
  date                       date                     NULL
  order                      integer                  NOT NULL
  project_id                 bigint                   NOT NULL
  FK: project_id -> projects_project.id
  PK: id

==================================================================
TABLE: projects_projectvideo
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  video_url                  character varying(200)   NOT NULL
  title                      character varying(150)   NOT NULL
  project_id                 bigint                   NOT NULL
  FK: project_id -> projects_project.id
  PK: id

==================================================================
TABLE: services_service
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(200)   NOT NULL
  slug                       character varying(50)    NOT NULL
  short_description          text                     NOT NULL
  detailed_description       text                     NOT NULL
  icon                       character varying(100)   NULL
  is_active                  boolean                  NOT NULL
  order                      integer                  NOT NULL
  PK: id

==================================================================
TABLE: services_service_industries
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  service_id                 bigint                   NOT NULL
  industry_id                bigint                   NOT NULL
  FK: industry_id -> core_industry.id
  FK: service_id -> services_service.id
  PK: id

==================================================================
TABLE: services_service_technologies
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  service_id                 bigint                   NOT NULL
  technology_id              bigint                   NOT NULL
  FK: service_id -> services_service.id
  FK: technology_id -> core_technology.id
  PK: id

==================================================================
TABLE: services_servicebenefit
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  text                       character varying(200)   NOT NULL
  service_id                 bigint                   NOT NULL
  FK: service_id -> services_service.id
  PK: id

==================================================================
TABLE: services_servicedeliverable
------------------------------------------------------------------
  id                         bigint                   NOT NULL
  title                      character varying(180)   NOT NULL
  service_id                 bigint                   NOT NULL
  FK: service_id -> services_service.id
  PK: id
```

---

# Proposed / Phase-2 Tables (NOT YET CREATED)

> **Status: design only.** None of the tables below exist in the live database
> yet. They are a proposed target for the larger enterprise scope (full CRM,
> support/ticketing, notifications, analytics). Do **not** run these against
> production without first creating the matching Django models + migrations.
>
> **Reality check on the "85% complete" claim:** that figure measures the build
> against a much bigger enterprise platform that was never the agreed scope.
> Measured against the **NexForge content pack** (the actual brief), the live
> schema is effectively complete. So "85%" is true only for the *aspirational*
> super-scope, not for what was contracted.

## Verdict per proposed table

| Proposed table | Verdict | Reason |
|----------------|---------|--------|
| `sales_enquiries` | ❌ **Redundant** | Duplicate of existing `contact_enquiry`. Do not create a second leads table. |
| `crm_leads` | ⚠️ **Overlaps** | An enquiry *is* a lead. Evolve `contact_enquiry` (add fields / a related pipeline) rather than a parallel table. |
| `crm_customers` | ⚠️ **Overlaps** | Existing `core_client` already represents customers. Extend it, don't duplicate. |
| `crm_lead_assignments` | ✅ New | Valid if you build a true pipeline (history of who owned a lead). |
| `crm_meetings` | ✅ New | Valid pipeline activity record. |
| `crm_proposals` | ✅ New | Valid pipeline stage. |
| `crm_negotiations` | ✅ New | Valid, though could be a status on a proposal. |
| `crm_lost_reasons` | ✅ New | Small lookup; useful for win/loss reporting. |
| `project_updates` | ✅ New | Progress updates per project; nothing equivalent exists. |
| `support_tickets` | ✅ New | Whole support module is missing today. |
| `support_assignments` | ✅ New | Ticket ownership history. |
| `support_engineers` | ⚠️ **Overlaps** | Likely just `auth_user` + a Group/role. Only needs a table if engineers have data beyond a user. |
| `ticket_comments` | ✅ New | Threaded replies on a ticket. |
| `visitors` | ⚠️ **Caution** | Anonymous visitor tracking is normally done by **Google Analytics** (already wired), not stored in Postgres. Heavy + privacy load. |
| `page_views` | ⚠️ **Caution** | Same as above. High write volume; prefer GA / a dedicated analytics store. |
| `user_sessions` | ⚠️ **Name clash** | Django already has `django_session`. If you mean analytics sessions, name it differently (e.g. `visit_sessions`). |
| `project_brochures` | ⚠️ **Overlaps** | Existing `content_download` already serves downloadable docs. Fold in or relate. |
| `brochure_downloads` | ✅ New (small) | A download-event log is valid if you want per-download analytics. |
| `notifications` | ✅ New | In-app notification feed; nothing exists. Pairs with the (not-built) async layer. |
| `audit_logs` | ⚠️ **Partial** | Django already has `django_admin_log` for admin actions. A broader app-level audit log is additive. |
| `dashboard_metrics` | ⚠️ **Optional** | The admin dashboard computes counts live today. Only add a metrics cache table if those queries get slow. |
| `content_media` | ⚠️ **Partial** | Images already live as file paths on each model. A central media library is a real CMS upgrade but optional. |

**Summary: ~10 of 22 are genuinely new and worth building; ~12 are redundant,
overlapping, or better handled another way.** Build the new ones as proper
Django apps (`crm`, `support`, `notifications`) when those modules are approved.

## Proposed DDL (PostgreSQL) — for the NEW tables only

```sql
-- ============ CRM (extends contact_enquiry, does not replace it) ============
CREATE TABLE crm_lead_assignments (
    id            BIGSERIAL PRIMARY KEY,
    enquiry_id    BIGINT NOT NULL REFERENCES contact_enquiry(id) ON DELETE CASCADE,
    assigned_to_id INTEGER NOT NULL REFERENCES auth_user(id),
    assigned_by_id INTEGER REFERENCES auth_user(id),
    assigned_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    note          TEXT NOT NULL DEFAULT ''
);

CREATE TABLE crm_meetings (
    id          BIGSERIAL PRIMARY KEY,
    enquiry_id  BIGINT NOT NULL REFERENCES contact_enquiry(id) ON DELETE CASCADE,
    scheduled_at TIMESTAMPTZ NOT NULL,
    mode        VARCHAR(20) NOT NULL DEFAULT 'online',  -- online/onsite/call
    summary     TEXT NOT NULL DEFAULT '',
    created_by_id INTEGER REFERENCES auth_user(id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE crm_proposals (
    id          BIGSERIAL PRIMARY KEY,
    enquiry_id  BIGINT NOT NULL REFERENCES contact_enquiry(id) ON DELETE CASCADE,
    title       VARCHAR(200) NOT NULL,
    amount      NUMERIC(14,2),
    currency    VARCHAR(8) NOT NULL DEFAULT 'INR',
    document    VARCHAR(100),                 -- file path
    status      VARCHAR(20) NOT NULL DEFAULT 'draft',
    sent_at     TIMESTAMPTZ,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE crm_negotiations (
    id          BIGSERIAL PRIMARY KEY,
    proposal_id BIGINT NOT NULL REFERENCES crm_proposals(id) ON DELETE CASCADE,
    round       INTEGER NOT NULL DEFAULT 1,
    note        TEXT NOT NULL DEFAULT '',
    revised_amount NUMERIC(14,2),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE crm_lost_reasons (
    id    BIGSERIAL PRIMARY KEY,
    label VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE project_updates (
    id          BIGSERIAL PRIMARY KEY,
    project_id  BIGINT NOT NULL REFERENCES projects_project(id) ON DELETE CASCADE,
    title       VARCHAR(200) NOT NULL,
    body        TEXT NOT NULL DEFAULT '',
    posted_by_id INTEGER REFERENCES auth_user(id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============ Support / Ticketing ============
CREATE TABLE support_tickets (
    id          BIGSERIAL PRIMARY KEY,
    reference   VARCHAR(20) NOT NULL UNIQUE,   -- e.g. NF-000123
    name        VARCHAR(150) NOT NULL,
    email       VARCHAR(254) NOT NULL,
    phone       VARCHAR(20) NOT NULL DEFAULT '',
    subject     VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    priority    VARCHAR(20) NOT NULL DEFAULT 'normal',
    status      VARCHAR(20) NOT NULL DEFAULT 'open',  -- open/in_progress/resolved/closed
    assigned_to_id INTEGER REFERENCES auth_user(id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX support_tickets_status_idx ON support_tickets(status);

CREATE TABLE support_assignments (
    id          BIGSERIAL PRIMARY KEY,
    ticket_id   BIGINT NOT NULL REFERENCES support_tickets(id) ON DELETE CASCADE,
    engineer_id INTEGER NOT NULL REFERENCES auth_user(id),
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ticket_comments (
    id          BIGSERIAL PRIMARY KEY,
    ticket_id   BIGINT NOT NULL REFERENCES support_tickets(id) ON DELETE CASCADE,
    author_id   INTEGER REFERENCES auth_user(id),
    is_internal BOOLEAN NOT NULL DEFAULT false,
    body        TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============ Notifications (pairs with a future Celery/Redis async layer) ============
CREATE TABLE notifications (
    id          BIGSERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    verb        VARCHAR(120) NOT NULL,          -- "New enquiry", "Ticket assigned"
    url         VARCHAR(300) NOT NULL DEFAULT '',
    is_read     BOOLEAN NOT NULL DEFAULT false,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX notifications_user_unread_idx ON notifications(user_id, is_read);

-- ============ Analytics (PREFER Google Analytics; store in DB only if required) ============
CREATE TABLE brochure_downloads (
    id          BIGSERIAL PRIMARY KEY,
    download_id BIGINT NOT NULL REFERENCES content_download(id) ON DELETE CASCADE,
    ip_hash     VARCHAR(64) NOT NULL DEFAULT '',  -- hashed, never raw IP (privacy)
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
-- visitors / page_views / dashboard_metrics: recommend Google Analytics instead
-- of bespoke tables. If still required, model them in a dedicated `analytics`
-- app and partition page_views by month (high write volume).
```

> When any of these modules is approved, implement it as a Django app + models +
> migrations so this schema stays the **generated truth**, not hand-written SQL
> that can drift from the ORM.
