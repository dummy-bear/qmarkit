from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    h1 = models.CharField(max_length=200)
    thing = models.CharField(max_length=200)
    url = models.SlugField()
    description = models.TextField()
    content = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200)

    def __str__(self):
        return self.h1

class Organization(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
		
    def __str__(self):
        return self.name

class Company(models.Model):
	name = models.TextField()
	description = RichTextUploadingField(null=True, blank=True)
	prefix = models.CharField(max_length=20)
	members = models.ManyToManyField(User)
	
	def __str__(self):
		return self.name

class Room(models.Model):
	number = models.CharField(max_length=200)
	name = models.TextField()
	url = models.SlugField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	company = models.ForeignKey(Company, null=True, blank=True, default=None, on_delete=models.CASCADE)
	   
	def __str__(self):
		return self.number
            
class Thing(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    visible = models.CharField(max_length=2, default='ic')
    #доступность: u-только пользователю, c-только компании, i-только по id, a-всем
    #комменты: u-только владельцу, c-только компании, s-всем но премодерация, a-всем
    company = models.ForeignKey(Company, null=True, blank=True, default=None, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, null=True, blank=True, default=None, on_delete=models.CASCADE)
    url = models.SlugField()
    description = RichTextUploadingField(null=True, blank=True)
    image = models.ImageField(default="default.png")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200)

    def __str__(self):
        return self.number

class Comment(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    image = models.ImageField(default="", blank=True, upload_to='upload/')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.text
