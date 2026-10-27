"""
Contact and Lead Generation forms for getNexiro.
"""

from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    """Contact form with name, email, subject, and message fields."""

    name = forms.CharField(
        label=_('Full Name'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': _('Your full name'),
            'class': 'form-input',
        }),
    )

    email = forms.EmailField(
        label=_('Email Address'),
        widget=forms.EmailInput(attrs={
            'placeholder': _('your@email.com'),
            'class': 'form-input',
        }),
    )

    subject = forms.CharField(
        label=_('Subject'),
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': _('How can we help?'),
            'class': 'form-input',
        }),
    )

    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea(attrs={
            'placeholder': _('Tell us about your project...'),
            'class': 'form-input form-textarea',
            'rows': 6,
        }),
    )

    # Optional high-precision browser GPS fields
    geo_lat = forms.CharField(required=False, widget=forms.HiddenInput())
    geo_lon = forms.CharField(required=False, widget=forms.HiddenInput())
    geo_accuracy = forms.CharField(required=False, widget=forms.HiddenInput())
    geo_city = forms.CharField(required=False, widget=forms.HiddenInput())


# ══════════════════════════════════════════════════════════════
# PHASE 2: Lead Generation Forms
# ══════════════════════════════════════════════════════════════


class QuoteStep1Form(forms.Form):
    """Step 1: Project type and description."""

    PROJECT_TYPE_CHOICES = [
        ('', _('— Select project type —')),
        ('website', _('Corporate Website')),
        ('ecommerce', _('E-Commerce Store')),
        ('webapp', _('Web Application / SaaS')),
        ('mobile', _('Mobile Application')),
        ('redesign', _('Website Redesign')),
        ('other', _('Other / Custom')),
    ]

    project_type = forms.ChoiceField(
        label=_('What type of project do you need?'),
        choices=PROJECT_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    project_description = forms.CharField(
        label=_('Tell us about your project'),
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Briefly describe what you want to build...'),
            'class': 'form-input form-textarea',
            'rows': 4,
        }),
    )


class QuoteStep2Form(forms.Form):
    """Step 2: Features, pages, and languages."""

    NUM_PAGES_CHOICES = [
        ('', _('— Select —')),
        ('1-5', '1 — 5'),
        ('5-10', '5 — 10'),
        ('10-20', '10 — 20'),
        ('20+', '20+'),
    ]

    # Features will be rendered as checkboxes from PricingRule objects
    features = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        help_text=_('Comma-separated feature keys'),
    )

    num_pages = forms.ChoiceField(
        label=_('Number of pages or screens'),
        choices=NUM_PAGES_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    num_languages = forms.IntegerField(
        label=_('Number of languages'),
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'min': '1', 'max': '10'}),
    )


class QuoteStep3Form(forms.Form):
    """Step 3: Timeline and budget."""

    TIMELINE_CHOICES = [
        ('', _('— Select timeline —')),
        ('asap', _('ASAP (rush)')),
        ('1-2months', _('1 — 2 months')),
        ('2-4months', _('2 — 4 months')),
        ('4-6months', _('4 — 6 months')),
        ('flexible', _('Flexible')),
    ]

    BUDGET_CHOICES = [
        ('', _('— Select budget range —')),
        ('5k-15k', '5,000 — 15,000 MAD'),
        ('15k-30k', '15,000 — 30,000 MAD'),
        ('30k-60k', '30,000 — 60,000 MAD'),
        ('60k-100k', '60,000 — 100,000 MAD'),
        ('100k+', '100,000+ MAD'),
        ('unsure', _('Not sure yet')),
    ]

    timeline = forms.ChoiceField(
        label=_('When do you need this delivered?'),
        choices=TIMELINE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    budget_range = forms.ChoiceField(
        label=_('What is your budget range?'),
        choices=BUDGET_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )


class QuoteStep4Form(forms.Form):
    """Step 4: Contact information."""

    name = forms.CharField(
        label=_('Full Name'),
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': _('Your full name'),
            'class': 'form-input',
        }),
    )

    email = forms.EmailField(
        label=_('Email Address'),
        widget=forms.EmailInput(attrs={
            'placeholder': _('your@email.com'),
            'class': 'form-input',
        }),
    )

    phone = forms.CharField(
        label=_('Phone Number'),
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('+212 6XX XXX XXX'),
            'class': 'form-input',
        }),
    )

    company = forms.CharField(
        label=_('Company Name'),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('Your company (optional)'),
            'class': 'form-input',
        }),
    )

    # Honeypot
    website_url = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'tabindex': '-1',
            'autocomplete': 'off',
            'style': 'position:absolute;left:-9999px;',
        }),
    )


class BookingForm(forms.Form):
    """Discovery call booking form."""

    name = forms.CharField(
        label=_('Full Name'),
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': _('Your full name'),
            'class': 'form-input',
        }),
    )

    email = forms.EmailField(
        label=_('Email Address'),
        widget=forms.EmailInput(attrs={
            'placeholder': _('your@email.com'),
            'class': 'form-input',
        }),
    )

    phone = forms.CharField(
        label=_('Phone Number'),
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('+212 6XX XXX XXX'),
            'class': 'form-input',
        }),
    )

    company = forms.CharField(
        label=_('Company Name'),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('Your company (optional)'),
            'class': 'form-input',
        }),
    )

    date = forms.DateField(
        label=_('Preferred Date'),
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input',
        }),
    )

    time_slot = forms.TimeField(
        label=_('Preferred Time (GMT+1)'),
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    message = forms.CharField(
        label=_('Tell us briefly about your project'),
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('What would you like to discuss?'),
            'class': 'form-input form-textarea',
            'rows': 3,
        }),
    )

    # Honeypot
    website_url = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'tabindex': '-1',
            'autocomplete': 'off',
            'style': 'position:absolute;left:-9999px;',
        }),
    )


class SubscriberForm(forms.Form):
    """Lead magnet / newsletter signup form."""

    email = forms.EmailField(
        label=_('Email Address'),
        widget=forms.EmailInput(attrs={
            'placeholder': _('your@email.com'),
            'class': 'form-input',
        }),
    )

    name = forms.CharField(
        label=_('Your Name'),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('Your name (optional)'),
            'class': 'form-input',
        }),
    )

    consent = forms.BooleanField(
        label=_('I agree to receive occasional emails from getNexiro. I can unsubscribe at any time.'),
        required=True,
    )

    # Honeypot
    website_url = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'tabindex': '-1',
            'autocomplete': 'off',
            'style': 'position:absolute;left:-9999px;',
        }),
    )
