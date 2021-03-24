from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .behaviours import Pledgeable
from .managers import CleanBillQuerySet, VegOutQuerySet

User = settings.AUTH_USER_MODEL


class VegOut(Pledgeable):
    """
    Model to store Veg Out pledges amongst users.
    Currently on verison 1.0 of calculation metrics.
    """

    class VegMealCount(float, models.Choices):
        ONE_TO_FIVE = 2.5, _('1 to 5')
        SIX_TO_TEN = 3, _('6 to 10')
        TEN_PLUS = 3.5, _('10+')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    current_meals = models.PositiveIntegerField(
        _('current meals'),
        validators=[MaxValueValidator(limit_value=42)],
        help_text=_(
            """
            The amount of meaty meals you currently have each week.
            """
        ),
    )
    veggie_meals = models.FloatField(
        _('veggie meals'),
        choices=VegMealCount.choices,
        default=VegMealCount.ONE_TO_FIVE,
        help_text=_(
            """
            The amount of meals you wish to go veggie for.
            """
        ),
    )
    version = models.FloatField(_('calculation version'), default=1.0)
    objects = VegOutQuerySet.as_manager()

    class Meta:
        ordering = ('-pledge_start',)
        verbose_name = _('veg out pledge')
        verbose_name_plural = _('veg out pledges')

    def __str__(self):
        return f'{self.user.username}\'s pledge on {self.pledge_start}'

    @property
    def pledge_text(self):
        return _(
            f"""\
            At the moment, I munch on {self.current_meals} meaty meals each week. For the next two months, I \
            pledge to go veg for {self.veggie_meals} extra meals each week.\
            """
        )

    @property
    def co2_savings(self):
        if self.veggie_meals:
            if self.version == 1.0:
                result = round(0.0884 * self.veggie_meals * 8.7, 2)
            else:
                result = 0
            return result

    @property
    def water_savings(self):
        if self.current_meals:
            if self.version == 1.0:
                result = round(0.75 * self.current_meals, 2)
        else:
            result = 0
        return result

    @property
    def waste_savings(self):
        if self.current_meals and self.veggie_meals:
            if self.version == 1.0:
                result = round(0.2 * self.current_meals * self.veggie_meals, 2)
        else:
            result = 0
        return result


class CleanBill(Pledgeable):
    """
    Model to store Clean Bill pledges amongst users.
    Currently on verison 1.0 of calculation metrics.
    """

    class EnergySupplier(float, models.Choices):
        BOG_STANDARD = 0.5, _('Bog Standard')
        GREEN_ENERGY = 0, _('Great Green Tariff')

    class HeatingSource(float, models.Choices):
        GAS_OR_OIL = 5, _('Gas or Oil')
        ELECTRICITY = 3, _('Electicity')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    number_of_people = models.PositiveIntegerField(
        _('number of people'),
        validators=[MaxValueValidator(limit_value=12)],
        help_text=_(
            """
            The number of people currently living in your house.
            """
        ),
    )
    energy_supplier = models.FloatField(
        _('energy supplier'),
        choices=EnergySupplier.choices,
        help_text=_(
            """
            Your current energy supplier.
            """
        ),
    )
    heating_source = models.FloatField(
        _('heating source'),
        choices=HeatingSource.choices,
        help_text=_(
            """
            Your current heating source.
            """
        ),
    )
    version = models.FloatField(_('calculation version'), default=1.0)
    objects = CleanBillQuerySet.as_manager()

    class Meta:
        ordering = ('-pledge_start',)
        verbose_name = _('clean bill pledge')
        verbose_name_plural = _('clean bill pledges')

    def __str__(self):
        return f'{self.user.username}\'s pledge on {self.pledge_start}'

    @property
    def pledge_text(self):
        return _(
            f"""\
            Within the next two months, I pledge to switch from my current energy supplier – which is \
                {self.get_energy_supplier_display()} – to a green energy supplier. {self.number_of_people} \
            people live in our home. My house is mainly heated by {self.get_heating_source_display()}.
            """
        )

    @property
    def co2_savings(self):
        if self.number_of_people and self.energy_supplier and self.heating_source:
            if self.version == 1.0:
                result = round(49 * self.energy_supplier * self.number_of_people * self.heating_source, 2)
        else:
            result = 0
        return result
