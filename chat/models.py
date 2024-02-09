import uuid
from django.db import models

from account.models import User


class Message(models.Model):
    body = models.TextField()
    sent_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('created_at',)
    
    def __str__(self):
        return f'{self.sent_by}'


class Room(models.Model):
    WAITING = 'waiting'
    ACTIVE = 'active'
    CLOSED = 'closed'

    CHOICES_STATUS = (
        (WAITING, 'Waiting'),
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    )

    uuid = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    agent = models.ForeignKey(User, related_name='rooms', blank=True, null=True, on_delete=models.SET_NULL)
    messages = models.ManyToManyField(Message, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return f'{self.client} - {self.uuid}'

class ChatSession(models.Model):
    WAITING = 'waiting'
    ACTIVE = 'active'
    CLOSED = 'closed'

    CHOICES_STATUS = (
        (WAITING, 'Waiting'),
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    )

    uuid = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    user_id = models.CharField(max_length=100)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    last_interaction = models.DateTimeField(null=True)
    started_by = models.CharField(max_length=100, null=True)
    summary = models.JSONField(null=True, blank=True)
    friendly_summary = models.TextField(null=True)
    channel = models.CharField(max_length=40, null=True)
    active = models.BooleanField(default=True)
    busy = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=WAITING)
    experience = models.CharField(max_length=40, null=True)

    class Meta:
        db_table = 'chat_session'

    def __str__(self):
        return str(self.pk)


class ChatMessage(models.Model):

    role = models.CharField(max_length=45, null=True)
    content = models.TextField(null=False, default="")
    created = models.DateTimeField(auto_now_add=True)
    intent = models.TextField(null=True)
    subject_of_interest = models.CharField(max_length=200, null=True)
    session = models.ForeignKey(ChatSession, related_name="phone", blank=True, null=True, on_delete=models.SET_NULL)
    stitches = models.IntegerField(default=0)
    skipped = models.IntegerField(default=0)

    class Meta:
        db_table = 'message'