"""
Dashboard statistics aggregation
"""
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import timedelta, datetime
from users.models import User
from webinars.models import Webinar, WebinarRegistration
from internships.models import Internship, InternshipRegistration
from memberships.models import Membership, MembershipRegistration
from feedback.models import Feedback


def get_dashboard_stats_simple():
    """
    Get basic dashboard statistics
    Returns counts of active internships, webinars, and memberships
    """
    normal_users = User.objects.filter(is_staff=False, is_superuser=False).count()
    internships = Internship.objects.filter(is_active=True).count()
    webinars = Webinar.objects.filter(is_active=True).count()
    memberships = Membership.objects.filter(is_active=True).count()
    
    return {
        'normal_users': normal_users,
        'internships': internships,
        'webinars': webinars,
        'memberships': memberships,
    }


def get_registration_status_stats():
    """Get registration status counts for internship, webinar, and membership"""
    return {
        'internship': {
            'approved': InternshipRegistration.objects.filter(status='accepted').count(),
            'rejected': InternshipRegistration.objects.filter(status='rejected').count(),
            'pending': InternshipRegistration.objects.filter(status='pending').count(),
        },
        'webinar': {
            'approved': WebinarRegistration.objects.filter(status='accepted').count(),
            'rejected': WebinarRegistration.objects.filter(status='rejected').count(),
            'pending': WebinarRegistration.objects.filter(status='pending').count(),
        },
        'membership': {
            'approved': MembershipRegistration.objects.filter(status='accepted').count(),
            'rejected': MembershipRegistration.objects.filter(status='rejected').count(),
            'pending': MembershipRegistration.objects.filter(status='pending').count(),
        },
    }


def get_past_registration_stats():
    """
    Get registration statistics for the past 10 days
    Groups by date and registration type (webinar, internship)
    """
    today = timezone.now()
    
    # Calculate date range (past 10 days including today)
    end_date = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    start_date = (today - timedelta(days=9)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get webinar registrations
    webinar_registrations = WebinarRegistration.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date
    ).values('created_at__date').annotate(count=Count('id'))
    
    # Get internship registrations
    internship_registrations = InternshipRegistration.objects.filter(
        applied_at__gte=start_date,
        applied_at__lte=end_date
    ).values('applied_at__date').annotate(count=Count('id'))
    
    # Create a dict for easy lookup
    webinar_dict = {item['created_at__date'].isoformat(): item['count'] for item in webinar_registrations}
    internship_dict = {item['applied_at__date'].isoformat(): item['count'] for item in internship_registrations}
    
    # Build result for past 10 days
    days = []
    for i in range(9, -1, -1):
        date = (today - timedelta(days=i)).date()
        date_str = date.isoformat()
        
        days.append({
            'date': date_str,
            'webinar': webinar_dict.get(date_str, 0),
            'internship': internship_dict.get(date_str, 0),
        })
    
    return days


def get_recent_registrations(limit=5):
    """
    Get recent registrations across webinars and internships
    Returns the most recent registrations with relevant details
    """
    recent = []
    
    # Get recent webinar registrations
    webinar_regs = WebinarRegistration.objects.select_related(
        'webinar', 'user'
    ).order_by('-created_at')[:limit]
    
    for reg in webinar_regs:
        recent.append({
            'id': str(reg.id),
            'full_name': reg.user.name,
            'email': reg.user.email,
            'phone_number': reg.user.phone_number,
            'reason': reg.reason,
            'type': 'webinar',
            'title': reg.webinar.title,
            'created_at': reg.created_at.isoformat(),
        })
    
    # Get recent internship registrations
    internship_regs = InternshipRegistration.objects.select_related(
        'internship', 'user'
    ).order_by('-applied_at')[:limit]
    
    for reg in internship_regs:
        recent.append({
            'id': str(reg.id),
            'full_name': reg.user.name,
            'email': reg.user.email,
            'phone_number': reg.user.phone_number,
            'reason': reg.reason,
            'type': 'internship',
            'title': reg.internship.title,
            'created_at': reg.applied_at.isoformat(),
        })
    
    # Sort by created_at descending and return top limit
    recent.sort(key=lambda x: x['created_at'], reverse=True)
    return recent[:limit]


