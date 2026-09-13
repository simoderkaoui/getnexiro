from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import activate
from core.models import (
    SiteConfig, Service, ProjectCategory, Project,
    TeamMember, Testimonial, Stat, ContactMessage,
    CompanyValue, ProcessStep, StoreItem,
)
from core.forms import ContactForm


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

    def test_store_page(self):
        response = self.client.get(reverse('core:store'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_get(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_form_submission(self):
        post_data = {
            'name': 'Karim Test',
            'email': 'karim@example.com',
            'subject': 'Inquiry regarding web platform',
            'message': 'Hello, we would like to build a new platform with your team.',
        }
        response = self.client.post(reverse('core:contact'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='karim@example.com').exists())



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

