from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from task_management.serializers import (
    CaseSerializer, BoradSerializer, BoradLaneSerializer, TaskCardSerializer
)
from task_management.models import (
    ClientCase, TaskBoard, BoardLanes, TaskCards
)
from task_management.permissions import IsOwner

# Create your views here.


class CaseListAPIView(ListCreateAPIView):
    serializer_class = CaseSerializer
    queryset = ClientCase.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        # generate_case_identifier()
        GET_FROM_TEMPALTE = 'GET Unique Case Identifier'
        return serializer.save(case_identifier='GET_FROM_TEMPALTE')

    def get_queryset(self):
        return self.queryset.filter(created_by_id=self.request.user)


class CaseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CaseSerializer
    queryset = ClientCase.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(created_by_id=self.request.user)


class BoardListAPIView(ListCreateAPIView):
    serializer_class = BoradSerializer
    queryset = TaskBoard.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.filter(created_by_id=self.request.user)


class BoardDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BoradSerializer
    queryset = TaskBoard.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(created_by_id=self.request.user)


class BoardLaneListAPIView(ListCreateAPIView):
    serializer_class = BoradLaneSerializer
    queryset = BoardLanes.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    lookup_board_kwarg = "task_board"

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        task_board_id = self.kwargs.get(self.lookup_board_kwarg)
        return self.queryset.filter(task_board_id=task_board_id)


class BoardLaneDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BoradLaneSerializer
    queryset = BoardLanes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"
    lookup_board_kwarg = "task_board"

    def get_queryset(self):
        task_board_id = self.kwargs.get(self.lookup_board_kwarg)
        return self.queryset.filter(task_board_id=task_board_id)


class TaskCardListAPIView(ListCreateAPIView):
    serializer_class = TaskCardSerializer
    queryset = TaskCards.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    lookup_lane_kwarg = "board_lane"

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        board_lane_id = self.kwargs.get(self.lookup_lane_kwarg)
        return self.queryset.filter(board_lane_id=board_lane_id)


class TaskCardDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskCardSerializer
    queryset = TaskCards.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"
    lookup_lane_kwarg = "board_lane"

    def get_queryset(self):
        board_lane_id = self.kwargs.get(self.lookup_lane_kwarg)
        return self.queryset.filter(board_lane_id=board_lane_id)
