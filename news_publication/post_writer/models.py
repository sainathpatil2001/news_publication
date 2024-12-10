from django.db import models
from first_app.models import Writer  # Import the Writer model from first_app

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='article_images/', null=True, blank=True)
    unique_number = models.CharField(max_length=50, unique=True)
    date = models.DateField(auto_now_add=True)
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title


class AdminQuery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='queries')
    query_content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Query for Article: {self.article.title} - Status: {self.status}"
