from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import CleanBill, VegOut

User = get_user_model()


class PledgeListView(TemplateView):
    """ Display all pledges from all users, savings and totals. """

    template_name = 'pledges/pledge_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['veg_out_list'] = veg_out = VegOut.objects.summary()
        context['veg_out_total'] = veg_out.total()
        context['clean_bill_list'] = clean_bill = CleanBill.objects.summary()
        context['clean_bill_total'] = clean_bill.total()
        return context


class UserPledgeListView(TemplateView):
    """ Display individual user pledges and savings. """

    template_name = 'pledges/user_pledge_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pledge_user'] = user_ = get_object_or_404(User, pk=self.kwargs.get('pk'))
        context['veg_out_list'] = VegOut.objects.filter(user=user_).summary()
        context['clean_bill_list'] = CleanBill.objects.filter(user=user_).summary()
        return context
