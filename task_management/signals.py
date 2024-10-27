from django.db.models.signals import post_save
from django.dispatch import receiver

from task_management.models import BoardLanes


@receiver(post_save, sender='task_management.TaskBoard')
def after_board_created(sender, instance, created, **kwargs):

    if created:
        lanes_detail = [{
            "title": "Pending",
            "lane_order": 1,
            "task_board": instance
        }, {
            "title": "In Progress",
            "lane_order": 2,
            "task_board": instance
        }, {
            "title": "In Review",
            "lane_order": 3,
            "task_board": instance
        }, {
            "title": "Completed",
            "lane_order": 4,
            "task_board": instance
        }]

        lanes_list = [BoardLanes(**lanes) for lanes in lanes_detail]

        BoardLanes.objects.bulk_create(lanes_list)
    else:
        pass
