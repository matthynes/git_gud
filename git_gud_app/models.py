from django.contrib.auth.models import User
from django.db import models
from vote.managers import VotableManager


class Post(models.Model):
    submitter = models.ForeignKey(User)
    date_submitted = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    text = models.TextField(max_length=200)

    votes = VotableManager()

    def __str__(self):
        return '{}: {}'.format(self.submitter, self.date_submitted)
