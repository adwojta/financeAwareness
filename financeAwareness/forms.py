from unittest import mock
from django import forms
from django.http import request

from financeAwareness.models.category import Category
from financeAwareness.models.account import Account
from financeAwareness.models.transaction import Transaction
from financeAwareness.models.transactionItem import TransactionItem
from financeAwareness.models.transfer import Transfer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class registerForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')


class TransactionForm(forms.ModelForm):
    def __init__(self,User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["account_id"] = forms.ModelChoiceField(queryset=Account.objects.filter(user_id=User))
        self.fields["date"] = forms.DateField(widget=forms.DateInput())

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control',})
            
        self.fields['is_income'].widget.attrs.update({'class': 'form-check-input',})
        

    class Meta:
        model = Transaction
        fields = ('name','account_id','value','description','date','is_income')
        


class TransactionItemForm(forms.ModelForm):
    def __init__(self,User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category_id"] = forms.ModelChoiceField(queryset=Category.objects.filter(user_id=User))
        self.fields["item_value"] = forms.FloatField(widget=forms.NumberInput(attrs={'onchange':'change_transaction_value()'}),initial=0)
        self.fields["is_planned"] = forms.ChoiceField(choices=((True,"Tak"),(False,"Nie")), widget=forms.Select(),required=True)

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })


    class Meta:       
        model = TransactionItem
        fields = ('item_name','category_id','item_value','is_planned')
        

class CategoryForm(forms.ModelForm):
    def __init__(self,User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Nazwa kategorii"
        #self.fields["master_category"] = forms.ModelChoiceField(queryset=Category.objects.filter(user_id=User,master_category=None),required=False)
        #self.fields["income"].label = "Kategoria nadrzędna"

    class Meta:
        model = Category
        exclude = ('user_id','income','master_category')

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name','is_cash')

class SavingGoalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["due_date"] = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Account
        fields = ('name','due_date','goal_value','is_active_saving_goal')

class TransferForm(forms.ModelForm):
    def __init__(self,User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"] = forms.DateField(widget=forms.SelectDateWidget())
        self.fields["from_account"] = forms.ModelChoiceField(queryset=Account.objects.filter(user_id=User))
        self.fields["to_account"] = forms.ModelChoiceField(queryset=Account.objects.filter(user_id=User))

    class Meta:
        model = Transfer
        fields = ('value','date','from_account','to_account')