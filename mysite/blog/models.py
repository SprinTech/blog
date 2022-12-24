from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self) :
        return super(PublishedManager, self).get_queryset().filter(status="published")
    
class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published")
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique_for_date="publish") # post that contains publish date and slug
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    body = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default="draft")
    
    objects = models.Manager()
    published = PublishedManager() # allow to retrieve all post with status published
    tags = TaggableManager()
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])
    class Meta:
        ordering = ("-publish",) # sort results according to publish field in descending order
            
    def __str__(self) -> str:
        return self.title
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)
        
    def __str__(self) -> str:
        return f"Comment by {self.name} on {self.post}"