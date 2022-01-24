from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import CategoryForm, TransactionForm, TransactionItemForm, SubcategoryForm, AccountForm,SavingGoalForm,TransferForm
from financeAwareness.models import transaction
from financeAwareness.models.account import Account
from financeAwareness.models.recurringTransaction import RecurringTransaction

from financeAwareness.models.transaction import Transaction
from financeAwareness.models.category import Category
from financeAwareness.models.transactionItem import TransactionItem
from financeAwareness.models.transfer import Transfer

#recurring
@login_required
def recurring_list(request):
    recurrings = RecurringTransaction.objects.filter(user_id=request.user.id)
    return render(request, 'views/recurring_transactions.html',{'recurrings': recurrings})

#account
@login_required
def account_list(request):
    accounts = Account.objects.filter(user_id=request.user.id,is_saving_goal=False)
    goals = Account.objects.filter(user_id=request.user.id,is_saving_goal=True)
    return render(request, 'views/account/accounts.html',{'accounts': accounts,'goals':goals})

@login_required
def account_form(request):
    if request.method == 'POST':
        account_form = AccountForm(data=request.POST)
        if account_form.is_valid():
            new_account = account_form.save(commit=False)
            new_account.user_id = request.user
            new_account.save()
            return redirect('financeAwareness:accounts')
    else:
        account_form = AccountForm()
    return render(request, 'views/account/account_form.html',{'account_form': account_form})

@login_required
def account_form_update(request,account_id):
    account = get_object_or_404(Account,id=account_id)  
    if request.user != account.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        account_form = AccountForm(instance=account)
        if request.method == 'POST':
            account_form = AccountForm(data=request.POST,instance=account)
            if account_form.is_valid():
                new_account = account_form.save(commit=False)
                new_account.user_id = request.user
                new_account.save()
                return redirect('financeAwareness:accounts')

        return render(request, 'views/account/account_update.html',{'account_form':account_form,'account_id':account_id})

@login_required
def account_form_delete(request,account_id):
    account = get_object_or_404(Account,id=account_id)
    if request.user != account.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            account.delete()
            return redirect('financeAwareness:accounts')

        return render(request, 'views/account/account_delete.html',{'account_id':account_id})

#Transfer
def transfer_form(request):
    if request.method == 'POST':
        transfer_form = TransferForm(data=request.POST,User=request.user)
        if transfer_form.is_valid():
            new_transfer = transfer_form.save(commit=False)
            new_transfer.user_id =request.user
            from_account = Account.objects.get(id=new_transfer.from_account.id)
            to_account = Account.objects.get(id=new_transfer.to_account.id)

            if from_account.value < new_transfer.value and from_account.is_cash==True:
                pass

            from_account.value -=new_transfer.value
            to_account.value +=new_transfer.value

            from_account.save()
            to_account.save()
            new_transfer.save()

            return redirect('financeAwareness:accounts')
    else:
        transfer_form = TransferForm(User=request.user)
    return render(request, 'views/transfer/transfer_form.html',{'transfer_form': transfer_form})

def transfer_form_update(request,transfer_id):
    transfer = get_object_or_404(Transfer,id=transfer_id)
    old_value = transfer.value
    
    if request.user != transfer.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        transfer_form = TransferForm(instance=transfer,User=request.user)
        if request.method == 'POST':
            transfer_form = TransferForm(data=request.POST,instance=transfer,User=request.user)
            if transfer_form.is_valid():              
                new_transfer = transfer_form.save(commit=False)
                from_account = Account.objects.get(id=new_transfer.from_account.id)
                to_account = Account.objects.get(id=new_transfer.to_account.id)

                new_value = new_transfer.value - old_value
                from_account.value -=new_value
                to_account.value +=new_value

                new_transfer.user_id = request.user
                from_account.save()
                to_account.save()                                
                new_transfer.save()
                return redirect('financeAwareness:transactions')

        return render(request, 'views/transfer/transfer_update.html',{'transfer_form':transfer_form,'transfer_id':transfer_id})


