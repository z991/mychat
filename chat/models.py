from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class MessageContent(models.Model):

    message = models.TextField(verbose_name="消息内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = verbose_name = "消息内容"