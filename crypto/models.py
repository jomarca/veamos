from django.db import models

# Create your models here.
class News1(models.Model):
  title = models.CharField(max_length=255)

  #pub_date1 = models.DateTimeField()
  body = models.TextField(unique=True)
  url = models.TextField()
  image = models.ImageField(upload_to='images/')
  created_at = models.DateTimeField(auto_now_add=True)
  

  def __str__(self):
    return self.title
  
  def summary(self):
    return self.body[:250]

  # def pub_date_pretty(self):
  #   return self.pub_date.strftime('%b %e %Y')

  def pub_date_pretty(self):
    return self.pub_date.strftime('%b %e %Y')


class Price(models.Model):
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
 
class Arbscrypto(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  pair = models.CharField(max_length=20)
  exchangebuy = models.CharField(max_length=50)
  exchangesell = models.CharField(max_length=50)
  percentage = models.FloatField()
  buyprice = models.FloatField()
  sellingprice = models.FloatField()
  gain = models.FloatField()
  volumesizebuy= models.FloatField(default=233)
  volumesizesell= models.FloatField(default=233)
  

  class Meta:
    #to avoid saving same arb twice in database
    unique_together = ('percentage', 'buyprice',)

  