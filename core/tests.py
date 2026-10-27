from decimal import Decimal
import datetime
from datetime import timedelta
from django.core import mail
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils.translation import activate
from django.utils import timezone
from core.models import (
    SiteConfig, Service, ServiceSolution, ProjectCategory, Project, ProjectImage,
    TeamMember, Testimonial, Stat, ContactMessage,
    CompanyValue, ProcessStep, StoreItem, BlogCategory, BlogPost,
    LegalPage, FAQ,
    Package, PackageFeature, PricingRule, QuoteRequest,
    WeeklyAvailability, Booking, Subscriber,
)
from core.forms import (
    ContactForm, QuoteStep1Form, QuoteStep2Form, QuoteStep3Form, QuoteStep4Form,
    BookingForm, SubscriberForm,
)


# ══════════════════════════════════════════════════════════════════
# Original Tests (Phases 1 & earlier)
# ══════════════════════════════════════════════════════════════════


class GetNexiroViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.config = SiteConfig.objects.create(
            site_name='getNexiro',
            hero_title_en='We Architect High-Velocity Digital Systems',
            hero_title_fr='Nous Concevons des Systèmes Numériques Haute-Performance',
            hero_title_ar='نصمم أنظمة رقمية عالية السرعة والأداء',
            email='getnexiro@gmail.com',
            phone='+212 663 017 817',
        )
        self.service = Service.objects.create(
            title_en='Web Development',
            title_fr='Développement Web',
            title_ar='تطوير مواقع الويب',
            description_en='Modern scalable websites.',
            icon='icon-web',
            is_featured=True,
            order=1,
        )
        self.category = ProjectCategory.objects.create(
            name_en='FinTech',
            name_fr='FinTech',
            name_ar='التكنولوجيا المالية',
            slug='fintech',
        )
        self.project = Project.objects.create(
            title_en='FinFlow Analytics',
            title_fr='FinFlow Analytics',
            title_ar='منصة FinFlow',
            category=self.category,
            description_en='Real-time financial dashboard',
            is_featured=True,
            order=1,
        )

    def test_home_page_en(self):
        activate('en')
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'getNexiro')
        self.assertContains(response, 'We Architect')

    def test_home_page_fr(self):
        activate('fr')
        response = self.client.get('/fr/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nous Concevons')

    def test_home_page_ar(self):
        activate('ar')
        response = self.client.get('/ar/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'نصمم')
        self.assertContains(response, 'dir="rtl"')

    def test_about_page(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)

    def test_services_page(self):
        response = self.client.get(reverse('core:services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Development')

    def test_projects_page(self):
        response = self.client.get(reverse('core:projects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'FinFlow Analytics')

    def test_project_detail_view(self):
        activate('en')
        response = self.client.get(reverse('core:project_detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'FinFlow Analytics')
        self.assertContains(response, 'Real-time financial dashboard')
        self.assertContains(response, 'Start a Similar Project')
        self.assertContains(response, 'Chat on WhatsApp')

    def test_project_detail_multilingual_ar(self):
        activate('ar')
        response = self.client.get(reverse('core:project_detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'منصة FinFlow')

    def test_project_detail_404_on_invalid_slug(self):
        response = self.client.get('/en/projects/non-existent-project/')
        self.assertEqual(response.status_code, 404)


    def test_blog_page(self):
        response = self.client.get(reverse('core:blog'))
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_page(self):
        activate('en')
        cat = BlogCategory.objects.create(name_en='Tech', slug='tech')
        post = BlogPost.objects.create(
            title_en='Test Blog Post',
            body_en='<p>Test content</p>',
            excerpt_en='Test excerpt',
            category=cat,
            status='published',
            published_at=timezone.now(),
        )
        response = self.client.get(reverse('core:blog_detail', kwargs={'slug': post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Blog Post')

    def test_blog_detail_404(self):
        response = self.client.get(reverse('core:blog_detail', kwargs={'slug': 'nonexistent-post'}))
        self.assertEqual(response.status_code, 404)

    def test_contact_page_get(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_form_submission_and_email_dispatch(self):
        activate('en')
        mail.outbox = []
        post_data = {
            'name': 'Karim Alami',
            'email': 'karim@example.com',
            'subject': 'Enterprise Architecture Inquiry',
            'message': 'Hello getNexiro, we need a high-performance backend platform in Tangier.',
        }
        response = self.client.post(reverse('core:contact'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='karim@example.com').exists())

        # Exactly 2 emails must be dispatched: Admin notification + Sender confirmation
        self.assertEqual(len(mail.outbox), 2)

        # 1. Admin Notification Email
        admin_email = mail.outbox[0]
        self.assertIn('getnexiro@gmail.com', admin_email.to)
        self.assertIn('Enterprise Architecture Inquiry', admin_email.subject)
        self.assertIn('Karim Alami', admin_email.subject)
        self.assertEqual(admin_email.reply_to, ['karim@example.com'])
        self.assertIn('karim@example.com', admin_email.body)
        self.assertIn('high-performance backend platform', admin_email.body)
        self.assertTrue(len(admin_email.alternatives) > 0)
        self.assertEqual(admin_email.alternatives[0][1], 'text/html')

        # 2. Sender Auto-responder Confirmation Email
        sender_email = mail.outbox[1]
        self.assertIn('karim@example.com', sender_email.to)
        self.assertIn('We received your message', sender_email.subject)
        self.assertEqual(sender_email.reply_to, ['getnexiro@gmail.com'])
        self.assertIn('Hi Karim Alami', sender_email.body)
        self.assertIn('The getNexiro Team', sender_email.body)
        self.assertIn('Tangier 90000, Morocco', sender_email.body)
        self.assertEqual(sender_email.extra_headers.get('Auto-Submitted'), 'auto-replied')
        self.assertTrue(len(sender_email.alternatives) > 0)
        self.assertEqual(sender_email.alternatives[0][1], 'text/html')

    def test_contact_confirmation_multilingual_fr(self):
        mail.outbox = []
        post_data = {
            'name': 'Claire Dubois',
            'email': 'claire@example.com',
            'subject': 'Développement Plateforme SaaS',
            'message': 'Bonjour, nous souhaitons développer une plateforme SaaS avec vous.',
        }
        response = self.client.post('/fr/contact/', post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 2)

        sender_email = mail.outbox[1]
        self.assertIn('Nous avons bien reçu votre message', sender_email.subject)
        self.assertIn('Bonjour Claire Dubois', sender_email.body)
        self.assertIn("L'équipe getNexiro", sender_email.body)

    def test_contact_confirmation_multilingual_ar(self):
        activate('ar')
        mail.outbox = []
        post_data = {
            'name': 'عمر الفاسي',
            'email': 'omar@example.com',
            'subject': 'استشارة معمارية برمجية',
            'message': 'مرحباً getNexiro، نريد تطوير منصة رقمية متطورة.',
        }
        response = self.client.post(reverse('core:contact'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 2)

        sender_email = mail.outbox[1]
        self.assertIn('تم استلام رسالتك بنجاح', sender_email.subject)
        self.assertIn('مرحباً عمر الفاسي', sender_email.body)
        self.assertIn('فريق getNexiro', sender_email.body)

    def test_contact_email_resilience_on_smtp_error(self):
        from unittest.mock import patch
        mail.outbox = []
        post_data = {
            'name': 'Resilience Test',
            'email': 'resilience@example.com',
            'subject': 'Network Failure Simulation',
            'message': 'Testing whether form works when SMTP server is down.',
        }
        with patch('core.emails.EmailMultiAlternatives.send', side_effect=Exception('SMTP Connection Timeout')):
            response = self.client.post(reverse('core:contact'), post_data, follow=True)
            self.assertEqual(response.status_code, 200)
            # Contact message must still be saved to the database
            self.assertTrue(ContactMessage.objects.filter(email='resilience@example.com').exists())

    def test_contact_with_browser_gps_coordinates(self):
        activate('en')
        mail.outbox = []
        post_data = {
            'name': 'Fes Mobile Client',
            'email': 'client.fes@example.com',
            'subject': 'Fintech Project from Fes',
            'message': 'We are located in Fes and need bespoke platform development.',
            'geo_lat': '34.0331',
            'geo_lon': '-5.0003',
            'geo_accuracy': '18',
            'geo_city': 'Fes, Fes-Meknes, Morocco',
        }
        response = self.client.post(reverse('core:contact'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 2)

        admin_email = mail.outbox[0]
        self.assertIn('Fes, Fes-Meknes, Morocco', admin_email.body)
        self.assertIn('Exact GPS', admin_email.body)
        self.assertIn('https://www.google.com/maps?q=34.0331,-5.0003', admin_email.body)


    def test_service_detail_view(self):
        activate('en')
        response = self.client.get(
            reverse('core:service_detail', kwargs={'slug': self.service.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Development')
        self.assertContains(response, 'Modern scalable websites.')

    def test_service_detail_with_solutions(self):
        activate('en')
        ServiceSolution.objects.create(
            service=self.service,
            title_en='Corporate Sites',
            title_fr='Sites Corporatifs',
            title_ar='مواقع الشركات',
            description_en='Professional corporate websites.',
            icon_emoji='🌐',
            order=1,
        )
        response = self.client.get(
            reverse('core:service_detail', kwargs={'slug': self.service.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Corporate Sites')

    def test_service_detail_404(self):
        response = self.client.get(
            reverse('core:service_detail', kwargs={'slug': 'nonexistent-service'})
        )
        self.assertEqual(response.status_code, 404)


class ModelLocalizationTest(TestCase):
    def test_localized_fallback(self):
        service = Service.objects.create(
            title_en='API Engineering',
            title_fr='Ingénierie API',
            description_en='Robust backends.',
        )
        activate('en')
        self.assertEqual(service.title, 'API Engineering')

        activate('fr')
        self.assertEqual(service.title, 'Ingénierie API')

        # Fallback to English when AR is empty
        activate('ar')
        self.assertEqual(service.title, 'API Engineering')

    def test_company_value_localization(self):
        val = CompanyValue.objects.create(
            icon='🌍',
            title_en='Gateway Location',
            title_fr='Emplacement Stratégique',
            title_ar='موقع استراتيجي',
            description_en='Close to Europe',
            description_fr='Proche de l Europe',
            description_ar='قريب من أوروبا',
        )
        activate('fr')
        self.assertEqual(val.title, 'Emplacement Stratégique')
        activate('ar')
        self.assertEqual(val.title, 'موقع استراتيجي')

    def test_process_step_localization(self):
        step = ProcessStep.objects.create(
            step_number='01',
            title_en='Discovery',
            title_fr='Découverte',
            title_ar='الاستكشاف',
            description_en='Analysis',
            description_fr='Analyse',
            description_ar='تحليل',
        )
        activate('fr')
        self.assertEqual(step.title, 'Découverte')

    def test_store_item_localization(self):
        item = StoreItem.objects.create(
            emoji='🚀',
            title_en='Design System',
            title_fr='Système Design',
            title_ar='نظام التصميم',
            description_en='UI Kit',
            badge_en='COMING SOON',
            badge_fr='BIENTÔT',
            badge_ar='قريباً',
        )
        activate('fr')
        self.assertEqual(item.title, 'Système Design')
        self.assertEqual(item.badge, 'BIENTÔT')

    def test_hero_video_and_wallpaper_rendering(self):
        activate('en')
        client = Client()
        config = SiteConfig.objects.create(
            site_name='getNexiro',
            hero_bg_type='video',
            hero_bg_video_url='https://example.com/hero.mp4',
            hero_badge_en='PREMIUM SOFTWARE',
            cta_title_en='Call To Action Title',
        )
        response = client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hero-bg-video')
        self.assertContains(response, 'https://example.com/hero.mp4')
        self.assertContains(response, 'PREMIUM SOFTWARE')
        self.assertContains(response, 'Call To Action Title')

    def test_per_page_header_video_customization(self):
        activate('en')
        client = Client()
        config = SiteConfig.objects.create(
            site_name='getNexiro',
            services_bg_video_url='https://example.com/custom-services.mp4',
            about_bg_video_url='https://example.com/custom-about.mp4',
            projects_bg_video_url='https://example.com/custom-projects.mp4',
            blog_bg_video_url='https://example.com/custom-blog.mp4',
            contact_bg_video_url='https://example.com/custom-contact.mp4',
        )
        res_services = client.get(reverse('core:services'))
        self.assertContains(res_services, 'https://example.com/custom-services.mp4')

        res_about = client.get(reverse('core:about'))
        self.assertContains(res_about, 'https://example.com/custom-about.mp4')

        res_projects = client.get(reverse('core:projects'))
        self.assertContains(res_projects, 'https://example.com/custom-projects.mp4')

        res_blog = client.get(reverse('core:blog'))
        self.assertContains(res_blog, 'https://example.com/custom-blog.mp4')

        res_contact = client.get(reverse('core:contact'))
        self.assertContains(res_contact, 'https://example.com/custom-contact.mp4')


# ══════════════════════════════════════════════════════════════════
# Phase 2 Tests: Lead Generation
# ══════════════════════════════════════════════════════════════════


class QuoteRequestModelTest(TestCase):
    """Tests for the QuoteRequest model and pricing calculation."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')
        # Create pricing rules
        PricingRule.objects.create(category='project_type', key='website', label_en='Corporate Website', value=Decimal('5000'), order=1)
        PricingRule.objects.create(category='project_type', key='ecommerce', label_en='E-Commerce', value=Decimal('12000'), order=2)
        PricingRule.objects.create(category='feature', key='auth', label_en='Authentication', value=Decimal('2000'), order=1)
        PricingRule.objects.create(category='feature', key='seo', label_en='SEO Optimization', value=Decimal('1500'), order=2)
        PricingRule.objects.create(category='pages', key='5-10', label_en='5-10 pages', value=Decimal('2500'), order=1)
        PricingRule.objects.create(category='pages', key='10-20', label_en='10-20 pages', value=Decimal('5000'), order=2)
        PricingRule.objects.create(category='language', key='extra', label_en='Additional Language', value=Decimal('1500'), order=1)
        PricingRule.objects.create(category='timeline', key='asap', label_en='ASAP', value=Decimal('1.30'), order=1)
        PricingRule.objects.create(category='timeline', key='flexible', label_en='Flexible', value=Decimal('0.90'), order=2)

    def test_quote_estimate_basic_website(self):
        """Test estimate calculation for a basic website."""
        from core.views import _compute_quote_estimate
        est_min, est_max = _compute_quote_estimate('website', '', '', 1, 'flexible')
        # Base: 5000, timeline multiplier: 0.9 => 4500
        # Range: 4500*0.85=3825 to 4500*1.25=5625
        self.assertEqual(est_min, 3825)
        self.assertEqual(est_max, 5625)

    def test_quote_estimate_with_features_and_languages(self):
        """Test estimate with features, pages, and extra languages."""
        from core.views import _compute_quote_estimate
        est_min, est_max = _compute_quote_estimate('website', 'auth,seo', '5-10', 3, '')
        # Base: 5000 + 2000 + 1500 + 2500 + 1500*2 = 14000
        # Multiplier: 1.0 (no timeline)
        # Range: 14000*0.85=11900 to 14000*1.25=17500
        self.assertEqual(est_min, 11900)
        self.assertEqual(est_max, 17500)

    def test_quote_estimate_rush_timeline(self):
        """Test that rush timeline multiplier increases price."""
        from core.views import _compute_quote_estimate
        est_min, est_max = _compute_quote_estimate('ecommerce', '', '', 1, 'asap')
        # Base: 12000, multiplier: 1.3 => 15600
        # Range: 15600*0.85=13260 to 15600*1.25=19500
        self.assertEqual(est_min, 13260)
        self.assertEqual(est_max, 19500)

    def test_quote_estimate_unknown_type_returns_none(self):
        """Test estimate with unknown project type returns (None, None) when base=0."""
        from core.views import _compute_quote_estimate
        est_min, est_max = _compute_quote_estimate('nonexistent', '', '', 1, '')
        self.assertIsNone(est_min)
        self.assertIsNone(est_max)

    def test_quote_model_creation(self):
        """Test QuoteRequest model creation and string representation."""
        quote = QuoteRequest.objects.create(
            project_type='website',
            name='Test User',
            email='test@example.com',
            estimated_min=5000,
            estimated_max=8000,
        )
        self.assertEqual(quote.status, 'new')
        self.assertIn('Test User', str(quote))
        self.assertIn('Corporate Website', str(quote))


class QuoteWizardViewTest(TestCase):
    """Tests for the quote wizard form submission flow."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')
        PricingRule.objects.create(category='project_type', key='website', label_en='Website', value=Decimal('5000'), order=1)
        PricingRule.objects.create(category='feature', key='auth', label_en='Auth', value=Decimal('2000'), order=1)

    def test_quote_wizard_get(self):
        """Test GET request renders the quote wizard form."""
        activate('en')
        response = self.client.get(reverse('core:quote_wizard'))
        self.assertEqual(response.status_code, 200)

    def test_quote_wizard_post_creates_quote(self):
        """Test full POST submission creates a QuoteRequest."""
        activate('en')
        post_data = {
            'project_type': 'website',
            'project_description': 'A corporate site',
            'features': 'auth',
            'num_pages': '',
            'num_languages': '1',
            'timeline': '',
            'budget_range': '5k-15k',
            'name': 'Youssef Test',
            'email': 'youssef@example.com',
            'phone': '+212600000000',
            'company': 'TestCo',
            'website_url': '',  # Honeypot should be empty
        }
        response = self.client.post(reverse('core:quote_wizard'), post_data)
        self.assertEqual(response.status_code, 302)  # Redirect to success

        # Verify QuoteRequest saved
        self.assertTrue(QuoteRequest.objects.filter(email='youssef@example.com').exists())
        quote = QuoteRequest.objects.get(email='youssef@example.com')
        self.assertEqual(quote.project_type, 'website')
        self.assertEqual(quote.name, 'Youssef Test')
        self.assertIsNotNone(quote.estimated_min)
        self.assertIsNotNone(quote.estimated_max)

    def test_quote_wizard_honeypot_blocks_bots(self):
        """Test that honeypot field catches bots."""
        activate('en')
        post_data = {
            'project_type': 'website',
            'project_description': '',
            'features': '',
            'num_pages': '',
            'num_languages': '1',
            'timeline': '',
            'budget_range': '',
            'name': 'Bot',
            'email': 'bot@spam.com',
            'website_url': 'http://spam.com',  # Honeypot filled!
        }
        response = self.client.post(reverse('core:quote_wizard'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        # No QuoteRequest should be saved for bots
        self.assertFalse(QuoteRequest.objects.filter(email='bot@spam.com').exists())

    def test_quote_wizard_prefill_from_package(self):
        """Test that ?type=ecommerce prefills the form."""
        activate('en')
        response = self.client.get(reverse('core:quote_wizard') + '?type=ecommerce')
        self.assertEqual(response.status_code, 200)

    def test_quote_success_redirect_without_session(self):
        """Test that quote_success redirects if not submitted."""
        activate('en')
        response = self.client.get(reverse('core:quote_success'))
        self.assertEqual(response.status_code, 302)


class BookingModelTest(TestCase):
    """Tests for the Booking model and slot conflict detection."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')

    def test_booking_creation(self):
        """Test creating a booking."""
        booking = Booking.objects.create(
            name='Sara Test',
            email='sara@example.com',
            date=datetime.date.today() + datetime.timedelta(days=7),
            time_slot=datetime.time(10, 0),
        )
        self.assertEqual(booking.status, 'new')
        self.assertIn('Sara Test', str(booking))

    def test_booking_slot_uniqueness(self):
        """Test that two bookings can't be created for the same slot."""
        future_date = datetime.date.today() + datetime.timedelta(days=7)
        Booking.objects.create(
            name='First', email='first@example.com',
            date=future_date, time_slot=datetime.time(10, 0),
        )
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Booking.objects.create(
                name='Second', email='second@example.com',
                date=future_date, time_slot=datetime.time(10, 0),
            )

    def test_google_calendar_url(self):
        """Test Google Calendar URL generation."""
        booking = Booking.objects.create(
            name='Cal Test', email='cal@example.com',
            date=datetime.date(2025, 6, 15), time_slot=datetime.time(14, 0),
        )
        url = booking.google_calendar_url
        self.assertIn('calendar.google.com', url)
        self.assertIn('20250615T140000', url)
        self.assertIn('getNexiro', url)


class BookingViewTest(TestCase):
    """Tests for the booking page views."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')
        # Create weekly availability
        for day in range(5):  # Mon-Fri
            WeeklyAvailability.objects.create(
                day_of_week=day,
                start_time=datetime.time(10, 0),
                end_time=datetime.time(10, 30),
            )

    def test_booking_page_get(self):
        """Test booking page renders correctly."""
        activate('en')
        response = self.client.get(reverse('core:booking'))
        self.assertEqual(response.status_code, 200)

    def test_booking_page_get_fr(self):
        """Test booking page in French."""
        activate('fr')
        response = self.client.get('/fr/booking/')
        self.assertEqual(response.status_code, 200)

    def test_booking_post_creates_booking(self):
        """Test POST creates a booking and renders success page."""
        activate('en')
        # Choose a Monday in the future
        today = datetime.date.today()
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        next_monday = today + datetime.timedelta(days=days_until_monday)

        post_data = {
            'name': 'Booking Person',
            'email': 'booking@example.com',
            'phone': '+212600000000',
            'company': 'BookCo',
            'date': next_monday.isoformat(),
            'time_slot': '10:00',
            'message': 'Test booking',
            'website_url': '',  # Honeypot empty
        }
        response = self.client.post(reverse('core:booking'), post_data)
        self.assertEqual(response.status_code, 200)  # Success page rendered
        self.assertTrue(Booking.objects.filter(email='booking@example.com').exists())

    def test_booking_duplicate_slot_rejected(self):
        """Test that booking a taken slot shows an error."""
        activate('en')
        future_date = datetime.date.today() + datetime.timedelta(days=7)
        # Create existing booking
        Booking.objects.create(
            name='Existing', email='existing@example.com',
            date=future_date, time_slot=datetime.time(10, 0),
        )
        post_data = {
            'name': 'Duplicate',
            'email': 'dup@example.com',
            'date': future_date.isoformat(),
            'time_slot': '10:00',
            'website_url': '',
        }
        response = self.client.post(reverse('core:booking'), post_data)
        self.assertEqual(response.status_code, 200)
        # Booking should NOT be created
        self.assertFalse(Booking.objects.filter(email='dup@example.com').exists())


class PackageModelTest(TestCase):
    """Tests for Package and PackageFeature models."""

    def test_package_creation(self):
        """Test creating a package with features."""
        pkg = Package.objects.create(
            name_en='Showcase', name_fr='Vitrine', name_ar='واجهة',
            slug='showcase', price_starting_from=5000, order=1,
        )
        PackageFeature.objects.create(
            package=pkg, text_en='5 Pages', text_fr='5 Pages', text_ar='5 صفحات',
            is_included=True, order=1,
        )
        PackageFeature.objects.create(
            package=pkg, text_en='CMS Dashboard', is_included=True, order=2,
        )
        self.assertEqual(pkg.features.count(), 2)

    def test_package_localization(self):
        """Test package name localization."""
        pkg = Package.objects.create(
            name_en='E-Commerce', name_fr='E-Commerce', name_ar='التجارة الإلكترونية',
            slug='ecommerce', order=1,
        )
        activate('ar')
        self.assertEqual(pkg.name, 'التجارة الإلكترونية')
        activate('fr')
        self.assertEqual(pkg.name, 'E-Commerce')


class PackagesViewTest(TestCase):
    """Tests for the packages page."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')
        self.pkg = Package.objects.create(
            name_en='Showcase', slug='showcase',
            price_starting_from=5000, is_active=True, order=1,
        )
        PackageFeature.objects.create(
            package=self.pkg, text_en='5 Pages', is_included=True, order=1,
        )

    def test_packages_page_renders(self):
        """Test packages page renders correctly."""
        activate('en')
        response = self.client.get(reverse('core:packages'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Showcase')
        self.assertContains(response, '5 Pages')

    def test_packages_page_fr(self):
        """Test packages page in French."""
        activate('fr')
        response = self.client.get('/fr/packages/')
        self.assertEqual(response.status_code, 200)


class SubscriberTest(TestCase):
    """Tests for the lead magnet / subscriber flow."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')

    def test_lead_magnet_get(self):
        """Test lead magnet page renders."""
        activate('en')
        response = self.client.get(reverse('core:lead_magnet'))
        self.assertEqual(response.status_code, 200)

    def test_lead_magnet_post_creates_subscriber(self):
        """Test POST creates a subscriber with pending status (double opt-in)."""
        activate('en')
        post_data = {
            'email': 'subscriber@example.com',
            'name': 'Sub Test',
            'consent': 'on',
            'website_url': '',  # Honeypot empty
        }
        response = self.client.post(reverse('core:lead_magnet'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Subscriber.objects.filter(email='subscriber@example.com').exists())
        sub = Subscriber.objects.get(email='subscriber@example.com')
        self.assertEqual(sub.status, 'pending')  # Double opt-in: starts as pending
        self.assertTrue(sub.consent)
        self.assertTrue(sub.confirmation_token)  # Token should be set
        self.assertIsNotNone(sub.token_created_at)

    def test_confirm_subscription_valid_token(self):
        """Test confirming subscription with a valid token."""
        activate('en')
        sub = Subscriber.objects.create(
            email='confirm@example.com',
            name='Confirm Test',
            consent=True,
            status='pending',
            confirmation_token='valid-test-token-123',
            token_created_at=timezone.now(),
        )
        response = self.client.get(reverse('core:confirm_subscription', args=['valid-test-token-123']))
        self.assertEqual(response.status_code, 200)
        sub.refresh_from_db()
        self.assertEqual(sub.status, 'confirmed')
        self.assertEqual(sub.confirmation_token, '')  # Token cleared after use

    def test_confirm_subscription_invalid_token(self):
        """Test confirming subscription with invalid token redirects."""
        activate('en')
        response = self.client.get(reverse('core:confirm_subscription', args=['nonexistent-token']), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_confirm_subscription_expired_token(self):
        """Test confirming subscription with expired token redirects."""
        activate('en')
        sub = Subscriber.objects.create(
            email='expired@example.com',
            name='Expired Test',
            consent=True,
            status='pending',
            confirmation_token='expired-token-123',
            token_created_at=timezone.now() - timedelta(hours=49),  # Expired
        )
        response = self.client.get(reverse('core:confirm_subscription', args=['expired-token-123']), follow=True)
        self.assertEqual(response.status_code, 200)
        sub.refresh_from_db()
        self.assertEqual(sub.status, 'pending')  # Still pending

    def test_lead_magnet_honeypot(self):
        """Test honeypot blocks bots."""
        activate('en')
        post_data = {
            'email': 'bot@spam.com',
            'name': 'SpamBot',
            'consent': 'on',
            'website_url': 'http://spam.com',  # Filled = bot
        }
        response = self.client.post(reverse('core:lead_magnet'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Subscriber.objects.filter(email='bot@spam.com').exists())

    def test_unsubscribe_flow(self):
        """Test unsubscribe via POST."""
        Subscriber.objects.create(email='unsub@example.com', consent=True)
        response = self.client.post(reverse('core:unsubscribe'), {'email': 'unsub@example.com'}, follow=True)
        self.assertEqual(response.status_code, 200)
        sub = Subscriber.objects.get(email='unsub@example.com')
        self.assertEqual(sub.status, 'unsubscribed')

    def test_unsubscribe_unknown_email(self):
        """Test unsubscribing unknown email shows info message."""
        response = self.client.post(reverse('core:unsubscribe'), {'email': 'unknown@example.com'}, follow=True)
        self.assertEqual(response.status_code, 200)


# ══════════════════════════════════════════════════════════════════
# Phase 3 Tests: Portfolio & Trust
# ══════════════════════════════════════════════════════════════════


class FAQModelTest(TestCase):
    """Tests for FAQ model."""

    def test_faq_creation_and_localization(self):
        faq = FAQ.objects.create(
            question_en='How long does a project take?',
            question_fr='Combien de temps prend un projet ?',
            question_ar='كم يستغرق المشروع؟',
            answer_en='Typically 4-12 weeks.',
            answer_fr='Généralement 4-12 semaines.',
            answer_ar='عادة 4-12 أسبوعًا.',
            section='general',
        )
        activate('fr')
        self.assertEqual(faq.question, 'Combien de temps prend un projet ?')
        activate('ar')
        self.assertEqual(faq.answer, 'عادة 4-12 أسبوعًا.')

    def test_faq_displayed_on_home(self):
        SiteConfig.objects.create(site_name='getNexiro')
        FAQ.objects.create(
            question_en='What services do you offer?',
            answer_en='Web dev, mobile, design.',
            section='general', is_active=True,
        )
        activate('en')
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'What services do you offer?')


class LegalPageTest(TestCase):
    """Tests for legal pages."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')
        LegalPage.objects.create(
            slug='privacy-policy',
            title_en='Privacy Policy',
            title_fr='Politique de Confidentialité',
            title_ar='سياسة الخصوصية',
            body_en='<p>We respect your privacy.</p>',
            body_fr='<p>Nous respectons votre vie privée.</p>',
            body_ar='<p>نحن نحترم خصوصيتكم.</p>',
        )

    def test_privacy_page_en(self):
        activate('en')
        response = self.client.get(reverse('core:privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Privacy Policy')
        self.assertContains(response, 'We respect your privacy')

    def test_privacy_page_fr(self):
        activate('fr')
        response = self.client.get('/fr/privacy-policy/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Politique de Confidentialité')

    def test_privacy_page_ar(self):
        activate('ar')
        response = self.client.get('/ar/privacy-policy/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'سياسة الخصوصية')


class ProjectCaseStudyTest(TestCase):
    """Tests for project detail / case study page."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')
        self.category = ProjectCategory.objects.create(
            name_en='Healthcare', slug='healthcare',
        )
        self.project = Project.objects.create(
            title_en='MedConnect Platform',
            description_en='Healthcare platform overview.',
            challenge_en='Fragmented patient data across clinics.',
            solution_en='Unified EHR system with FHIR API.',
            results_en='40% reduction in data entry time.',
            client_feedback_quote_en='Excellent work.',
            client_feedback_author='Dr. Smith',
            category=self.category,
            is_featured=True, order=1,
        )

    def test_case_study_sections_rendered(self):
        """Test all case study sections appear on detail page."""
        activate('en')
        response = self.client.get(
            reverse('core:project_detail', kwargs={'slug': self.project.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MedConnect Platform')
        self.assertContains(response, 'Fragmented patient data')
        self.assertContains(response, 'Unified EHR system')
        self.assertContains(response, '40% reduction')

    def test_related_projects_displayed(self):
        """Test related projects section."""
        Project.objects.create(
            title_en='Second Project',
            description_en='Another project.',
            category=self.category, order=2,
        )
        activate('en')
        response = self.client.get(
            reverse('core:project_detail', kwargs={'slug': self.project.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Second Project')


class TeamMemberTest(TestCase):
    """Tests for team member model."""

    def test_team_member_localization(self):
        member = TeamMember.objects.create(
            name='Simo Derkaoui',
            role_en='Lead Engineer',
            role_fr='Ingénieur Principal',
            role_ar='المهندس الرئيسي',
            bio_en='Full-stack developer.',
        )
        activate('fr')
        self.assertEqual(member.role, 'Ingénieur Principal')
        activate('ar')
        self.assertEqual(member.role, 'المهندس الرئيسي')


# ══════════════════════════════════════════════════════════════════
# Phase 4 Tests: SEO & Content
# ══════════════════════════════════════════════════════════════════


class SitemapRobotsTest(TestCase):
    """Tests for sitemap.xml and robots.txt."""

    def test_robots_txt(self):
        """Test robots.txt returns correct content."""
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        content = response.content.decode()
        self.assertIn('User-agent: *', content)
        self.assertIn('Sitemap:', content)
        self.assertIn('sitemap.xml', content)
        self.assertIn('Disallow: /admin/', content)

    def test_sitemap_xml(self):
        """Test sitemap.xml returns valid XML with hreflang."""
        SiteConfig.objects.create(site_name='getNexiro')
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        content = response.content.decode()
        self.assertIn('<?xml version="1.0"', content)
        self.assertIn('<urlset', content)
        self.assertIn('hreflang', content)
        self.assertIn('x-default', content)

    def test_sitemap_includes_dynamic_pages(self):
        """Test sitemap includes services, projects, blog posts."""
        SiteConfig.objects.create(site_name='getNexiro')
        Service.objects.create(
            title_en='Test Service', description_en='Test', icon='icon-web',
        )
        cat = ProjectCategory.objects.create(name_en='Cat', slug='cat')
        Project.objects.create(
            title_en='Test Project', description_en='Test', category=cat,
        )
        BlogPost.objects.create(
            title_en='Test Post', body_en='Test', status='published',
            published_at=timezone.now(),
        )
        response = self.client.get('/sitemap.xml')
        content = response.content.decode()
        self.assertIn('test-service', content)
        self.assertIn('test-project', content)
        self.assertIn('test-post', content)


class BlogSEOTest(TestCase):
    """Tests for blog SEO features."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')
        self.cat = BlogCategory.objects.create(name_en='Tech', slug='tech')

    def test_blog_post_auto_slug(self):
        """Test blog post auto-generates slug."""
        post = BlogPost.objects.create(
            title_en='How to Build a SaaS Platform',
            body_en='<p>Guide content</p>',
            category=self.cat, status='published',
            published_at=timezone.now(),
        )
        self.assertEqual(post.slug, 'how-to-build-a-saas-platform')

    def test_blog_post_meta_fields(self):
        """Test blog post meta_title and meta_description properties."""
        post = BlogPost.objects.create(
            title_en='SEO Guide',
            body_en='<p>SEO content</p>',
            excerpt_en='A quick SEO guide for developers.',
            meta_title_en='Custom SEO Title',
            meta_description_en='Custom meta desc.',
            category=self.cat, status='published',
            published_at=timezone.now(),
        )
        activate('en')
        self.assertEqual(post.meta_title, 'Custom SEO Title')
        self.assertEqual(post.meta_description, 'Custom meta desc.')

    def test_blog_post_meta_fallback(self):
        """Test meta fields fall back to title/excerpt when empty."""
        post = BlogPost.objects.create(
            title_en='Fallback Test',
            body_en='<p>Content</p>',
            excerpt_en='This is the excerpt.',
            category=self.cat, status='published',
            published_at=timezone.now(),
        )
        activate('en')
        self.assertEqual(post.meta_title, 'Fallback Test')
        self.assertEqual(post.meta_description, 'This is the excerpt.')

    def test_blog_category_filter(self):
        """Test blog filtering by category."""
        BlogPost.objects.create(
            title_en='Tech Post', body_en='<p>Tech</p>',
            category=self.cat, status='published',
            published_at=timezone.now(),
        )
        other_cat = BlogCategory.objects.create(name_en='Design', slug='design')
        BlogPost.objects.create(
            title_en='Design Post', body_en='<p>Design</p>',
            category=other_cat, status='published',
            published_at=timezone.now(),
        )
        activate('en')
        response = self.client.get(reverse('core:blog') + '?category=tech')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tech Post')
        self.assertNotContains(response, 'Design Post')


# ══════════════════════════════════════════════════════════════════
# Phase 5 Tests: UX Polish
# ══════════════════════════════════════════════════════════════════


class ThemeToggleTest(TestCase):
    """Tests for dark/light theme toggle."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')

    def test_theme_toggle_in_navbar(self):
        """Test that the theme toggle button exists in the base template."""
        activate('en')
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'theme-toggle')


class WhatsAppTrackingTest(TestCase):
    """Tests for WhatsApp button and source tracking."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')

    def test_whatsapp_button_present(self):
        """Test WhatsApp floating button is present."""
        activate('en')
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'whatsappFloat')
        self.assertContains(response, 'wa.me')


# ══════════════════════════════════════════════════════════════════
# Phase 6 Tests: Form Validation
# ══════════════════════════════════════════════════════════════════


class FormValidationTest(TestCase):
    """Tests for form validation logic."""

    def test_contact_form_valid(self):
        form = ContactForm(data={
            'name': 'Valid User',
            'email': 'valid@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.',
        })
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_email(self):
        form = ContactForm(data={
            'name': 'Test',
            'email': 'not-an-email',
            'subject': 'Test',
            'message': 'Test message.',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_contact_form_missing_required_fields(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('subject', form.errors)
        self.assertIn('message', form.errors)

    def test_quote_step1_valid(self):
        form = QuoteStep1Form(data={'project_type': 'website'})
        self.assertTrue(form.is_valid())

    def test_quote_step1_empty_type(self):
        form = QuoteStep1Form(data={'project_type': ''})
        self.assertFalse(form.is_valid())

    def test_quote_step4_valid(self):
        form = QuoteStep4Form(data={
            'name': 'Test',
            'email': 'test@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_booking_form_requires_date_and_time(self):
        form = BookingForm(data={
            'name': 'Test',
            'email': 'test@example.com',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_subscriber_form_requires_consent(self):
        form = SubscriberForm(data={
            'email': 'test@example.com',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('consent', form.errors)

    def test_subscriber_form_valid(self):
        form = SubscriberForm(data={
            'email': 'test@example.com',
            'consent': True,
        })
        self.assertTrue(form.is_valid())


# ══════════════════════════════════════════════════════════════════
# Multilingual URL Tests
# ══════════════════════════════════════════════════════════════════


class MultilingualViewsTest(TestCase):
    """Test that all key pages render in EN, FR, AR using reverse()."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')
        Service.objects.create(
            title_en='API Dev', description_en='APIs', icon='icon-api',
        )
        Package.objects.create(
            name_en='Basic', slug='basic',
            price_starting_from=3000, is_active=True,
        )
        LegalPage.objects.create(
            slug='privacy-policy', title_en='Privacy Policy',
            body_en='<p>Policy</p>',
        )
        LegalPage.objects.create(
            slug='terms-of-service', title_en='Terms',
            body_en='<p>Terms</p>',
        )

    def _test_view_all_languages(self, url_name, kwargs=None):
        """Helper: test a named URL in all three languages using reverse()."""
        for lang in ('en', 'fr', 'ar'):
            activate(lang)
            url = reverse(url_name, kwargs=kwargs)
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f'Failed for {url_name} in {lang}: {url} returned {response.status_code}'
            )

    def test_home_all_langs(self):
        self._test_view_all_languages('core:home')

    def test_about_all_langs(self):
        self._test_view_all_languages('core:about')

    def test_services_all_langs(self):
        self._test_view_all_languages('core:services')

    def test_projects_all_langs(self):
        self._test_view_all_languages('core:projects')

    def test_blog_all_langs(self):
        self._test_view_all_languages('core:blog')

    def test_contact_all_langs(self):
        self._test_view_all_languages('core:contact')

    def test_packages_all_langs(self):
        self._test_view_all_languages('core:packages')

    def test_quote_all_langs(self):
        self._test_view_all_languages('core:quote_wizard')

    def test_booking_all_langs(self):
        self._test_view_all_languages('core:booking')

    def test_checklist_all_langs(self):
        self._test_view_all_languages('core:lead_magnet')

    def test_privacy_all_langs(self):
        self._test_view_all_languages('core:privacy_policy')

    def test_terms_all_langs(self):
        self._test_view_all_languages('core:terms_of_service')

    def test_ar_pages_have_rtl(self):
        """Test that Arabic pages include dir='rtl'."""
        activate('ar')
        response = self.client.get(reverse('core:home'))
        self.assertContains(response, 'dir="rtl"')
        response = self.client.get(reverse('core:services'))
        self.assertContains(response, 'dir="rtl"')
        response = self.client.get(reverse('core:packages'))
        self.assertContains(response, 'dir="rtl"')


class BlogUpgradesTest(TestCase):
    """Tests for Task 5: Blog upgrades — RSS feed, category archive, tag archive."""

    def setUp(self):
        SiteConfig.objects.get_or_create(pk=1)
        self.cat = BlogCategory.objects.create(name_en='Web Dev', name_fr='Dev Web', name_ar='تطوير ويب', slug='web-dev')
        self.post = BlogPost.objects.create(
            title_en='Test Post', title_fr='Article Test', title_ar='مقال اختبار',
            slug='test-post', body_en='Test body content', excerpt_en='Test excerpt',
            category=self.cat, status='published', author_name='Test Author',
            tags='django, python, web',
            published_at=timezone.now(),
        )

    def test_blog_rss_feed(self):
        """Test RSS feed returns valid XML."""
        activate('en')
        response = self.client.get(reverse('core:blog_rss_feed'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/rss+xml', response['Content-Type'])
        self.assertIn(b'Test Post', response.content)

    def test_blog_category_archive(self):
        """Test category archive page shows filtered posts."""
        activate('en')
        response = self.client.get(reverse('core:blog_category_archive', args=['web-dev']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_blog_category_archive_404(self):
        """Test category archive returns 404 for nonexistent category."""
        activate('en')
        response = self.client.get(reverse('core:blog_category_archive', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)

    def test_blog_tag_archive(self):
        """Test tag archive page shows posts with matching tag."""
        activate('en')
        response = self.client.get(reverse('core:blog_tag_archive', args=['django']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_blog_tag_archive_empty(self):
        """Test tag archive with no matching posts shows empty state."""
        activate('en')
        response = self.client.get(reverse('core:blog_tag_archive', args=['nonexistent-tag']))
        self.assertEqual(response.status_code, 200)

