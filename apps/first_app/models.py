from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class Job(models.Model):
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    location = models.CharField(max_length = 45)
    user = models.ForeignKey(User,related_name="jobs")
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

