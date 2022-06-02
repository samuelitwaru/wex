from dataclasses import fields
from rest_framework import serializers
from rest_framework.fields import JSONField, CharField, ListField, IntegerField
from .models import (
    AccountType, FiscalYear, SubAccount, AccountingSettings,
    AccountsJournals, DraftBudgetPlan, BudgetPlan)


class AccounTypeSerializer(serializers.ModelSerializer):
    additional_data = JSONField(required=False)
    class Meta:
        model = AccountType
        exclude = ["_additional_data"]

class SubAccountSerializer(serializers.ModelSerializer):
    account_type = AccounTypeSerializer(read_only=True, many=True)
    additional_data = JSONField(required=False)
    
    class Meta:
        model = SubAccount
        exclude = ["_additional_data"]

class FiscalYearSerializer(serializers.ModelSerializer):
    account_types = AccounTypeSerializer(many=True, read_only=True)
    class Meta:
        model = FiscalYear
        exclude = ["state"]


class AccountingSettingsSerializer(serializers.ModelSerializer):
    additional_data = JSONField()
    item = CharField()

    class Meta:
        model = AccountingSettings
        exclude = ["_additional_data"]

class AccountsJournalsSerializers(serializers.ModelSerializer):
    additional_data = JSONField()

    budgetitem  = IntegerField(write_only=True)
    class Meta:
        model = AccountsJournals
        exclude = ["_additional_data", "siblings", "item_id"]


class DraftBudgetPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = DraftBudgetPlan
        fields = "__all__"

class BudgetPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = BudgetPlan
        fields = "__all__"