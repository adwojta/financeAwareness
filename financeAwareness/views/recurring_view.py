from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from financeAwareness.models.recurringTransaction import RecurringTransaction


#recurring
@login_required
def recurring_list(request):
    recurrings = RecurringTransaction.objects.filter(user_id=request.user.id)
    return render(request, 'views/recurring_transactions.html',{'recurrings': recurrings})