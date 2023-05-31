import uuid

from django.db import models

# Create your models here.
class Speaker(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    LANGUAGE_CHOICES = [
        ('ZH', 'Chinese'),
        ('EN', 'English'),
        # Add more languages as needed
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='speakers/')
    image_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
class VirtualPerson(models.Model):
    POS_CHOICES = [
        ('half', '半身'),
        ('sitting', '坐姿'),
        ('full_sitting', '大半身'),
        ('full_body', '全身')
        # Add more languages as needed
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    pose = models.CharField(max_length=255,choices=POS_CHOICES)
    default_pos = models.CharField(max_length=255)
    image = models.ImageField(upload_to='virtualperson/Images/')
    image_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    video = models.FileField(upload_to='virtualperson/Videos/')
    video_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
class BackGround(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='backgrand/')
    image_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
class FrontGround(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='frontground/')
    image_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