def get_dashboard_stats():
    """Comprehensive dashboard statistics aggregation"""
    
    # User Stats
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    normal_users = User.objects.filter(is_staff=False, is_superuser=False).count()
    
    # Webinar Stats
    total_webinars = Webinar.objects.count()
    active_webinars = Webinar.objects.filter(is_active=True).count()
    total_webinar_registrations = WebinarRegistration.objects.count()
    
    webinar_registration_status = {
        'pending': WebinarRegistration.objects.filter(status='pending').count(),
        'accepted': WebinarRegistration.objects.filter(status='accepted').count(),
        'rejected': WebinarRegistration.objects.filter(status='rejected').count(),
    }
    
    webinar_attendance = WebinarRegistration.objects.filter(attended=True).count()
    
    # Internship Stats
    total_internships = Internship.objects.count()
    active_internships = Internship.objects.filter(is_active=True).count()
    total_internship_applications = InternshipRegistration.objects.count()
    
    internship_application_status = {
        'pending': InternshipRegistration.objects.filter(status='pending').count(),
        'accepted': InternshipRegistration.objects.filter(status='accepted').count(),
        'rejected': InternshipRegistration.objects.filter(status='rejected').count(),
    }
    
    # Membership Stats
    total_memberships = Membership.objects.count()
    active_memberships = Membership.objects.filter(is_active=True).count()
    total_membership_registrations = MembershipRegistration.objects.count()
    
    membership_registration_status = {
        'pending': MembershipRegistration.objects.filter(status='pending').count(),
        'accepted': MembershipRegistration.objects.filter(status='accepted').count(),
        'rejected': MembershipRegistration.objects.filter(status='rejected').count(),
    }
    
    membership_payment_status = {
        'pending': MembershipRegistration.objects.filter(payment_status='pending').count(),
        'completed': MembershipRegistration.objects.filter(payment_status='completed').count(),
        'failed': MembershipRegistration.objects.filter(payment_status='failed').count(),
        'refunded': MembershipRegistration.objects.filter(payment_status='refunded').count(),
    }
    
    # Payment Revenue
    total_revenue = MembershipRegistration.objects.filter(
        payment_status='completed'
    ).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    # Feedback Stats
    total_feedback = Feedback.objects.count()
    average_rating = Feedback.objects.aggregate(avg=Avg('rating'))['avg']
    
    feedback_by_type = dict(
        Feedback.objects.values('feedback_type').annotate(count=Count('id'))
        .values_list('feedback_type', 'count')
    )
    
    # Recent Activity (Last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    
    recent_webinar_registrations = WebinarRegistration.objects.filter(
        created_at__gte=seven_days_ago
    ).count()
    
    recent_internship_applications = InternshipRegistration.objects.filter(
        applied_at__gte=seven_days_ago
    ).count()
    
    recent_membership_registrations = MembershipRegistration.objects.filter(
        created_at__gte=seven_days_ago
    ).count()
    
    recent_new_users = User.objects.filter(created_at__gte=seven_days_ago).count()
    
    return {
        'users': {
            'total': total_users,
            'active': active_users,
            'staff': staff_users,
            'normal': normal_users,
            'inactive': total_users - active_users,
            'recent_signups_7days': recent_new_users,
        },
        'webinars': {
            'total': total_webinars,
            'active': active_webinars,
            'total_registrations': total_webinar_registrations,
            'registration_status': webinar_registration_status,
            'attendance': webinar_attendance,
            'attendance_rate': round(
                (webinar_attendance / total_webinar_registrations * 100) if total_webinar_registrations > 0 else 0,
                2
            ),
            'recent_registrations_7days': recent_webinar_registrations,
        },
        'internships': {
            'total': total_internships,
            'active': active_internships,
            'total_applications': total_internship_applications,
            'application_status': internship_application_status,
            'recent_applications_7days': recent_internship_applications,
        },
        'memberships': {
            'total': total_memberships,
            'active': active_memberships,
            'total_registrations': total_membership_registrations,
            'registration_status': membership_registration_status,
            'payment_status': membership_payment_status,
            'total_revenue': float(total_revenue),
            'recent_registrations_7days': recent_membership_registrations,
        },
        'feedback': {
            'total': total_feedback,
            'average_rating': round(average_rating, 2) if average_rating else 0,
            'by_type': feedback_by_type,
        },
        'summary': {
            'total_users': total_users,
            'total_registrations': total_webinar_registrations + total_internship_applications + total_membership_registrations,
            'total_revenue': float(total_revenue),
            'pending_approvals': (
                webinar_registration_status['pending'] +
                internship_application_status['pending'] +
                membership_registration_status['pending']
            ),
        }
    }
