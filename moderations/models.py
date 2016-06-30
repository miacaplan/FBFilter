import hashlib

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class FBGroup(models.Model):
    fb_group_id = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    hate_words = models.TextField()

    @property
    def hate_words_list(self):
        return self.hate_words.split(';')

class Moderator(models.Model):
    models.OneToOneField(User, on_delete=models.CASCADE)
    fb_user_id = models.CharField(max_length=50)
    registered_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(FBGroup, related_name="moderators")

def calc_hash(message):
    return hashlib.sha256(message.encode()).hexdigest()

class Postment(models.Model):
    class Type:
        COMMENT = 1
        POST = 2

        types = ((COMMENT, 'comment'), (POST, 'post'))

    type = models.IntegerField(choices=Type.types)

    fb_id = models.CharField(max_length=50)
    fb_user_id = models.CharField(max_length=50)
    message = models.TextField()
    img = models.ImageField(null=True, blank=True)
    group = models.ForeignKey(FBGroup, related_name='postments')
    posted_at = models.DateTimeField()
    nesting_level = models.PositiveSmallIntegerField()
    hash_val = models.CharField(max_length=64)
    num_reactions = models.PositiveSmallIntegerField(default=0)
    parent = models.ForeignKey('self', default=None, related_name='comments', null=True, blank=True)

    class Status:
        PASSED_FILTER = 0
        PENDING = 1
        AWAITING_EDIT = 2
        DELETED = 3
        APPROVED = 4


        statuses = ((PENDING, 'pending'), (AWAITING_EDIT, 'awaiting_edit'), (DELETED, 'deleted'), (APPROVED, 'approved'))

    status = models.IntegerField(choices=Status.statuses, default=Status.PENDING)


    # def hash_message(self):
    #     return calc_hash(self.message)
    #
    # hash_val = property(hash_message)


    def save(self, *args, **kwargs):
        self.hash_val = calc_hash(self.message)
        super(Postment, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("mederations:detail", args=(self.pk,))

class Action(models.Model):
    class Type:
        FILTERED = 1
        VIEWED = 2
        REQUESTED_EDIT = 3
        APPROVED = 4
        REMOVED = 5
        BLOCKED = 6

        types = ((FILTERED, 'filtered'), (VIEWED, 'viewed'), (REQUESTED_EDIT, 'requested_edit'), (APPROVED, 'approved'),
                 (REMOVED, 'removed'), (BLOCKED, 'blocked'))
    type = models.IntegerField(choices=Type.types)
    performed_at = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(Moderator, related_name='actions', null=True)
    postment = models.ForeignKey(Postment, related_name='actions')

    @classmethod
    def add_action(cls, postment, action_type, user):
        cls.objects.create(
                type = action_type,
                performed_by = user,
                postment = postment
        )
