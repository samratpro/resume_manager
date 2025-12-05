from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Application, LanguageDetail
import json


def home(request):
    return render(request, 'resumemanager/home.html')


def application_form(request):
    if request.method == 'POST':
        try:
            # Debug: Print what we're receiving
            print("=" * 50)
            print("FORM SUBMISSION RECEIVED")
            print("=" * 50)
            print("POST data keys:", list(request.POST.keys()))
            print("FILES data keys:", list(request.FILES.keys()))

            # Create application instance
            application = Application()

            # Section 1: General Information
            application.first_name = request.POST.get('first_name', '')
            application.last_name = request.POST.get('last_name', '')
            application.date_of_birth = request.POST.get('date_of_birth')
            application.country = request.POST.get('country', '')
            application.city = request.POST.get('city', '')
            application.phone = request.POST.get('phone', '')
            application.email = request.POST.get('email', '')
            application.linkedin = request.POST.get('linkedin', '')

            print(f"Section 1 - Name: {application.first_name} {application.last_name}")

            # File uploads
            if request.FILES.get('cv'):
                application.cv = request.FILES['cv']
                print("CV uploaded:", application.cv.name)
            if request.FILES.get('audio_recording'):
                application.audio_recording = request.FILES['audio_recording']
                print("Audio uploaded:", application.audio_recording.name)

            # Section 2: Profile & Availability
            application.current_situation = request.POST.get('current_situation', '')
            application.contract_types = request.POST.getlist('contract_types')
            application.availability = request.POST.get('availability', '')
            application.availability_details = request.POST.get('availability_details', '')
            application.full_time_flexibility = request.POST.get('full_time_flexibility', '')
            application.full_time_conditions = request.POST.get('full_time_conditions', '')
            application.weekly_hours = request.POST.get('weekly_hours', '')
            application.time_slots = request.POST.getlist('time_slots')
            application.week_days = request.POST.getlist('week_days')
            application.week_days_details = request.POST.get('week_days_details', '')
            application.work_mode = request.POST.get('work_mode', '')
            application.personal_constraints = request.POST.get('personal_constraints', '')

            print(f"Section 2 - Situation: {application.current_situation}")
            print(f"Section 2 - Contract types: {application.contract_types}")

            # Section 3: Languages (kept for backward compatibility)
            application.languages = request.POST.getlist('languages')
            print(f"Section 3 - Languages: {application.languages}")

            # Section 4: Target Positions
            application.target_positions = request.POST.getlist('target_positions')
            application.priority_position = request.POST.get('priority_position', '')
            print(f"Section 4 - Positions: {application.target_positions}")

            # Section 5: Experience
            application.has_call_center_experience = request.POST.get('has_call_center_experience', '')
            print(f"Section 5 - Has experience: {application.has_call_center_experience}")

            # Section 6: Detailed Experiences
            experiences_json = request.POST.get('experiences_json', '[]')
            try:
                application.experiences = json.loads(experiences_json)
                print(f"Section 6 - Experiences: {len(application.experiences)} entries")
            except:
                application.experiences = []

            # Section 7: Performance & KPIs
            application.worked_with_kpis = request.POST.get('worked_with_kpis', '')
            application.top_performer = request.POST.get('top_performer', '')
            application.achievement_story = request.POST.get('achievement_story', '')
            print(f"Section 7 - KPIs: {application.worked_with_kpis}")

            # Section 8: Equipment
            application.equipment_types = request.POST.getlist('equipment_types')
            application.operating_system = request.POST.get('operating_system', '')
            application.has_headset = request.POST.get('has_headset', '')
            application.internet_connection_type = request.POST.get('internet_connection_type', '')

            # Speedtest - new numeric fields
            download_speed = request.POST.get('download_speed', '')
            upload_speed = request.POST.get('upload_speed', '')
            application.download_speed = float(download_speed) if download_speed else None
            application.upload_speed = float(upload_speed) if upload_speed else None

            application.workspace_type = request.POST.get('workspace_type', '')
            application.work_agreements = request.POST.getlist('work_agreements')
            print(f"Section 8 - Equipment: {application.equipment_types}")
            print(f"Section 8 - Speedtest: Download={application.download_speed}Mbps, Upload={application.upload_speed}Mbps")

            # Section 9: Compensation
            application.payment_modes_accepted = request.POST.getlist('payment_modes_accepted')
            application.preferred_payment_mode = request.POST.get('preferred_payment_mode', '')
            application.salary_expectations = request.POST.get('salary_expectations', '')
            application.accept_variable_compensation = request.POST.get('accept_variable_compensation', '')
            print(f"Section 9 - Payment modes: {application.payment_modes_accepted}")

            # Section 10: Mindset
            application.difficult_client_response = request.POST.get('difficult_client_response', '')
            application.preferred_work_environment = request.POST.get('preferred_work_environment', '')
            application.three_qualities = request.POST.get('three_qualities', '')
            application.three_improvements = request.POST.get('three_improvements', '')
            application.has_coached_colleague = request.POST.get('has_coached_colleague', '')
            print(f"Section 10 - Work environment: {application.preferred_work_environment}")

            # Section 11: Supervision
            application.supervisor_experience = request.POST.get('supervisor_experience', '')
            application.team_size_managed = request.POST.get('team_size_managed', '')
            application.management_style = request.POST.get('management_style', '')
            print(f"Section 11 - Supervisor: {application.supervisor_experience}")

            # Section 13: WhatsApp
            application.whatsapp_number = request.POST.get('whatsapp_number', '')
            application.interview_availability = request.POST.get('interview_availability', '')
            print(f"Section 13 - WhatsApp: {application.whatsapp_number}")

            # Save application first
            application.save()
            print(f"Application saved with reference: {application.reference_number}")

            # Section 3: Save Language Details
            selected_languages = request.POST.getlist('languages')
            for language in selected_languages:
                try:
                    global_level = request.POST.get(f'lang_global_{language}', '')
                    listening_level = request.POST.get(f'lang_listening_{language}', '')
                    speaking_level = request.POST.get(f'lang_speaking_{language}', '')
                    writing_level = request.POST.get(f'lang_writing_{language}', '')

                    if global_level and listening_level and speaking_level and writing_level:
                        LanguageDetail.objects.create(
                            application=application,
                            language=language,
                            global_level=global_level,
                            listening_level=listening_level,
                            speaking_level=speaking_level,
                            writing_level=writing_level
                        )
                        print(f"Language detail saved: {language} - {global_level}")
                except Exception as e:
                    print(f"Error saving language {language}: {str(e)}")

            print("=" * 50)

            messages.success(request, 'Votre candidature a été envoyée avec succès!')
            return redirect('confirmation', reference=application.reference_number)

        except Exception as e:
            import traceback
            print("=" * 50)
            print("ERROR OCCURRED:")
            print(traceback.format_exc())
            print("=" * 50)
            messages.error(request, f'Erreur lors de la soumission: {str(e)}')
            return render(request, 'resumemanager/multi_step_form.html')
    else:
        return render(request, 'resumemanager/multi_step_form.html')


def confirmation(request, reference):
    try:
        application = Application.objects.get(reference_number=reference)
        context = {
            'email': application.email,
            'reference': reference
        }
    except Application.DoesNotExist:
        context = {
            'email': 'N/A',
            'reference': reference
        }
    return render(request, 'resumemanager/confirmation.html', context)
