from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    cuisine = models.CharField(max_length=80, default="Multi-cuisine")
    location = models.CharField(max_length=120, default="Kadapa")
    image_url = models.URLField(blank=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="food_items")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image_url = models.URLField(blank=True)
    is_vegetarian = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} — {self.restaurant.name}"
