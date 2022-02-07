from django.shortcuts import redirect
from financeAwareness.forms import RecurringForm, TransactionForm
from financeAwareness.models.transaction import Transaction
from financeAwareness.views.transaction_view import AbstractCreateTransaction, AbstractDelete, AbstractDetailView, AbstractListView, AbstractUpdateTransaction
from dateutil.relativedelta import relativedelta

#recurring
class RecurringListView(AbstractListView):
    success_view = 'views/recurring/recurrings.html'
    types = ['recurringExpense','recurringIncome']

class RecurringDetailView(AbstractDetailView):
    redirect_view = 'financeAwareness:recurrings'
    success_view = 'views/recurring/recurring_details.html'

class CreateRecurringIncome(AbstractCreateTransaction):
    type = 'recurringIncome'
    category_type = 'income'
    get_view = 'views/recurring/recurring_form.html'
    form = RecurringForm

    def post(self, request,is_planned=True, *args, **kwargs):
        super().post(request,is_planned)        
        return redirect('financeAwareness:recurrings')

class CreateRecurringExpense(AbstractCreateTransaction):
    type = 'recurringExpense'
    category_type = 'expense'
    get_view = 'views/recurring/recurring_form.html'
    form = RecurringForm

    def post(self, request,is_planned=True, *args, **kwargs):
        super().post(request,is_planned)        
        return redirect('financeAwareness:recurrings')

class RecurringUpdate(AbstractUpdateTransaction):
    get_view = 'views/recurring/recurring_update.html'
    form = RecurringForm

    def form_valid(self, request, *args, **kwargs):
        super().form_valid(request, *args, **kwargs)
        self.update_transaction(request)

    def post(self, request, *args, **kwargs):
        super().post(request,is_planned=True)
        return redirect('financeAwareness:recurring_details',transaction_id=self.new_transaction.id)

class RecurringDelete(AbstractDelete):
    redirect_view = 'financeAwareness:recurrings'
    get_view = 'views/recurring/recurring_delete.html'

class RecurringAdd(AbstractUpdateTransaction):
    form = TransactionForm
    get_view = 'views/recurring/recurring_add.html'
    
    def post(self, request, *args, **kwargs):
        super().post(request,is_planned=True)
        return redirect('financeAwareness:recurrings')

    def form_valid(self, request, *args, **kwargs):
        super().form_valid(request)

        recurring_transaction = Transaction.objects.get(id=self.new_transaction.id)
        self.new_transaction.id = None
        account = self.new_transaction.account_id

        if self.items_valid:
            if recurring_transaction.type =='recurringExpense':
                account.value = account.value - self.new_transaction.value
            else:
                account.value = account.value + self.new_transaction.value
            
            account.save()

            if recurring_transaction.reccuring_type == 'month':
                recurring_transaction.date = recurring_transaction.date + relativedelta(months=1)
            elif recurring_transaction.reccuring_type == 'quarter':
                recurring_transaction.date = recurring_transaction.date + relativedelta(months=3)
            elif recurring_transaction.reccuring_type == 'year':
                recurring_transaction.date = recurring_transaction.date + relativedelta(years=1)
            elif recurring_transaction.reccuring_type == 'week':
                recurring_transaction.date = recurring_transaction.date + relativedelta(weeks=1)

            if recurring_transaction.type =='recurringExpense':
                self.new_transaction.type = 'expense'
            else:
                self.new_transaction.type = 'income'
            
            recurring_transaction.save()
            self.new_transaction.save()
            self.transaction = Transaction.objects.latest('id')
            
            self.set_tags()
            self.set_items(new_items=True)
