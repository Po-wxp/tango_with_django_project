from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class Category(models.Model):
      views = models.IntegerField(default=0)
      likes = models.IntegerField(default=0)
      NAME_MAX_LENGTH=128
      name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
      slug = models.SlugField(unique = True)
      
      def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)

      class Meta:
             verbose_name_plural = 'Categories'

      def __str__(self):
             return self.name

class Page(models.Model):
       category = models.ForeignKey(Category, on_delete=models.CASCADE)
       TITLE_MAX_LENGTH=128
       URL_MAX_LENGTH=200
       title = models.CharField(max_length=TITLE_MAX_LENGTH)
       url = models.URLField(max_length=URL_MAX_LENGTH)
       views = models.IntegerField(default=0)

       def __str__(self):
             return self.title


      
