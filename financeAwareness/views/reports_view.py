import calendar,locale
from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum
from financeAwareness.models.category import Category
from financeAwareness.models.tag import Tag
from financeAwareness.models.transaction import Transaction
from financeAwareness.models.transactionItem import TransactionItem
from financeAwareness.forms import DateForm
from django.contrib.auth.decorators import login_required

@login_required
def reports_list(request):
    locale.setlocale(locale.LC_ALL,'pl_PL')
    month = datetime.now().month    
    year = datetime.now().year

    #Expense/income
    labels =['Wydatek','Przychód']
    expense = Transaction.objects.filter(user=request.user,type='expense',date__month=month).aggregate(Sum('value'))['value__sum']
    income = Transaction.objects.filter(user=request.user,type='income',date__month=month).aggregate(Sum('value'))['value__sum']    
    if expense == None:
        expense = 0
    if income == None:
        income = 0
    data_exp_in = [int(expense),int(income)]

    #Recurring expense/income
    labels_r =['Wydatek','Przychód']
    r_expense = Transaction.objects.filter(user=request.user,type='recurringExpense',date__month=month).aggregate(Sum('value'))['value__sum']
    r_income = Transaction.objects.filter(user=request.user,type='recurringIncome',date__month=month).aggregate(Sum('value'))['value__sum']
    if r_expense == None:
        r_expense = 0
    if r_income == None:
        r_income = 0    
    data_r_exp_in = [int(r_expense),int(r_income)]

    #Category expense
    labels_c_e =[]
    data_c_e = []
    categories = Category.objects.filter(user=request.user,master_category=None)
    transactions = Transaction.objects.filter(user=request.user,type='expense',date__month=month)
    for category in categories:
        subcategories = Category.objects.filter(user=request.user,master_category=category)
        if subcategories:
            category_value = 0
            for subcategory in subcategories:
                value = TransactionItem.objects.filter(transaction__in=transactions,category=subcategory).aggregate(Sum('item_value'))['item_value__sum']
                if value == None:
                    continue
                else:
                    category_value +=int(value)
            if category_value > 0:
                data_c_e.append(category_value)
                labels_c_e.append(category.name)
        else:
            value = TransactionItem.objects.filter(transaction__in=transactions,category=category).aggregate(Sum('item_value'))['item_value__sum']
            if value:
                if value > 0:
                    data_c_e.append(value)
                    labels_c_e.append(category.name)

    #Planned
    labels_planned =['Zaplanowane','Nieplanowane']
    data_planned = []
    value = TransactionItem.objects.filter(transaction__in=transactions,is_planned=True).aggregate(Sum('item_value'))['item_value__sum']
    if value == None:
        value = 0
    data_planned.append(int(value))

    value = TransactionItem.objects.filter(transaction__in=transactions,is_planned=False).aggregate(Sum('item_value'))['item_value__sum']
    if value == None:
        value = 0
    data_planned.append(int(value))

    #Tags
    labels_tags =[]
    data_tags = []

    tags = Tag.objects.filter(user=request.user)
    if tags != None:
        for tag in tags:
            value = Transaction.objects.filter(tags=tag,date__month=month,type='expense').aggregate(Sum('value'))['value__sum']
            if value == None:
                value = 0
            else:
                labels_tags.append(tag.name)
                data_tags.append(int(value))

    month = calendar.month_name[month]
    return render(request, 'views/report/reports.html',
    {'year':year,'month':month,
    'labels':labels,'data_exp_in':data_exp_in,
    'labels_r':labels_r,'data_r_exp_in':data_r_exp_in,
    'labels_c_e':labels_c_e,'data_c_e':data_c_e,
    'labels_planned':labels_planned,'data_planned':data_planned,
    'labels_tags':labels_tags,'data_tags':data_tags})

@login_required
def expense_income_details_report(request):
    labels =[]
    data =[]
    if request.GET:
        date_form = DateForm(data=request.GET)
        date_from = datetime.strptime(request.GET['date_from'],'%d.%m.%Y') 
        date_to =  datetime.strptime(request.GET['date_to'],'%d.%m.%Y')
        labels =['Wydatek','Przychód']
        expense = Transaction.objects.filter(user=request.user,type='expense',date__range=[date_from,date_to]).aggregate(Sum('value'))['value__sum']
        income = Transaction.objects.filter(user=request.user,type='income',date__range=[date_from,date_to]).aggregate(Sum('value'))['value__sum']    
        if expense == None:
            expense = 0
        if income == None:
            income = 0
        data = [int(expense),int(income)]

    else:        
        month = datetime.now().month
        date_form = DateForm()
        labels =['Wydatek','Przychód']
        expense = Transaction.objects.filter(user=request.user,type='expense',date__month=month).aggregate(Sum('value'))['value__sum']
        income = Transaction.objects.filter(user=request.user,type='income',date__month=month).aggregate(Sum('value'))['value__sum']    
        if expense == None:
            expense = 0
        if income == None:
            income = 0
        data = [int(expense),int(income)]
    return render(request, 'views/report/report_expense_income.html',{'date_form':date_form,'labels':labels,'data':data})

