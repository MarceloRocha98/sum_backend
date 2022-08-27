from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table='user' 

class Blotter(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
     ticker = models.CharField(max_length = 200, blank = False, default = None)
     volume = models.FloatField(default= 0)
     price = models.FloatField(default= 0)
    

     def __str__(self):
         return str(self.id)

     class Meta:
        db_table='blotter' 