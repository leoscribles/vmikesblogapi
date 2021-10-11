from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.text import slugify
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children", on_delete=CASCADE)

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = 'categories'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent 
        return ' -> '.join(full_path[::-1])

class Post(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    slug = models.SlugField(null=True)
    featured_image = models.ImageField(upload_to = 'images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('Post', null=True, blank=True, on_delete=CASCADE)  #field
    name = models.CharField(max_length=100)                                     #field
    body = models.TextField()                                                   #fields
    created_at = models.DateTimeField(auto_now_add=True)                        #field
    email = models.EmailField(max_length=200)                                   #field

    #these things are just fields
    


    def __str__(self):
        return self.body    #the returns the body for the database. Not what the user will see on the website.
                            #the views that will be displayed on the browser can be found in views-->template.



