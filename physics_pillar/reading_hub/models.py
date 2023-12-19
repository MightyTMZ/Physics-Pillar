from django.db import models
from users.models import CustomUser
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_picture_url = models.CharField(max_length=2083, editable=False)
    
    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


"""class Engineer(models.Model):
    pass"""
    


lorem_ipsum_40_words = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""


class Article(models.Model):
    @property
    def created_at_date(self):
        return self.created_at.date()

    '''@property
    def last_updated_date(self):
        return self.updated_at.date()'''
    
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(default="-", editable=False, max_length=250)
    image_url = models.CharField(max_length=2083, default="-")
    content = models.TextField(max_length=10000)
    content_just_text = models.TextField(max_length=10000, default=lorem_ipsum_40_words)
    """On the home page, landing page, search results page, the article is rendered with the first 30-40 words
    as part of the thumbnail. Since the "content" field of the article model class stores the markup, it cannot be used as
    the thumbnail text, therefore, we created a field to store PURELY the content and not the markup for specific purposes in
    the future.
    """
    category = models.ManyToManyField(Category)
    authors = models.ManyToManyField(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trending = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title} - by {self.authors} - Trending {self.trending} - {self.created_at}"

    def save(self, *args, **kwargs):
        # Update the slug using the title when the article is saved
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_article_url(self):
        # Construct the URL using created_at and slugified title
        return f'/{self.created_at.date()}/{self.slug}/'



# url structure:
# engineeringcornerstone.com/median_form(e.g. article, blog, etc)/created_at_date/slug
# example url:
# https://www.engineeringcornerstone.com/article/2023-12-03/django-is-a-python-backend-framework