def transfer_form_delete(request,transfer_id):
    transfer = get_object_or_404(Transfer,id=transfer_id)
    if request.user != transfer.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            from_account = Account.objects.get(id=transfer.from_account.id)
            to_account = Account.objects.get(id=transfer.to_account.id)

            from_account.value +=transfer.value
            to_account.value -=transfer.value
            from_account.save()
            to_account.save()

            transfer.delete()
            return redirect('financeAwareness:transactions')

        return render(request, 'views/transfer/transfer_delete.html',{'transfer_id':transfer_id})

#Saving goal
def saving_goal_form(request):
    if request.method == 'POST':
        saving_goal_form = SavingGoalForm(data=request.POST)
        if saving_goal_form.is_valid():
            new_saving_goal = saving_goal_form.save(commit=False)
            new_saving_goal.user_id = request.user
            new_saving_goal.is_cash = False
            new_saving_goal.is_saving_goal = True
            new_saving_goal.save()
            return redirect('financeAwareness:accounts')
    else:
        saving_goal = SavingGoalForm()
    return render(request, 'views/account/saving_goal_form.html',{'saving_goal_form': saving_goal_form})

def saving_goal_form_update(request,account_id):
    saving_goal = get_object_or_404(Account,id=account_id)  
    if request.user != saving_goal.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        saving_goal_form = SavingGoalForm(instance=saving_goal)
        if request.method == 'POST':
            saving_goal_form = SavingGoalForm(data=request.POST,instance=saving_goal)
            if saving_goal_form.is_valid():
                new_saving_goal = saving_goal_form.save(commit=False)
                new_saving_goal.user_id = request.user
                new_saving_goal.save()
                return redirect('financeAwareness:accounts')
        return render(request, 'views/account/saving_goal_update.html',{'saving_goal_form':saving_goal_form,'account_id':account_id})

def saving_goal_form_delete(request,account_id):
    saving_goal = get_object_or_404(Account,id=account_id)
    if request.user != saving_goal.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            saving_goal.delete()
            return redirect('financeAwareness:accounts')
        return render(request, 'views/account/saving_goal_delete.html',{'account_id':account_id})

#Category
@login_required
def category_details(request,category_id):
    category = get_object_or_404(Category,id=category_id)
    if request.user != category.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        subcategories = category.subcategories.all()
        return render(request, 'views/category/category_details.html',{'subcategories': subcategories,'category':category})
        

@login_required
def category_list(request):
    expenses = Category.objects.filter(user_id=request.user.id, master_category=None,income=False)
    incomes = Category.objects.filter(user_id=request.user.id, master_category=None,income=True)
    return render(request, 'views/category/category.html',{'expenses': expenses,'incomes':incomes})

@login_required
def category_form(request, income=None):
    if request.method == 'POST':
        category_form = CategoryForm(data=request.POST,User=request.user)
        if category_form.is_valid():
            new_category = category_form.save(commit=False)
            if income == 'income':
                new_category.income = True
            else:
                new_category.income = False
            new_category.user_id = request.user
            new_category.save()
            return redirect('financeAwareness:categories')
    else:
        category_form = CategoryForm(User=request.user)
    return render(request, 'views/category/category_form.html',{'category_form': category_form})

@login_required
def category_form_update(request,category_id):   
    category = get_object_or_404(Category,id=category_id)        
    if request.user != category.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        category_form = CategoryForm(instance=category,User=request.user)
        if request.method == 'POST':
            category_form = CategoryForm(data=request.POST,instance=category,User=request.user)
            if category_form.is_valid():
                category_form.save()
                return redirect('financeAwareness:category_details',category_id)

        return render(request, 'views/category/category_update.html',{'category_form':category_form,'category_id':category_id})

    

def category_form_delete(request,category_id):
    category = get_object_or_404(Category,id=category_id)
    if request.user != category.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            category.delete()
            return redirect('financeAwareness:categories')
        return render(request, 'views/category/category_delete.html',{'category_id':category_id})

#Subcategory
@login_required
def subcategory_details(request,subcategory_id):
    subcategory = get_object_or_404(Category,id=subcategory_id)
    if request.user != subcategory.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        return render(request, 'views/category/subcategory_details.html',{'subcategory':subcategory})

