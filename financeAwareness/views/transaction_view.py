from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import TransactionForm, TransactionItemForm


from financeAwareness.models.transaction import Transaction

from financeAwareness.models.transfer import Transfer

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