from abc import ABC, abstractmethod
import datetime
import os
from .site_view import AbstractDelete
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core import serializers
from financeAwareness.forms import SearchForm, TransactionForm,TransactionItemForm
from financeAwareness.models.category import Category
from financeAwareness.models.transaction import Transaction
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.base import TemplateView
from django.contrib.postgres.search import SearchVector
from financeAwareness.models.transactionItem import TransactionItem

class AbstractTransaction(ABC):
    type = ""
    category_type = ""
    items_valid = True
    get_view = ""
    title = ""
    is_not_planned = True
    form = None
    new_transaction = None
    tags = []
    items_data = []

    item_names = ""    
    item_categories = ""
    item_subcategories = ""
    item_values = ""
    items_planned = ""
    items_amount = 0
    transaction_item_forms = []

    transaction = None

    def get_items_data(self, request, *args, **kwargs):
            self.tags = request.POST.getlist("tags")
            self.items_data = []

            self.item_subcategories = request.POST.getlist("subcategory")
            self.item_names = request.POST.getlist("item_name")
            self.item_categories = request.POST.getlist("category")
            self.item_values = request.POST.getlist("item_value")
            self.items_planned = request.POST.getlist("is_planned")

            self.items_amount = len(self.item_names)

    def set_tags(self):
        tag_to_add = []
        for tag in self.tags:
            tag_to_add.append(Transaction.tags.through(transaction = self.transaction, tag_id=tag))

        Transaction.tags.through.objects.bulk_create(tag_to_add)

    def set_items(self,new_items=False):
        for i,item in enumerate(self.items_data):
            new_item = item.save(commit=False)
            new_item.transaction = self.transaction
            if new_items:
                new_item.id = None
            if int(self.item_subcategories[i]) == -1:
                new_item.save()
            else:
                new_item.category = Category.objects.get(id=self.item_subcategories[i])  
                new_item.save()

    @abstractmethod
    def set_items_data_form(self, request,is_planned=False, *args, **kwargs):
        pass

class AbstractListView(LoginRequiredMixin,TemplateView,ABC):
    max_in_page = 16
    type = []
    title = ""
    def get(self, request, *args, **kwargs):
        self.transactions_list = Transaction.objects.filter(user=request.user.id, type__in=self.type)
        paginator = Paginator(self.transactions_list,self.max_in_page)
        page_number = request.GET.get('page','1')
        try:
            transactions = paginator.page(page_number)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        page_number = paginator.get_page(page_number)

        return render(request, 'views/transaction/transactions.html',{'transactions': transactions,'page_number':page_number,'title':self.title})

class AbstractDetailView(LoginRequiredMixin,TemplateView,ABC):
    redirect_view = ""
    success_view = ""
    title =""

    def get(self, request,transaction_id, *args, **kwargs):
        transaction = get_object_or_404(Transaction,id=transaction_id)
        if request.user != transaction.user:
            return redirect(self.redirect_view)       
        else:
            items = transaction.items.all()
            context = []
            for item in items:
                category = item.category
                if category.master_category:
                    subcategory = category
                    item.category = category.master_category
                else:
                    subcategory = 'brak'
                context.append([item,subcategory])
            return render(request, 'views/transaction/transaction_details.html',{'context': context,'transaction': transaction,'title':self.title})

