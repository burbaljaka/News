from django.db import models


class Post(models.Model):
    post_title = models.CharField(unique=True)
    post_subtitle = models.CharField()
    post_content = models.CharField()
    post_date = models.DateField()

    def __str__(self):
        return self.post_title
