import io

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from financeAwareness.models.transaction import Transaction
from financeAwareness.forms import TransactionForm
from financeAwareness.models.transaction import Transaction
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from financeAwareness.views.transaction_view import AbstractCreateTransaction, AbstractDelete, AbstractDetailView, AbstractListView, AbstractUpdateTransaction

#Planned
class PlannedListView(AbstractListView):
    success_view = 'views/planned/planned.html'
    types = ['planned']

class PlannedDetailView(AbstractDetailView):
    redirect_view = 'financeAwareness:planned'
    success_view = 'views/planned/planned_details.html'

class CreatePlannedExpense(AbstractCreateTransaction):
    type = 'planned'
    category_type = 'expense'
    get_view = 'views/planned/planned_form.html'
    form = TransactionForm

    def post(self, request,is_planned=True, *args, **kwargs):
        super().post(request,is_planned)        
        return redirect('financeAwareness:planned')

class PlannedUpdate(AbstractUpdateTransaction):
    get_view = 'views/planned/planned_update.html'
    form = TransactionForm

    def form_valid(self, request, *args, **kwargs):
        super().form_valid(request, *args, **kwargs)
        self.update_transaction(request)

    def post(self, request,transaction_id, *args, **kwargs):
        super().post(request,transaction_id)
        return redirect('financeAwareness:planned_details',transaction_id=self.new_transaction.id)

class PlannedDelete(AbstractDelete):
    redirect_view = 'financeAwareness:transactions'
    get_view = 'views/planned/planned_delete.html'

class PlannedAdd(AbstractUpdateTransaction):
    form = TransactionForm
    get_view = 'views/planned/planned_add.html'
    type = 'expense'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return redirect('financeAwareness:transactions')

    def form_valid(self, request, *args, **kwargs):
        super().form_valid(request)
        account = self.new_transaction.account_id
        if self.items_valid:
            account.value = account.value - self.new_transaction.value
            
            account.save()
                
            self.new_transaction.type = 'expense'
            self.new_transaction.save()

            self.set_tags()
            self.set_items()

@login_required
def planned_to_pdf(request,transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    items = transaction.items.all()

    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdfmetrics.registerFont(TTFont('ROBOTO','ROBOTO-REGULAR.ttf'))
    pdf.setTitle('Lista zakupowa'+ transaction.name)
    pdf.setFont('ROBOTO',32) 
    pdf.drawCentredString(300,800,'Lista zakupowa')
    pdf.setFontSize(22)   
    pdf.drawCentredString(300,770,transaction.name)

    lines = []
    pdf.setFontSize(18) 
    text = pdf.beginText(80,700)

    for number,item in enumerate(items): 
        lines.append(str(number+1) + '.' + ' ' + item.item_name)

    for page,line in enumerate(lines):
        if page%40 == 0 and page > 0:         
            pdf.drawText(text)
            pdf.showPage()

            pdf.setFontSize(32) 
            pdf.drawCentredString(300,800,'Lista zakupowa')
            pdf.setFontSize(22)   
            pdf.drawCentredString(300,780,transaction.name)
            pdf.setFontSize(18)
            
            text = pdf.beginText(80,700)
            
        text.textLine(line.strip())

    pdf.drawText(text)
    pdf.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=(transaction.name + '.pdf'))