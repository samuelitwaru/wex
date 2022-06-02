from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.db.models.expressions import RawSQL
from django.db.models import Count, Sum, Q
from django.db import transaction

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    AccountState, AccountingSettings, AccountsJournals, FiscalYear, AccountType,
    SubAccount, IncreaseState, DraftBudgetPlan, BudgetPlan)
from .serializers import (
    FiscalYearSerializer, DraftBudgetPlanSerializer, SubAccountSerializer, AccounTypeSerializer,
    AccountingSettingsSerializer, AccountsJournalsSerializers,
    DraftBudgetPlan, BudgetPlanSerializer)


class FiscalYearCreateListView(APIView):
    def get(self, request, id=None):
        if id:
            fiscal_year = get_object_or_404(FiscalYear, id=id)
            serializer = FiscalYearSerializer(fiscal_year)

            return Response(
                serializer.data)
        else:
            fiscal_years = FiscalYear.objects.all()
            serializer = FiscalYearSerializer(fiscal_years, many=True)

            return Response(serializer.data)

    def post(self, request):
        data = request.data

        serializer = FiscalYearSerializer(data=data)

        open_fiscal_year = FiscalYear.objects.filter(
            state=AccountState.choices[0][0]).first()

        if open_fiscal_year:
            return Response(
                data="Cannot create new fiscal year when there is an existing open fiscal year",
                status=status.HTTP_400_BAD_REQUEST)

        elif serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class CurrentFiscalYearView(APIView):
    def get(self, request):
        current_fiscal_year = FiscalYear.objects.filter(
            state=AccountState.choices[0][0]).all()

        if len(current_fiscal_year) == 1:
            serializer = FiscalYearSerializer(current_fiscal_year[0])

            return Response(serializer.data)
        elif len(current_fiscal_year) > 1:
            return Response(
                data="System error, Please contact the administrator",
                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                data="Current Fiscal year not set",
                status=status.HTTP_404_NOT_FOUND)


