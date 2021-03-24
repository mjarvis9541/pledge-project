from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

from ..models import CleanBill, VegOut


class VegOutModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_fred = User.objects.create_user(username='freddy', password='passsword')
        cls.user_alice = User.objects.create_user(username='alice', password='passsword')
        cls.pledge_by_fred = VegOut.objects.create(user=cls.user_fred, current_meals=30, veggie_meals=3.5)
        cls.pledge_by_alice = VegOut.objects.create(user=cls.user_alice, current_meals=23, veggie_meals=3)

    def test_freds_pledge_exists(self):
        self.assertIsInstance(self.pledge_by_fred, VegOut)

    def test_alices_pledge_exists(self):
        self.assertIsInstance(self.pledge_by_alice, VegOut)

    def test_string_representation_is_correct(self):
        self.assertEqual(
            str(self.pledge_by_fred), f'{self.user_fred.username}\'s pledge on {self.pledge_by_fred.pledge_start}'
        )

    def test_string_representation_is_not_incorrect(self):
        self.assertNotEqual(
            str(self.pledge_by_alice), f'{self.user_fred.username}\'s pledge on {self.pledge_by_fred.pledge_start}'
        )

    # Testing pledge calculations

    def test_property_fred_co2_savings_for_v1_is_correct(self):
        self.assertEqual(self.pledge_by_fred.co2_savings, 2.69)
        self.assertNotEqual(self.pledge_by_fred.co2_savings, 0)

    def test_property_fred_water_savings_for_v1_is_correct(self):
        self.assertEqual(self.pledge_by_fred.water_savings, 22.5)
        self.assertNotEqual(self.pledge_by_fred.water_savings, 0)

    def test_property_fred_waste_savings_for_v1_is_correct(self):
        self.assertEqual(self.pledge_by_fred.waste_savings, 21.0)
        self.assertNotEqual(self.pledge_by_fred.waste_savings, 0)

    def test_property_alice_co2_savings_for_v1_is_correct(self):
        self.assertEqual(self.pledge_by_alice.co2_savings, 2.31)
        self.assertNotEqual(self.pledge_by_alice.co2_savings, 0)

    def test_property_alice_water_savings_for_v1_is_correct(self):
        self.assertEqual(self.pledge_by_alice.water_savings, 17.25)
        self.assertNotEqual(self.pledge_by_alice.water_savings, 0)

    def test_property_alice_waste_savings_for_v1_is_correct(self):
        self.assertEqual(self.pledge_by_alice.waste_savings, 13.8)
        self.assertNotEqual(self.pledge_by_alice.waste_savings, 0)


class CleanBillModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_fred = User.objects.create_user(username='freddy', password='passsword')
        cls.user_alice = User.objects.create_user(username='alice', password='passsword')
        cls.pledge_by_fred = CleanBill.objects.create(
            user=cls.user_fred, number_of_people=5, energy_supplier=0.5, heating_source=5.0
        )
        cls.pledge_by_alice = CleanBill.objects.create(
            user=cls.user_alice, number_of_people=3, energy_supplier=0, heating_source=3.0
        )

    def test_freds_pledge_exists(self):
        self.assertIsInstance(self.pledge_by_fred, CleanBill)

    def test_alices_pledge_exists(self):
        self.assertIsInstance(self.pledge_by_alice, CleanBill)

    def test_string_representation_is_correct(self):
        self.assertEqual(
            str(self.pledge_by_fred), f'{self.user_fred.username}\'s pledge on {self.pledge_by_fred.pledge_start}'
        )

    def test_string_representation_is_not_incorrect(self):
        self.assertNotEqual(
            str(self.pledge_by_alice), f'{self.user_fred.username}\'s pledge on {self.pledge_by_fred.pledge_start}'
        )

    # Testing pledge calculations

    def test_property_fred_co2_savings_for_v1_is_correct(self):
        self.assertEqual(self.pledge_by_fred.co2_savings, 612.5)
        self.assertNotEqual(self.pledge_by_fred.co2_savings, 0)

    def test_property_alice_co2_savings_for_v1_is_correct(self):
        self.assertEqual(self.pledge_by_alice.co2_savings, 0)
        self.assertNotEqual(self.pledge_by_alice.co2_savings, 10)