@login_required
def category_details_report(request):
    labels =[]
    data =[]
    labels_subcategories =[]
    data_subcategories =[]
    labels_income =[]
    data_income =[]
    labels_income_subcategories =[]
    data_income_subcategories =[]
    most_value_category = ''

    if request.GET:
        date_form = DateForm(data=request.GET,user = request.user)
        date_from = datetime.strptime(request.GET['date_from'],'%d.%m.%Y') 
        date_to =  datetime.strptime(request.GET['date_to'],'%d.%m.%Y')
        category_expense = request.GET['category_expense']
        category_income = request.GET['category_income']
        categories = Category.objects.filter(user=request.user,master_category=None)
        transactions = Transaction.objects.filter(user=request.user,type='expense',date__range=[date_from,date_to])
        for category in categories:
            subcategories = Category.objects.filter(user=request.user,master_category=category)
            category_value = TransactionItem.objects.filter(transaction__in=transactions,category=category).aggregate(Sum('item_value'))['item_value__sum']
            if category_value:
                category_value = int(category_value)
            else:
                category_value = 0
                
            for subcategory in subcategories:
                value = TransactionItem.objects.filter(transaction__in=transactions,category=subcategory).aggregate(Sum('item_value'))['item_value__sum']
                if value == None:
                    continue
                else:
                    category_value +=int(value)
            if category_value > 0:
                data.append(category_value)
                labels.append(category.name)    
        
        if category_expense =="":
            if data:
                most_value_category = Category.objects.get(user=request.user,name=labels[0],master_category=None)
                min_value = min(data)
                for i,category in enumerate(data):
                    if min_value < category:
                        min_value = category
                        most_value_category = Category.objects.get(user=request.user,name=labels[i])
            category_expense = most_value_category

        if category_expense !="":
            subcategories = Category.objects.filter(user=request.user,master_category=category_expense)
            for subcategory in subcategories:
                value = TransactionItem.objects.filter(transaction__in=transactions,category=subcategory).aggregate(Sum('item_value'))['item_value__sum']
                if value == None:
                    continue
                else:
                    if value > 0:
                        data_subcategories.append(int(value))
                        labels_subcategories.append(subcategory.name)

        transactions = Transaction.objects.filter(user=request.user,type='income',date__range=[date_from,date_to])
        for category in categories:
            subcategories = Category.objects.filter(user=request.user,master_category=category)
            category_value = TransactionItem.objects.filter(transaction__in=transactions,category=category).aggregate(Sum('item_value'))['item_value__sum']
            if category_value:
                category_value = int(category_value)
            else:
                category_value = 0
            for subcategory in subcategories:
                value = TransactionItem.objects.filter(transaction__in=transactions,category=subcategory).aggregate(Sum('item_value'))['item_value__sum']
                if value == None:
                    continue
                else:
                    category_value +=int(value)
            if category_value > 0:
                data_income.append(category_value)
                labels_income.append(category.name)
        
        most_value_category =""
        if category_income =="":
            if data_income:
                most_value_category = Category.objects.get(user=request.user,name=labels_income[0],master_category=None)
                min_value = min(data_income)
                for i,category in enumerate(data):
                    if min_value < category:
                        min_value = category
                        most_value_category = Category.objects.get(user=request.user,name=labels_income[i])
                category_income = most_value_category

        if category_income !="":
            subcategories = Category.objects.filter(user=request.user,master_category=category_income)
            for subcategory in subcategories:
                value = TransactionItem.objects.filter(transaction__in=transactions,category=subcategory).aggregate(Sum('item_value'))['item_value__sum']
                if value == None:
                    continue
                else:
                    if value > 0:
                        data_income_subcategories.append(int(value))
                        labels_income_subcategories.append(subcategory.name)

    else:        
        month = datetime.now().month
        date_form = DateForm(user = request.user)
        categories = Category.objects.filter(user=request.user,master_category=None)
        transactions = Transaction.objects.filter(user=request.user,type='expense',date__month=month)
        for category in categories:
            subcategories = Category.objects.filter(user=request.user,master_category=category)
            category_value = TransactionItem.objects.filter(transaction__in=transactions,category=category).aggregate(Sum('item_value'))['item_value__sum']
            if category_value:
                category_value = int(category_value)
            else:
                category_value = 0
            for subcategory in subcategories:
                value = TransactionItem.objects.filter(transaction__in=transactions,category=subcategory).aggregate(Sum('item_value'))['item_value__sum']
                if value == None:
                    continue
                else:
                    category_value +=int(value)
            if category_value > 0:
                data.append(category_value)
                labels.append(category.name)

            if data:
                most_value_category = Category.objects.get(user=request.user,name=labels[0],master_category=None)
                min_value = min(data)
                for i,category in enumerate(data):
                    if min_value < category:
                        min_value = category
                        most_value_category = Category.objects.get(user=request.user,name=labels[i])

        if most_value_category:
            subcategories = Category.objects.filter(user=request.user,master_category=most_value_category)
            for subcategory in subcategories:
                value = TransactionItem.objects.filter(transaction__in=transactions,category=subcategory).aggregate(Sum('item_value'))['item_value__sum']
                if value == None:
                    continue
                else:
                    if value > 0:
                        data_subcategories.append(int(value))
                        labels_subcategories.append(subcategory.name)

        transactions = Transaction.objects.filter(user=request.user,type='income',date__month=month)
        for category in categories:
            subcategories = Category.objects.filter(user=request.user,master_category=category)
            category_value = TransactionItem.objects.filter(transaction__in=transactions,category=category).aggregate(Sum('item_value'))['item_value__sum']
            if category_value:
                category_value = int(category_value)
            else:
                category_value = 0
            for subcategory in subcategories:
                value = TransactionItem.objects.filter(transaction__in=transactions,category=subcategory).aggregate(Sum('item_value'))['item_value__sum']
                if value == None:
                    continue
                else:
                    category_value +=int(value)
            if category_value > 0:
                data_income.append(category_value)
                labels_income.append(category.name)

        most_value_category = ''
        if data_income:
            most_value_category = Category.objects.get(user=request.user,name=labels_income[0],master_category=None)
            min_value = min(data_income)
            for i,category in enumerate(data):
                if min_value < category:
                    min_value = category
                    most_value_category = Category.objects.get(user=request.user,name=labels_income[i])
        
        if most_value_category:
            subcategories = Category.objects.filter(user=request.user,master_category=most_value_category)
            for subcategory in subcategories:
                value = TransactionItem.objects.filter(transaction__in=transactions,category=subcategory).aggregate(Sum('item_value'))['item_value__sum']
                if value == None:
                    continue
                else:
                    if value > 0:
                        data_income_subcategories.append(int(value))
                        labels_income_subcategories.append(subcategory.name)

    return render(request, 'views/report/report_category.html',
    {'date_form':date_form,
    'labels':labels,'data':data,
    'labels_subcategories':labels_subcategories,'data_subcategories':data_subcategories,
    'labels_income':labels_income,'data_income':data_income,
    'labels_income_subcategories':labels_income_subcategories,'data_income_subcategories':data_income_subcategories})

