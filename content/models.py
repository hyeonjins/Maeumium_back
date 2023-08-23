from django.db import models


# Create your models here.
class DiaryContent(models.Model):
    content = models.TextField()
    image = models.TextField()
    user_id = models.TextField()
