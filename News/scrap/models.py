from django.db import models


class Post(models.Model):
    post_title = models.CharField(unique=True, max_length = 100)
    post_subtitle = models.CharField(max_length = 100)
    post_content = models.CharField(max_length = 2000)
    post_date = models.DateField()
    post_link = models.CharField(max_length = 300)

    def __str__(self):
        return self.post_title
