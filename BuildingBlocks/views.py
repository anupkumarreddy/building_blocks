from django.shortcuts import render
from .models import Payment, Rent, Debt, WishListItem, Tenant, CreditCard, CreditCardBill, Asset, Task, GoldItem
from .models import Income, Expense, RecurringExpense, RecurringIncome
from django.views.generic import View
from django.db.models import Sum
import datetime, calendar
from django.shortcuts import redirect
from .forms import ShoppingFormSet, WishListItemForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class CurrencyToNameConverter:
    def __init__(self):
        pass

    def convert(self, number):
        if number > 10000000:
            return format(number / 10000000, ".2f") + " Cr"
        elif number > 100000:
            return format(number / 100000, '.2f') + " Lk"
        else:
            return str(number)


@method_decorator(login_required, name='dispatch')
class MainView(View):
    template_name = "app/index.html"

    def get(self, request, *args, **kwargs):
        this_month = datetime.datetime.now().month
        all_rents = Rent.objects.all()
        total_amount = Rent.objects.all().aggregate(Sum('rent_amount'))
        total_paid_amount = 0
        num_of_collected = 0
        num_of_rentals = Rent.objects.all().count()
        sum_of_assets = Asset.objects.all().aggregate(Sum('asset_price'))
        num_of_assets = Asset.objects.all().count()
        sum_of_debts = Debt.objects.all().aggregate(Sum('debt_amount'))
        num_of_debts = Debt.objects.all().count()
        equity = sum_of_assets['asset_price__sum'] - float(sum_of_debts['debt_amount__sum'])
        converter = CurrencyToNameConverter()

        for rent in all_rents:
            payment = Payment.objects.filter(payment_date__month=this_month).filter(
                payment_tenant_name=rent.rent_tenant_name)
            if payment:
                rent.rent_amount_paid = payment[0].payment_amount
                total_paid_amount = total_paid_amount + payment[0].payment_amount
                rent.rent_paid_date = payment[0].payment_date
                num_of_collected = num_of_collected + 1
            else:
                rent.rent_amount_paid = 0
                rent.rent_paid_date = ""
        total_due_amount = total_amount['rent_amount__sum'] - total_paid_amount
        num_of_pending = num_of_rentals - num_of_collected
        context = {"total_rents": total_amount['rent_amount__sum'], "num_of_rentals": num_of_rentals,
                   "total_rents_collected": total_paid_amount, "total_rents_pending": total_due_amount,
                   "num_of_collected": num_of_collected, "num_of_pending": num_of_pending,
                   "sum_of_assets": converter.convert(sum_of_assets['asset_price__sum']),
                   "sum_of_debts": converter.convert(sum_of_debts['debt_amount__sum']),
                   "num_of_assets": num_of_assets, "num_of_debts": num_of_debts, "equity": converter.convert(equity)}
        return render(request, self.template_name, context)


class MonthlyRentsView(View):
    template_name = "app/tables_dynamic.html"

    def get(self, request, *args, **kwargs):
        this_month = datetime.datetime.now().month
        if 'rent_id' in self.kwargs:
            rent_id = self.kwargs['rent_id']
            rent = Rent.objects.get(id=rent_id)
            payment = Payment.objects.filter(payment_date__month=this_month).filter(
                payment_tenant_name=rent.rent_tenant_name)
            if payment:
                pass
            else:
                today = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, 5)
                payment = Payment(payment_tenant_name=rent.rent_tenant_name, payment_asset_name=rent.rent_asset_name,
                                  payment_amount=rent.rent_amount, payment_date=datetime.datetime.now(),
                                  payment_due_date=today, payment_partial_amount=0)
                payment.save()

        all_rents = Rent.objects.all()
        total_amount = Rent.objects.all().aggregate(Sum('rent_amount'))
        total_paid_amount = 0
        total_paid_amount1 = 0

        for rent in all_rents:
            payment = Payment.objects.filter(payment_date__month=this_month).filter(
                payment_asset_name=rent.rent_asset_name)
            if payment:
                rent.rent_amount_paid = payment[0].payment_amount
                total_paid_amount = total_paid_amount + payment[0].payment_amount
                rent.rent_paid_date = payment[0].payment_date
            else:
                rent.rent_amount_paid = 0
                rent.rent_paid_date = ""
        total_due_amount = total_amount['rent_amount__sum'] - total_paid_amount
        all_rents1 = Rent.objects.all()
        for rent in all_rents1:
            payment = Payment.objects.filter(payment_date__month=this_month-1).filter(
                payment_asset_name=rent.rent_asset_name)
            if payment:
                rent.rent_amount_paid = payment[0].payment_amount
                total_paid_amount1 = total_paid_amount1 + payment[0].payment_amount
                rent.rent_paid_date = payment[0].payment_date
            else:
                rent.rent_amount_paid = 0
                rent.rent_paid_date = ""
        total_due_amount1 = total_amount['rent_amount__sum'] - total_paid_amount1
        context = {"month": calendar.month_name[this_month], "all_rents": all_rents,"all_rents1": all_rents1,
                   "total_rent_amount": total_amount['rent_amount__sum'], "total_rent_paid": total_paid_amount,
                   "total_due_pending": total_due_amount, "month1": calendar.month_name[this_month-1],
                   "total_rent_paid1": total_paid_amount1,
                   "total_due_pending1": total_due_amount1}
        return render(request, self.template_name, context)


