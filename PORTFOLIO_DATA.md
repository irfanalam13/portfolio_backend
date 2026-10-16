# Portfolio section data in production

The portfolio's public content is served from Django/PostgreSQL. The Next.js app reads the existing section APIs for projects, skills, experience, education, and certifications, and reads profile, stats, services, navigation, and social links from `GET /api/core/homepage/`.

## Import the current JSON data

From the repository root, validate the current `frontend/src/data/*.json` files without a database connection:

```sh
cd backend
python manage.py import_portfolio_data --dry-run
```

After applying migrations in a release/deploy step, import the content:

```sh
python manage.py migrate
python manage.py import_portfolio_data
```

The command reads each section JSON file directly from `frontend/src/data/` when run from the repository. It is safe to re-run: stable slugs/natural keys update imported rows, it does not delete rows, and the whole import runs in a transaction. Admin-edited fields on imported records are overwritten by a future import of that record, so run it only when intentionally syncing the JSON source.

The backend Docker build context does not include the frontend directory. The backend image therefore contains a bundled `apps/core/seed_data/portfolio-seed.json` snapshot. In the image, the importer uses that snapshot by default. To deploy newer section JSON, mount/copy a directory containing files named `about.json`, `projects.json`, `skills.json`, `experience.json`, `education.json`, `achievement.json`, `certifications.json`, `navigations.json`, `services.json`, and/or `social-link.json`, then pass `--data-dir /path/to/data` to the import command after migration.

Run migrations and data import once as a deployment/release step, not from every web worker startup. Anonymous clients can read portfolio content; Django staff users manage writes through Django admin. API mutations for projects, experience, achievements, certifications, blog, and timeline require a staff user.

## Import mappings and caveats

- The three entries in `achievement.json` are summary-stat cards; they import to `SummaryStat`, not the awards/recognition model.
- Project legacy keys are normalized (`description`, `github`, `live`, and `image`) and the extra category/features/status/technologies/case-study values are preserved. IDs are not database IDs; project slugs are stable import keys.
- Year-only education, experience, and certification dates are stored as January 1 of that year. The frontend displays year-only values. “Present” or a blank end year is stored as a current record.
- Skill level labels are preserved exactly in `level_label`; the existing numeric chart value maps Beginner → 35, Intermediate → 65, Advanced → 90. These numbers are display-scale approximations, not measured scores.
- Social URLs containing `yourusername` are imported inactive and never exposed publicly. Replace those placeholders with real profile URLs before enabling them in admin.
- Referenced media URLs/paths are preserved, but the importer does not upload files. Make sure `/images/profile.jpg`, project/certificate images, and `/resume.pdf` are actually deployed in frontend `public/` or replace them with uploaded/hosted URLs. Missing source assets cannot be repaired by importing the database records.
- `contact.json` is currently empty and is ignored; contact form submissions continue to use the existing contact API.