class AbstractCreateTransaction(LoginRequiredMixin,CreateView,AbstractTransaction,ABC):
    get_view = 'views/transaction/transaction_form.html'

    def set_items_data_form(self, request,is_planned, *args, **kwargs):       
        if is_planned:
            for item in range(self.items_amount):        
                data={'item_name':self.item_names[item],'category':self.item_categories[item],"item_value":self.item_values[item],"is_planned":True}
                self.items_data.append(TransactionItemForm(User=request.user,data=data,type=self.category_type))
        else:        
            for item in range(self.items_amount):        
                data={'item_name':self.item_names[item],'category':self.item_categories[item],"item_value":self.item_values[item],"is_planned":self.items_planned[item]}
                self.items_data.append(TransactionItemForm(User=request.user,data=data,type=self.category_type))
        

    def post(self, request,is_planned=False, *args, **kwargs):   
        self.transaction_form = self.form(data=request.POST,files=request.FILES,User=request.user)
        self.get_items_data(request)
        self.set_items_data_form(request,is_planned)
        self.transaction_item_forms = self.items_data
        self.form_valid(request)

    def form_valid(self, request, *args, **kwargs):
        if self.transaction_form.is_valid():
            self.new_transaction = self.transaction_form.save(commit=False)
            for item in self.items_data: 
                if not item.is_valid():
                    self.items_valid= False
            if self.items_valid:
                self.new_transaction.user = request.user
                self.new_transaction.type = self.type
                self.new_transaction.save()                                                  
                self.transaction = Transaction.objects.latest('id')
                self.set_tags()
                self.set_items()

    def get(self, request, *args, **kwargs):
        self.transaction_item_forms = (TransactionItemForm(User=request.user,type=self.category_type),)
        self.transaction_form = self.form(User=request.user)
        return render(request, self.get_view,{'transaction_form': self.transaction_form,'transaction_item_forms': self.transaction_item_forms,'title':self.title,'is_not_planned':self.is_not_planned})

class AbstractUpdateTransaction(LoginRequiredMixin,UpdateView,AbstractTransaction,ABC):
    get_view = 'views/transaction/transaction_form.html'
    transactionItems = None
    items_to_delete = []
    path = None    

    def set_items_data_form(self, request,is_planned=False, *args, **kwargs):
        if self.items_amount < len(self.transactionItems):
            self.items_to_delete = self.transactionItems[self.items_amount:]
            self.transactionItems = self.transactionItems[:self.items_amount]

        if is_planned:
            for item in range(self.items_amount):       
                if item > len(self.transactionItems)-1:        
                    data={'item_name':self.item_names[item],'category':self.item_categories[item],"item_value":self.item_values[item],"is_planned":True}
                    self.items_data.append(TransactionItemForm(User=request.user,data=data,type=self.category_type))
                else:      
                    data={'item_name':self.item_names[item],'category':self.item_categories[item],"item_value":self.item_values[item],"is_planned":True}
                    self.items_data.append(TransactionItemForm(User=request.user,data=data,instance=self.transactionItems[item],type=self.category_type))
        else:        
            for item in range(self.items_amount):       
                if item > len(self.transactionItems)-1:        
                    data={'item_name':self.item_names[item],'category':self.item_categories[item],"item_value":self.item_values[item],"is_planned":self.items_planned[item]}
                    
                    self.items_data.append(TransactionItemForm(User=request.user,data=data,type=self.category_type))
                else:                         
                    data={'item_name':self.item_names[item],'category':self.item_categories[item],"item_value":self.item_values[item],"is_planned":self.items_planned[item]}
                    self.items_data.append(TransactionItemForm(User=request.user,data=data,instance=self.transactionItems[item],type=self.category_type)) 

    def form_valid(self, request, *args, **kwargs):
        if self.transaction_form.is_valid():
            self.new_transaction = self.transaction_form.save(commit=False)
            for item in self.items_data:
                if not item.is_valid():
                    self.items_valid= False
            if self.items_valid:
                new_image= bool(request.FILES)
                if request.POST.__contains__('image-clear'):
                    self.transaction.image.delete()
                if new_image and self.path !=None:
                    os.unlink(self.path)


    def update_transaction(self,request):
        if self.items_valid:
            self.new_transaction.user = request.user
            self.new_transaction.type = self.type
            self.new_transaction.save()                                                  
            self.set_tags()
            self.set_items()

    def setup(self, request, *args, **kwargs):
        self.transaction = get_object_or_404(Transaction,id=kwargs['transaction_id'])
        if self.transaction.image:
            self.path = self.transaction.image.path
        self.transactionItems = self.transaction.items.all()
        self.old_value = self.transaction.value
        self.old_account = self.transaction.account
        self.type = self.transaction.type
        self.transaction_item_forms = []

        if self.type == 'recurringExpense' or self.type == 'planned':
            self.category_type = 'expense'
        elif self.type == 'recurringIncome':
            self.category_type = 'income'
        else:
            self.category_type = self.type

        return super().setup(request, *args, **kwargs)

    def set_tags(self):
        self.new_transaction.tags.clear()
        super().set_tags()

    def set_items(self,new_items=False):
        super().set_items(new_items)
        for item in self.items_to_delete:
            item.delete()

    def post(self, request,is_planned=False, *args, **kwargs):       
        self.get_items_data(request)
        self.set_items_data_form(request,is_planned)

        self.transaction_form = self.form(data=request.POST,files=request.FILES,User=request.user,instance=self.transaction)
        self.transaction_item_forms = self.items_data

        self.form_valid(request)

    def get(self, request, *args, **kwargs):
        self.transaction_form = self.form(User=request.user,instance=self.transaction)
        for item in self.transactionItems:
            self.transaction_item_forms.append(TransactionItemForm(User=request.user,instance=item,type=self.category_type))

        return render(request, self.get_view,{'transaction_form': self.transaction_form,'transaction_item_forms': self.transaction_item_forms,'title':self.title,'is_not_planned':self.is_not_planned,'update':True})

