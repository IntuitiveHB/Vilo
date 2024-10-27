from django.db import models
from django.contrib.auth import get_user_model

import datetime

from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField

from task_management.enums import BoardTypes, TaskPriorities

from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

# Create your models here.

""" 
    =======
    Each task board is associated with a case of the client.
    A client can have multiple cases registered and each case can have multiple task boards.
    We first create the case for a client, then for that specific case we create task boards,
    and each task boards contains the list of tasks, their related users: VILO team and client team
    ======
"""

User = get_user_model()


def setyear():
    """
    Setting default year current year
    """
    today = datetime.date.today()
    today = today.timetuple()
    defaultyear = today[0]
    defaultyear = str(defaultyear)
    return defaultyear


"""
    Case model class
"""


class ClientCase(models.Model):
    """ 
    TODO
    create choice enum for the case types 
    get_case_type_options_from_global_settings()
    """

    case_identifier = models.CharField(
        max_length=50, null=False, blank=False)
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='client')
    case_type = models.CharField(max_length=20, null=False, blank=False)
    case_title = models.CharField(max_length=255, null=False, blank=False)
    notes = models.TextField(null=True, blank=True)
    service_year = models.CharField(max_length=6, default=setyear)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField(related_name='owner')
    updated_by = CurrentUserField(
        on_update=True, related_name="last_updated_by")

    def __str__(self):
        return self.client_identifier


class TaskBoard(models.Model):
    board_type = models.CharField(_('Board Type'), max_length=50, choices=BoardTypes.choices(),
                                  # Default is general use
                                  default=BoardTypes.GENERAL_USE.value)
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='board_client', blank=True, null=True)
    client_case = models.ForeignKey(
        ClientCase, on_delete=models.CASCADE, related_name='client_case', blank=True, null=True)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    collaborators = ArrayField(models.CharField())

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField(related_name='board_owner')
    updated_by = CurrentUserField(
        on_update=True, related_name="board_last_updated_by")

    def __str__(self):
        return self.title


class BoardLanes(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    lane_order = models.SmallIntegerField(null=False, blank=False)
    maximum_cards_in_lane = models.SmallIntegerField(
        null=False, blank=False, default=0)
    task_board = models.ForeignKey(
        TaskBoard, on_delete=models.CASCADE, related_name='task_board', blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = CurrentUserField(related_name='lane_created_by')

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = CurrentUserField(
        on_update=True, related_name="lane_last_updated_by")

    def __str__(self):
        return self.title


class TaskCards(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(_('Priority'), max_length=50,
                                choices=TaskPriorities.choices(), null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assignee', blank=True, null=True)
    board_lane = models.ForeignKey(
        BoardLanes, on_delete=models.CASCADE, related_name='task_lane', blank=False, null=False)
    order_in_lane = models.SmallIntegerField(null=True, blank=True)
    is_archived = models.BooleanField(null=True, blank=True, default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = CurrentUserField(related_name='task_created_by')

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = CurrentUserField(
        on_update=True, related_name="task_last_updated_by")

    def __str__(self):
        return self.title
