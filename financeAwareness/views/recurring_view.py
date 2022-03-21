from django.shortcuts import redirect
from financeAwareness.forms import RecurringForm, TransactionForm
from financeAwareness.models.transaction import Transaction
from financeAwareness.views.transaction_view import AbstractCreateTransaction, AbstractDelete, AbstractDetailView, AbstractListView, AbstractUpdateTransaction
from dateutil.relativedelta import relativedelta

#recurring
class RecurringListView(AbstractListView):
    type = ['recurringExpense','recurringIncome']
    title='Stałe transakcje'

class RecurringDetailView(AbstractDetailView):
    redirect_view = 'financeAwareness:recurrings'
    title = 'Stała transakcja'

class CreateRecurringIncome(AbstractCreateTransaction):
    type = 'recurringIncome'
    category_type = 'income'
    title = 'Dodaj stały przychód'
    is_not_planned = False
    form = RecurringForm

    def post(self, request,is_planned=True, *args, **kwargs):
        super().post(request,is_planned)        
        return redirect('financeAwareness:recurrings')

class CreateRecurringExpense(AbstractCreateTransaction):
    type = 'recurringExpense'
    category_type = 'expense'
    title = 'Dodaj stały wydatek'
    is_not_planned = False
    form = RecurringForm

    def post(self, request,is_planned=True, *args, **kwargs):
        super().post(request,is_planned)        
        return redirect('financeAwareness:recurrings')

class RecurringUpdate(AbstractUpdateTransaction):
    title = 'Zaktualizuj stałą transakcje'
    is_not_planned = False
    form = RecurringForm

    def form_valid(self, request, *args, **kwargs):
        super().form_valid(request, *args, **kwargs)
        self.update_transaction(request)

    def post(self, request, *args, **kwargs):
        super().post(request,is_planned=True)
        return redirect('financeAwareness:recurring_details',transaction_id=self.new_transaction.id)

class RecurringDelete(AbstractDelete):
    redirect_view = 'financeAwareness:recurrings'
    model = Transaction
    delete_type = "Reccuring"
    title = "Usuń stałą transakcje"

class RecurringAdd(AbstractUpdateTransaction):
    form = TransactionForm
    title = 'Dodaj stałą transakcje'
    
    def post(self, request, *args, **kwargs):
        super().post(request,is_planned=True)
        return redirect('financeAwareness:recurrings')

    def form_valid(self, request, *args, **kwargs):
        super().form_valid(request)

        recurring_transaction = Transaction.objects.get(id=self.new_transaction.id)
        self.new_transaction.id = None
        account = self.new_transaction.account
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
