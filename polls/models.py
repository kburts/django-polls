from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now())
    user = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <  now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class MakePoll(models.Model):
    def __unicode__(self):
        return self.question
    question = models.CharField(max_length=200)
    option0 = models.CharField(max_length=200)
    option1 = models.CharField(max_length=200)

    author = models.CharField(max_length=80)
    pub_date = models.DateTimeField('date published')


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username