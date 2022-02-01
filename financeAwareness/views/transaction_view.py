from sys import prefix
import django
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, model_to_dict, modelform_factory, modelformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core import serializers
from financeAwareness.forms import TransactionForm, IncomeItemForm,ExpenseItemForm
from financeAwareness.models.account import Account
from financeAwareness.models.category import Category
from financeAwareness.models.transaction import Transaction
from financeAwareness.models.transactionItem import TransactionItem


#Transaction
@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user_id=request.user.id)
    return render(request, 'views/transaction/transactions.html',{'transactions': transactions})

@login_required
def transaction_details(request,transaction_id):
    transaction = get_object_or_404(Transaction,id=transaction_id)
    if request.user != transaction.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        items = transaction.items.all()
        return render(request, 'views/transaction/transaction_details.html',{'items': items,'transaction': transaction})

@login_required
def expense_form(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(data=request.POST,User=request.user)
        item_names = request.POST.getlist("item_name")
        item_categories = request.POST.getlist("category_id")
        item_subcategories = request.POST.getlist("subcategory")
        item_values = request.POST.getlist("item_value")
        items_planned = request.POST.getlist("is_planned")
        tags = request.POST.getlist("tags")
        items_data = []
        items = len(item_names)
        items_valid = True

        for item in range(items):        
            data={'item_name':item_names[item],'category_id':item_categories[item],"item_value":item_values[item],"is_planned":items_planned[item]}
            items_data.append(ExpenseItemForm(User=request.user,data=data))

        transaction_item_forms = (ExpenseItemForm(User=request.user))
        if transaction_form.is_valid():
            new_transaction = transaction_form.save(commit=False)
            account = new_transaction.account_id
            
            for item in items_data:
                if not item.is_valid():
                    items_valid= False
            if items_valid:
                account.value = account.value - new_transaction.value
                account.save()
                new_transaction.user_id = request.user
                new_transaction.type = 'expense'
                new_transaction.save()
                transaction_id = Transaction.objects.latest('id')
                
                tag_to_add = []
                for tag in tags:
                    tag_to_add.append(Transaction.tags.through(transaction_id = transaction_id.id, tag_id=tag))
                
                Transaction.tags.through.objects.bulk_create(tag_to_add)

                for i,item in enumerate(items_data):
                    new_item = item.save(commit=False)
                    new_item.transaction_id = transaction_id
                    if int(item_subcategories[i]) == -1:
                        new_item.save()
                    else:
                        new_item.category_id = Category.objects.get(id=item_subcategories[i])  
                        new_item.save()

                return redirect('financeAwareness:transactions')

    else:
        transaction_item_forms = (ExpenseItemForm(User=request.user,auto_id=False),)
        transaction_form = TransactionForm(User=request.user)
    return render(request, 'views/transaction/transaction_form.html',{'transaction_form': transaction_form,'transaction_item_forms': transaction_item_forms})

def getSubcategories(request):
    if request.is_ajax and request.method == 'GET':
        category = request.GET['category']

        try:
            master_category = Category.objects.get(id=category)
            subcategories = Category.objects.filter(master_category = master_category)
            if subcategories:
                subcategories_JSON = serializers.serialize('json',subcategories)
                return JsonResponse({'subcategories':subcategories_JSON},status=200)
            else:
                return HttpResponse(status=204)
        except:
            return HttpResponse(status=204)

@login_required
def income_form(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(data=request.POST,User=request.user)
        item_names = request.POST.getlist("item_name")
        item_categories = request.POST.getlist("category_id")
        item_subcategories = request.POST.getlist("subcategory")
        item_values = request.POST.getlist("item_value")
        items_planned = request.POST.getlist("is_planned")
        tags = request.POST.getlist("tags")
        items_data = []
        items = len(item_names)
        items_valid = True
        for item in range(items):        
            data={'item_name':item_names[item],'category_id':item_categories[item],"item_value":item_values[item],"is_planned":items_planned[item]}
            items_data.append(IncomeItemForm(User=request.user,data=data))

        transaction_item_forms = (IncomeItemForm(User=request.user))
        if transaction_form.is_valid():
            new_transaction = transaction_form.save(commit=False)
            account = new_transaction.account_id
            
            for item in items_data:
                if not item.is_valid():
                    items_valid= False
            if items_valid:
                account.value = account.value + new_transaction.value
                account.save()
                new_transaction.user_id = request.user
                new_transaction.type = 'income'
                new_transaction.save()
                transaction_id = Transaction.objects.latest('id')
                
                tag_to_add = []
                for tag in tags:
                    tag_to_add.append(Transaction.tags.through(transaction_id = transaction_id.id, tag_id=tag))
                
                Transaction.tags.through.objects.bulk_create(tag_to_add)

                for i,item in enumerate(items_data):
                    new_item = item.save(commit=False)
                    new_item.transaction_id = transaction_id
                    if int(item_subcategories[i]) == -1:
                        new_item.save()
                    else:
                        new_item.category_id = Category.objects.get(id=item_subcategories[i])  
                        new_item.save()
                return redirect('financeAwareness:transactions')

    else:
        transaction_item_forms = (IncomeItemForm(User=request.user,auto_id=False),)
        transaction_form = TransactionForm(User=request.user)
    return render(request, 'views/transaction/transaction_form.html',{'transaction_form': transaction_form,'transaction_item_forms': transaction_item_forms})


def transaction_form_delete(request,transaction_id):
    transaction = get_object_or_404(Transaction,id=transaction_id)
    if request.user != transaction.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            account = transaction.account_id
            if transaction.type == 'income':
                account.value -= transaction.value
            elif transaction.type == 'expense':
                account.value += transaction.value

            account.save()
            transaction.delete()
            return redirect('financeAwareness:transactions')

        return render(request, 'views/transaction/transaction_delete.html',{'transaction_id':transaction_id})

def transaction_form_update(request,transaction_id):
    transaction = get_object_or_404(Transaction,id=transaction_id)
    old_value = transaction.value
    old_account = transaction.account_id

    if transaction.type == 'income':
                itemform = IncomeItemForm
    elif transaction.type == 'expense':
                itemform = ExpenseItemForm
    
    if request.method == 'POST':        
        transaction_form = TransactionForm(data=request.POST,User=request.user,instance=transaction)
        item_names = request.POST.getlist("item_name")
        item_categories = request.POST.getlist("category_id")
        item_subcategories = request.POST.getlist("subcategory")
        item_values = request.POST.getlist("item_value")
        items_planned = request.POST.getlist("is_planned")
        tags = request.POST.getlist("tags")
        transaction_item_forms = []
        items = len(item_names)
        items_valid = True
        
        transactionItems = transaction.items.all()
        data = {}
        items_to_delete = {}

        if items < len(transactionItems):
            items_to_delete = transactionItems[items:]
            transactionItems = transactionItems[:items]

        for item in range(items):       
            if item > len(transactionItems)-1:        
                data={'item_name':item_names[item],'category_id':item_categories[item],"item_value":item_values[item],"is_planned":items_planned[item]}
                transaction_item_forms.append(itemform(User=request.user,data=data))
            else:      
                data={'item_name':item_names[item],'category_id':item_categories[item],"item_value":item_values[item],"is_planned":items_planned[item]}
                transaction_item_forms.append(itemform(User=request.user,data=data,instance=transactionItems[item]))

        if transaction_form.is_valid():
            updated_transaction = transaction_form.save(commit=False)
            account = updated_transaction.account_id

            for item in transaction_item_forms:
                if not item.is_valid():
                    items_valid= False

            if items_valid:
                if transaction.type == 'expense':
                    if old_account == updated_transaction.account_id:
                        if old_value != updated_transaction.value:
                            new_value = old_value - updated_transaction.value
                            account.value =account.value + new_value
                            account.save()
                    else:
                        old_account.value = old_account.value + old_value
                        account.value = account.value - updated_transaction.value
                        old_account.save()
                        account.save()
                elif transaction.type == 'income':
                    if old_account == updated_transaction.account_id:
                        if old_value != updated_transaction.value:
                            new_value = old_value - updated_transaction.value
                            account.value =account.value - new_value
                            account.save()
                    else:
                        old_account.value = old_account.value - old_value
                        account.value = account.value + updated_transaction.value
                        old_account.save()
                        account.save()

                updated_transaction.save()
                
                updated_transaction.tags.clear()

                tag_to_add = []
                for tag in tags:
                    tag_to_add.append(Transaction.tags.through(transaction_id = transaction.id, tag_id=tag))
                
                Transaction.tags.through.objects.bulk_create(tag_to_add)
                for i,item in enumerate(transaction_item_forms):
                    updated_item = item.save(commit=False)
                    updated_item.transaction_id = transaction
                    if int(item_subcategories[i]) == -1:
                        updated_item.save()
                    else:
                        updated_item.category_id = Category.objects.get(id=item_subcategories[i])  
                        updated_item.save()
                for item in items_to_delete:
                    item.delete()
                
                return redirect('financeAwareness:transaction_details',transaction_id=transaction.id)

    else:
        transaction_form = TransactionForm(User=request.user,instance=transaction)
        transactionItems = transaction.items.all()
        transaction_item_forms = []
        for item in transactionItems:
            transaction_item_forms.append(itemform(User=request.user,instance=item))

        return render(request, 'views/transaction/transaction_update.html',{'transaction_form': transaction_form,'transaction_item_forms': transaction_item_forms})
