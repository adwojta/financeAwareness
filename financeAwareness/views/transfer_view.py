from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import TransferForm
from financeAwareness.models.account import Account
from financeAwareness.models.transaction import Transaction

#Transfer
@login_required
def transfer_form(request):
    if request.method == 'POST':
        transfer_form = TransferForm(data=request.POST,User=request.user)
        if transfer_form.is_valid():
            new_transfer = transfer_form.save(commit=False)
            new_transfer.user_id =request.user
            from_account = Account.objects.get(id=new_transfer.account_id.id)
            to_account = Account.objects.get(id=new_transfer.transfer_account.id)

            from_account.value -=new_transfer.value
            to_account.value +=new_transfer.value

            new_transfer.name = from_account.name + "->" + to_account.name
            new_transfer.type = 'transfer'

            from_account.save()
            to_account.save()
            new_transfer.save()

            return redirect('financeAwareness:transactions')
    else:
        transfer_form = TransferForm(User=request.user)

    return render(request, 'views/transfer/transfer_form.html',{'transfer_form': transfer_form})

@login_required
def transfer_form_update(request,transfer_id):
    transfer = get_object_or_404(Transaction,id=transfer_id)
    old_value = transfer.value
    old_from_account = Account.objects.get(id=transfer.account_id.id)
    old_to_account = Account.objects.get(id=transfer.transfer_account.id)

    if request.user != transfer.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        transfer_form = TransferForm(instance=transfer,User=request.user)
        if request.method == 'POST':
            transfer_form = TransferForm(data=request.POST,instance=transfer,User=request.user)
            if transfer_form.is_valid():              
                new_transfer = transfer_form.save(commit=False)
                from_account = Account.objects.get(id=new_transfer.account_id.id)
                to_account = Account.objects.get(id=new_transfer.transfer_account.id)

                if old_from_account == from_account and old_to_account == to_account:
                    new_value = new_transfer.value - old_value
                    from_account.value -=new_value
                    to_account.value +=new_value
                else:
                    old_from_account.value += old_value
                    old_to_account.value -= old_value
                    old_from_account.save()
                    old_to_account.save()

                    from_account.value -= new_transfer.value
                    to_account.value += new_transfer.value

                new_transfer.user_id = request.user
                from_account.save()
                to_account.save()                                
                new_transfer.save()
                return redirect('financeAwareness:transactions')

        return render(request, 'views/transfer/transfer_update.html',{'transfer_form':transfer_form,'transfer_id':transfer_id})

@login_required
def transfer_form_delete(request,transfer_id):
    transfer = get_object_or_404(Transaction,id=transfer_id)

    if request.user != transfer.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            from_account = Account.objects.get(id=transfer.account_id.id)
            to_account = Account.objects.get(id=transfer.transfer_account.id)

            if from_account.accomplished_date==None and to_account.accomplished_date==None:
                from_account.value +=transfer.value
                to_account.value -=transfer.value
            from_account.save()
            to_account.save()

            transfer.delete()
            return redirect('financeAwareness:transactions')

        return render(request, 'views/transfer/transfer_delete.html',{'transfer_id':transfer_id})