from hashids import Hashids
from django.db import models
from django.conf import settings
from django.urls import reverse

hashids = Hashids(salt=settings.SECRET_KEY, min_length=8)

class Order(models.Model):
    """Just an example of the model to store Order's data."""

    date_created = models.DateTimeField(auto_now_add=True)
    grand_total = models.DecimalField(max_digits=8, decimal_places=2)
    language = models.CharField(max_length=5, default=settings.LANGUAGE_CODE)

    @property
    def public_id(self):
        return hashids.encode(self.pk)

    def get_absolute_url(self):
        return reverse('ticket_details', args=(self.public_id,))