@login_required
def tags_details_report(request):
    labels =[]
    data =[]
    if request.GET:
        date_form = DateForm(data=request.GET)
        date_from = datetime.strptime(request.GET['date_from'],'%d.%m.%Y') 
        date_to =  datetime.strptime(request.GET['date_to'],'%d.%m.%Y')
        tags = Tag.objects.filter(user=request.user)
        if tags != None:
            for tag in tags:
                value = Transaction.objects.filter(tags=tag,date__range=[date_from,date_to],type='expense').aggregate(Sum('value'))['value__sum']
                if value == None:
                    value = 0
                else:
                    labels.append(tag.name)
                    data.append(int(value))

    else:        
        month = datetime.now().month
        date_form = DateForm()

        tags = Tag.objects.filter(user=request.user)
        if tags != None:
            for tag in tags:
                value = Transaction.objects.filter(tags=tag,date__month=month,type='expense').aggregate(Sum('value'))['value__sum']
                if value == None:
                    value = 0
                else:
                    labels.append(tag.name)
                    data.append(int(value))

    return render(request, 'views/report/report_tag.html',{'date_form':date_form,'labels':labels,'data':data})

@login_required
def planned_details_report(request):
    labels =[]
    data =[]
    if request.GET:
        date_form = DateForm(data=request.GET)
        date_from = datetime.strptime(request.GET['date_from'],'%d.%m.%Y') 
        date_to =  datetime.strptime(request.GET['date_to'],'%d.%m.%Y')
        transactions = Transaction.objects.filter(user=request.user,type='expense',date__range=[date_from,date_to])
        labels =['Zaplanowane','Nieplanowane']
        value = TransactionItem.objects.filter(transaction__in=transactions,is_planned=True).aggregate(Sum('item_value'))['item_value__sum']
        if value == None:
            value = 0
        data.append(int(value))

        value = TransactionItem.objects.filter(transaction__in=transactions,is_planned=False).aggregate(Sum('item_value'))['item_value__sum']
        if value == None:
            value = 0
        data.append(int(value))

    else:        
        month = datetime.now().month
        transactions = Transaction.objects.filter(user=request.user,type='expense',date__month=month)
        date_form = DateForm()
        labels =['Zaplanowane','Nieplanowane']
        value = TransactionItem.objects.filter(transaction__in=transactions,is_planned=True).aggregate(Sum('item_value'))['item_value__sum']
        if value == None:
            value = 0
        data.append(int(value))

        value = TransactionItem.objects.filter(transaction__in=transactions,is_planned=False).aggregate(Sum('item_value'))['item_value__sum']
        if value == None:
            value = 0
        data.append(int(value))

    return render(request, 'views/report/report_planned.html',{'date_form':date_form,'labels':labels,'data':data})