class DebtsView(View):
    template_name = "app/debts.html"

    def get(self, request, *args, **kwargs):
        all_debts = Debt.objects.all()
        total_debt_amount = Debt.objects.all().aggregate(Sum('debt_amount'))
        total_debt_pid = Debt.objects.all().aggregate(Sum('debt_amount_paid'))
        total_emi = Debt.objects.all().aggregate(Sum('debt_emi'))
        context = {'all_debts': all_debts}
        return render(request, self.template_name, context)


class ShoppingView(View):
    template_name = "app/tables.html"

    def get(self, request, *args, **kwargs):
        form = WishListItemForm()
        if 'shopping_id' in self.kwargs:
            shopping_id = self.kwargs['shopping_id']
        else:
            shopping_id = -1
        if shopping_id >= 0:
            item = WishListItem.objects.get(pk=shopping_id)
            form = WishListItemForm(instance=item)
        all_items = WishListItem.objects.all()
        context = {'all_items': all_items, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        delete = False
        if 'shopping_id' in self.kwargs:
            shopping_id = self.kwargs['shopping_id']
        else:
            shopping_id = -1
            if 'delete_id' in self.kwargs:
                shopping_id = self.kwargs['delete_id']
                delete = True

        if shopping_id == -1:
            form = WishListItemForm(request.POST)
        else:
            if delete:
                WishListItem.objects.get(pk=shopping_id).delete()
            else:
                item = WishListItem.objects.get(pk=shopping_id)
                form = WishListItemForm(instance=item, data=request.POST)
                form.is_valid()
                model_instance = form.save(commit=False)
                model_instance.save()
        return redirect("shopping_default")


class TenantsView(View):
    template_name = "app/tenants.html"

    def get(self, request, *args, **kwargs):
        all_items = Tenant.objects.all()
        context = {'all_tenants': all_items}
        return render(request, self.template_name, context)


class CardsView(View):
    template_name = "app/cards.html"

    def get(self, request, *args, **kwargs):
        all_items = CreditCard.objects.all()
        for item in all_items:
            item.creditcardbillset = item.creditcardbill_set.all()
        print(all_items[0].creditcardbill_set.all())
        context = {'all_cards': all_items}
        return render(request, self.template_name, context)


class AssetsView(View):
    template_name = "app/assets.html"

    def get(self, request, *args, **kwargs):
        all_items = Asset.objects.all()
        context = {'all_assets': all_items}
        return render(request, self.template_name, context)


class TasksView(View):
    template_name = "app/tasks.html"

    def get(self, request, *args, **kwargs):
        all_items = Task.objects.all()
        context = {'all_tasks': all_items}
        return render(request, self.template_name, context)


class IncomeView(View):
    template_name = "app/income.html"

    def get(self, request, *args, **kwargs):
        all_items = Income.objects.all()
        context = {'all_incomes': all_items}
        return render(request, self.template_name, context)


class ExpenseView(View):
    template_name = "app/expense.html"

    def get(self, request, *args, **kwargs):
        all_items = Expense.objects.all()
        context = {'all_expenses': all_items}
        return render(request, self.template_name, context)


class RecurringIncomeView(View):
    template_name = "app/r_income.html"

    def get(self, request, *args, **kwargs):
        all_items = RecurringIncome.objects.all()
        context = {'all_incomes': all_items}
        return render(request, self.template_name, context)


class RecurringExpenseView(View):
    template_name = "app/r_expense.html"

    def get(self, request, *args, **kwargs):
        all_items = RecurringExpense.objects.all()
        context = {'all_expenses': all_items}
        return render(request, self.template_name, context)
