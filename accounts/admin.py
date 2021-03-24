from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from pledges.models import CleanBill, VegOut

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CleanBillInline(admin.StackedInline):
    model = CleanBill
    extra = 0


class VegOutInline(admin.StackedInline):
    model = VegOut
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
    )
    inlines = [
        CleanBillInline,
        VegOutInline,
    ]

    def get_inline_instances(self, request, obj=None):
        # Only include inlines in the admin edit form.
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
