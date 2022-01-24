from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import SavingGoalForm
from financeAwareness.models.account import Account



#Saving goal
@login_required
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
