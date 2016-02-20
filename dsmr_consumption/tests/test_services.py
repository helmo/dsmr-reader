from django.test import TestCase
from django.utils import timezone

from dsmr_backend.tests.mixins import CallCommandStdoutMixin
from dsmr_datalogger.models.reading import DsmrReading
from dsmr_consumption.models.consumption import ElectricityConsumption, GasConsumption
from dsmr_consumption.models.settings import ConsumptionSettings
import dsmr_consumption.services


class TestServices(CallCommandStdoutMixin, TestCase):
    fixtures = ['dsmr_consumption/test_dsmrreading.json']

    def setUp(self):
        self.assertEqual(DsmrReading.objects.all().count(), 3)
        self.assertTrue(DsmrReading.objects.unprocessed().exists())

        # Initializes singleton model.
        ConsumptionSettings.get_solo()

    def test_processing(self):
        """ Test fixed data parse outcome. """
        # Default is grouping by minute, so make sure to revert that here.
        consumption_settings = ConsumptionSettings.get_solo()
        consumption_settings.compactor_grouping_type = ConsumptionSettings.COMPACTOR_GROUPING_BY_READING
        consumption_settings.save()

        dsmr_consumption.services.compact_all()

        self.assertTrue(DsmrReading.objects.processed().exists())
        self.assertFalse(DsmrReading.objects.unprocessed().exists())
        self.assertEqual(ElectricityConsumption.objects.count(), 3)
        self.assertEqual(GasConsumption.objects.count(), 1)

    def test_grouping(self):
        """ Test grouping per minute, instead of the default 10-second interval. """
        # Make sure to verify the blocking of read ahead.
        dr = DsmrReading.objects.get(pk=3)
        dr.timestamp = timezone.now()
        dr.save()

        dsmr_consumption.services.compact_all()

        self.assertEqual(DsmrReading.objects.unprocessed().count(), 1)
        self.assertTrue(DsmrReading.objects.unprocessed().exists())
        self.assertEqual(ElectricityConsumption.objects.count(), 1)
        self.assertEqual(GasConsumption.objects.count(), 1)

    def test_creation(self):
        """ Test the datalogger's builtin fallback for initial readings. """
        self.assertFalse(ElectricityConsumption.objects.exists())
        self.assertFalse(GasConsumption.objects.exists())

        dsmr_consumption.services.compact_all()

        self.assertTrue(ElectricityConsumption.objects.exists())
        self.assertTrue(GasConsumption.objects.exists())

    def test_day_consumption(self):
        with self.assertRaises(LookupError):
            dsmr_consumption.services.day_consumption(timezone.now() + timezone.timedelta(weeks=1))
