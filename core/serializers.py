from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    
    users = serializers.DictField()
    webinars = serializers.DictField()
    internships = serializers.DictField()
    memberships = serializers.DictField()
    feedback = serializers.DictField()
    summary = serializers.DictField()
