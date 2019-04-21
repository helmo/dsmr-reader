from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel
from datetime import time
from django.utils import timezone


class DayStatistics(models.Model):
    """ Daily consumption usage summary. """
    day = models.DateField(unique=True, db_index=True, verbose_name=_('Date'))
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Total cost'))

    electricity1 = models.DecimalField(
        max_digits=9, decimal_places=3, verbose_name=_('Electricity 1 (low tariff)')
    )
    electricity2 = models.DecimalField(
        max_digits=9, decimal_places=3, verbose_name=_('Electricity 2 (high tariff)')
    )
    electricity1_returned = models.DecimalField(
        max_digits=9, decimal_places=3, verbose_name=_('Electricity 1 returned (low tariff)')
    )
    electricity2_returned = models.DecimalField(
        max_digits=9, decimal_places=3, verbose_name=_('Electricity 2 returned (high tariff)')
    )
    electricity1_cost = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name=_('Electricity 1 price (low tariff)')
    )
    electricity2_cost = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name=_('Electricity 2 price (high tariff)')
    )

    # Gas readings are optional/not guaranteed.
    gas = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, default=None, verbose_name=_('Gas')
    )
    gas_cost = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, default=None, verbose_name=_('Gas price')
    )

    # Temperature readings depend on user settings.
    lowest_temperature = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, default=None, verbose_name=_('Lowest temperature')
    )
    highest_temperature = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, default=None, verbose_name=_('Highest temperature')
    )
    average_temperature = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, default=None, verbose_name=_('Average temperature')
    )

    @property
    def electricity_merged(self):
        return self.electricity1 + self.electricity2

    @property
    def electricity_returned_merged(self):
        return self.electricity1_returned + self.electricity2_returned

    class Meta:
        default_permissions = tuple()
        verbose_name = _('Day statistics (automatically generated data)')
        verbose_name_plural = verbose_name
        ordering = ['day']

    def __str__(self):
        return '{}: {}'.format(
            self.__class__.__name__, self.day
        )


class HourStatistics(models.Model):
    """ Hourly consumption usage summary. """
    hour_start = models.DateTimeField(unique=True, db_index=True, verbose_name=_('Hour start'))

    electricity1 = models.DecimalField(
        max_digits=9, decimal_places=3, verbose_name=_('Electricity 1 (low tariff)')
    )
    electricity2 = models.DecimalField(
        max_digits=9, decimal_places=3, verbose_name=_('Electricity 2 (high tariff)')
    )
    electricity1_returned = models.DecimalField(
        max_digits=9, decimal_places=3, verbose_name=_('Electricity 1 returned (low tariff)')
    )
    electricity2_returned = models.DecimalField(
        max_digits=9, decimal_places=3, verbose_name=_('Electricity 2 returned (high tariff)')
    )

    # Gas readings are optional/not guaranteed. But need to be zero due to averages.
    gas = models.DecimalField(max_digits=9, decimal_places=3, default=0, verbose_name=_('Gas'))

    @property
    def electricity_merged(self):
        return self.electricity1 + self.electricity2

    @property
    def electricity_returned_merged(self):
        return self.electricity1_returned + self.electricity2_returned

    class Meta:
        default_permissions = tuple()
        verbose_name = _('Hour statistics (automatically generated data)')
        verbose_name_plural = verbose_name
        ordering = ['hour_start']

    def __str__(self):
        return '{}: {}'.format(
            self.__class__.__name__, self.hour_start
        )


class ElectricityStatistics(SingletonModel):
    """ Keeps track of the highest electricity statistics per phase. """
    highest_usage_l1_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest usage on L1+')
    )
    highest_usage_l2_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest usage on L2+')
    )
    highest_usage_l3_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest usage on L3+')
    )
    highest_return_l1_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest return on L1-')
    )
    highest_return_l2_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest return on L2-')
    )
    highest_return_l3_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest return on L3-')
    )
    lowest_usage_l1_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of lowest usage on L1+')
    )
    lowest_usage_l2_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of lowest usage on L2+')
    )
    lowest_usage_l3_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of lowest usage on L3+')
    )

    """ Day usage/return """
    highest_day_usage_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest day usage')
    )
    highest_day_return_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest day return')
    )
    highest_day_usage_1_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest day usage 1')
    )
    highest_day_return_1_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest day return 1')
    )
    highest_day_usage_2_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest day usage 2')
    )
    highest_day_return_2_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of highest day return 2')
    )
    lowest_day_usage_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of lowest day usage')
    )
    lowest_day_usage_1_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of lowest day usage 1')
    )
    lowest_day_usage_2_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of lowest day usage 2')
    )
    lowest_day_return_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of lowest day return')
    )
    lowest_day_return_1_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of lowest day return 1')
    )
    lowest_day_return_2_timestamp = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_('Timestamp of lowest day return 2')
    )

    highest_usage_l1_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest usage on L1+ (in Watt)')
    )
    highest_usage_l2_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest usage on L2+ (in Watt)')
    )
    highest_usage_l3_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest usage on L3+ (in Watt)')
    )
    highest_return_l1_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest return on L1- (in Watt)')
    )
    highest_day_return_l1_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest return on L1- (in Watt)')
    )
    highest_return_l2_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest return on L2- (in Watt)')
    )
    highest_return_l3_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest return on L3- (in Watt)')
    )
    lowest_usage_l1_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Lowest usage on L1+ (in Watt)')
    )
    lowest_usage_l2_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Lowest usage on L2+ (in Watt)')
    )
    lowest_usage_l3_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Lowest usage on L3+ (in Watt)')
    )

    """ Day usage """
    highest_day_usage_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest day usage (in Wh)')
    )
    highest_day_usage_1_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest day usage 1 (in Wh)')
    )
    highest_day_usage_2_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest day usage 2 (in Wh)')
    )
    highest_day_return_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest day return (in Wh)')
    )
    highest_day_return_1_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest day return 1 (in Wh)')
    )
    highest_day_return_2_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Highest day return 2 (in Wh)')
    )
    lowest_day_usage_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Lowest day usage (in Wh)')
    )
    lowest_day_usage_1_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Lowest day usage 1 (in Wh)')
    )
    lowest_day_usage_2_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Lowest day usage 2 (in Wh)')
    )
    lowest_day_return_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Lowest day return (in Wh)')
    )
    lowest_day_return_1_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Lowest day return 1 (in Wh)')
    )
    lowest_day_return_2_value = models.DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True, default=None,
        verbose_name=_('Lowest day return 2 (in Wh)')
    )

    def clear(self):
        """ Clear the data. """
        data = self.__dict__
        now = timezone.localtime(timezone.now())
        for key in data.keys():
            if key.endswith('_value'):
                data[key] = 0
            else:
#                data[key] = 0
                data[key] =  now.date()
#                data[key] = "2000-01-01"
#                data[key] = "0000-00-00"
#                setattr(data[key], "0000-00-00")

        self.save()

    def export(self):
        """ Converts the data in to ready to use format. """
        data = self.__dict__

        for key in data.keys():
            if key.endswith('_value'):
                try:
                    data[key] = int(data[key] * 1000) or 0
                except TypeError:
                    data[key] = 0

        return data

    class Meta:
        default_permissions = tuple()
        verbose_name = _('Electricity statistics')
