from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import AccountForm, SavingGoalForm, TransferForm
from financeAwareness.models.account import Account
from financeAwareness.views.site_view import AbstractDelete


#account
@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user.id,is_saving_goal=False)
    goals = Account.objects.filter(user=request.user.id,is_saving_goal=True)
    return render(request, 'views/account/accounts.html',{'accounts': accounts,'goals':goals})

@login_required
def account_form(request):
    title = 'Dodaj konto'
    type = 'account'
    if request.method == 'POST':
        form = AccountForm(data=request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return redirect('financeAwareness:accounts')
    else:
        form = AccountForm()
    return render(request, 'form.html',{'form': form,'title':title,'type':type})

@login_required
def account_form_update(request,account_id):
    title = 'Zaktualizuj konto'
    type = 'account'
    account = get_object_or_404(Account,id=account_id)  
    if request.user != account.user:
        return redirect('financeAwareness:transactions')       
    else:
        form = AccountForm(instance=account)
        if request.method == 'POST':
            form = AccountForm(data=request.POST,instance=account)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.user = request.user            
                new_account.save()
                return redirect('financeAwareness:accounts')

        return render(request, 'form.html',{'form':form,'title':title,'type':type})

class AccountDelete(AbstractDelete):
    redirect_view = 'financeAwareness:accounts'
    model = Account
    delete_type = "Account"
    title = "Usuń konto"

class GoalDelete(AbstractDelete):
    redirect_view = 'financeAwareness:accounts'
    model = Account
    delete_type = "Goal"
    title = "Usuń cel"

#Saving goal
@login_required
def saving_goal_form(request):
    title = 'Dodaj cel'
    if request.method == 'POST':
        saving_goal_form = SavingGoalForm(data=request.POST)
        if saving_goal_form.is_valid():
            new_saving_goal = saving_goal_form.save(commit=False)
            if new_saving_goal.is_active_saving_goal:
                accounts = Account.objects.filter(user_id=request.user)
                for account in accounts:
                    account.is_active_saving_goal = False
                    account.save()
            new_saving_goal.user_id = request.user.id
            new_saving_goal.is_cash = False
            new_saving_goal.is_saving_goal = True
            new_saving_goal.save()
            return redirect('financeAwareness:accounts')
    else:
        saving_goal_form = SavingGoalForm()
    return render(request, 'views/account/saving_goal_form.html',{'saving_goal_form': saving_goal_form,'title':title})

@login_required
def saving_goal_form_update(request,account_id):
    title = 'Zaktualizuj cel'
    saving_goal = get_object_or_404(Account,id=account_id)
    if request.user != saving_goal.user:
        return redirect('financeAwareness:transactions')       
    else:
        saving_goal_form = SavingGoalForm(instance=saving_goal)
        if request.method == 'POST':
            saving_goal_form = SavingGoalForm(data=request.POST,instance=saving_goal)
            if saving_goal_form.is_valid():
                new_saving_goal = saving_goal_form.save(commit=False)
                if new_saving_goal.is_active_saving_goal:
                    accounts = Account.objects.filter(user_id=request.user)
                    for account in accounts:
                        account.is_active_saving_goal = False
                        account.save()

                new_saving_goal.user_id = request.user
                new_saving_goal.save()
                return redirect('financeAwareness:accounts')
        return render(request, 'views/account/saving_goal_form.html',{'saving_goal_form':saving_goal_form,'account_id':account_id,'title':title})

@login_required
def saving_goal_accomplished(request,account_id):
    title = 'Wykonaj cel'
    goal = Account.objects.get(id=account_id)
    value = Account.objects.get(id=account_id).value
    if request.method == 'POST':
        transfer_form = TransferForm(data=request.POST,User=request.user)
        if transfer_form.is_valid():
            new_transfer = transfer_form.save(commit=False)
            new_transfer.user =request.user
            from_account = Account.objects.get(id=new_transfer.account.id)
            to_account = Account.objects.get(id=new_transfer.transfer_account.id)
            to_account.value +=new_transfer.value

            new_transfer.name = from_account.name + "->" + to_account.name
            new_transfer.type = 'transfer'
            from_account.accomplished_date = new_transfer.date
            from_account.is_active_saving_goal = False
            from_account.save()
            
            to_account.save()
            new_transfer.save()

            return redirect('financeAwareness:transactions')
    else:
        transfer_form = TransferForm(User=request.user,saving_goal=True,initial={'account':goal,'value':value,'date':datetime.now()},goal_id=goal.id)

    return render(request, 'views/transaction/transfer_form.html',{'transfer_form': transfer_form,'title':title})

