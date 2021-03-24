from django.db import models
from django.db.models import ExpressionWrapper, F, Sum


class VegOutQuerySet(models.QuerySet):
    def summary(self):
        return self.select_related('user').annotate(
            qs_co2_savings=0.0884 * F('veggie_meals') * 8.7,
            qs_water_savings=ExpressionWrapper(0.75 * F('current_meals'), output_field=models.FloatField()),
            qs_waste_savings=ExpressionWrapper(
                0.2 * F('current_meals') * F('veggie_meals'), output_field=models.FloatField()
            ),
        )

    def total(self):
        return self.summary().aggregate(
            total_co2=Sum('qs_co2_savings'),
            total_water=Sum('qs_water_savings'),
            total_waste=Sum('qs_waste_savings'),
        )


class CleanBillQuerySet(models.QuerySet):
    def summary(self):
        return self.select_related('user').annotate(
            qs_co2_savings=ExpressionWrapper(
                49 * F('energy_supplier') * F('number_of_people') * F('heating_source'),
                output_field=models.FloatField(),
            ),
        )

    def total(self):
        return self.summary().aggregate(
            total_co2=Sum('qs_co2_savings'),
        )
