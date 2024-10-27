from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from chat.serializers import (
    ConversationListSerializer, ConversationSerializer
)
from chat.models import Conversation

from django.shortcuts import render, redirect, reverse
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
    }
))
@api_view(['POST'])
def start_convo(request, ):
    serializer_class = ConversationSerializer

    data = request.data
    email = data.pop('email')

    try:
        participant = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'message': 'You cannot chat with a non existent user'})

    conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                               Q(initiator=participant, receiver=request.user))

    if conversation.exists():
        return redirect(reverse('get_conversation', args=(conversation[0].id,)))
    else:
        conversation = Conversation.objects.create(
            initiator=request.user, receiver=participant)
        return Response(ConversationSerializer(instance=conversation).data)


@api_view(['GET'])
def get_conversation(request, convo_id):
    conversation = Conversation.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Conversation does not exist'})
    else:
        serializer = ConversationSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(['GET'])
def conversations(request):
    conversation_list = Conversation.objects.filter(Q(initiator=request.user) |
                                                    Q(receiver=request.user))
    serializer = ConversationListSerializer(
        instance=conversation_list, many=True)
    return Response(serializer.data)
