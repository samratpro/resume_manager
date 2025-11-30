from django.contrib import admin
from .models import Application, LanguageDetail


class LanguageDetailInline(admin.TabularInline):
    model = LanguageDetail
    extra = 0
    fields = ['language', 'level', 'oral_level', 'written_level', 'phone_experience']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'last_name', 'first_name', 'email', 'phone', 'country', 'status', 'recruiter_score', 'created_at']
    list_filter = ['created_at', 'status', 'country', 'current_situation', 'work_mode', 'has_call_center_experience']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'reference_number']
    readonly_fields = ['created_at', 'updated_at', 'reference_number']
    inlines = [LanguageDetailInline]

    fieldsets = (
        ('Référence', {
            'fields': ('reference_number',)
        }),
        ('Section 1: Informations personnelles', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'country', 'city', 'phone', 'email')
        }),
        ('Section 1: Documents', {
            'fields': ('cv', 'linkedin')
        }),
        ('Section 2: Profil & Disponibilités', {
            'fields': (
                'current_situation', 'contract_types', 'availability', 'availability_details',
                'full_time_flexibility', 'full_time_conditions', 'weekly_hours',
                'time_slots', 'week_days', 'week_days_details', 'work_mode', 'personal_constraints'
            )
        }),
        ('Section 3: Langues', {
            'fields': ('languages',)
        }),
        ('Section 4: Poste(s) Visé(s)', {
            'fields': ('target_positions', 'priority_position')
        }),
        ('Section 5: Expérience Call Center', {
            'fields': ('has_call_center_experience',)
        }),
        ('Section 6: Expériences Détaillées', {
            'fields': ('experiences',)
        }),
        ('Section 7: Performance & KPIs', {
            'fields': ('worked_with_kpis', 'top_performer', 'achievement_story')
        }),
        ('Section 8: Matériel & Conditions', {
            'fields': (
                'equipment_types', 'operating_system', 'has_headset',
                'internet_connection_type', 'speedtest_result', 'workspace_type', 'work_agreements'
            )
        }),
        ('Section 9: Rémunération (DT)', {
            'fields': (
                'payment_modes_accepted', 'preferred_payment_mode',
                'salary_expectations', 'accept_variable_compensation'
            )
        }),
        ('Section 10: Mindset & Soft Skills', {
            'fields': (
                'difficult_client_response', 'preferred_work_environment',
                'three_qualities', 'three_improvements', 'has_coached_colleague'
            )
        }),
        ('Section 11: Supervision', {
            'fields': ('supervisor_experience', 'team_size_managed', 'management_style')
        }),
        ('Section 12: Enregistrement Audio', {
            'fields': ('audio_recording',)
        }),
        ('Section 13: WhatsApp Interview', {
            'fields': ('whatsapp_number', 'interview_availability')
        }),
        ('Gestion Recruteur', {
            'fields': ('status', 'recruiter_score', 'assigned_to', 'last_contacted'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LanguageDetail)
class LanguageDetailAdmin(admin.ModelAdmin):
    list_display = ['application', 'language', 'level', 'oral_level', 'written_level', 'phone_experience']
    list_filter = ['language', 'level']
    search_fields = ['application__email', 'application__first_name', 'application__last_name']
