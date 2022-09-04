from django.db import models

# Create your models here.
class User(models.Model):
    uid=models.IntegerField(unique=True,null=False)
    name=models.CharField(max_length=30)
    code=models.CharField(max_length=8)
    email=models.EmailField()

    def __str__(self):
        return self.name


class History(models.Model):
    uid=models.IntegerField(editable=False)
    transaction_id=models.UUIDField(editable=False)
    activity=models.DateTimeField(auto_now_add=True,editable=False)
    status=models.BooleanField(default=False,editable=False)
    
    def __str__(self):
        #get will return the object of the model
        #filter will return the queryset of the model

        name=User.objects.get(uid=self.uid).name  
        return name