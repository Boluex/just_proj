from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Chatroom where two users can have a conversation
class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_chats')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Chat {self.id}"


# To store user messages
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} in {self.chat} at {self.timestamp}"