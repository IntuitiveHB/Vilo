from rest_framework import serializers

from chat.models import Conversation, Message

from authentication.serializers import ChatUserSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('conversation',)


class ConversationListSerializer(serializers.ModelSerializer):
    initiator = ChatUserSerializer()
    receiver = ChatUserSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['initiator', 'receiver', 'last_message']

    def get_last_message(self, instance):
        message = instance.message_set.first()
        return MessageSerializer(instance=message).data


class ConversationSerializer(serializers.ModelSerializer):
    initiator = ChatUserSerializer()
    receiver = ChatUserSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['initiator', 'receiver', 'message_set']