class CreateExpense(AbstractCreateTransaction):
    type = 'expense'
    category_type = 'expense'
    title = 'Dodaj wydatek'
    form =TransactionForm

    def form_valid(self, request):
        super().form_valid(request)       
        account = self.new_transaction.account
        account.value = account.value - self.new_transaction.value
        account.save()

    def post(self, request, *args, **kwargs):
        super().post(request)        
        return redirect('financeAwareness:transactions')

class CreateIncome(AbstractCreateTransaction):
    type = 'income'
    category_type = 'income'
    title = 'Dodaj przychód'
    form =TransactionForm

    def form_valid(self, request):
        super().form_valid(request)
        account = self.new_transaction.account
        account.value = account.value + self.new_transaction.value
        account.save()

    def post(self, request, *args, **kwargs):
        super().post(request)        
        return redirect('financeAwareness:transactions')

class TransactionUpdate(AbstractUpdateTransaction):
    title = 'Zaktualizuj transakcje'
    form = TransactionForm
    

    def form_valid(self, request, *args, **kwargs):
        super().form_valid(request, *args, **kwargs)
        self.update_transaction(request)
        account = self.new_transaction.account
        if self.transaction.type == 'expense':
            if self.old_account == self.new_transaction.account:
                if self.old_value != self.new_transaction.value:
                    new_value = self.old_value - self.new_transaction.value
                    account.value = account.value + new_value
                    account.save()
            else:
                self.old_account.value = self.old_account.value + self.old_value
                account.value = account.value - self.new_transaction.value
                self.old_account.save()
                account.save()
        elif self.new_transaction.type == 'income':
            if self.old_account == self.new_transaction.account:
                if self.old_value != self.new_transaction.value:
                    new_value = self.old_value - self.new_transaction.value
                    account.value = account.value - new_value
                    account.save()
            else:
                self.old_account.value = self.old_account.value - self.old_value
                account.value = account.value + self.new_transaction.value
                self.old_account.save()
                account.save()
            
    def post(self, request, *args, **kwargs):
        super().post(request)    
        return redirect('financeAwareness:transaction_details',transaction_id=self.new_transaction.id)

class TransactionDetailView(AbstractDetailView):
    redirect_view = 'financeAwareness:transactions'
    title = 'Transakcja'

class TransactionListView(AbstractListView):
    type=['income','expense','transfer']
    title='Transakcje'

class TransactionDelete(AbstractDelete):
    redirect_view = 'financeAwareness:transactions'
    model = Transaction
    delete_type = "Transaction"
    title = "Usuń transakcje"

    def post(self, request, *args, **kwargs):
        account = self.object.account
        if self.object.type == 'income':
            account.value -= self.object.value
        elif self.object.type == 'expense':
            account.value += self.object.value
        account.save()
        super().post(request)
        return redirect(self.redirect_view)
    
@login_required
def get_subcategories(request):
    if request.is_ajax and request.method == 'GET':
        category = request.GET['category']
        try:
            master_category = Category.objects.get(id=category)
            subcategories = Category.objects.filter(master_category = master_category)
            if subcategories:
                subcategories_JSON = serializers.serialize('json',subcategories)
                return JsonResponse({'subcategories':subcategories_JSON},status=200)
            else:
                return HttpResponse(status=204)
        except:
            return HttpResponse(status=204)

