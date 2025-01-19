from datetime import timedelta
from django.db import models
from django.utils import timezone

class VotingStatus(models.Model):
    can_vote = models.BooleanField(default=False)

    def __str__(self):
        return f"Voting Status: {'Allowed' if self.can_vote else 'Not Allowed'}"
