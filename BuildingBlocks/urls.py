from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import MonthlyRentsView, DebtsView, ShoppingView, MainView, TenantsView, CardsView
from .views import AssetsView, TasksView, IncomeView, ExpenseView, RecurringExpenseView, RecurringIncomeView

urlpatterns = [
    #path('accounts/', include('django.contrib.auth.urls')),
    path('', MainView.as_view(), name='home'),
    path('shopping/', ShoppingView.as_view(), name='shopping_default'),
    path('shopping/<int:shopping_id>', ShoppingView.as_view(), name='shopping'),
    path('shopping/delete/<int:delete_id>', ShoppingView.as_view(), name='delete_shopping'),
    path('debts/', DebtsView.as_view(), name='debts'),
    path('assets/', AssetsView.as_view(), name='assets'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('rental_payments/', MonthlyRentsView.as_view(), name='rental_monthly_payments'),
    path('rental_payments/<int:rent_id>', MonthlyRentsView.as_view(), name='rental_payments_mark'),
    path('tenants/', TenantsView.as_view(), name='tenants'),
    path('cards/', CardsView.as_view(), name='cards'),
    path('income/', IncomeView.as_view(), name='income'),
    path('expenses/', ExpenseView.as_view(), name='expenses'),
    path('r_income/', RecurringIncomeView.as_view(), name='r_income'),
    path('r_expenses/', RecurringExpenseView.as_view(), name='r_expenses'),
]
