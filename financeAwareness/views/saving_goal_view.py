from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import SavingGoalForm, TransferForm
from financeAwareness.models.account import Account
from datetime import datetime


#Saving goal
@login_required
def saving_goal_form(request):
    if request.method == 'POST':
        saving_goal_form = SavingGoalForm(data=request.POST)
        if saving_goal_form.is_valid():
            new_saving_goal = saving_goal_form.save(commit=False)
            print(new_saving_goal.is_active_saving_goal)
            if new_saving_goal.is_active_saving_goal:
                accounts = Account.objects.filter(user_id=request.user)
                for account in accounts:
                    account.is_active_saving_goal = False
                    account.save()


            new_saving_goal.user_id = request.user
            new_saving_goal.is_cash = False
            new_saving_goal.is_saving_goal = True
            new_saving_goal.save()
            return redirect('financeAwareness:accounts')
    else:
        saving_goal_form = SavingGoalForm()
    return render(request, 'views/account/saving_goal_form.html',{'saving_goal_form': saving_goal_form})

@login_required
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
                if new_saving_goal.is_active_saving_goal:
                    accounts = Account.objects.filter(user_id=request.user)
                    for account in accounts:
                        account.is_active_saving_goal = False
                        account.save()

                new_saving_goal.user_id = request.user
                new_saving_goal.save()
                return redirect('financeAwareness:accounts')
        return render(request, 'views/account/saving_goal_update.html',{'saving_goal_form':saving_goal_form,'account_id':account_id})

@login_required
def saving_goal_form_delete(request,account_id):
    saving_goal = get_object_or_404(Account,id=account_id)
    if request.user != saving_goal.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            saving_goal.delete()
            return redirect('financeAwareness:accounts')
        return render(request, 'views/account/saving_goal_delete.html',{'account_id':account_id})

@login_required
def saving_goal_accomplished(request,account_id):
    goal = Account.objects.get(id=account_id)
    value = Account.objects.get(id=account_id).value
    if request.method == 'POST':
        transfer_form = TransferForm(data=request.POST,User=request.user)
        print(request.POST)
        if transfer_form.is_valid():
            new_transfer = transfer_form.save(commit=False)
            new_transfer.user_id =request.user
            from_account = Account.objects.get(id=new_transfer.account_id.id)
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
        transfer_form = TransferForm(User=request.user,saving_goal=True,initial={'account_id':goal,'value':value,'date':datetime.now()})

    return render(request, 'views/account/saving_goal_accomplished.html',{'transfer_form': transfer_form})
