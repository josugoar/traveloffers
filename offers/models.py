from django.db import models
from django.urls import reverse


class Category(models.Model):
    image = models.ImageField(upload_to="media", blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("offers:category-detail", args=(self.id,))

    def __str__(self):
        return self.name


class Country(models.Model):
    image = models.ImageField(upload_to="media", blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "countries"

    def get_absolute_url(self):
        return reverse("offers:country-detail", args=(self.id,))

    def __str__(self):
        return self.name


class Offer(models.Model):
    categories = models.ManyToManyField(Category, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    days = models.IntegerField()
    description = models.TextField()
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to="media", blank=True)
    name = models.CharField(max_length=255)
    participants = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    score = models.FloatField(blank=True)
    valuations = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("offers:offer-detail", args=(self.id,))

    def __str__(self):
        return self.name
