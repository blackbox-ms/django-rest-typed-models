from django.db import models
from typedmodels.models import TypedModel


class BlogBase(TypedModel):
    name = models.CharField(max_length=10)
    slug = models.SlugField(max_length=255, unique=True)


class BlogOne(BlogBase):
    info = models.CharField(max_length=10, null=True)


class BlogTwo(BlogBase):
    pass


class BlogThree(BlogBase):
    about = models.CharField(max_length=255, null=True)
    