@login_required
def get_categories(request):
    if request.is_ajax and request.method == 'GET':
        transaction_type = request.GET['transaction_type']
        if transaction_type == None:
            return HttpResponse(status=404)
        try:
            categories = Category.objects.filter(user=request.user.id,is_income=transaction_type,master_category=None)
            categories_JSON = serializers.serialize('json',categories)
            return JsonResponse({'categories':categories_JSON},status=200)
        except:
            return HttpResponse(status=204)

@login_required
def search_transactions(request):
    max_in_page = 16
    title = 'Znalezione transakcje'
    if request.GET:
        search_form = SearchForm(data=request.GET,user=request.user)
        if search_form.is_valid():   
            clean_data = search_form.cleaned_data
            transactions = None
            value = clean_data['search']
            transactions = Transaction.objects.annotate(search = SearchVector('name','description'),).filter(search=value,user = request.user.id,type__in=['expense','income'])
            if transactions.exists():
                transactions = transactions | Transaction.objects.filter(id__in=(TransactionItem.objects.annotate(search = SearchVector('item_name'),).filter(search=value).values('transaction').distinct()),user = request.user.id,type__in=['expense','income']) 
            else:
                transactions = Transaction.objects.filter(id__in=(TransactionItem.objects.annotate(search = SearchVector('item_name'),).filter(search=value).values('transaction').distinct()),user = request.user.id,type__in=['expense','income']) 
            
            if transactions.exists():
                transactions = transactions | Transaction.objects.filter(tags__in=clean_data['tags'],user = request.user.id,type__in=['expense','income'])
            else:
                transactions = Transaction.objects.filter(tags__in=clean_data['tags'],user = request.user.id,type__in=['expense','income'])
            
            if clean_data['date_from'] and clean_data['date_to'] and clean_data['date_to'] > clean_data['date_from']:
                if transactions.exists():
                    transactions = transactions & Transaction.objects.filter(date__range=[(clean_data['date_from']),(clean_data['date_to'] + datetime.timedelta(days=1))],user = request.user.id,type__in=['expense','income'])
                else:            
                    transactions =  Transaction.objects.filter(date__range=[(clean_data['date_from']),(clean_data['date_to'] + datetime.timedelta(days=1))],user = request.user.id,type__in=['expense','income'])

            if bool(request.GET['subcategories']) and int(request.GET['subcategories']) != -1:
                category = request.GET['subcategories']
                if transactions.exists():
                    transactions = transactions & Transaction.objects.filter(id__in=TransactionItem.objects.filter(category=category).values('transaction').distinct())
                else:
                    transactions = Transaction.objects.filter(id__in=TransactionItem.objects.filter(category=category).values('transaction').distinct(),type__in=['expense','income'])
            elif bool(request.GET['categories']) and int(request.GET['categories']) != -1:
                category = Category.objects.filter(user = request.user.id,master_category=request.GET['categories'])
                category = category | Category.objects.filter(id=request.GET['categories'])
                if transactions.exists():
                    transactions = transactions & Transaction.objects.filter(id__in=TransactionItem.objects.filter(category__in=category).values('transaction').distinct(),type__in=['expense','income'])
                else:
                    transactions = Transaction.objects.filter(id__in=TransactionItem.objects.filter(category__in=category).values('transaction').distinct(),type__in=['expense','income'])

            if clean_data['planned']:
                if transactions.exists():
                    transactions = transactions & Transaction.objects.filter(id__in=TransactionItem.objects.filter(is_planned=clean_data['planned']).values('transaction').distinct(),type__in=['expense','income'])
                else:
                    transactions = Transaction.objects.filter(id__in=TransactionItem.objects.filter(is_planned=clean_data['planned']).values('transaction').distinct(),type__in=['expense','income'])
        
        paginator = Paginator(transactions,max_in_page)
        page_number = request.GET.get('page','1')
        try:
            transactions = paginator.page(page_number)
        except PageNotAnInteger:
            transactions = paginator.page(1)
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        page_number = paginator.get_page(page_number)

        return render(request, 'views/transaction/transactions.html',{'transactions': transactions,'page_number':page_number,'title':title})
    else:
        search_form = SearchForm(user = request.user)
    return render(request, 'views/transaction/transaction_search.html',{'search_form': search_form})
