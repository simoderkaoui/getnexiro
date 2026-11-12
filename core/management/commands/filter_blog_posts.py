from django.core.management.base import BaseCommand
from core.models import BlogPost, Author

INDEXABLE_SLUGS = [
    'django-best-framework-enterprise-web-2026',
    'ui-ux-design-principles-convert-visitors-customers',
    'choose-right-tech-stack-startup-morocco',
]

class Command(BaseCommand):
    help = 'Filter and manage blog posts indexation status (keep high-authority posts indexed, noindex off-topic/thin posts).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reindex-all',
            action='store_true',
            help='Re-index all published posts.',
        )
        parser.add_argument(
            '--author-name',
            default='getNexiro Engineering Studio',
            help='Default author name for E-E-A-T attribution.',
        )

    def handle(self, *args, **options):
        reindex_all = options['reindex_all']

        # Ensure default Author exists
        author, created = Author.objects.get_or_create(
            slug='getnexiro-engineering-team',
            defaults={
                'name': options['author_name'],
                'role_en': 'Lead Software Architect & Engineering Team',
                'role_fr': 'Architecte Logiciel Principal & Équipe Ingénierie',
                'role_ar': 'كبير مهندسي البرمجيات وفريق التطوير',
                'bio_en': 'Senior software architects at getNexiro in Tangier, Morocco, specializing in Python/Django, Next.js, and cloud systems.',
                'bio_fr': 'Architectes logiciels seniors chez getNexiro à Tanger, spécialisés en Python/Django, Next.js et architectures cloud.',
                'bio_ar': 'كبار مهندسي البرمجيات في جيت نكسيرو بطنجة، متخصصون في بايثون/دجانغو ونكست والحوسبة السحابية.',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created default author profile: {author.name}"))

        posts = BlogPost.objects.all()
        kept_count = 0
        noindexed_count = 0

        for post in posts:
            # Assign author if missing
            if not post.author:
                post.author = author

            if reindex_all or post.slug in INDEXABLE_SLUGS:
                post.noindex = False
                post.index_in_sitemap = True
                post.save()
                kept_count += 1
                self.stdout.write(self.style.SUCCESS(f"  [INDEXED] {post.slug}"))
            else:
                post.noindex = True
                post.index_in_sitemap = False
                post.save()
                noindexed_count += 1
                self.stdout.write(self.style.WARNING(f"  [NOINDEX] {post.slug}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! {kept_count} posts indexed in search/sitemap, {noindexed_count} posts set to noindex."
        ))
