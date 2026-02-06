from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.stats import (
    get_dashboard_stats,
    get_dashboard_stats_simple,
    get_registration_status_stats,
    get_past_registration_stats,
    get_recent_registrations
)
from core.serializers import DashboardStatsSerializer


class StatsViewSet(ViewSet):
    """
    ViewSet for dashboard statistics endpoints
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Get basic dashboard statistics with active counts
        Returns: internships, webinars, memberships counts
        """
        stats = get_dashboard_stats_simple()
        return Response(stats)

    @action(detail=False, methods=['get'])
    def past_registrations(self, request):
        """
        Get registration statistics for past 10 days
        Groups by date and registration type
        Returns: list of days with webinar and internship counts
        """
        stats = get_past_registration_stats()
        return Response(stats)

    @action(detail=False, methods=['get'])
    def recent_registrations(self, request):
        """
        Get recent registrations across webinars and internships
        Query params: limit (default: 5)
        """
        limit = int(request.query_params.get('limit', 5))
        registrations = get_recent_registrations(limit=limit)
        return Response(registrations)

    @action(detail=False, methods=['get'])
    def registration_status(self, request):
        """Get registration status counts for internship, webinar, and membership"""
        stats = get_registration_status_stats()
        return Response(stats)

    @action(detail=False, methods=['get'])
    def comprehensive(self, request):
        """
        Get comprehensive dashboard statistics
        Includes detailed breakdowns of all modules
        """
        stats = get_dashboard_stats()
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)
