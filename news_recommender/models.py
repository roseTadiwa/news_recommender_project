from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    pubDate = models.DateTimeField()
    guid = models.URLField(unique=True)
    link = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.title