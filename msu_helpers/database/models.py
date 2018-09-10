#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=64, default='Funny')
    last_name = models.CharField(max_length=64, default='Bunny')
    study_group = models.CharField(max_length=10, default='BNBO-01-15')
    birthday = models.DateField(auto_now_add=True)
    about = models.TextField(max_length=1000, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='media/users/profile_pics', null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    lang = models.CharField(max_length=5, default='ru-ru')
    activated = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = '_User'

    def __str__(self):
        return f'{self.email} - {self.first_name} {self.last_name}'

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserAdmin(admin.ModelAdmin):
    exclude = ('password', 'last_login', 'user_permissions', 'groups')


class Post(models.Model):
    body = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        db_table = '_Post'

    def __str__(self):
        return f'{self.user.email} - {self.timestamp}'


class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name = _('Reaction')
        verbose_name_plural = _('Reactions')
        unique_together = ('post', 'user')
        db_table = '_Reaction'

    def __str__(self):
        return f'{self.user.email} liked {str(self.post)} post'


class AttachmentType(models.Model):
    VIDEO = 'VID'
    AUDIO = 'AUD'
    IMAGE = 'IMG'
    LINK = 'LNK'
    DOC = 'DOC'
    TYPE_CHOICES = (
        (VIDEO, 'Video'),
        (AUDIO, 'Audio'),
        (IMAGE, 'Image'),
        (LINK, 'Link'),
        (DOC, 'Document')
    )
    tag = models.CharField(max_length=3, choices=TYPE_CHOICES, default=DOC, unique=True)

    class Meta:
        verbose_name = _('Attachment Type')
        verbose_name_plural = _('Attachment Types')
        db_table = '_AttachmentType'

    def __str__(self):
        return f'{self.get_tag_display()}'


class Attachment(models.Model):
    attachment_type = models.ForeignKey(AttachmentType, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to=f'media/attachments/{attachment_type}/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')
        db_table = '_Attachment'

    def __str__(self):
        return f'{self.file.name}'


class Comment(models.Model):
    body = models.TextField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        db_table = '_Comment'

    def __str__(self):
        return f"{self.user.email} commented under {self.post.user.email}'s post at {self.timestamp}"


class Mention(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    had_seen = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = _('Mention')
        verbose_name_plural = _('Mentions')
        unique_together = ('comment', 'user')
        db_table = '_Mention'

    def __str__(self):
        return f'{self.comment.user.email} mentioned {self.user.email} in his comment ({self.had_seen})'


class Chat(models.Model):

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')
        db_table = '_Chat'

    def __str__(self):
        return f'{self.pk}'


class ChatMember(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = _('Chat Member')
        verbose_name_plural = _('Chat Members')
        unique_together = ('chat', 'user')
        db_table = '_ChatMember'

    def __str__(self):
        return f'Chat: {self.chat.pk}; User: {self.user.email}'


class Message(models.Model):
    body = models.TextField(max_length=150)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        db_table = '_Message'

    def __str__(self):
        return f'Chat: {self.chat.pk}; Sender: {self.sender.pk}'


class UserMessage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('User Message')
        verbose_name_plural = _('User Messages')
        unique_together = ('message', 'user')
        db_table = '_UserMessage'

    def __str__(self):
        return f'User: {self.user.pk}; Message: {self.message.pk}'
