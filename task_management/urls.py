from django.urls import path
from . import views

urlpatterns = [
    path('cases', views.CaseListAPIView.as_view(), name="cases"),
    path('case/<int:id>', views.CaseDetailAPIView.as_view(), name="case"),
    path('boards', views.BoardListAPIView.as_view(), name="boards"),
    path('board/<int:id>', views.BoardDetailAPIView.as_view(), name="board"),
    path('lanes/<int:task_board>',
         views.BoardLaneListAPIView.as_view(), name="lanes"),
    path('lane/<int:task_board>/<int:id>',
         views.BoardLaneDetailAPIView.as_view(), name="lane"),
    path('cards/<int:board_lane>',
         views.TaskCardListAPIView.as_view(), name="cards"),
    path('card/<int:board_lane>/<int:id>',
         views.TaskCardDetailAPIView.as_view(), name="card"),
]
