#!-*-coding: utf-8 -*-
from django.db import models
from eproduct.models import *
from epartnumber.models import *

#### Region

class Region(models.Model):
    title = models.CharField(max_length=200)

#### City

class City(models.Model):
    title = models.CharField(max_length=200)
    region = models.ForeignKey(Region)

class FilterCityIdRegion(models.Model):
    pickup_points = models.ManyToManyField(City)
    regions = models.ManyToManyField(Region)

#### Storage

class Storage(models.Model):
    title = models.CharField(max_length=200)

    def quantity(self, product):
        quantity = 0
        for stock in Stock.objects.filter(storage=self, product=product):
            quantity += stock.quantity
        return quantity

    def list_product(self):
        products = set()
        for stock in Stock.objects.filter(storage=self):
            products.add(stock.product)
        return list(products)

    def list_part_number_for_product(self, product):
        part_numbers = set()
        for stock in Stock.objects.filter(storage=self, product=product):
            part_numbers.add(stock.part_number)
        return list(part_numbers)

    def load(self, product, quantity, part_number):
        stock = Stock(product=product, quantity=quantity, storage=self, part_number=part_number)
        stock.save()

class Stock(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(u"Количество")
    storage = models.ForeignKey(Storage)
    part_number = models.ForeignKey(PartNumber)

class FilterStorageId(models.Model):
    storages = models.ManyToManyField(Storage)

#### PickupPoint

class PickupPoint(models.Model):
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City)

    def get_city(self):
        return self.city

class FilterPickupPointIdCity(models.Model):
    pickup_points = models.ManyToManyField(PickupPoint)
    cities = models.ManyToManyField(City)
