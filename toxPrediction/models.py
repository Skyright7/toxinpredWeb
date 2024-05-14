from django.db import models

# Create your models here.
class taskResultList(models.Model):
    taskId = models.IntegerField(primary_key=True)
    # 输出地址
    outputPath = models.TextField()
    # 输出预览地址
    outputPreviewPath = models.TextField()

    def __str__(self):
        return self.taskId

    class Meta:
        ordering = ['-taskId']