@login_required
def subcategory_form(request,master_category):
    if request.method == 'POST':
        subcategory_form = SubcategoryForm(data=request.POST)
        if subcategory_form.is_valid():
            master = get_object_or_404(Category,id=master_category)
            new_subcategory = subcategory_form.save(commit=False)
            new_subcategory.master_category=master
            new_subcategory.user_id = request.user
            new_subcategory.save()
            return redirect('financeAwareness:category_details',category_id=master.id)
    else:
        subcategory_form = SubcategoryForm()
    return render(request, 'views/category/subcategory_form.html',{'subcategory_form': subcategory_form})

@login_required
def subcategory_form_update(request,subcategory_id):
    subcategory = get_object_or_404(Category,id=subcategory_id)
    if request.user != subcategory.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            subcategory_form = SubcategoryForm(data=request.POST,instance=subcategory)
            if subcategory_form.is_valid():
                updated_subcategory = subcategory_form.save(commit=False)
                updated_subcategory.save()
                return redirect('financeAwareness:subcategory_details',subcategory_id)
        else:
            subcategory_form = SubcategoryForm(instance=subcategory)
        return render(request, 'views/category/subcategory_update.html',{'subcategory_form':subcategory_form,'subcategory_id':subcategory_id})

def subcategory_form_delete(request,subcategory_id):
    subcategory = get_object_or_404(Category,id=subcategory_id)
    if request.user != subcategory.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            master = subcategory.master_category
            subcategory.delete()
            return redirect('financeAwareness:category_details',category_id=master.id)

        return render(request, 'views/category/subcategory_delete.html',{'subcategory_id':subcategory_id})


#Transaction
@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user_id=request.user.id)
    transfers = Transfer.objects.filter(user_id=request.user.id)
    return render(request, 'views/transaction/transactions.html',{'transactions': transactions,'transfers':transfers})

@login_required
def transaction_details(request,transaction_id):
    transaction = get_object_or_404(Transaction,id=transaction_id)
    if request.user != transaction.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        items = transaction.items.all()
        return render(request, 'views/transaction/transaction_details.html',{'items': items,'transaction': transaction})

@login_required
def transaction_form(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(data=request.POST,User=request.user)
        item_names = request.POST.getlist("item_name")
        item_categories = request.POST.getlist("category_id")
        item_values = request.POST.getlist("item_value")
        items_planned = request.POST.getlist("is_planned")
        items_data = []
        items = len(item_names)
        items_valid = True
        for item in range(items):
            data={'item_name':item_names[item],'category_id':item_categories[item],"item_value":item_values[item],"is_planned":items_planned[item]}
            items_data.append(TransactionItemForm(User=request.user,data=data))

        transaction_item_forms = (TransactionItemForm(User=request.user))
        if transaction_form.is_valid():
            new_transaction = transaction_form.save(commit=False)
            account = new_transaction.account_id
            if account.value >= new_transaction.value and new_transaction.is_income==False:
                for item in items_data:
                    if not item.is_valid():
                        items_valid= False
                if items_valid:
                    account.value = account.value - new_transaction.value
                    account.save()
                    new_transaction.user_id = request.user
                    new_transaction.save()
                    transaction_id = Transaction.objects.latest('id')

                    for item in items_data:
                        new_item = item.save(commit=False)
                        new_item.transaction_id = transaction_id
                        new_item.save()

                    return redirect('financeAwareness:transactions')
            elif new_transaction.is_income==True:
                for item in items_data:
                    if not item.is_valid():
                        items_valid= False
                if items_valid:
                    account.value = account.value + new_transaction.value
                    account.save()
                    new_transaction.user_id = request.user
                    new_transaction.save()
                    transaction_id = Transaction.objects.latest('id')

                    for item in items_data:
                        new_item = item.save(commit=False)
                        new_item.transaction_id = transaction_id
                        new_item.save()

                    return redirect('financeAwareness:transactions')
    else:
        transaction_item_forms = (TransactionItemForm(User=request.user,auto_id=False),)
        transaction_form = TransactionForm(User=request.user)
    return render(request, 'views/transaction/transaction_form.html',{'transaction_form': transaction_form,'transaction_item_forms': transaction_item_forms})