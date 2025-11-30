from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from resumemanager.models import Application
from .models import Comment, ContactLog, StatusHistory


def recruiter_login(request):
    """Custom login page for recruiters"""
    if request.user.is_authenticated:
        return redirect('recruiter_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('recruiter_dashboard')
        else:
            messages.error(request, 'Identifiants incorrects')

    return render(request, 'recruiter/login.html')


def recruiter_logout(request):
    """Logout view"""
    logout(request)
    return redirect('recruiter_login')


@login_required(login_url='recruiter_login')
def dashboard(request):
    """Main dashboard with statistics"""
    # Get statistics
    now = timezone.now()
    last_24h = now - timedelta(hours=24)

    stats = {
        'new_24h': Application.objects.filter(created_at__gte=last_24h).count(),
        'to_contact': Application.objects.filter(status='to_contact').count(),
        'interviews': Application.objects.filter(status='interview').count(),
        'hired': Application.objects.filter(status='hired').count(),
        'total': Application.objects.count(),
    }

    # Recent applications
    recent_applications = Application.objects.all()[:10]

    context = {
        'stats': stats,
        'recent_applications': recent_applications,
    }

    return render(request, 'recruiter/dashboard.html', context)


@login_required(login_url='recruiter_login')
def candidate_list(request):
    """List of all candidates with filters"""
    applications = Application.objects.all()

    # Filters
    status_filter = request.GET.get('status')
    position_filter = request.GET.get('position')
    language_filter = request.GET.get('language')
    country_filter = request.GET.get('country')
    min_score = request.GET.get('min_score')
    has_voice = request.GET.get('has_voice')
    has_experience = request.GET.get('has_experience')
    search_query = request.GET.get('search')

    if status_filter:
        applications = applications.filter(status=status_filter)

    if position_filter:
        applications = applications.filter(target_positions__contains=position_filter)

    if language_filter:
        applications = applications.filter(languages__contains=language_filter)

    if country_filter:
        applications = applications.filter(country__icontains=country_filter)

    if min_score:
        applications = applications.filter(recruiter_score__gte=int(min_score))

    if has_voice == 'yes':
        applications = applications.exclude(audio_recording='')

    if has_experience == 'yes':
        applications = applications.filter(has_call_center_experience='yes')

    if search_query:
        applications = applications.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(reference_number__icontains=search_query)
        )

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    applications = applications.order_by(sort_by)

    # Get unique values for filters
    all_applications = Application.objects.all()
    all_positions = set()
    all_languages = set()
    all_countries = set(all_applications.values_list('country', flat=True))

    for app in all_applications:
        if app.target_positions:
            all_positions.update(app.target_positions)
        if app.languages:
            all_languages.update(app.languages)

    context = {
        'applications': applications,
        'all_positions': sorted(all_positions),
        'all_languages': sorted(all_languages),
        'all_countries': sorted(all_countries),
        'status_choices': Application.STATUS_CHOICES,
        'current_filters': request.GET,
    }

    return render(request, 'recruiter/candidate_list.html', context)


@login_required(login_url='recruiter_login')
def candidate_detail(request, pk):
    """Detailed view of a single candidate"""
    application = get_object_or_404(Application, pk=pk)

    # Handle POST requests for comments, status changes, and contact logging
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_comment':
            content = request.POST.get('content')
            if content:
                Comment.objects.create(
                    application=application,
                    author=request.user,
                    content=content
                )
                messages.success(request, 'Commentaire ajouté')

        elif action == 'change_status':
            new_status = request.POST.get('status')
            notes = request.POST.get('notes', '')
            if new_status and new_status != application.status:
                StatusHistory.objects.create(
                    application=application,
                    changed_by=request.user,
                    old_status=application.status,
                    new_status=new_status,
                    notes=notes
                )
                application.status = new_status
                application.save()
                messages.success(request, 'Statut mis à jour')

        elif action == 'update_score':
            score = request.POST.get('score')
            if score:
                application.recruiter_score = int(score)
                application.save()
                messages.success(request, 'Score mis à jour')

        elif action == 'log_contact':
            contact_type = request.POST.get('contact_type')
            message_sent = request.POST.get('message_sent', '')
            notes = request.POST.get('contact_notes', '')

            ContactLog.objects.create(
                application=application,
                recruiter=request.user,
                contact_type=contact_type,
                message_sent=message_sent,
                notes=notes
            )
            application.last_contacted = timezone.now()
            application.save()
            messages.success(request, 'Contact enregistré')

        return redirect('candidate_detail', pk=pk)

    # Get related data
    comments = application.comments.all()
    status_history = application.status_history.all()
    contact_logs = application.contact_logs.all()

    context = {
        'application': application,
        'comments': comments,
        'status_history': status_history,
        'contact_logs': contact_logs,
        'status_choices': Application.STATUS_CHOICES,
    }

    return render(request, 'recruiter/candidate_detail.html', context)
