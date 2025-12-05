from django.db import models
from django.core.validators import FileExtensionValidator


class Application(models.Model):
    SITUATION_CHOICES = [
        ('employed', 'En emploi (CDI/CDD)'),
        ('freelance', 'Freelance / Auto-entrepreneur'),
        ('student', 'Étudiant(e)'),
        ('seeking', 'En recherche active'),
        ('other', 'Autre'),
    ]

    AVAILABILITY_CHOICES = [
        ('immediate', 'Immédiate'),
        ('week', 'Sous 1 semaine'),
        ('twoweeks', 'Sous 2 semaines'),
        ('month', 'Sous 1 mois'),
        ('later', 'Plus tard (préciser)'),
    ]

    FLEXIBILITY_CHOICES = [
        ('yes', 'Oui, totalement'),
        ('conditions', 'Oui, mais sous conditions (préciser)'),
        ('no', 'Non, uniquement temps partiel'),
    ]

    HOURS_CHOICES = [
        ('20-25', '20-25h'),
        ('25-30', '25-30h'),
        ('30-35', '30-35h'),
        ('35-40', '35-40h'),
        ('40+', '40h et plus'),
    ]

    WORK_MODE_CHOICES = [
        ('remote', '100% télétravail'),
        ('office', '100% sur site'),
        ('hybrid', 'Hybride'),
        ('flexible', 'Flexible / Indifférent'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Section 1: General Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    cv = models.FileField(
        upload_to='cvs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    linkedin = models.URLField(blank=True, null=True)

    # Section 2: Profile & Availability
    current_situation = models.CharField(max_length=50, choices=SITUATION_CHOICES)
    contract_types = models.JSONField(default=list)
    availability = models.CharField(max_length=50, choices=AVAILABILITY_CHOICES)
    availability_details = models.TextField(blank=True, null=True)
    full_time_flexibility = models.CharField(max_length=50, choices=FLEXIBILITY_CHOICES)
    full_time_conditions = models.TextField(blank=True, null=True)
    weekly_hours = models.CharField(max_length=20, choices=HOURS_CHOICES)
    time_slots = models.JSONField(default=list)
    week_days = models.JSONField(default=list)
    week_days_details = models.TextField(blank=True, null=True)
    work_mode = models.CharField(max_length=50, choices=WORK_MODE_CHOICES)
    personal_constraints = models.TextField(blank=True, null=True)

    # Section 3: Languages
    languages = models.JSONField(default=list)

    # Section 4: Poste(s) Visé(s)
    target_positions = models.JSONField(default=list)
    priority_position = models.CharField(max_length=200, blank=True, null=True)

    # Section 5: Experience
    has_call_center_experience = models.CharField(max_length=10, blank=True, null=True)

    # Section 6: Detailed Experiences
    experiences = models.JSONField(default=list, blank=True)

    # Section 7: Performance & KPIs
    worked_with_kpis = models.CharField(max_length=50, blank=True, null=True)
    top_performer = models.CharField(max_length=50, blank=True, null=True)
    achievement_story = models.TextField(blank=True, null=True)

    # Section 8: Equipment & Working Conditions
    equipment_types = models.JSONField(default=list, blank=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    has_headset = models.CharField(max_length=100, blank=True, null=True)
    internet_connection_type = models.CharField(max_length=100, blank=True, null=True)
    speedtest_result = models.TextField(blank=True, null=True)  # Kept for backward compatibility
    download_speed = models.FloatField(null=True, blank=True, help_text="Download speed in Mbps")
    upload_speed = models.FloatField(null=True, blank=True, help_text="Upload speed in Mbps")
    workspace_type = models.CharField(max_length=200, blank=True, null=True)
    work_agreements = models.JSONField(default=list, blank=True)

    # Section 9: Compensation (in DT)
    payment_modes_accepted = models.JSONField(default=list, blank=True)
    preferred_payment_mode = models.CharField(max_length=200, blank=True, null=True)
    salary_expectations = models.CharField(max_length=200, blank=True, null=True)
    accept_variable_compensation = models.CharField(max_length=50, blank=True, null=True)

    # Section 10: Mindset & Soft Skills
    difficult_client_response = models.TextField(blank=True, null=True)
    preferred_work_environment = models.CharField(max_length=200, blank=True, null=True)
    three_qualities = models.TextField(blank=True, null=True)
    three_improvements = models.TextField(blank=True, null=True)
    has_coached_colleague = models.CharField(max_length=10, blank=True, null=True)

    # Section 11: Supervision (if applicable)
    supervisor_experience = models.CharField(max_length=10, blank=True, null=True)
    team_size_managed = models.CharField(max_length=100, blank=True, null=True)
    management_style = models.TextField(blank=True, null=True)

    # Section 12: Audio Recording
    audio_recording = models.FileField(
        upload_to='audio_recordings/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'webm', 'ogg', 'm4a'])]
    )

    # Section 13: WhatsApp Interview
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    interview_availability = models.TextField(blank=True, null=True)

    # Reference number
    reference_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    # Recruiter fields
    STATUS_CHOICES = [
        ('new', '🆕 New'),
        ('to_contact', '📲 To Contact'),
        ('contacted', '📧 Contacted'),
        ('interview', '📅 Interview Scheduled'),
        ('hired', '✅ Hired'),
        ('rejected', '❌ Rejected'),
        ('archived', '📦 Archived'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    recruiter_score = models.IntegerField(null=True, blank=True, help_text="Score from 1 to 10")
    last_contacted = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_applications')

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.reference_number:
            import random
            self.reference_number = f"#{random.randint(10000000, 99999999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class LanguageDetail(models.Model):
    """Detailed language proficiency for each candidate"""

    GLOBAL_LEVEL_CHOICES = [
        ('A1', 'A1 – Débutant'),
        ('A2', 'A2 – Élémentaire'),
        ('B1', 'B1 – Intermédiaire'),
        ('B2', 'B2 – Intermédiaire avancé'),
        ('C1', 'C1 – Avancé'),
        ('C2', 'C2 – Bilingue / Langue maternelle'),
    ]

    SKILL_LEVEL_CHOICES = [
        ('faible', 'Faible'),
        ('moyen', 'Moyen'),
        ('bon', 'Bon'),
        ('excellent', 'Excellent'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='language_details')
    language = models.CharField(max_length=50)
    global_level = models.CharField(max_length=20, choices=GLOBAL_LEVEL_CHOICES, default='B1')
    listening_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='moyen')
    speaking_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='moyen')
    writing_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='moyen')

    class Meta:
        unique_together = ['application', 'language']
        ordering = ['language']

    def __str__(self):
        return f"{self.application.reference_number} - {self.language} ({self.global_level})"