class StartupAccountsView(APIView):
    def post(self, request):
        """
        data structure \n
        {
            selling_products: {
                value: True,
                cash_sales: {
                    value: True
                },
                credit_sales: {
                    value: True
                },
                check_sales: {
                    value: True
                },
                other_cash_accounts: {
                    value: [
                        {
                            name: '',
                            additional_data: ''
                        }
                    ]
                }
            },
            making_payments: {
                value: True,
                cash_payments: {
                    value: True
                },
                credit_payments: {
                    value: True
                },
                check_payments: {
                    value: True
                },
                other_cash_accounts: {
                    value: [
                        {
                            name: '',
                            additional_data: {}
                        }
                    ]
                }
            },

        } 
        """
        accounts = {}
        # default revenue account

        current_fiscal_year = FiscalYear.objects.get(
            state=AccountState.choices[0][0])

        revenue_account_type = AccountType.objects.get(
            name__startswith="Revenue",
            state=AccountState.choices[0][0])
        asset_account_type = AccountType.objects.get(
            name__startswith="Assets",
            state=AccountState.choices[0][0])
        expense_account_type = AccountType.objects.get(
            name__startswith="Expenses",
            state=AccountState.choices[0][0])
        liabilities_account_type = AccountType.objects.get(
            name__startswith="Expenses",
            state=AccountState.choices[0][0])

        revenue_subaccount = SubAccount.objects.get(
            name__startswith="Revenue",
            state=AccountState.choices[0][0])

        if not revenue_account_type:
            revenue_account_type = AccountType.objects.create(
                name="Revenue",
                increase=IncreaseState.choices[1][0])
            current_fiscal_year.account_types.add(revenue_account_type)
            current_fiscal_year.save()

        if not revenue_subaccount:
            revenue_subaccount = SubAccount(name="Revenue Account")
            revenue_subaccount.account_type.add(revenue_account_type)
            revenue_subaccount.save()

        selling_products = accounts["selling_products"]
        if selling_products.value:
            if not asset_account_type:
                asset_account_type = AccountType.objects.create(
                    name="Assets",
                    increase=IncreaseState.choices[0][0])
                current_fiscal_year.account_types.add(asset_account_type)
                current_fiscal_year.save()
                asset_account_type.save()

            if not expense_account_type:
                expense_account_type = AccountType.objects.create(
                    name="Expenses",
                    increase=IncreaseState.choices[0][0])
                current_fiscal_year.account_types.add(expense_account_type)
                current_fiscal_year.save()
                expense_account_type.save()

            product_sales_subaccount = SubAccount.objects.get(
                name__startswith="Product Sales",
                state=AccountState.choices[0][0])
            if not product_sales_subaccount:
                product_sales_subaccount = SubAccount(
                    name="Product Sales Account")
                product_sales_subaccount.account_type.add(revenue_account_type)
                product_sales_subaccount.save()

            inventory_subaccount = SubAccount.objects.get(
                name__startswith="Inventory",
                state=AccountState.choices[0][0])
            if not inventory_subaccount:
                inventory_subaccount = SubAccount(name="Inventory Account")
                inventory_subaccount.account_type.add(asset_account_type)
                inventory_subaccount.save()

            cogs_subaccount = SubAccount.objects.get(
                name__startswith="Cost of Goods Sold",
                state=AccountState.choices[0][0])
            if not cogs_subaccount:
                cogs_subaccount = SubAccount(name="Cost of Goods Sold Account")
                cogs_subaccount.account_type.add(expense_account_type)
                cogs_subaccount.save()

            if selling_products.cash_sales.value:
                cash_subaccount = SubAccount.objects.get(
                    name__startswith="Cash",
                    state=AccountState.choices[0][0])
                if not cash_subaccount:
                    cash_subaccount = SubAccount(name="Cash Account")
                    cash_subaccount.account_type.add(asset_account_type)
                    cash_subaccount.save()

            if selling_products.credit_sales.value:
                credit_sales_subaccount = SubAccount.objects.get(
                    name__startswith="Accounts Receivable",
                    state=AccountState.choices[0][0])
                if not credit_sales_subaccount:
                    credit_sales_subaccount = SubAccount(
                        name="Inventory Account")
                    credit_sales_subaccount.account_type.add(
                        asset_account_type)
                    credit_sales_subaccount.save()

            if selling_products.check_sales.value:
                check_subaccount = SubAccount.objects.get(
                    name__startswith="Checking Account",
                    state=AccountState.choices[0][0])
                if not check_subaccount:
                    check_subaccount = SubAccount(name="Checking Account")
                    check_subaccount.account_type.add(asset_account_type)
                    check_subaccount.save()

            if selling_products.other_cash_accounts.value:
                for account in selling_products.other_cash_accounts.value:
                    cash_m_subaccount = SubAccount.objects.get(
                        name__startswith=account.name,
                        state=AccountState.choices[0][0])
                    if not cash_m_subaccount:
                        cash_m_subaccount = SubAccount(
                            name=account.name.capitalize(),
                            additional_data=account.additional_data)
                        cash_m_subaccount.account_type.add(asset_account_type)
                        cash_m_subaccount.save()

        making_payments = accounts["making_payments"]
        if making_payments.value:
            if not asset_account_type:
                asset_account_type = AccountType.objects.create(
                    name="Assets",
                    increase=IncreaseState.choices[0][0])
                current_fiscal_year.account_types.add(asset_account_type)
                current_fiscal_year.save()
                asset_account_type.save()

            if making_payments.credit_payments.value:
                if not liabilities_account_type:
                    liabilities_account_type = AccountType.objects.create(
                        name="Liabilities",
                        increase=IncreaseState.choices[1][0])
                    current_fiscal_year.account_types.add(
                        liabilities_account_type)
                    current_fiscal_year.save()
                    liabilities_account_type.save()
                credit_payments_subaccount = SubAccount.objects.get(
                    name__startswith="Accounts Payable",
                    state=AccountState.choices[0][0])
                if not credit_payments_subaccount:
                    credit_payments_subaccount = SubAccount(
                        name="Accounts Payable")
                    credit_payments_subaccount.account_type.add(
                        liabilities_account_type)
                    credit_payments_subaccount.save()

            if making_payments.cash_payments.value:
                cash_subaccount = SubAccount.objects.get(
                    name__startswith="Cash",
                    state=AccountState.choices[0][0])
                if not cash_subaccount:
                    cash_subaccount = SubAccount(name="Cash Account")
                    cash_subaccount.account_type.add(asset_account_type)
                    cash_subaccount.save()

            if making_payments.check_payments.value:
                check_subaccount = SubAccount.objects.get(
                    name__startswith="Checking Account",
                    state=AccountState.choices[0][0])
                if not check_subaccount:
                    check_subaccount = SubAccount(name="Checking Account")
                    check_subaccount.account_type.add(asset_account_type)
                    check_subaccount.save()

            if making_payments.other_cash_accounts.value:
                for account in selling_products.other_cash_accounts.value:
                    payment_m_subaccount = SubAccount.objects.get(
                        name__startswith=account.name,
                        state=AccountState.choices[0][0])
                    if not payment_m_subaccount:
                        payment_m_subaccount = SubAccount(
                            name=account.name.capitalize(),
                            additional_data=account.additional_data)
                        payment_m_subaccount.account_type.add(
                            asset_account_type)
                        payment_m_subaccount.save()

        return


