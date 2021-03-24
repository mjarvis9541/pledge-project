from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Pledgeable(models.Model):
    """
    Model to store common fields and properties across pledges.
    """

    comments = models.CharField(
        _('comments'),
        max_length=225,
        null=True,
        blank=True,
        help_text=_(
            """
            Anything to say about your pledge? This will be publicly visible.
            """
        ),
    )

    pledge_start = models.DateField(_('pledge start'), default=timezone.now)

    class Meta:
        abstract = True

    @property
    def pledge_end(self):
        result = self.pledge_start + relativedelta(months=2)
        return result
