from django import forms
from django.forms import inlineformset_factory
from .models import Application, LanguageDetail


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'country', 'city',
            'phone', 'email', 'cv', 'linkedin',
            'current_situation', 'contract_types', 'availability', 'availability_details',
            'full_time_flexibility', 'full_time_conditions', 'weekly_hours',
            'time_slots', 'week_days', 'week_days_details', 'work_mode', 'personal_constraints',
            'languages'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre nom'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre pays'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre ville'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+216 XX XXX XXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'votre@email.com'
            }),
            'cv': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': '.pdf,.doc,.docx'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://linkedin.com/in/votre-profil'
            }),
            'availability_details': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Disponible à partir du 15 janvier'
            }),
            'full_time_conditions': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Décrivez vos contraintes...',
                'rows': 3
            }),
            'week_days_details': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Expliquez votre planning variable...',
                'rows': 3
            }),
            'personal_constraints': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Ex: autre emploi, études, garde d\'enfants, déplacements...',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certain fields optional
        self.fields['cv'].required = False
        self.fields['linkedin'].required = False
        self.fields['availability_details'].required = False
        self.fields['full_time_conditions'].required = False
        self.fields['week_days_details'].required = False
        self.fields['personal_constraints'].required = False

    def clean(self):
        cleaned_data = super().clean()

        # Validate conditional fields
        availability = cleaned_data.get('availability')
        if availability == 'later' and not cleaned_data.get('availability_details'):
            self.add_error('availability_details', 'Ce champ est requis lorsque vous choisissez "Plus tard"')

        full_time_flexibility = cleaned_data.get('full_time_flexibility')
        if full_time_flexibility == 'conditions' and not cleaned_data.get('full_time_conditions'):
            self.add_error('full_time_conditions', 'Ce champ est requis lorsque vous avez des conditions')

        # Validate that at least one contract type is selected
        contract_types = self.data.getlist('contract_types')
        if not contract_types:
            raise forms.ValidationError("Veuillez sélectionner au moins un type de contrat")

        # Validate that at least one time slot is selected
        time_slots = self.data.getlist('time_slots')
        if not time_slots:
            raise forms.ValidationError("Veuillez sélectionner au moins une tranche horaire")

        # Validate that at least one day is selected
        week_days = self.data.getlist('week_days')
        if not week_days:
            raise forms.ValidationError("Veuillez sélectionner au moins un jour de disponibilité")

        # Validate that at least one language is selected
        languages = self.data.getlist('languages')
        if not languages:
            raise forms.ValidationError("Veuillez sélectionner au moins une langue")

        return cleaned_data


class LanguageDetailForm(forms.ModelForm):
    class Meta:
        model = LanguageDetail
        fields = ['language', 'level', 'oral_level', 'written_level', 'phone_experience']
        widgets = {
            'language': forms.HiddenInput(),
            'level': forms.RadioSelect(attrs={'class': 'radio-group'}),
            'oral_level': forms.RadioSelect(attrs={'class': 'radio-group'}),
            'written_level': forms.RadioSelect(attrs={'class': 'radio-group'}),
            'phone_experience': forms.RadioSelect(attrs={'class': 'radio-group'}),
        }


LanguageDetailFormSet = inlineformset_factory(
    Application,
    LanguageDetail,
    form=LanguageDetailForm,
    extra=6,  # Support up to 6 languages
    max_num=6,
    can_delete=False
)