class SubAccountsByIdsListView(APIView):
    def post(self, request):
        data = request.data

        accounts_ids = data.get("accounts_ids")

        accounts = []

        for id in accounts_ids:
            accounts.append(SubAccount.objects.get(id=id))

        serializer = SubAccountSerializer(accounts, many=True)

        return Response(serializer.data)


class SubAccountsListCreateView(APIView):
    def get(self, request):
        data = request.query_params
        id = data.get("id")
        name = data.get("name")

        if id:
            sub_account = get_object_or_404(SubAccount, id=id)

            serializer = SubAccountSerializer(sub_account)

        elif name:
            sub_account = get_object_or_404(
                SubAccount, name__contains=name, state=AccountState.choices[0][0])

            serializer = SubAccountSerializer(sub_account)
        else:
            sub_accounts = SubAccount.objects.filter(
                state=AccountState.choices[0][0]).all()

            serializer = SubAccountSerializer(sub_accounts, many=True)

        return Response(serializer.data)

    def post(self, request, id):
        data = request.data

        sub_account = data.get("sub_account")

        sub_accounts = data.get("sub_accounts")

        account_type = get_object_or_404(AccountType, id=id)

        if sub_accounts:
            for sub_account__ in sub_accounts:
                serializer = SubAccountSerializer(data=sub_account__)

                if serializer.is_valid():
                    sub_account = SubAccount.objects.create(**serializer.data)
                    sub_account.account_type.add(account_type)
                    sub_account.save()

                else:
                    return Response(
                        data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
            return Response(
                data="New accounts have been created successfully",
                status=status.HTTP_201_CREATED)

        elif sub_account:
            serializer = SubAccountSerializer(data=sub_account)

            if serializer.is_valid():
                sub_account = SubAccount.objects.create(**serializer.data)
                sub_account.account_type.add(account_type)
                sub_account.save()
                serializer = SubAccountSerializer(sub_account)

                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED)
            else:
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST)


