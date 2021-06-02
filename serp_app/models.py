from django.db import models
from django.utils import timezone

# Create your models here.


class SearchResult(models.Model):
    search_result_id = models.AutoField(
                  auto_created = True,
                  primary_key = True,
                  serialize = False, 
                )
    query = models.CharField(max_length=200)
    results_total = models.BigIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    client_ip =  models.GenericIPAddressField()


class Link_with_position(models.Model):
    link_id = models.AutoField(
                  auto_created = True,
                  primary_key = True,
                  serialize = False, 
                )
    link = models.CharField(max_length=1000)
    position = models.IntegerField()
    search_result =  models.ForeignKey(SearchResult, on_delete=models.CASCADE)

class PopularWord(models.Model):
    word_id = models.AutoField(
                  auto_created = True,
                  primary_key = True,
                  serialize = False, 
                )
    word = models.CharField(max_length=100)
    occurances = models.IntegerField()
    search_result =  models.ForeignKey(SearchResult, on_delete=models.CASCADE)

