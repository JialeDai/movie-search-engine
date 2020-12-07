from django.db import models
from djongo import models
import uuid
from bson.json_util import dumps
from django.urls import reverse

rating_choice = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5')
)

# Create your models here.
class Users(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    
    def __str__(self):
        return '{0}({1})'.format(self._id, self.name)


class Genre(models.Model):
    genre = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.genre


class Cast(models.Model):
    cast = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.cast


class Country(models.Model):
    country = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.country


class Language(models.Model):
    language = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.language


class Director(models.Model):
    director = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.director


class Writers(models.Model):
    writer = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.writer


class Imdb(models.Model):
    rating = models.PositiveIntegerField(null=True)
    votes = models.PositiveIntegerField(null=True)
    id = models.PositiveIntegerField(null=True)

    class Meta:
        abstract = True


class DouBan(models.Model):
    rating = models.PositiveIntegerField(default=-1)
    doubanlink = models.CharField(max_length=100, default="no link")

    class Meta:
        abstract = True


class Tomatoes(models.Model):
    fresh = models.PositiveIntegerField(null=True)
    rotten = models.PositiveIntegerField(null=True)

    class Meta:
        abstract = True


class Movies(models.Model):
    _id = models.ObjectIdField()
    plot = models.CharField(max_length=1000)
    genres = models.ArrayModelField(model_container=Genre)
    runtime = models.PositiveIntegerField()
    cast = models.ArrayModelField(model_container=Cast)
    poster = models.CharField(max_length=1000, null=True)
    title = models.CharField(max_length=1000)
    fullplot = models.CharField(max_length=1000)
    countries = models.ArrayModelField(model_container=Country)
    released = models.DateField()
    languages = models.ArrayModelField(model_container=Language)
    directors = models.ArrayModelField(model_container=Director)
    writers = models.ArrayModelField(model_container=Writers)
    year = models.PositiveIntegerField()
    imdb = models.EmbeddedModelField(model_container=Imdb)
    tomatoes = models.EmbeddedModelField(model_container=Tomatoes)
    Douban = models.EmbeddedModelField(model_container=DouBan)

    meta = {
        'indexes': [
            {'fields': ['plot'], 'sparse': True},
            {'fields': ['genres'], 'sparse': True},
            {'fields': ['runtime'], 'sparse': True},
            {'fields': ['cast'], 'sparse': True},
            {'fields': ['poster'], 'sparse': True},
            {'fields': ['title'], 'sparse': True},
            {'fields': ['fullplot'], 'sparse': True},
            {'fields': ['countries'], 'sparse': True},
            {'fields': ['released'], 'sparse': True},
            {'fields': ['languages'], 'sparse': True},
            {'fields': ['directors'], 'sparse': True},
            {'fields': ['writers'], 'sparse': True},
            {'fields': ['year'], 'sparse': True},
            {'fields': ['imdb'], 'sparse': True},
            {'fields': ['tomatoes'], 'sparse': True},
            {'fields': ['Douban'], 'sparse': True},
        ],
    }

    def __str__(self):
        return '{0}({1})'.format(self._id, self.title)

    def get_absolute_url(self):
        _id = dumps(self._id)['_id']['$oid']
        return reverse('result_detail', args=[_id])


class Ratings(models.Model):
    _id = models.ObjectIdField()
    movie_id = models.ArrayReferenceField(to=Movies, on_delete=models.CASCADE)
    user_id = models.ArrayReferenceField(to=Users, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(choices=rating_choice)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return '{0}({1}, {2}, {3}, {4})'.format(self._id, self.film_id, self.user_id, self.date, self.rating)
