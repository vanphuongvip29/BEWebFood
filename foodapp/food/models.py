from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to="uploads/%Y/%m")


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name


class IteamBase(models.Model):
    name = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to="food/%Y/%m", default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Food(IteamBase):
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(
        "Tag", related_name="tags_detail", blank=True, null=True
    )


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# class Comment(models.Model):
#     content = models.CharField(max_length=100, unique=True)
#     # food_comment = models.ForeignKey(
#     #     Food, related_name="f_comment", on_delete=models.CASCADE, null=True
#     # )
#     user = models.ForeignKey("User", on_delete=models.CASCADE)
#     updated_date = models.DateTimeField(auto_now=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     food_comment = models.ForeignKey(
#         Food, related_name="food_comment", on_delete=models.CASCADE
#     )

#     class Meta:
#         ordering = ["-created_date"]

#     def __str__(self):
#         return self.content
