from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

from .. import views
from ..models import CleanBill, VegOut


class PledgeListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='freddy', password='passsword')
        cls.veg_out_obj = VegOut.objects.create(
            user=cls.user,
            current_meals=12,
            veggie_meals=3.5,
            pledge_start='2021-03-23',
        )
        cls.clean_bill_obj = CleanBill.objects.create(
            user=cls.user,
            number_of_people=5,
            energy_supplier=0.5,
            heating_source=5.0,
            pledge_start='2021-03-23',
        )
        cls.url = reverse('pledges:pledge_list')

    def test_url_resolves_to_correct_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.resolver_match.func.__name__, views.PledgeListView.as_view().__name__)

    def test_user_can_access_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'pledges/pledge_list.html')

    def test_template_contains_correct_html(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'All Pledges')

    def test_template_does_not_contain_incorrect_html(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, 'Not All Pledges')

    def test_context_data_contains_object_lists(self):
        response = self.client.get(self.url)
        self.assertTrue('veg_out_list' in response.context)
        self.assertTrue('clean_bill_list' in response.context)

    def test_context_data_contains_correct_object_lists(self):
        response = self.client.get(self.url)
        self.assertQuerysetEqual(response.context['veg_out_list'], ['<VegOut: freddy\'s pledge on 2021-03-23>'])
        self.assertQuerysetEqual(response.context['clean_bill_list'], ['<CleanBill: freddy\'s pledge on 2021-03-23>'])


class UserPledgeListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setting up test data for different user's access
        cls.another_user = User.objects.create_user(username='alice', password='passsword')
        cls.user = User.objects.create_user(username='freddy', password='passsword')
        # Setting up test data for different user's object lists
        cls.another_veg_out_obj = VegOut.objects.create(
            user=cls.another_user,
            current_meals=8,
            veggie_meals=2.5,
            pledge_start='2021-03-23',
        )
        cls.another_clean_bill_obj = CleanBill.objects.create(
            user=cls.another_user,
            number_of_people=1,
            energy_supplier=0.5,
            heating_source=5.0,
            pledge_start='2021-03-23',
        )
        cls.veg_out_obj = VegOut.objects.create(
            user=cls.user,
            current_meals=12,
            veggie_meals=3.5,
            pledge_start='2021-03-23',
        )
        cls.clean_bill_obj = CleanBill.objects.create(
            user=cls.user,
            number_of_people=5,
            energy_supplier=0.5,
            heating_source=5.0,
            pledge_start='2021-03-23',
        )
        # Setting up test data for different user specific urls
        cls.url = reverse('pledges:user_pledge_list', kwargs={'pk': cls.user.pk})
        cls.alice_url = reverse('pledges:user_pledge_list', kwargs={'pk': cls.another_user.pk})
        cls.invalid_url = reverse('pledges:user_pledge_list', kwargs={'pk': 9999})

    def test_url_resolves_to_correct_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.resolver_match.func.__name__, views.UserPledgeListView.as_view().__name__)

    def test_user_can_access_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_url_kwarg_raises_404(self):
        response = self.client.get(self.invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_correct_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'pledges/user_pledge_list.html')

    def test_template_contains_correct_html(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Freddy\'s Pledges')

    def test_template_does_not_contain_incorrect_html(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, 'Not Freddy\'s Pledges')

    def test_context_data_contains_object_lists(self):
        response = self.client.get(self.url)
        self.assertTrue('veg_out_list' in response.context)
        self.assertTrue('clean_bill_list' in response.context)

    def test_context_data_contains_correct_object_lists_for_user(self):
        response = self.client.get(self.url)
        self.assertQuerysetEqual(response.context['veg_out_list'], ['<VegOut: freddy\'s pledge on 2021-03-23>'])
        self.assertQuerysetEqual(response.context['clean_bill_list'], ['<CleanBill: freddy\'s pledge on 2021-03-23>'])

    def test_context_data_contains_correct_object_lists_for_another_user(self):
        response = self.client.get(self.alice_url)
        self.assertQuerysetEqual(response.context['veg_out_list'], ['<VegOut: alice\'s pledge on 2021-03-23>'])
        self.assertQuerysetEqual(response.context['clean_bill_list'], ['<CleanBill: alice\'s pledge on 2021-03-23>'])
