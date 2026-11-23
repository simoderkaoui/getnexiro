import re
import json
from decimal import Decimal
import datetime
from datetime import timedelta
from django.core import mail
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils.translation import activate
from django.utils import timezone

User = get_user_model()
from core.models import (
    SiteConfig, Service, ServiceSolution, ProjectCategory, Project, ProjectImage,
    TeamMember, Testimonial, Stat, ContactMessage,
    CompanyValue, ProcessStep, StoreItem, BlogCategory, BlogPost, Author,
    LegalPage, FAQ,
    Package, PackageFeature, PricingRule, QuoteRequest,
    WeeklyAvailability, Booking, Subscriber,
    CityServicePage,
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
            hero_title_en='Web & App <span class="text-gradient">Development Agency</span><br>in Tangier, Morocco',
            hero_title_fr='Agence de <span class="text-gradient">Développement Web & Mobile</span><br>à Tanger, Maroc',
            hero_title_ar='وكالة <span class="text-gradient">تطوير مواقع وتطبيقات</span><br>في طنجة والمغرب',
            email='contact@getnexiro.com',
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
        self.assertContains(response, 'Development Agency')

    def test_home_page_fr(self):
        activate('fr')
        response = self.client.get('/fr/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Développement Web & Mobile')

    def test_home_page_ar(self):
        activate('ar')
        response = self.client.get('/ar/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'تطوير مواقع وتطبيقات')
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
        self.assertIn('contact@getnexiro.com', admin_email.to)
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
        self.assertEqual(sender_email.reply_to, ['contact@getnexiro.com'])
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


class DarkThemeOnlyTest(TestCase):
    """Tests to verify the site is exclusively dark theme (no light theme toggle)."""

    def setUp(self):
        SiteConfig.objects.create(site_name='getNexiro')

    def test_no_light_theme_toggle_in_navbar(self):
        """Test that the light theme toggle button is removed from the navbar."""
        activate('en')
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'themeToggle')
        self.assertNotContains(response, 'theme-toggle-btn')
        self.assertNotContains(response, 'data-theme="light"')


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

    def test_blog_index_excludes_noindex_posts(self):
        """Verify noindex off-topic posts are excluded from /blog/ listing."""
        off_cat = BlogCategory.objects.create(name_en='Money & Income', slug='money-income')
        off_post = BlogPost.objects.create(
            title_en='Off-topic Income Report', slug='off-topic-income-report',
            body_en='Earned $10,000', excerpt_en='Summary', category=off_cat,
            status='published', noindex=True, index_in_sitemap=False,
            published_at=timezone.now(),
        )
        activate('en')
        res = self.client.get(reverse('core:blog'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Test Post')
        self.assertNotContains(res, 'Off-topic Income Report')
        # Category nav must hide 'Money & Income' because it has no indexable posts
        self.assertNotContains(res, 'Money & Income')

    def test_blog_detail_author_box_and_fallback_image(self):
        """Verify on-topic blog detail renders visible author box with bio/role, updated date, and og-image fallback."""
        author = Author.objects.create(
            name='Youssef Benali', slug='youssef-benali',
            role_en='Principal Cloud Architect', bio_en='Expert in Django and AWS',
        )
        self.post.author = author
        self.post.save()

        activate('en')
        res = self.client.get(reverse('core:blog_detail', args=['test-post']))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Youssef Benali')
        self.assertContains(res, 'Principal Cloud Architect')
        self.assertContains(res, 'Expert in Django and AWS')
        self.assertContains(res, 'Last updated')
        self.assertNotContains(res, '✍️')
        # Image fallback
        self.assertContains(res, 'images/og-image.png')



class CityServicePageTest(TestCase):
    """Tests for City x Service landing pages, canonical short slugs, and 301 redirects."""

    def setUp(self):
        SiteConfig.objects.get_or_create(pk=1)
        self.service = Service.objects.create(
            title_en='Web Development', title_fr='Dev Web', title_ar='تطوير ويب',
            slug='web-development', description_en='Web dev services',
            icon='icon-web', is_featured=True, order=1,
        )
        self.page = CityServicePage.objects.create(
            service=self.service, city='tangier', slug='tangier',
            h1_en='Web Development in Tangier', h1_fr='Dev Web Tanger', h1_ar='تطوير ويب طنجة',
            intro_en='Intro text', intro_fr='Texte intro', intro_ar='نص تمهيدي',
            body_en='<p>Body content</p>', body_fr='<p>Contenu</p>', body_ar='<p>محتوى</p>',
            is_published=True, noindex=False,
        )
        self.remote_page = CityServicePage.objects.create(
            service=self.service, city='tetouan', slug='tetouan',
            h1_en='Web Development in Tetouan', h1_fr='Dev Web Tétouan', h1_ar='تطوير ويب تطوان',
            intro_en='Remote intro text', intro_fr='Texte remote', intro_ar='نص عن بعد',
            body_en='<p>Remote body</p>', body_fr='<p>Contenu distant</p>', body_ar='<p>محتوى عن بعد</p>',
            is_published=True, noindex=True, is_remote_service=True,
        )

    def test_city_page_published(self):
        """Test published city page renders with canonical short slug."""
        activate('en')
        response = self.client.get(
            reverse('core:city_service_page', args=['web-development', 'tangier'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Development in Tangier')

    def test_city_page_legacy_long_slug_301_redirect(self):
        """Test legacy long slug /web-development-tangier/ 301 redirects to /tangier/ across languages."""
        # English
        res = self.client.get('/en/services/web-development/web-development-tangier/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/en/services/web-development/tangier/')

        # French
        res_fr = self.client.get('/fr/services/web-development/web-development-tangier/')
        self.assertEqual(res_fr.status_code, 301)
        self.assertEqual(res_fr.headers.get('Location'), '/fr/services/web-development/tangier/')

        # Remote city redirect
        res_tet = self.client.get('/en/services/web-development/web-development-tetouan/')
        self.assertEqual(res_tet.status_code, 301)
        self.assertEqual(res_tet.headers.get('Location'), '/en/services/web-development/tetouan/')

    def test_city_page_heading_no_tangier_to_tangier(self):
        """Verify the template bug 'from Tangier to Tangier' is fixed and neutral/accurate."""
        activate('en')
        response = self.client.get('/en/services/web-development/tangier/')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf-8')
        self.assertNotIn('from Tangier to Tangier', html)
        self.assertIn('Software Engineering & Architecture Hub in Tangier', html)

        # Remote page heading
        response_tet = self.client.get('/en/services/web-development/tetouan/')
        self.assertEqual(response_tet.status_code, 200)
        html_tet = response_tet.content.decode('utf-8')
        self.assertIn('Remote from Tangier HQ', html_tet)

    def test_city_page_noindex_for_remote_cities(self):
        """Verify remote/unverified city pages render noindex and are omitted from sitemap."""
        activate('en')
        res_tet = self.client.get('/en/services/web-development/tetouan/')
        self.assertContains(res_tet, '<meta name="robots" content="noindex, follow">')

        res_tangier = self.client.get('/en/services/web-development/tangier/')
        self.assertContains(res_tangier, '<meta name="robots" content="index, follow, max-image-preview:large">')

    def test_city_page_unpublished_404(self):
        """Test unpublished city page returns 404."""
        activate('en')
        self.page.is_published = False
        self.page.save()
        response = self.client.get(
            reverse('core:city_service_page', args=['web-development', 'tangier'])
        )
        self.assertEqual(response.status_code, 404)

    def test_city_page_wrong_service_404(self):
        """Test city page with wrong service slug returns 404."""
        activate('en')
        response = self.client.get(
            reverse('core:city_service_page', args=['nonexistent-service', 'tangier'])
        )
        self.assertEqual(response.status_code, 404)

    def test_city_page_model_str(self):
        """Test CityServicePage string representation."""
        self.assertEqual(str(self.page), 'Web Development - Tangier')

    def test_city_page_industries_list(self):
        """Test industries_list property."""
        self.page.industries_served_en = 'Tourism\nRetail\nLogistics'
        self.page.save()
        self.assertEqual(len(self.page.industries_list), 3)



class BlogSearchAndPhase2ImprovementsTest(TestCase):
    """Tests for Phase 2: Blog search, JSON-LD Sitelinks, and OpenGraph enhancements."""

    def setUp(self):
        SiteConfig.objects.get_or_create(pk=1)
        self.cat1 = BlogCategory.objects.create(name_en='Tech', name_fr='Tech FR', name_ar='تقنية', slug='tech')
        self.cat2 = BlogCategory.objects.create(name_en='Design', name_fr='Design FR', name_ar='تصميم', slug='design')
        self.post1 = BlogPost.objects.create(
            title_en='Django Performance Optimization',
            title_fr='Optimisation Django',
            title_ar='تحسين أداء دجانغو',
            slug='django-performance-optimization',
            excerpt_en='Speed up your app',
            body_en='<p>Full article on cache, redis and db indexes.</p>',
            category=self.cat1,
            status='published',
            author_name='Schneider',
        )
        self.post2 = BlogPost.objects.create(
            title_en='UI Design Trends in Tangier',
            title_fr='Tendances Design Tanger',
            title_ar='اتجاهات التصميم في طنجة',
            slug='ui-design-trends-tangier',
            excerpt_en='Modern dark themes',
            body_en='<p>Glassmorphism and luxury minimalism.</p>',
            category=self.cat2,
            status='published',
            author_name='Schneider',
        )

    def test_blog_search_matching_query(self):
        """Test searching blog posts filters results correctly."""
        activate('en')
        response = self.client.get(reverse('core:blog') + '?search=Performance')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Performance Optimization')
        self.assertNotContains(response, 'UI Design Trends in Tangier')

    def test_blog_search_body_content(self):
        """Test searching matches content inside article body."""
        activate('en')
        response = self.client.get(reverse('core:blog') + '?search=Glassmorphism')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'UI Design Trends in Tangier')
        self.assertNotContains(response, 'Django Performance Optimization')

    def test_blog_search_no_results(self):
        """Test search with no matches displays empty message."""
        activate('en')
        response = self.client.get(reverse('core:blog') + '?search=NonexistentSuperTerm123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 0)

    def test_jsonld_sitelinks_and_catalog(self):
        """Test home page contains WebSite SearchAction and OfferCatalog JSON-LD."""
        activate('en')
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('"@type": "SearchAction"', content)
        self.assertIn('"@type": "WebSite"', content)
        self.assertIn('"@type": "OfferCatalog"', content)
        self.assertIn('"ProfessionalService"', content)
        self.assertIn('"Organization"', content)

    def test_opengraph_dimensions_and_locale(self):
        """Test OpenGraph meta tags include dimensions and formatted locale."""
        activate('en')
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'property="og:image:width" content="1200"')
        self.assertContains(response, 'property="og:image:height" content="630"')
        self.assertContains(response, 'property="og:locale" content="en_US"')

        activate('fr')
        response_fr = self.client.get(reverse('core:home'))
        self.assertContains(response_fr, 'property="og:locale" content="fr_FR"')

        activate('ar')
        response_ar = self.client.get(reverse('core:home'))
        self.assertContains(response_ar, 'property="og:locale" content="ar_MA"')


# ══════════════════════════════════════════════════════════════════
# Phase 14: Comprehensive SEO Master Test Suite
# ══════════════════════════════════════════════════════════════════

class SEOMasterTestSuite(TestCase):
    """
    Automated verification of the entire Technical & On-Page SEO System:
    - Titles <= 60 chars ending with ' | getNexiro'
    - Descriptions between 120 and 155 chars
    - Single H1 per page
    - Absolute canonical links
    - Complete reciprocal hreflang + x-default
    - Sitemap excludes noindex pages
    - Valid, syntax-clean JSON-LD schemas
    - No obsolete meta keywords or geo tags
    """

    def setUp(self):
        self.client = Client()
        self.config = SiteConfig.load()
        self.config.site_name = 'getNexiro'
        self.config.save()

    def _get_soup(self, url):
        from bs4 import BeautifulSoup
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200, f"Page {url} did not return 200 OK")
        return BeautifulSoup(res.content.decode('utf-8'), 'html.parser')

    def test_seo_titles_length_and_format(self):
        """All main indexable views across EN, FR, AR must have titles <= 60 chars ending in | getNexiro."""
        named_views = ['core:home', 'core:about', 'core:services', 'core:projects', 'core:blog', 'core:contact']
        for lang in ('en', 'fr', 'ar'):
            activate(lang)
            for v_name in named_views:
                url = reverse(v_name)
                soup = self._get_soup(url)
                self.assertIsNotNone(soup.title, f"Missing <title> tag on {url}")
                title = soup.title.string.strip()
                self.assertTrue(len(title) <= 60, f"Title on {url} exceeds 60 chars: '{title}' ({len(title)} chars)")
                self.assertTrue(title.endswith("getNexiro"), f"Title on {url} does not end with getNexiro: '{title}'")

    def test_seo_descriptions_length(self):
        """Descriptions must be between 120 and 155 characters across all main pages."""
        named_views = ['core:home', 'core:about', 'core:services', 'core:projects', 'core:blog', 'core:contact']
        for lang in ('en', 'fr', 'ar'):
            activate(lang)
            for v_name in named_views:
                url = reverse(v_name)
                soup = self._get_soup(url)
                meta_desc = soup.find('meta', {'name': 'description'})
                self.assertIsNotNone(meta_desc, f"Missing meta description on {url}")
                desc = meta_desc.get('content', '').strip()
                self.assertTrue(120 <= len(desc) <= 155, f"Description on {url} not in 120-155 chars: '{desc}' ({len(desc)} chars)")

    def test_single_h1_per_page(self):
        """Every page must have exactly one semantic <h1> element."""
        named_views = ['core:home', 'core:about', 'core:services', 'core:projects', 'core:blog', 'core:contact']
        for lang in ('en', 'fr', 'ar'):
            activate(lang)
            for v_name in named_views:
                url = reverse(v_name)
                soup = self._get_soup(url)
                h1_elements = soup.find_all('h1')
                self.assertEqual(len(h1_elements), 1, f"Page {url} has {len(h1_elements)} <h1> tags (expected exactly 1)")

    def test_canonicals_present_and_clean(self):
        """Canonical link must be absolute and ignore tracking parameters."""
        activate('en')
        url_with_params = reverse('core:home') + '?utm_source=google&fbclid=12345'
        soup = self._get_soup(url_with_params)
        canonical = soup.find('link', {'rel': 'canonical'})
        self.assertIsNotNone(canonical, "Missing canonical link")
        href = canonical.get('href', '')
        self.assertTrue(href.startswith('https://getnexiro.com/en/'), f"Canonical {href} is not absolute")
        self.assertNotIn('utm_source', href, "Canonical includes tracking parameters")
        self.assertNotIn('fbclid', href, "Canonical includes tracking parameters")

    def test_hreflang_reciprocity_and_xdefault(self):
        """Hreflang tags must include en, fr, ar alternates and an x-default."""
        activate('en')
        soup = self._get_soup(reverse('core:home'))
        alts = soup.find_all('link', {'rel': 'alternate'})
        hreflangs = {a.get('hreflang'): a.get('href') for a in alts if a.get('hreflang')}
        self.assertIn('en', hreflangs)
        self.assertIn('fr', hreflangs)
        self.assertIn('ar', hreflangs)
        self.assertIn('x-default', hreflangs)

    def test_sitemap_excludes_noindex(self):
        """Sitemap.xml must exclude posts flagged as noindex=True."""
        hidden_post = BlogPost.objects.create(
            title_en="Hidden Thin Post",
            slug="hidden-thin-post-seo-test",
            status="published",
            noindex=True,
            index_in_sitemap=False
        )
        res = self.client.get('/sitemap.xml')
        self.assertEqual(res.status_code, 200)
        content = res.content.decode('utf-8')
        self.assertNotIn('hidden-thin-post-seo-test', content)

    def test_valid_jsonld_schemas(self):
        """All JSON-LD blocks must parse into valid JSON objects without syntax errors."""
        named_views = ['core:home', 'core:about', 'core:contact']
        for lang in ('en', 'fr'):
            activate(lang)
            for v_name in named_views:
                url = reverse(v_name)
                soup = self._get_soup(url)
                scripts = soup.find_all('script', {'type': 'application/ld+json'})
                self.assertTrue(len(scripts) >= 1, f"No JSON-LD script found on {url}")
                for s in scripts:
                    try:
                        data = json.loads(s.string)
                        self.assertIsInstance(data, dict)
                    except Exception as e:
                        self.fail(f"Invalid JSON-LD on {url}: {e}\nScript:\n{s.string}")

    def test_no_meta_keywords_or_obsolete_geo_tags(self):
        """Ensure obsolete meta keywords and geo tags are removed from all pages."""
        for v_name in ['core:home', 'core:about', 'core:contact']:
            soup = self._get_soup(reverse(v_name))
            self.assertIsNone(soup.find('meta', {'name': 'keywords'}), f"Found obsolete meta keywords on {v_name}")
            self.assertIsNone(soup.find('meta', {'name': 'ICBM'}), f"Found obsolete ICBM on {v_name}")
            self.assertIsNone(soup.find('meta', {'name': 'geo.position'}), f"Found obsolete geo.position on {v_name}")
            self.assertIsNone(soup.find('meta', {'name': 'geo.region'}), f"Found obsolete geo.region on {v_name}")
            self.assertIsNone(soup.find('meta', {'name': 'geo.placename'}), f"Found obsolete geo.placename on {v_name}")

    def test_arabic_and_multilingual_url_normalization(self):
        """Ensure normalized ASCII Arabic URLs return 200 and legacy Arabic URLs 301 redirect cleanly."""
        # 1. Canonical ASCII Arabic URLs must return 200
        res = self.client.get('/ar/about/')
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/ar/services/')
        self.assertEqual(res.status_code, 200)

        # 2. Legacy percent-encoded and Arabic slug aliases must 301 redirect to canonical ASCII URLs
        res = self.client.get('/ar/%D9%85%D9%86-%D9%86%D8%AD%D9%86/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/about/')

        res = self.client.get('/ar/من-نحن/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/about/')

        res = self.client.get('/ar/خدمات/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/services/')

        # 3. French aliases (/fr/a-propos/) must 301 redirect to French canonicals (/fr/about/)
        res = self.client.get('/fr/a-propos/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/fr/about/')

        res = self.client.get('/fr/about/')
        self.assertEqual(res.status_code, 200)

        # 4. Unprefixed localized slugs must 301 redirect to language prefix
        res = self.client.get('/من-نحن/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/about/')

        # 5. Trailing and duplicate language tokens (e.g. /ar/من-نحن/ar/ar/) must 301 redirect cleanly
        res = self.client.get('/ar/من-نحن/ar/ar/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/about/')
        follow_res = self.client.get(res.headers.get('Location'), follow=True)
        self.assertEqual(follow_res.status_code, 200)

        res = self.client.get('/ar/من-نحن/ar/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/about/')

        res = self.client.get('/ar/ar/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/')

        res = self.client.get('/en/ar/about/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/en/about/')

        # 6. Chained page navigation (e.g. /ar/من-نحن/ar/خدمات/) must 301 redirect to target section
        res = self.client.get('/ar/من-نحن/ar/خدمات/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/services/')
        follow_res = self.client.get(res.headers.get('Location'), follow=True)
        self.assertEqual(follow_res.status_code, 200)

        res = self.client.get('/ar/من-نحن/ar/services/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/services/')

        res = self.client.get('/ar/من-نحن/services/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/services/')

        res = self.client.get('/ar/من-نحن/ar/مشاريع/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/projects/')

        # Services -> Projects chained
        res = self.client.get('/ar/خدمات/ar/مشاريع/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/projects/')

        # Percent-encoded Services -> Projects chained
        res = self.client.get('/ar/%D8%AE%D8%AF%D9%85%D8%A7%D8%AA/ar/%D9%85%D8%B4%D8%A7%D8%B1%D9%8A%D8%B9/')
        self.assertEqual(res.status_code, 301)
        self.assertEqual(res.headers.get('Location'), '/ar/projects/')

    def test_force_script_name_prevents_wsgi_script_name_pollution(self):
        """
        Verify that even if Apache mod_passenger passes SCRIPT_NAME populated with
        the Arabic route segment, FORCE_SCRIPT_NAME='' and UrlNormalizationMiddleware
        prevent link concatenation.
        """
        res = self.client.get('/ar/services/', SCRIPT_NAME='/ar/%D8%AE%D8%AF%D9%85%D8%A7%D8%AA')
        self.assertEqual(res.status_code, 200)
        html = res.content.decode('utf-8')
        # Navbar links must NOT have /ar/خدمات/ar/ or duplicate paths
        self.assertNotIn('/ar/خدمات/ar/', html)
        self.assertNotIn('/ar/%D8%AE%D8%AF%D9%85%D8%A7%D8%AA/ar/', html)
        # Canonical URL must be clean
        self.assertIn('https://getnexiro.com/ar/services/', html)

    def test_direct_flag_switcher_links_in_navbar(self):
        """Ensure flag switcher in base.html generates direct, crawlable <a> links without forms."""
        res = self.client.get('/ar/about/')
        self.assertEqual(res.status_code, 200)
        html = res.content.decode('utf-8')
        # Navbar flag switcher must be anchor tags, not forms
        self.assertIn('class="flag-btn', html)
        self.assertNotIn('<form action="/i18n/setlang/"', html)
        # Alternate languages must link cleanly
        self.assertIn('/en/about/', html)
        self.assertIn('/fr/about/', html)


class SEOPhase3Phase4AuditTest(TestCase):
    """
    Comprehensive tests for SEO Phase 3 (Meta Tags & Social) and Phase 4 (International SEO).
    """
    def setUp(self):
        from bs4 import BeautifulSoup
        self.soup_cls = BeautifulSoup
        self.service = Service.objects.create(
            title_en="Web Development in Tangier, Morocco",
            slug="web-development",
            seo_description_en="High-performance custom web development in Tangier, Morocco. Django and React engineering.",
            noindex=False,
        )
        self.city_page = CityServicePage.objects.create(
            service=self.service,
            city='tangier',
            slug='tangier',
            h1_en="Web Development Agency in Tangier, Morocco",
            seo_title_en="Web Development in Tangier | getNexiro",
            seo_description_en="Professional web development services for companies in Tangier, delivered by getNexiro studio.",
            is_published=True,
            noindex=False,
        )
        self.post = BlogPost.objects.create(
            title_en="Enterprise Web Engineering Guide",
            slug="enterprise-web-engineering-guide",
            body_en="<p>Detailed guide on enterprise engineering.</p>",
            status='published',
            noindex=False,
            index_in_sitemap=True,
        )

    def test_meta_title_and_description_constraints(self):
        """
        Phase 3:
        - Title <= 60 characters
        - Pattern: '<Topic> | getNexiro'
        - Description between 120 and 160 characters
        - No meta keywords tag
        """
        urls = [
            '/en/', '/fr/', '/ar/',
            '/en/about/', '/fr/about/', '/ar/about/',
            '/en/services/', '/fr/services/', '/ar/services/',
            '/en/services/web-development/',
            '/en/services/web-development/tangier/',
            '/en/blog/', '/fr/blog/', '/ar/blog/',
            '/en/contact/', '/fr/contact/', '/ar/contact/',
            '/en/blog/enterprise-web-engineering-guide/',
        ]
        for url in urls:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Page {url} did not return 200")
            html = res.content.decode('utf-8')
            soup = self.soup_cls(html, 'html.parser')

            # 1. No meta keywords
            self.assertIsNone(soup.find('meta', {'name': 'keywords'}), f"Found keywords meta on {url}")

            # 2. Title length <= 60
            title_tag = soup.find('title')
            self.assertIsNotNone(title_tag, f"Missing title tag on {url}")
            title_text = title_tag.text.strip()
            self.assertTrue(len(title_text) <= 60, f"Title on {url} exceeds 60 chars ({len(title_text)}): '{title_text}'")
            self.assertTrue(title_text.endswith('| getNexiro'), f"Title on {url} does not end with '| getNexiro': '{title_text}'")

            # 3. Description length 120 <= len <= 160
            desc_tag = soup.find('meta', {'name': 'description'})
            self.assertIsNotNone(desc_tag, f"Missing description on {url}")
            desc_text = desc_tag.get('content', '').strip()
            self.assertTrue(120 <= len(desc_text) <= 160, f"Description on {url} out of bounds ({len(desc_text)} chars): '{desc_text}'")

    def test_open_graph_and_twitter_sync(self):
        """
        Phase 3:
        - Twitter tags match Open Graph tags
        - og:locale matches language with alternates
        - og:image has 1200x630 or omitted dimensions (never logo.png declared as 1200x630)
        """
        for url in ['/en/about/', '/fr/about/', '/ar/about/']:
            res = self.client.get(url)
            soup = self.soup_cls(res.content.decode('utf-8'), 'html.parser')

            og_title = soup.find('meta', {'property': 'og:title'})['content']
            tw_title = soup.find('meta', {'name': 'twitter:title'})['content']
            self.assertEqual(og_title, tw_title)

            og_desc = soup.find('meta', {'property': 'og:description'})['content']
            tw_desc = soup.find('meta', {'name': 'twitter:description'})['content']
            self.assertEqual(og_desc, tw_desc)

            og_img = soup.find('meta', {'property': 'og:image'})['content']
            tw_img = soup.find('meta', {'name': 'twitter:image'})['content']
            self.assertEqual(og_img, tw_img)

            # Robots tag includes max-image-preview:large
            robots = soup.find('meta', {'name': 'robots'})['content']
            self.assertIn('max-image-preview:large', robots)

    def test_reciprocal_hreflang_and_x_default(self):
        """
        Phase 4:
        - Every page outputs reciprocal hreflang links for en, fr, ar, and x-default
        - All URLs are absolute
        """
        for url in ['/en/about/', '/fr/about/', '/ar/about/', '/en/services/web-development/tangier/']:
            res = self.client.get(url)
            soup = self.soup_cls(res.content.decode('utf-8'), 'html.parser')

            hreflangs = {link.get('hreflang'): link.get('href') for link in soup.find_all('link', {'rel': 'alternate'}) if link.get('hreflang')}
            for req_lang in ['en', 'fr', 'ar', 'x-default']:
                self.assertIn(req_lang, hreflangs, f"Missing hreflang '{req_lang}' on {url}")
                self.assertTrue(hreflangs[req_lang].startswith('https://getnexiro.com/'), f"Non-absolute hreflang on {url}: {hreflangs[req_lang]}")

    def test_arabic_slug_normalization_and_redirects(self):
        """
        Phase 4:
        - Arabic canonical URLs are clean ASCII (/ar/about/, /ar/services/web-development/tangier/)
        - Legacy Arabic-character URLs 301 redirect cleanly
        """
        redirects = [
            ('/ar/من-نحن/', '/ar/about/'),
            ('/ar/خدمات/', '/ar/services/'),
            ('/ar/خدمات/web-development/tangier/', '/ar/services/web-development/tangier/'),
            ('/ar/مشاريع/', '/ar/projects/'),
            ('/ar/مدونة/', '/ar/blog/'),
            ('/ar/تواصل/', '/ar/contact/'),
            ('/ar/من-نحن/ar/خدمات/', '/ar/services/'),
            ('/ar/خدمات/ar/مشاريع/', '/ar/projects/'),
        ]
        for src, dest in redirects:
            res = self.client.get(src)
            self.assertEqual(res.status_code, 301, f"{src} did not return 301")
            self.assertEqual(res.headers.get('Location'), dest, f"{src} redirected to {res.headers.get('Location')} instead of {dest}")

    def test_organization_and_localbusiness_structured_data(self):
        """
        Phase 5:
        - Organization & ProfessionalService schema with exact Tangier HQ address and geo
        - contactPoint with phone and email
        - areaServed and languages
        - No aggregateRating or reviews
        """
        res = self.client.get('/en/')
        soup = self.soup_cls(res.content.decode('utf-8'), 'html.parser')
        scripts = soup.find_all('script', {'type': 'application/ld+json'})
        org_schema = None
        for s in scripts:
            data = json.loads(s.string)
            types = data.get('@type')
            if types and ('ProfessionalService' in types or 'Organization' in types):
                org_schema = data
                break

        self.assertIsNotNone(org_schema, "Organization/ProfessionalService schema not found on homepage")
        self.assertEqual(org_schema.get('email'), 'contact@getnexiro.com')
        self.assertIn('+212', org_schema.get('telephone'))
        self.assertEqual(org_schema.get('geo', {}).get('latitude'), '35.7796')
        self.assertEqual(org_schema.get('geo', {}).get('longitude'), '-5.8030')
        self.assertIn('Ibn Batouta Bureaux', org_schema.get('address', {}).get('streetAddress'))
        self.assertEqual(org_schema.get('address', {}).get('postalCode'), '90000')
        self.assertEqual(org_schema.get('address', {}).get('addressCountry'), 'MA')

        # ContactPoint
        cp = org_schema.get('contactPoint')
        self.assertTrue(cp, "Missing contactPoint in Organization schema")

        # No fake reviews or aggregateRating
        self.assertNotIn('aggregateRating', org_schema)
        self.assertNotIn('review', org_schema)

    def test_breadcrumblist_on_inner_pages(self):
        """
        Phase 5:
        - BreadcrumbList present on all inner pages
        - Matching breadcrumb hierarchy with valid position and URLs
        """
        inner_urls = [
            '/en/about/',
            '/en/services/',
            '/en/services/web-development/',
            '/en/services/web-development/tangier/',
            '/en/projects/',
            '/en/blog/',
            '/en/contact/',
            '/en/packages/',
        ]
        for url in inner_urls:
            res = self.client.get(url)
            soup = self.soup_cls(res.content.decode('utf-8'), 'html.parser')
            bc_found = False
            for s in soup.find_all('script', {'type': 'application/ld+json'}):
                data = json.loads(s.string)
                if data.get('@type') == 'BreadcrumbList':
                    bc_found = True
                    items = data.get('itemListElement', [])
                    self.assertTrue(len(items) >= 2, f"Breadcrumb on {url} has fewer than 2 items")
                    for pos, item in enumerate(items, 1):
                        self.assertEqual(item.get('position'), pos)
                        self.assertTrue(item.get('name'))
                        self.assertTrue(item.get('item').startswith('https://getnexiro.com/'))
                    break
            self.assertTrue(bc_found, f"BreadcrumbList schema missing on {url}")

    def test_article_blogposting_and_service_schema(self):
        """
        Phase 5:
        - Article/BlogPosting on blog detail page with fallback image and required properties
        - Service schema on service detail and city service page
        - No FAQPage schema
        """
        # Blog detail BlogPosting
        res = self.client.get(f'/en/blog/{self.post.slug}/')
        soup = self.soup_cls(res.content.decode('utf-8'), 'html.parser')
        article_found = False
        for s in soup.find_all('script', {'type': 'application/ld+json'}):
            data = json.loads(s.string)
            if '@graph' in data:
                for item in data['@graph']:
                    if item.get('@type') == 'BlogPosting':
                        article_found = True
                        self.assertEqual(item.get('headline'), self.post.title)
                        self.assertTrue(item.get('image', {}).get('url'))
                        self.assertEqual(item.get('author', {}).get('@type'), 'Person')
                        self.assertEqual(item.get('publisher', {}).get('@type'), 'Organization')
        self.assertTrue(article_found, "BlogPosting schema not found on blog detail")

        # Service schema
        for s_url in ['/en/services/web-development/', '/en/services/web-development/tangier/']:
            res = self.client.get(s_url)
            soup = self.soup_cls(res.content.decode('utf-8'), 'html.parser')
            svc_found = any(json.loads(s.string).get('@type') == 'Service' for s in soup.find_all('script', {'type': 'application/ld+json'}))
            self.assertTrue(svc_found, f"Service schema not found on {s_url}")

        # No FAQPage schema anywhere
        res = self.client.get('/en/services/')
        soup = self.soup_cls(res.content.decode('utf-8'), 'html.parser')
        for s in soup.find_all('script', {'type': 'application/ld+json'}):
            self.assertNotEqual(json.loads(s.string).get('@type'), 'FAQPage', "FAQPage schema should be skipped")

    def test_jsonld_same_as_serialization(self):
        """
        Verify that SiteConfig and Author serialize social URLs via json.dumps,
        preventing any 'Missing comma or bracket in array declaration' parsing errors in JSON-LD.
        """
        config, _ = SiteConfig.objects.get_or_create(pk=1)
        config.instagram_url = "https://instagram.com/getnexiro"
        config.twitter_url = "https://x.com/getnexiro"
        config.linkedin_url = ""
        config.github_url = "https://github.com/getnexiro"
        config.save()

        self.assertEqual(len(config.same_as_list), 3)
        self.assertIn("https://instagram.com/getnexiro", config.same_as_list)
        self.assertIn("https://x.com/getnexiro", config.same_as_list)
        self.assertIn("https://github.com/getnexiro", config.same_as_list)

        parsed_config_json = json.loads(config.same_as_json)
        self.assertIsInstance(parsed_config_json, list)
        self.assertEqual(len(parsed_config_json), 3)

        author = Author.objects.create(
            name="Test Lead Architect",
            slug="test-lead-architect",
            linkedin_url="https://linkedin.com/in/test",
            github_url="",
            twitter_url="https://twitter.com/test",
            website_url="https://test.com"
        )
        self.assertEqual(len(author.same_as_list), 3)
        parsed_author_json = json.loads(author.same_as_json)
        self.assertIsInstance(parsed_author_json, list)
        self.assertEqual(len(parsed_author_json), 3)

        # Test actual HTTP response and JSON-LD parsing on the author page
        res = self.client.get(f'/en/blog/author/{author.slug}/')
        self.assertEqual(res.status_code, 200)
        soup = self.soup_cls(res.content.decode('utf-8'), 'html.parser')
        scripts = soup.find_all('script', {'type': 'application/ld+json'})
        self.assertTrue(len(scripts) >= 1)
        for s in scripts:
            data = json.loads(s.string)
            self.assertIsInstance(data, dict)
            if data.get('@type') == 'Person':
                self.assertEqual(data.get('sameAs'), [
                    "https://linkedin.com/in/test",
                    "https://twitter.com/test",
                    "https://test.com"
                ])

    def test_phase6_sitemap_and_robots(self):
        """
        Phase 6:
        - Sitemap includes only 200, indexable, canonical URLs with accurate lastmod
        - robots.txt allows all, disallows admin & search/filter params, references sitemap
        - Root / 301 redirects to /en/
        - Canonical non-www host redirect works in a single hop
        """
        # 1. robots.txt
        res_robots = self.client.get('/robots.txt')
        self.assertEqual(res_robots.status_code, 200)
        content_robots = res_robots.content.decode('utf-8')
        self.assertIn('Allow: /', content_robots)
        self.assertIn('Disallow: /admin/', content_robots)
        self.assertIn('Disallow: /*?search=*', content_robots)
        self.assertIn('Disallow: /*?category=*', content_robots)
        self.assertIn('Sitemap: https://getnexiro.com/sitemap.xml', content_robots)

        # 2. Root / 301 redirects to /en/
        res_root = self.client.get('/')
        self.assertEqual(res_root.status_code, 301)
        self.assertEqual(res_root.headers.get('Location'), '/en/')

        # 3. Canonical www -> non-www single hop
        res_www = self.client.get('/en/', HTTP_HOST='www.getnexiro.com')
        self.assertEqual(res_www.status_code, 301)
        self.assertEqual(res_www.headers.get('Location'), 'https://getnexiro.com/en/')

        # 4. Sitemap.xml content audit
        res_sitemap = self.client.get('/sitemap.xml')
        self.assertEqual(res_sitemap.status_code, 200)
        content_sitemap = res_sitemap.content.decode('utf-8')
        self.assertIn('<urlset', content_sitemap)
        self.assertIn('https://getnexiro.com/en/', content_sitemap)
        self.assertIn('https://getnexiro.com/fr/', content_sitemap)
        self.assertIn('https://getnexiro.com/ar/', content_sitemap)
        # Excludes noindex city pages (tetouan, fes, meknes)
        self.assertNotIn('/tetouan/', content_sitemap)
        self.assertNotIn('/fes/', content_sitemap)
        self.assertNotIn('/meknes/', content_sitemap)
        # Includes indexable city page (tangier)
        self.assertIn('https://getnexiro.com/en/services/web-development/tangier/', content_sitemap)
        self.assertIn('https://getnexiro.com/ar/services/web-development/tangier/', content_sitemap)

    def test_phase7_performance_and_media(self):
        """
        Phase 7:
        - Hero background video has preload='none' and a poster image
        - Carousel clones have aria-hidden='true' and empty alt
        - Key templates output width, height, and alt on images
        """
        res = self.client.get('/en/')
        self.assertEqual(res.status_code, 200)
        soup = self.soup_cls(res.content.decode('utf-8'), 'html.parser')

        # Video tag preload and poster check
        for video in soup.find_all('video', class_='hero-bg-video'):
            self.assertEqual(video.get('preload'), 'none')
            self.assertTrue(video.get('poster'))

        # Marquee clone check
        for clone in soup.find_all('div', class_='client-logo-item', attrs={'aria-hidden': 'true'}):
            img = clone.find('img')
            if img:
                self.assertEqual(img.get('alt'), '')

    def test_phase8_onpage_polish_and_internal_linking(self):
        """
        Phase 8:
        - Contact page has lazy-loaded Google Maps embed for Tangier HQ
        - Service detail page links to related technical blog articles
        - Blog detail page links to related engineering services
        - No personal GitHub repo link in footer
        """
        # 1. Contact page Google Maps embed
        res_contact = self.client.get('/en/contact/')
        soup_contact = self.soup_cls(res_contact.content.decode('utf-8'), 'html.parser')
        iframe = soup_contact.find('iframe')
        self.assertIsNotNone(iframe, "Missing map iframe on contact page")
        self.assertEqual(iframe.get('loading'), 'lazy')
        self.assertIn('maps.google.com', iframe.get('src', ''))

        # 2. Service detail links to related blog posts
        res_svc = self.client.get('/en/services/web-development/')
        soup_svc = self.soup_cls(res_svc.content.decode('utf-8'), 'html.parser')
        blog_links = soup_svc.find_all('a', href=re.compile(r'/en/blog/'))
        self.assertTrue(len(blog_links) > 0, "Service page missing internal links to blog")

        # 3. Blog detail links to relevant engineering services
        res_blog = self.client.get(f'/en/blog/{self.post.slug}/')
        soup_blog = self.soup_cls(res_blog.content.decode('utf-8'), 'html.parser')
        svc_links = soup_blog.find_all('a', href=re.compile(r'/en/services/'))
        self.assertTrue(len(svc_links) > 0, "Blog detail missing internal links to services")

        # 4. No public personal github repo link in footer
        footer = soup_contact.find('footer')
        self.assertIsNotNone(footer)
        personal_gh = footer.find('a', href=re.compile(r'github\.com/simoderkaoui', re.IGNORECASE))
        self.assertIsNone(personal_gh, "Personal GitHub repo link should not be present in public footer")


class AdminProjectSaveTest(TestCase):
    """Ensure saving a project in the Django admin never crashes with 500."""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='adminuser',
            email='adminuser@example.com',
            password='testpassword123'
        )
        self.client.login(username='adminuser', password='testpassword123')
        self.category = ProjectCategory.objects.create(
            name_en='SaaS',
            slug='saas'
        )
        self.project = Project.objects.create(
            title_en='Test Project',
            title_fr='Projet Test',
            title_ar='مشروع تجريبي',
            slug='test-project',
            category=self.category,
            order=1
        )

    def test_save_project_without_inline_management_form_fields(self):
        """Omitting gallery_images management form fields must NOT cause 500."""
        post_data = {
            'title_en': 'Updated Test Project',
            'title_fr': 'Projet Test MAJ',
            'title_ar': 'مشروع تجريبي محدث',
            'slug': 'updated-test-project',
            'category': self.category.pk,
            'description_en': 'Clean description',
            'description_fr': 'Description propre',
            'description_ar': 'وصف نظيف',
            'order': 1,
            '_save': 'Save',
        }
        response = self.client.post(
            f'/en/admin/core/project/{self.project.pk}/change/',
            post_data,
            follow=False
        )
        # Must redirect on success, never return 500
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title_en, 'Updated Test Project')

    def test_save_project_preserves_existing_gallery_images(self):
        """Saving project when inline management form is omitted must preserve existing gallery images."""
        img1 = ProjectImage.objects.create(
            project=self.project,
            image='projects/gallery/test1.jpg',
            caption_en='Screen 1',
            order=1
        )
        img2 = ProjectImage.objects.create(
            project=self.project,
            image='projects/gallery/test2.jpg',
            caption_en='Screen 2',
            order=2
        )
        self.assertEqual(self.project.gallery_images.count(), 2)

        post_data = {
            'title_en': 'Updated Title',
            'title_fr': 'Titre MAJ',
            'title_ar': 'عنوان محدث',
            'slug': 'updated-title',
            'category': self.category.pk,
            'description_en': 'Desc',
            'description_fr': 'Desc',
            'description_ar': 'Desc',
            'order': 1,
            '_continue': 'Save and continue editing',
        }
        response = self.client.post(
            f'/en/admin/core/project/{self.project.pk}/change/',
            post_data,
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        # Both images must still exist untouched
        self.assertEqual(self.project.gallery_images.count(), 2)
        self.assertTrue(ProjectImage.objects.filter(pk=img1.pk).exists())
        self.assertTrue(ProjectImage.objects.filter(pk=img2.pk).exists())


# ── Phase 6: Tests for the 5 New Production Features ─────────────────

class FiveFeaturesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_search_api_empty_query(self):
        res = self.client.get('/en/search/?q=a')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['total'], 0)
        self.assertEqual(len(data['groups']), 0)

    def test_search_api_matches(self):
        res = self.client.get('/en/search/?q=web')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue('groups' in data)
        self.assertIn('total', data)

    def test_sticky_mini_cta_included(self):
        res = self.client.get('/en/')
        self.assertContains(res, 'id="stickyMiniCta"')
        self.assertContains(res, 'https://wa.me/212787862187')

    def test_sticky_mini_cta_excluded_on_contact(self):
        res = self.client.get('/en/contact/')
        self.assertNotContains(res, 'id="stickyMiniCta"')

    def test_newsletter_subscribe_success(self):
        res = self.client.post('/en/newsletter/subscribe/', {
            'email': 'techlead@moroccotips.ma',
            'language': 'en',
            'website_url': '',
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['status'], 'success')
        sub = Subscriber.objects.get(email='techlead@moroccotips.ma')
        self.assertFalse(sub.is_confirmed)
        self.assertTrue(bool(sub.confirmation_token))

    def test_newsletter_subscribe_honeypot(self):
        res = self.client.post('/en/newsletter/subscribe/', {
            'email': 'spambot@example.com',
            'language': 'en',
            'website_url': 'http://spam-site.com',
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['status'], 'success')
        # Bot is silently ignored, not saved to DB
        self.assertFalse(Subscriber.objects.filter(email='spambot@example.com').exists())

    def test_client_dashboard_demo_view(self):
        res = self.client.get('/en/client-dashboard-demo/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Client Dashboard Demo')
        self.assertContains(res, 'TKT-2026-401')
        self.assertContains(res, '28,000 MAD')
        self.assertContains(res, '<link rel="canonical"')
        self.assertContains(res, 'hreflang="fr"')

    def test_process_timeline_included_home_and_about(self):
        res_home = self.client.get('/en/')
        self.assertContains(res_home, 'id="ourProcessTimeline"')
        self.assertContains(res_home, '01')
        self.assertContains(res_home, 'Discovery & Architecture')

        res_about = self.client.get('/en/about/')
        self.assertContains(res_about, 'id="ourProcessTimeline"')

    def test_send_newsletter_command_dry_run(self):
        from io import StringIO
        from django.core.management import call_command
        Subscriber.objects.create(
            email='active@client.ma',
            is_confirmed=True,
            status='confirmed',
            language='fr'
        )
        out = StringIO()
        call_command('send_newsletter', '--subject=Test Subject', '--body=<p>Hello World</p>', '--dry-run', stdout=out)
        self.assertIn('[DRY-RUN] Would send to 1 subscriber(s)', out.getvalue())






