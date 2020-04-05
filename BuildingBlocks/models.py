from django.db import models
from django.contrib import admin


class Tenant(models.Model):
    tenant_name = models.CharField(max_length=30, blank=False)
    tenant_address = models.CharField(max_length=300, null=True, blank=True)
    tenant_identity = models.IntegerField(null=True, blank=True)
    tenant_date_of_birth = models.DateField(null=True, blank=True)
    tenant_profession = models.CharField(max_length=50, null=True, blank=True)
    tenant_photo = models.URLField(max_length=500, null=True, blank=True)
    tenant_active = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.tenant_name


class Asset(models.Model):
    asset_name = models.CharField(max_length=200, blank=False, null=False)
    asset_price = models.FloatField(blank=False, null=False)
    asset_details = models.CharField(max_length=500)
    asset_bought_date = models.DateField(blank=False, null=False)
    asset_rate_of_return = models.FloatField()
    asset_market_value = models.FloatField()

    def __str__(self):
        return self.asset_name


class Payment(models.Model):
    payment_tenant_name = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    payment_asset_name = models.ForeignKey(Asset, on_delete=models.CASCADE)
    payment_date = models.DateField(blank=True, null=True)
    payment_due_date = models.DateField()
    payment_amount = models.DecimalField(decimal_places=2, max_digits=10)
    payment_partial_amount = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.payment_tenant_name.tenant_name + "( "+ self.payment_asset_name.asset_name +" ) " + "paid" + " " + str(self.payment_amount) + " on " + str(self.payment_date)


class Rent(models.Model):
    rent_tenant_name = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    rent_asset_name = models.ForeignKey(Asset, on_delete=models.CASCADE)
    rent_amount = models.DecimalField(decimal_places=2, max_digits=10)
    rent_advance_amount = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.rent_tenant_name.tenant_name + "( "+ self.rent_asset_name.asset_name +" ) " + "paying" + " a rent of " + str(self.rent_amount) + " with an advance of " + str(self.rent_advance_amount)


class Debt(models.Model):
    debt_source = models.CharField(max_length=500)
    debt_amount = models.DecimalField(decimal_places=2, max_digits=10)
    debt_interest = models.DecimalField(decimal_places=2, max_digits=5)
    debt_amount_paid = models.DecimalField(decimal_places=2, max_digits=10)
    debt_emi = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return "Debt of " + str(self.debt_amount) + " from " + self.debt_source + " @ " + str(self.debt_interest) + "% with an EMI of " + str(self.debt_emi)


class WishListItem(models.Model):
    item_name = models.CharField(max_length=500)
    item_amount = models.DecimalField(decimal_places=2, max_digits=10)
    item_bought = models.BooleanField(default=False)

    def __str__(self):
        return str(self.item_name)


class GoldItem(models.Model):
    item_name = models.CharField(max_length=500)
    item_weight = models.DecimalField(decimal_places=2, max_digits=10)
    item_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.item_name) + " (" + str(self.item_weight) + "gms )"


class CreditCard(models.Model):
    card_name = models.CharField(max_length=500)
    card_last_digits = models.IntegerField()
    card_expiry = models.DateField()

    def __str__(self):
        return str(self.card_name) + " (" + str(self.card_last_digits) + " ), expiry " + str(self.card_expiry)


class CreditCardBill(models.Model):
    bill_card_name = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    bill_month = models.DateField()
    bill_amount = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.bill_card_name.card_name) + " @ " + str(self.bill_month) + " bill is " + str(self.bill_amount)


class Task(models.Model):
    PRIORITY_CHOICES = ((0, 'low'), (1, 'medium'), (2, 'high'), (3, 'urgent'))
    STATUS_CHOICES = ((0, 'not started'), (1, 'started'), (2, 'differed'), (3, 'complete'))
    task_name = models.CharField(max_length=200)
    task_details = models.CharField(max_length=500)
    task_priority = models.IntegerField(choices=PRIORITY_CHOICES)
    task_status = models.IntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return self.task_name


class Expense(models.Model):
    expense_name = models.CharField(max_length=300)
    expense_amount = models.DecimalField(decimal_places=2, max_digits=10)
    expense_date = models.DateField()

    def __str__(self):
        return self.expense_name


class Income(models.Model):
    income_name = models.CharField(max_length=300)
    income_amount = models.DecimalField(decimal_places=2, max_digits=10)
    income_date = models.DateField()

    def __str__(self):
        return self.income_name


class RecurringExpense(models.Model):
    r_expense_name = models.CharField(max_length=300)
    r_expense_amount = models.DecimalField(decimal_places=2, max_digits=10)
    r_expense_date = models.DateField()

    def __str__(self):
        return self.r_expense_name


class RecurringIncome(models.Model):
    r_income_name = models.CharField(max_length=300)
    r_income_amount = models.DecimalField(decimal_places=2, max_digits=10)
    r_income_date = models.DateField()

    def __str__(self):
        return self.r_income_name
