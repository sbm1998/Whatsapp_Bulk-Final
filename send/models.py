from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Whatsapp_Numbers(models.Model):
    number = PhoneNumberField(null=False,blank=False)
    user = models.CharField(max_length=32)

    def __str__(self):
        return str(self.number) 

class Read_csv(models.Model):
    File = models.FileField(upload_to="Csv_file")

    def __str__(self):
        return str(self.File)

class Attachment(models.Model):
    File = models.FileField(upload_to="Attachments")

    def __str__(self):
        return str(self.File)