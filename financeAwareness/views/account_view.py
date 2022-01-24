from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import AccountForm
from financeAwareness.models.account import Account


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
