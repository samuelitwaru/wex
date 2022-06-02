import json

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.


class IncreaseState(models.TextChoices):
    """
        `0` represents DEBIT. \n
        `1` represents CREDIT.
    """
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class AccountState(models.TextChoices):
    """
        `0` represents OPEN. \n
        `1` represents CLOSED.
    """
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class JournalEntryType(models.IntegerChoices):
    PRODUCT_SALE = 1
    ASSET_SALE = 2
    PURCHASE = 3
    PAYMENT = 4
    EXPENSE = 5


class PayeeType(models.IntegerField):
    SUPPLIER = 1
    EMPLOYEE = 2
    OTHER = 3


class Company(models.Model):
    name = models.TextField()
    description = models.TextField()
    address = models.TextField()
    contacts = models.TextField()
    _additional_data = models.TextField(blank=True)

    @property
    def additional_data(self):
        return json.loads(self._additional_data) if self._additional_data or len(self._additional_data) > 0 else {}

    @additional_data.setter
    def additional_data(self, kwargs):
        self._additional_data = json.dumps(kwargs)


class FiscalYear(models.Model):

    start = models.DateField(db_index=True, unique=True, null=False)
    end = models.DateField(db_index=True, unique=True, null=False)
    state = models.TextField(choices=AccountState.choices,
                             default=AccountState.choices[0][0])

    account_types = models.ManyToManyField(
        "AccountType",
        through="FiscalYearAccountType",
        through_fields=("fiscal_year", "account_type"))

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except ValidationError as e:
            return e.message

    # def clean(self) -> None:
    #     try:
    #         latest = FiscalYear.objects.latest("start", "end")
    #     except:
    #         latest = FiscalYear.objects.last()

    #     if latest and (self.end < latest.end or self.start < latest.start):
    #         raise ValidationError({"start and end dates": _(
    #             "Start and End dates are not correct please erectify")})
    # class Meta:
    #     verbose_name = _("FiscalYear")
    #     verbose_name_plural = _("FiscalYears")

class DraftBudgetPlan(models.Model):
    category = models.TextField()
    identifier = models.TextField(unique=True, db_index=True)
    name = models.TextField(db_index=True)
    amount = models.IntegerField()
    _additional_data = models.TextField(blank=True)

    @property
    def additional_data(self):
        return json.loads(self._additional_data) if self._additional_data or len(self._additional_data) > 0 else {}

    @additional_data.setter
    def additional_data(self, kwargs):
        self._additional_data = json.dumps(kwargs)

class BudgetPlan(models.Model):
    category = models.TextField()
    identifier = models.TextField(unique=True, db_index=True)
    name = models.TextField(db_index=True)
    amount = models.IntegerField()
    _additional_data = models.TextField(blank=True)

    fiscalYear = models.ManyToManyField(
        "FiscalYear", 
        through="FiscalYearBudgetPlan",
        through_fields=("budget_plan","fiscal_year"))

    @property
    def additional_data(self):
        return json.loads(self._additional_data) if self._additional_data or len(self._additional_data) > 0 else {}

    @additional_data.setter
    def additional_data(self, kwargs):
        self._additional_data = json.dumps(kwargs)

class AccountingSettings(models.Model):
    item = models.TextField(unique=True)

    _additional_data = models.TextField(blank=True)

    @property
    def additional_data(self):
        return json.loads(self._additional_data) if self._additional_data or len(self._additional_data) > 0 else {}

    @additional_data.setter
    def additional_data(self, kwargs):
        data = self.additional_data
        data.update(kwargs)
        self._additional_data = json.dumps(data)
        

class AccountType(models.Model):

    name = models.TextField(db_index=True, unique=True)
    increase = models.TextField(choices=IncreaseState.choices)
    _additional_data = models.TextField(blank=True)
    state = models.TextField(choices=AccountState.choices,
                             default=AccountState.choices[0][0])
    date = models.DateTimeField(default=timezone.now)

    @property
    def additional_data(self):
        return json.loads(self._additional_data) if self._additional_data or len(self._additional_data) > 0 else {}

    @additional_data.setter
    def additional_data(self, kwargs):
        self._additional_data = json.dumps(kwargs)


