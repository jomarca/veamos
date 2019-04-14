from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


class Product(models.Model):
  title = models.CharField(max_length=255)
  pub_date = models.DateTimeField()
  body = models.TextField(max_length=255)
  url = models.TextField()
  image = models.ImageField(upload_to='images/')
  icon = models.ImageField(upload_to='images/')
  votes_total = models.IntegerField(default=1)
  max_supply = models.IntegerField()
  circulating_supply = models.IntegerField()
  hunter = models.ForeignKey(User, on_delete = models.CASCADE)
  

  def __str__(self):
    return self.title
  
  def summary(self):
    return self.body[:250]

  def pub_date_pretty(self):
    return self.pub_date.strftime('%b %e %Y')

#to ensure users are able to vote only once, we create a model called Vote to have a product ID and userID and check to see if user has a vote casted for the prodcut ID already then it should not be able to vote:
class Vote(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    unique_together = ('product','user')

# class Comment(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='comments')
#     name = models.CharField(max_length=80)
#     email = models.EmailField()
#     body = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    

#     class Meta:
#         ordering = ('created',)

#     def __str__(self):
#         return 'Comment by {} on {}'.format(self.name, self.post)
