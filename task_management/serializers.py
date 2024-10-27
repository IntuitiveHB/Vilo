from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib import auth

from task_management.models import (
    ClientCase, TaskBoard, BoardLanes, TaskCards
)


class CaseSerializer(serializers.ModelSerializer):

    '''case_identifier = serializers.CharField(max_length=255, min_length=6)
    client = serializers.CharField(max_length=255, min_length=6)
    case_type = serializers.CharField(max_length=255, min_length=6)
    case_title = serializers.CharField(max_length=255, min_length=6)
    notes = serializers.CharField(max_length=255, min_length=6)
    service_year = serializers.CharField(max_length=255, min_length=6)

    created_at = serializers.CharField(max_length=255, min_length=6)
    updated_at = serializers.CharField(max_length=255, min_length=6)
    created_by = serializers.CharField(max_length=255, min_length=6)
    updated_by = serializers.CharField(max_length=255, min_length=6)'''

    class Meta:
        model = ClientCase
        fields = ['id', 'client', 'case_type',
                  'case_title', 'notes']


class BoradSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskBoard
        fields = ['id', 'title', 'description', 'board_type',
                  'client', 'client_case', 'collaborators']


class BoradLaneSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoardLanes
        fields = ['id', 'title', 'lane_order', 'task_board',
                  'maximum_cards_in_lane']


class TaskCardSerializer(serializers.ModelSerializer):
    archived = serializers.BooleanField(source="is_archived")

    class Meta:
        model = TaskCards
        fields = ['id', 'title', 'description', 'priority', 'due_date',
                  'assignee', 'board_lane', 'order_in_lane', 'archived']