class SubAccount(models.Model):
    name = models.TextField(db_index=True, unique=True)
    opening_balance = models.BigIntegerField()
    closing_balance = models.BigIntegerField(blank=True, null=True)
    state = models.TextField(choices=AccountState.choices,
                             default=AccountState.choices[0][0])
    date = models.DateTimeField(default=timezone.now)
    _additional_data = models.TextField(blank=True)

    account_type = models.ManyToManyField(
        AccountType,
        through="AccountTypeSubAccount",
        through_fields=("sub_account", "account_type"))

    @property
    def additional_data(self):
        return json.loads(self._additional_data) if self._additional_data or len(self._additional_data) > 0 else {}

    @additional_data.setter
    def additional_data(self, kwargs):
        data = self._additional_data
        data.update(kwargs)
        self._additional_data = json.dumps(data)


class AccountsJournals(models.Model):

    date = models.DateTimeField(db_index=True, default=timezone.now)
    amount = models.BigIntegerField()
    item_id = models.TextField()
    entry_type = models.TextField(choices=IncreaseState.choices)

    _additional_data = models.TextField()

    sub_account = models.ManyToManyField(
        SubAccount,
        through="SubAccountAccountsJournal",
        through_fields=("accounts_journal","sub_account"))

    siblings = models.ManyToManyField("self")

    @property
    def item_name(self):
        item_name_settings = AccountingSettings.objects.get(item="item_id")
        if item_name_settings:
            if item_name_settings.additional_data["use_budget_plan"]:
                item = BudgetPlan.objects.get(identifier = self.item_id)
                if item:
                    return item.category
        return ""

    @property
    def additional_data(self):
        return json.loads(self._additional_data) if self._additional_data or len(self._additional_data) > 0 else {}

    @additional_data.setter
    def additional_data(self, kwargs):
        data = self.additional_data
        data.update(kwargs)
        self._additional_data = json.dumps(data)

    def set_additional_data(self, columns):
        for column in columns:
            setattr(self, "__"+column, self.additional_data.get(column))


# class ExpensesJournal(models.Model):

#     date = models.DateTimeField(db_index=True, default=timezone.now())
#     payee_id = models.IntegerField()
#     payee_type = models.IntegerField(choices=PayeeType.choices, db_index=True)
#     amount = models.BigIntegerField()
#     subtotal = models.BigIntegerField()

#     _additional_data = models.TextField()

#     sub_account = models.ManyToManyField(
#         SubAccount,
#         through="SubAccountExpensesJournal",
#         through_fields=("sub_account", "expenses_journal"))

#     @property
#    def additional_data(self):
#        return json.loads(self._additional_data) if self._additional_data or len(self._additional_data) > 0 else {}
#
#    @additional_data.setter
#    def additional_data(self, kwargs):
#        self._additional_data = json.dumps(kwargs)


# relationships

class FiscalYearAccountType(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear, db_index=True, null=True, on_delete=models.SET_NULL)
    account_type = models.ForeignKey(AccountType, db_index=True, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now)


class AccountTypeSubAccount(models.Model):
    account_type = models.ForeignKey(AccountType, db_index=True, null=True, on_delete=models.SET_NULL)
    sub_account = models.ForeignKey(SubAccount, db_index=True, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now)


# class SubAccountExpensesJournal(models.Model):
#     sub_account = models.ForeignKey(SubAccount, db_index=True)
#     expenses_journal = models.ForeignKey(ExpensesJournal, db_index=True)
#     date = models.DateTimeField(default=timezone.now())


class SubAccountAccountsJournal(models.Model):
    sub_account = models.ForeignKey(SubAccount, db_index=True, null=True, on_delete=models.SET_NULL)
    accounts_journal = models.ForeignKey(AccountsJournals, db_index=True, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now)

class FiscalYearBudgetPlan(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear, db_index=True, null=True, on_delete=models.SET_NULL)
    budget_plan = models.ForeignKey(BudgetPlan, db_index=True, null=True, on_delete=models.SET_NULL)