from django.db import models


class PriceSummaryMixin:
    def price_summary(self):
        price = self.products.all().aggregate(models.Sum('price')).get('price__sum')
        return price
