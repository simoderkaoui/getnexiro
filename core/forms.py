"""
Contact form for getNexiro.
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
