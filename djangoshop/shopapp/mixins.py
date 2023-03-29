from django.db import models


class PriceSummaryMixin:
    def price_summary(self):
        price = self.products.all().aggregate(models.Sum('price')).get('price__sum')
        return price

    # def price_summary_wo_aggregate(self): #  все равно 14 запросов но пересчет на сервере а не базе
    #     price = sum(i.price for i in self.products.all())
    #     return price