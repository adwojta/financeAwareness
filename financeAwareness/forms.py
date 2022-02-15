from datetime import datetime
from django import forms
from django.http import request

from financeAwareness.models.category import Category
from financeAwareness.models.account import Account
from financeAwareness.models.transaction import Transaction
from financeAwareness.models.transactionItem import TransactionItem
from financeAwareness.models.tag import Tag
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from dateutil.relativedelta import relativedelta

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class registerForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control form-control-sm',})      
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')


class TransactionForm(forms.ModelForm):
    def __init__(self,User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["account_id"] = forms.ModelChoiceField(queryset=Account.objects.filter(user_id=User,is_saving_goal=False))
        self.fields["date"] = forms.DateField(widget=forms.DateInput())
        self.fields['value'] = forms.FloatField(widget=forms.NumberInput(),initial=0)
        self.fields["tags"] = forms.ModelMultipleChoiceField(queryset=Tag.objects.filter(user_id=User) ,widget=forms.CheckboxSelectMultiple)
        self.fields["image"] = forms.ImageField(widget=forms.FileInput)

        #Labals
        self.fields["name"].label = "Nazwa transakcji"
        self.fields["account_id"].label = "Konto"
        self.fields["value"].label = "Wartość"
        self.fields["description"].label = "Opis"
        self.fields["date"].label = "Data transakcji"
        self.fields["image"].label = "Zdjęcie"

        self.fields["name"].widget.attrs.update({'class': 'form-control',}) 
        self.fields["account_id"].widget.attrs.update({'class': 'form-control',}) 
        self.fields["value"].widget.attrs.update({'class': 'form-control',}) 
        self.fields["description"].widget.attrs.update({'class': 'form-control',}) 
        self.fields["date"].widget.attrs.update({'class': 'form-control',})
        self.fields["image"].widget.attrs.update({'class': 'form-control',})    
        self.fields["tags"].required=False
        self.fields["image"].required=False

        self.fields['value'].widget.attrs['readonly'] = True

    class Meta:
        model = Transaction
        fields = ('name','account_id','value','description','date','tags','image')
        
class RecurringForm(forms.ModelForm):
    def __init__(self,User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["account_id"] = forms.ModelChoiceField(queryset=Account.objects.filter(user_id=User,is_saving_goal=False))
        self.fields["date"] = forms.DateField(widget=forms.DateInput())
        self.fields['value'] = forms.FloatField(widget=forms.NumberInput(),initial=0)
        self.fields["tags"] = forms.ModelMultipleChoiceField(queryset=Tag.objects.filter(user_id=User) ,widget=forms.CheckboxSelectMultiple)

        #Labals
        self.fields["name"].label = "Nazwa transakcji"
        self.fields["account_id"].label = "Konto"
        self.fields["value"].label = "Wartość"
        self.fields["description"].label = "Opis"
        self.fields["date"].label = "Data następnej transakcji"

        self.fields["name"].widget.attrs.update({'class': 'form-control',}) 
        self.fields["account_id"].widget.attrs.update({'class': 'form-control',}) 
        self.fields["value"].widget.attrs.update({'class': 'form-control',}) 
        self.fields["description"].widget.attrs.update({'class': 'form-control',}) 
        self.fields["date"].widget.attrs.update({'class': 'form-control',})
        self.fields["reccuring_type"].widget.attrs.update({'class': 'form-control',})
        self.fields["tags"].required=False     

        self.fields['value'].widget.attrs['readonly'] = True

    class Meta:
        model = Transaction
        fields = ('name','account_id','value','description','date','tags','reccuring_type')

class TransactionItemForm(forms.ModelForm):

    subcategory = forms.CharField(widget=forms.Select(choices=((-1,'Wybierz kategorie'),(-1,'brak'))),label="Nazwa podkategorii",required=False)

    def __init__(self,User,type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        income = None 
        if type == 'income':
            income = True
        elif type == 'expense':
            income = False
            
        if kwargs.get('instance'):
            category = kwargs['instance'].category_id
            
            if category.master_category:             
                self['subcategory'].initial = category
                self['subcategory'].field =forms.ModelChoiceField(
                    queryset=Category.objects.filter(user_id=User,master_category=category.master_category,income=income),initial=category,
                    widget=forms.Select(attrs={'class': 'form-control form-control-sm',}),required=False)
                
                category = category.master_category

            self.initial["category_id"] = category


            self.fields["category_id"] = forms.ModelChoiceField(
                queryset=Category.objects.filter(user_id=User,master_category=None,income=income),initial=category,
                widget=forms.Select(attrs={'onclick':'getSubcategories(this)',}))
            
        else:
            self.fields["category_id"] = forms.ModelChoiceField(
                queryset=Category.objects.filter(user_id=User,master_category=None,income=income),
                widget=forms.Select(attrs={'onclick':'getSubcategories(this)'}))
        
        self.fields["item_value"] = forms.FloatField(widget=forms.NumberInput(attrs={'onchange':'change_transaction_value()'}),initial=0,min_value=0)
        self.fields["is_planned"] = forms.ChoiceField(choices=((True,"Tak"),(False,"Nie")), widget=forms.Select(),required=True)
        self.fields["item_value"] = forms.FloatField(widget=forms.NumberInput(attrs={'onchange':'change_transaction_value()'}),initial=0,min_value=0)
        self.fields["is_planned"] = forms.ChoiceField(choices=((True,"Tak"),(False,"Nie")), widget=forms.Select(),required=True)

        #Labals
        self.fields["item_name"].label = "Nazwa produktu"
        self.fields["category_id"].label = "Nazwa kategorii"
        self.fields["item_value"].label = "Wartość"
        self.fields["is_planned"].label = "Planowany?"


        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control form-control-sm',})

    class Meta:       
        model = TransactionItem
        fields = ('item_name','category_id','item_value','is_planned')    

class CategoryForm(forms.ModelForm):
    def __init__(self,User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Nazwa kategorii"

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control',})   

    class Meta:
        model = Category
        exclude = ('user_id','income','master_category')

class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Labals
        self.fields["name"].label = "Nazwa konta"
        self.fields["is_cash"].label = "Gotówka?"

        self.fields['name'].widget.attrs.update({'class': 'form-control',})
        self.fields["is_cash"].widget.attrs.update({'class': 'form-check-input',})    

    class Meta:
        model = Account
        fields = ('name','is_cash')

class SavingGoalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["due_date"] = forms.DateField(widget=forms.SelectDateWidget())

        #Labals
        self.fields["name"].label = "Nazwa celu"
        self.fields["due_date"].label = "Planowany termin realizacji celu"
        self.fields["goal_value"].label = "Kwota do osiągnięcia"
        self.fields["is_active_saving_goal"].label = "Aktywny cel?"

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control',})

        self.fields["is_active_saving_goal"].widget.attrs.update({'class': 'form-check-input',})     

    class Meta:
        model = Account
        fields = ('name','due_date','goal_value','is_active_saving_goal')


class TransferForm(forms.ModelForm):
    def __init__(self,User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"] = forms.DateField(widget=forms.DateInput())
        self.fields["account_id"] = forms.ModelChoiceField(queryset=Account.objects.filter(user_id=User))
        self.fields["transfer_account"] = forms.ModelChoiceField(queryset=Account.objects.filter(user_id=User))

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class': 'form-control',})

        self.fields["date"].label = "Wartość"
        self.fields["date"].label = "Data"
        self.fields["account_id"].label = "Konto"
        self.fields["transfer_account"].label = "Konto docelowe"

    class Meta:
        model = Transaction
        fields = ('value','date','account_id','transfer_account')


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField()
        self.fields['name'].widget.attrs.update({'class': 'form-control',})

    class Meta:
        model = Tag
        fields = ('name',)

class SearchForm(forms.Form):
    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'] = forms.ModelMultipleChoiceField(queryset=Tag.objects.filter(user_id=user) ,widget=forms.CheckboxSelectMultiple,required=False)
        
    choices =((True,'Przychód'),(False,'Wydatek'),(None,'-------'))
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    search = forms.CharField(required=False)
    transaction_type = forms.ChoiceField(choices=choices,initial=None,required=False)
    planned = forms.ChoiceField(choices=((True,"Tak"),(False,"Nie"),(None,"-------")), widget=forms.Select(),required=False,initial=None)
    tags = forms.ModelMultipleChoiceField(queryset=None)

    date_from.label = 'Od'
    date_to.label = 'Do'
    search.label = 'Szukaj słowa'
    transaction_type.label = 'Typ'
    planned.label = 'Zaplanowana'
    date_from.widget.attrs.update({'class': 'form-control',})
    date_to.widget.attrs.update({'class': 'form-control',})
    search.widget.attrs.update({'class': 'form-control',})
    transaction_type.widget.attrs.update({'class': 'form-control','onchange':'SearchCategories(this)'})
    planned.widget.attrs.update({'class': 'form-control',})

class DateForm(forms.Form):

    def __init__(self,user=None,date_from=(datetime.now()+relativedelta(day=1)),date_to=(datetime.now()+relativedelta(months=1, day=1, days=-1)), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_from'] = forms.DateField(initial=date_from)
        self.fields['date_to'] = forms.DateField(initial=date_to)
        self.fields['date_from'].label = 'Od'
        self.fields['date_to'].label = 'Do'
        if user:
            self.fields["category_expense"] = forms.ModelChoiceField(queryset=Category.objects.filter(user_id=user,master_category=None, income=False))
            self.fields["category_income"] = forms.ModelChoiceField(queryset=Category.objects.filter(user_id=user,master_category=None, income=True) )
            self.fields["category_expense"].required = False
            self.fields["category_income"].required = False
            self.fields["category_expense"].label = 'Kategoria wydatki'
            self.fields["category_income"].label = 'Kategoria przychody'
            self.fields["category_expense"].widget.attrs.update({'class': 'form-control',})
            self.fields["category_income"].widget.attrs.update({'class': 'form-control',})

    date_from = forms.DateField()
    date_to = forms.DateField()
    category_expense = forms.Select()
    category_income = forms.Select()

    date_from.widget.attrs.update({'class': 'form-control',})
    date_to.widget.attrs.update({'class': 'form-control',})