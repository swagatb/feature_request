from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned


CLIENT_CHOICES = [
    ("Client-A","Client-A"), 
    ("Client-B","Client-B"), 
    ("Client-C","Client-C"), 
    ("Client-D","Client-D"), 
]

PRODUCT_CHOICES = [
    ("None", "None"),
    ("Policies", "Policies"), 
    ("Billing", "Billing"), 
    ("Claims", "Claims"), 
    ("Reports", "Reports")
]

# Create your models here.
    
class Feature(models.Model):
    reporter = models.ForeignKey(User)
    title = models.CharField(max_length = 200)
    description = models.TextField()
    client = models.CharField(max_length=10,
                              choices=CLIENT_CHOICES)
    client_priority = models.IntegerField()
    target_date = models.DateField()
    product_area = models.CharField(max_length=10,
                                    choices=PRODUCT_CHOICES)

    #class Meta:
        #unique_together = (("client", "client_priority"),)
    
    def __unicode__(self):
        return self.title
    
    def save(self, is_update_priority=False, *args, **kwargs):
        def update_priority():
            features = self.__class__.objects.filter(reporter=self.reporter, client=self.client)
            for ft in features:
                ft.client_priority +=1
                ft.save()

        if is_update_priority:
            # Save called for update priority only
            # bool check to prevent recursive loop
            return super(Feature, self).save(is_update_priority=True, *args, **kwargs)
        try:
            exist_instance = self.__class__.objects.get(client=self.client,
                                                        client_priority=self.client_priority)
        except (Feature.DoesNotExist):
            pass
        except MultipleObjectsReturned:
            update_priority()
        else:
            update_priority()
        finally:    
            return super(Feature, self).save(*args, **kwargs)
