from django.contrib import admin
from BuildingBlocks.models import Tenant, Asset, Payment, Rent, Debt, WishListItem, GoldItem, CreditCard, CreditCardBill
from BuildingBlocks.models import Task, Income, Expense, RecurringExpense, RecurringIncome


class TenantAdmin(admin.ModelAdmin):
    list_display=('tenant_name','tenant_address','tenant_identity','tenant_profession','active')
    list_display_links = ('tenant_name',)
    list_filter = ('tenant_name','tenant_address','tenant_identity','tenant_profession')
    search_fields = ('tenant_name','tenant_address','tenant_identity','tenant_profession')

    def active(self, obj):
        return obj.tenant_active

    active.boolean = True


# Register your models here.
admin.site.register(Tenant, TenantAdmin)
admin.site.register(Asset)
admin.site.register(Payment)
admin.site.register(Rent)
admin.site.register(Debt)
admin.site.register(WishListItem)
admin.site.register(GoldItem)
admin.site.register(CreditCard)
admin.site.register(CreditCardBill)
admin.site.register(Task)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(RecurringIncome)
admin.site.register(RecurringExpense)