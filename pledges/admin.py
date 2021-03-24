from django.contrib import admin

from .models import CleanBill, VegOut


@admin.register(VegOut)
class VegOutAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    ordering = ('-pledge_start',)
    list_display = (
        'user',
        'pledge_start',
        'pledge_end',
        'current_meals',
        'veggie_meals',
        'co2_savings',
        'water_savings',
        'waste_savings',
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'user',
                    'current_meals',
                    'veggie_meals',
                    'comments',
                    'pledge_text',
                    'version',
                    'pledge_start',
                    'pledge_end',
                    'co2_savings',
                    'water_savings',
                    'waste_savings',
                )
            },
        ),
    )
    readonly_fields = (
        'pledge_text',
        'pledge_end',
        'co2_savings',
        'water_savings',
        'waste_savings',
    )


@admin.register(CleanBill)
class CleanBillsAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    ordering = ('-pledge_start',)
    list_display = (
        'user',
        'pledge_start',
        'pledge_end',
        'number_of_people',
        'energy_supplier',
        'heating_source',
        'co2_savings',
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'user',
                    'number_of_people',
                    'energy_supplier',
                    'heating_source',
                    'comments',
                    'pledge_text',
                    'version',
                    'pledge_start',
                    'pledge_end',
                    'co2_savings',
                )
            },
        ),
    )
    readonly_fields = (
        'pledge_text',
        'pledge_end',
        'co2_savings',
    )
