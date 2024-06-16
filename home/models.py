from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime  # добавляем импорт для работы с датой и временем

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=500)
    content = models.TextField()
    published_date = models.DateTimeField(default=datetime.now)  # добавляем поле published_date

    def __str__(self) -> str:
        return self.title