@login_required
def recurring_details_report(request):
    
    labels=[]
    labels_month=[]
    labels_week=[]
    labels_quarter=[]
    labels_year=[]
    data =[]
    data_month=[]
    data_week=[]
    data_quarter=[]
    data_year=[]
    month = datetime.now().month
    if request.GET:
        date_from = datetime.strptime(request.GET['date_from'],'%d.%m.%Y') 
        date_to =  datetime.strptime(request.GET['date_to'],'%d.%m.%Y')
        date_form = DateForm(data=request.GET)
        expense = Transaction.objects.filter(user=request.user,type='recurringExpense',date__range=[date_from,date_to]).aggregate(Sum('value'))['value__sum']
        income = Transaction.objects.filter(user=request.user,type='recurringIncome',date__range=[date_from,date_to]).aggregate(Sum('value'))['value__sum']    
        if expense != None:
            labels.append('Wydatek')
            data.append(int(expense))
        if income != None:
            labels.append('Przychód')
            data.append(int(income))  

    else:               
        date_form = DateForm()
        expense = Transaction.objects.filter(user=request.user,type='recurringExpense',date__month=month).aggregate(Sum('value'))['value__sum']
        income = Transaction.objects.filter(user=request.user,type='recurringIncome',date__month=month).aggregate(Sum('value'))['value__sum']    
        if expense != None:
            labels.append('Wydatek')
            data.append(int(expense))
        if income != None:
            labels.append('Przychód')
            data.append(int(income))    

    expense = Transaction.objects.filter(user=request.user,type='recurringExpense', recurring_type='week').aggregate(Sum('value'))['value__sum']
    income = Transaction.objects.filter(user=request.user,type='recurringIncome', recurring_type='week').aggregate(Sum('value'))['value__sum']    
    if expense != None:
        labels_week.append('Wydatek')
        data_week.append(int(expense))
    if income != None:
        labels_week.append('Przychód')
        data_week.append(int(income)) 

    expense = Transaction.objects.filter(user=request.user,type='recurringExpense', recurring_type='quarter').aggregate(Sum('value'))['value__sum']
    income = Transaction.objects.filter(user=request.user,type='recurringIncome', recurring_type='quarter').aggregate(Sum('value'))['value__sum']    
    if expense != None:
        labels_quarter.append('Wydatek')
        data_quarter.append(int(expense))
    if income != None:
        labels_quarter.append('Przychód')
        data_quarter.append(int(income)) 

    expense = Transaction.objects.filter(user=request.user,type='recurringExpense', recurring_type='year').aggregate(Sum('value'))['value__sum']
    income = Transaction.objects.filter(user=request.user,type='recurringIncome', recurring_type='year').aggregate(Sum('value'))['value__sum']    
    if expense != None:
        labels_year.append('Wydatek')
        data_year.append(int(expense))
    if income != None:
        labels_year.append('Przychód')
        data_year.append(int(income))         

    expense = Transaction.objects.filter(user=request.user,type='recurringExpense', recurring_type='month').aggregate(Sum('value'))['value__sum']
    income = Transaction.objects.filter(user=request.user,type='recurringIncome', recurring_type='month').aggregate(Sum('value'))['value__sum']    
    if expense != None:
        labels_month.append('Wydatek')
        data_month.append(int(expense))
    if income != None:
        labels_month.append('Przychód')
        data_month.append(int(income))

    recurrings = Transaction.objects.filter(user=request.user,type__in=['recurringExpense','recurringIncome'])
    labels_all =[]
    data_all = []
    for recurring in recurrings:
        if recurring.value == 0:
            continue
        else:
            labels_all.append(recurring.name)
            data_all.append(int(recurring.value))
        
    return render(request, 'views/report/report_recurring.html',
    {'date_form':date_form,
    'labels':labels,'data':data,
    'data_week':data_week,'labels_week':labels_week,
    'data_quarter':data_quarter,'labels_quarter':labels_quarter,
    'data_year':data_year,'labels_year':labels_year,
    'data_month':data_month,'labels_month':labels_month,
    'data_all':data_all,'labels_all':labels_all})