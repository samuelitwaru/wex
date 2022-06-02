from django.contrib import admin
from django.urls import path, include

from .views import (
    FiscalYearCreateListView, SubAccountsListCreateView,
    AccountTypesListCreateView, AccountingSettingsRetrieveCreateView,
    AccountsJounrnalsCreateListView, BudgetPlanCreateListView,
    DraftBudgetPlanCreateRetrieveView, CurrentFiscalYearView,
    SubAccountsByIdsListView, BudgetPlanByCategoryListView,
    BudgetPlanItemView, FinancialDocumentsView)


urlpatterns = [
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("fiscal-year/", FiscalYearCreateListView.as_view(),
         name="fiscal_year_create_view"),
    path("fiscal-year/<int:id>", FiscalYearCreateListView.as_view(),
         name="fiscal_year_list_view"),
    path("fiscal-year/current/", CurrentFiscalYearView.as_view(),
         name="current_fiscal_year"),
    # path("accounts/<int:id>", SubAccountsListCreateView.as_view(), name="sub_accounts_create_view"),
    path("accounts/", SubAccountsListCreateView.as_view(),
         name="sub_accounts_list_view"),
    path("accounts/list/", SubAccountsByIdsListView.as_view(),
         name="sub_accounts_by_ids_list_view"),
    path("account-types/", AccountTypesListCreateView.as_view(),
         name="account_types_create_view"),
    path("account-types/<int:id>", AccountTypesListCreateView.as_view(),
         name="account_types_list_view"),
    path("settings/<str:item>", AccountingSettingsRetrieveCreateView.as_view(),
         name="account_settings_retrieve_view"),
    path("settings/", AccountingSettingsRetrieveCreateView.as_view(),
         name="account_settings_create_view"),
    path("journals/<int:id>", AccountsJounrnalsCreateListView.as_view(),
         name="accounts_journals_create_list_view"),
    path("journals/<int:id>/<str:entry_type>", AccountsJounrnalsCreateListView.as_view(),
         name="accounts_journals_by_entry_type_list_view"),
    path("journals/", AccountsJounrnalsCreateListView.as_view(),
         name="accounts_journals_list_view"),
    path("budget-plan/item/<int:id>", BudgetPlanItemView.as_view(),
         name="budget_plan_item_view"),
    path("budget-plan/", BudgetPlanCreateListView.as_view(),
         name="budget_plan_list_view"),
    path("budget-plan/<int:id>", BudgetPlanCreateListView.as_view(),
         name="budget_plan_create_list_view"),
    path("budget-plan/<int:id>/<str:collection>",
         BudgetPlanCreateListView.as_view(), name="budget_plan_list_view_by_category"),
    path("budget-plan/<int:id>/category/<str:category>",
         BudgetPlanByCategoryListView.as_view(), name="budget_plan_by_category_list_view"),
    path("budget-plan/draft/", DraftBudgetPlanCreateRetrieveView.as_view(),
         name="government_budget_plan_create_list_view"),
    path("financial-documents/", FinancialDocumentsView.as_view(), name="financial_documents_list_view")
]


# urlpatterns += router.urls