class AccountTypesListCreateView(APIView):
    def get(self, request, id=None):
        if id:
            account_type = AccountType.objects.get(id=id)

            serializer = AccounTypeSerializer(account_type)

        else:
            account_types = AccountType.objects.filter(
                state=AccountState.choices[0][0]).all()

            serializer = AccounTypeSerializer(account_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        serializer = AccounTypeSerializer(data=data)

        if serializer.is_valid():
            account_type = serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class AccountingSettingsRetrieveCreateView(APIView):
    def get(self, request, item=None):
        if item:
            settings = get_object_or_404(AccountingSettings, item=item)

            serializer = AccountingSettingsSerializer(settings)
        else:
            settings = AccountingSettings.objects.all()
            serializer = AccountingSettingsSerializer(settings, many=True)

        return Response(data=serializer.data)

    def post(self, request):
        data = request.data["data"]

        serializer = AccountingSettingsSerializer(data=data, many=True)
        if serializer.is_valid():
            for setting in serializer.data:
                existing_setting = AccountingSettings.objects.filter(
                    item=setting["item"]).first()
                if existing_setting:
                    existing_setting.additional_data = setting["additional_data"]
                    existing_setting.save()
                else:
                    new_setting = AccountingSettings.objects.create(
                        item=setting["item"])
                    new_setting.additional_data = setting["additional_data"]
                    new_setting.save()

            serializer = AccountingSettingsSerializer(
                AccountingSettings.objects.all(), many=True)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class AccountsJounrnalsCreateListView(APIView):
    def get(self, request, id=None, entry_type=None):
        if id and entry_type:

            journal_entries = AccountsJournals.objects.filter(
                sub_account__id=id,
                entry_type=entry_type).all()

            serializer = AccountsJournalsSerializers(
                journal_entries, many=True)
            data = serializer.data

        elif id:
            sub_account = get_object_or_404(
                SubAccount,
                id=id)

            journal_entries = sub_account.accountsjournals_set.all()

            serializer = AccountsJournalsSerializers(
                journal_entries, many=True)
            data = serializer.data
        else:
            subaccounts = SubAccount.objects.filter(
                state=AccountState.choices[0][0]).all()
            data = []
            for subaccount in subaccounts:
                data.append(
                    {
                        "account": SubAccountSerializer(subaccount).data,
                        "journals": AccountsJournalsSerializers(
                            subaccount.accountsjournals_set.all(),
                            many=True).data})

        return Response(data)

    @transaction.atomic(durable=True)
    def post(self, request, id):
        data = request.data

        subaccount = get_object_or_404(SubAccount, id=id)

        serializer = AccountsJournalsSerializers(data=data)

        if serializer.is_valid():
            if subaccount.account_type.all()[0].increase == data["entry_type"]:
                amount = data["amount"]
            else:
                amount = 0 - data["amount"]
            
            new_entry = AccountsJournals.objects.create(
                date=data["date"],
                amount=amount,
                item_id=data["budgetitem"],
                entry_type=data["entry_type"],
                additional_data=data["additional_data"])

            new_entry.sub_account.add(subaccount)

            budget_settings = AccountingSettings.objects.get(
                item="ITEMS_SPECIFICATION")
            if budget_settings.additional_data and \
                    budget_settings.additional_data["use_budget_plan"] and \
                    budget_settings.additional_data["use_budget_plan"]["value"]:

                budget_item = get_object_or_404(
                    BudgetPlan, id=data["budgetitem"])

                budget_subaccount = get_object_or_404(
                    SubAccount,
                    name="Budget_Item_%s_%s" % (budget_item.identifier, budget_item.name))

                
                new_entry2 = AccountsJournals.objects.create(
                    amount=amount,
                    item_id=data["budgetitem"],
                    entry_type=budget_subaccount.account_type.all()[0].increase)

                new_entry2.sub_account.add(budget_subaccount)

                new_entry2.save()

            new_entry.save()

            return Response(
                data="Added entry successfully.",
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class BudgetPlanItemView(APIView):
    def get(self, request, id):
        budget_item = get_object_or_404(BudgetPlan, id=id)

        serializer = BudgetPlanSerializer(budget_item)

        return Response(serializer.data)

class BudgetPlanCreateListView(APIView):
    def get(self, request, id=None, collection="list"):
        """Returns budget plan using fiscal year id

        Args:
            request : Request information
            id (Int, optional): id for fiscal year to return fiscal year budget. Defaults to None.

        Returns:
            Response: Returns budget plan if id is specified or all budget plans list.
        """
        data = None
        if id:
            if collection == "list":
                fiscal_year = get_object_or_404(FiscalYear, id=id)

                budget_plan = fiscal_year.budgetplan_set.all()

                serializer = BudgetPlanSerializer(budget_plan, many=True)

                data = serializer.data
            elif collection == "category":
                categories = BudgetPlan.objects.filter(fiscalYear__id=id).values(
                    "category").annotate(Count("category")).all()
                data = []
                for item in categories:
                    category = item["category"]
                    data.append(
                        {
                            "category": category,
                            "items": BudgetPlanSerializer(
                                BudgetPlan.objects.filter(
                                    category=category).all(),
                                many=True).data})
        else:
            budget_plans = BudgetPlan.objects.all()

            serializer = BudgetPlanSerializer(budget_plans, many=True)
            data = serializer.data

        return Response(data)

    @transaction.atomic(durable=True)
    def post(self, request, id):
        data = request.data
        fiscal_year = get_object_or_404(FiscalYear, id=id)

        item = data.get("item")
        items = data.get("items")

        if item:
            serializer = BudgetPlanSerializer(data=item)
            if serializer.is_valid():
                new_budget_item = BudgetPlan.objects.create(**item)
                new_budget_item.fiscalYear.add(fiscal_year)
                # new_budget_item.save()

                account_type = AccountType.objects.filter(
                    name__contains=item["category"]).first()

                if not account_type:
                    return Response(
                        data="Failed to set account.",
                        status=status.HTTP_400_BAD_REQUEST)

                new_sub_account = SubAccount.objects.create(
                    name="Budget_Item_%s_%s" % (
                        new_budget_item.identifier,
                        new_budget_item.name),
                    opening_balance=0)
                new_sub_account.account_type.add(account_type)
                # new_sub_account.save()

                new_budget_item.save()

                new_sub_account.save()

                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED)
            else:
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
        elif items:
            serializer = BudgetPlanSerializer(data=items, many=True)
            if serializer.is_valid():
                for item in items:
                    new_budget_item = BudgetPlan.objects.create(**item)
                    new_budget_item.fiscalYear.add(fiscal_year)
                    # new_budget_item.save()

                    account_type = AccountType.objects.filter(
                        name__contains=item["category"]).first()

                    if not account_type:
                        return Response(
                            data="Failed to set account.",
                            status=status.HTTP_400_BAD_REQUEST)

                    new_sub_account = SubAccount.objects.create(
                        name="Budget_Item_%s_%s" % (
                            new_budget_item.identifier,
                            new_budget_item.name),
                        opening_balance=0)
                    new_sub_account.account_type.add(account_type)
                    # new_sub_account.save()

                    new_budget_item.save()

                    new_sub_account.save()

                return Response(
                    data="New budget item created succesfully",
                    status=status.HTTP_201_CREATED)
            else:
                # rollback()
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class BudgetPlanByCategoryListView(APIView):
    def get(self, request, id, category):
        items = BudgetPlan.objects.filter(
            fiscalYear__id=id, category__contains=category).all()
        serializer = BudgetPlanSerializer(items, many=True)
        return Response(serializer.data)


class DraftBudgetPlanCreateRetrieveView(APIView):
    def get(self, request):
        budget_plan = DraftBudgetPlan.objects.all()

        categories = DraftBudgetPlan.objects.values(
            "category").annotate(Count("category")).all()
        data = []
        for item in categories:
            category = item["category"]
            data.append(
                {
                    "category": category,
                    "items": DraftBudgetPlanSerializer(
                        DraftBudgetPlan.objects.filter(
                            category=category).all(),
                        many=True).data})

        return Response(data)

    def post(self, request):
        data = request.data

        # existing_budget_plan = DraftBudgetPlan.objects.first()
        # if existing_budget_plan:
        #     return Response(
        #         data="Cannot create new budget",
        #         status=status.HTTP_400_BAD_REQUEST)

        serializer = DraftBudgetPlanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        data = request.data

        serializer = DraftBudgetPlanSerializer(data=data)

        if serializer.is_valid():
            DraftBudgetPlan.objects.filter(id=id)\
                .update(**serializer.data)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class FinancialDocumentsView(APIView):
    def get(self, request, document):
        if document == "TRIAL_BALANCE":
            data = SubAccount.objects.annotate(
                balance= Sum("accountsjournals__amount"))\
                .values(
                    "name", 
                    "balance", 
                    account_type="account_type__name")

            return Response(data)

        if document == "INCOME_STATEMENT":
            # net income = (Revenue + Gains) - (Expenses + Losses)
            data = SubAccount.objects.annotate(
                balance= Sum("accountsjournals__amount"))\
                .values(
                    "name", 
                    "balance", 
                    account_type="account_type__name")\
                .filter(account_type__name__contains=["Revenue", "Expense"])
            
            return Response(data)
