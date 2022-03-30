from abc import ABC
from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase,Client
from django.urls import reverse
from financeAwareness.models.account import Account

from financeAwareness.models.category import Category
from financeAwareness.models.tag import Tag
from financeAwareness.models.transaction import Transaction
from financeAwareness.models.transactionItem import TransactionItem

class AbstractTestView(ABC):
    template = ""
    url_name = ""
    url = ""
    
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1")
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")

    def test_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name))       
        self.assertEqual(response.status_code,200)

    def test_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,self.template)

    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

class TestAccountList(AbstractTestView,TestCase):
    template = "views/account/accounts.html"
    url_name = "accounts"
    url = "/accounts"

class TestCategoryList(AbstractTestView,TestCase):
    template = "views/category/category.html"
    url_name = "categories"
    url = "/categories"

class TestTagList(AbstractTestView,TestCase):
    template = "views/tags.html"
    url_name = "tags"
    url = "/tags"

class TestTransactionList(AbstractTestView,TestCase):
    template = "views/transaction/transactions.html"
    url_name = "transactions"
    url = "/dashboard"

class TestRecurringList(AbstractTestView,TestCase):
    template = "views/transaction/transactions.html"
    url_name = "recurrings"
    url = "/transaction/recurring"

class TestPlannedList(AbstractTestView,TestCase):
    template = "views/transaction/transactions.html"
    url_name = "planned"
    url = "/transaction/planned"

class TestCategoryDetail(AbstractTestView,TestCase):
    template = "views/category/category_details.html"
    url_name = "category_details"
    url = "/categories/1"

    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(user=self.user,name='Test')
        self.category.id=1
        self.category.save()

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class TestTransactionDetail(AbstractTestView,TestCase):
    template = "views/transaction/transaction_details.html"
    url_name = "transaction_details"
    url = "/transaction/1"

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False)
        self.transaction = Transaction.objects.create(user=self.user,name='Sklep A', account=self.account,value = 123.45,date=datetime.now(),type='expense')
        self.category = Category.objects.create(user=self.user,name='Test')
        self.product = TransactionItem(transaction=self.transaction,category=self.category,item_name='Test',item_value=123.45,is_planned=True)
        self.transaction.id=1

        self.account.save()
        self.category.save()
        self.product.save()
        self.transaction.save()

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class TestRecurringDetail(AbstractTestView,TestCase):
    template = "views/transaction/transaction_details.html"
    url_name = "recurring_details"
    url = "/transaction/recurring/1"

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False)
        self.transaction = Transaction(user=self.user,name='Rachunek B', account=self.account,value = 123.45,date=datetime.now(),type='recurringExpense',recurring_type=('month'))
        self.category = Category.objects.create(user=self.user,name='Test')
        self.product = TransactionItem(transaction=self.transaction,category=self.category,item_name='Test',item_value=123.45,is_planned=True)
        self.transaction.id=1

        self.account.save()
        self.category.save()
        self.product.save()
        self.transaction.save()

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class TestPlannedDetail(AbstractTestView,TestCase):
    template = "views/transaction/transaction_details.html"
    url_name = "planned_details"
    url = "/transaction/planned/1"

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False)
        self.transaction = Transaction(user=self.user,name='Sklep C', account=self.account,value = 123.45,date=datetime.now(),type='planned')
        self.category = Category.objects.create(user=self.user,name='Test')
        self.product = TransactionItem(transaction=self.transaction,category=self.category,item_name='Test',item_value=123.45,is_planned=True)
        self.transaction.id=1

        self.account.save()
        self.category.save()
        self.product.save()
        self.transaction.save()

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class AbstractTestCreateUpdateDeleteView(ABC):
    template = ""
    url_name = ""
    url = ""
    post = ""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1")
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")

    def test_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name))       
        self.assertEqual(response.status_code,200)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,self.template)

    def test_post(self):
        response = self.client.post(self.url,self.post)
        self.assertEqual(response.status_code,302)

    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

class TestAccountCreate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "form.html"
    url_name = "new_account"
    url = "/accounts/new"  

    def setUp(self):
        super().setUp()
        self.post = {'name': ['TestAccountCreate'],'is_cash': ['True']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Account.objects.last().name,'TestAccountCreate')

class TestSavingGoalCreate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/account/saving_goal_form.html"
    url_name = "saving_goal_form"
    url = "/savings/new"  

    def setUp(self):
        super().setUp()
        self.post = {'name':['TestSavingGoalCreate'],'due_date':['26.03.2022'],'goal_value':['1000'],'is_active_saving_goal':['on']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Account.objects.last().name,'TestSavingGoalCreate')

class TestCategoryCreateIncome(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "form.html"
    url_name = "new_category"
    url = "/categories/new/income"  

    def setUp(self):
        super().setUp()
        self.post = {'name': ['TestCategoryCreateIncome']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Category.objects.last().name,'TestCategoryCreateIncome')

class TestCategoryCreate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "form.html"
    url_name = "new_category"
    url = "/categories/new/"  

    def setUp(self):
        super().setUp()
        self.post = {'name': ['TestCategoryCreate']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Category.objects.last().name,'TestCategoryCreate')

class TestSubcategoryCreate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "form.html"
    url_name = "subcategory_form"
    url = "/subcategories/new/1"  

    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(user=self.user,name='Test')
        self.category.id = 1
        self.category.save()
        self.post = {'name': ['TestSubcategoryCreate']}

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

    def test_post(self):
        super().test_post()
        self.assertEqual(Category.objects.last().name,'TestSubcategoryCreate')

class TestTagCreate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "form.html"
    url_name = "new_tag"
    url = "/tags/new"  

    def setUp(self):
        super().setUp()
        self.post = {'name': ['TestTagCreate']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Tag.objects.last().name,'TestTagCreate')

class TestAccountUpdate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "form.html"
    url_name = "account_form_update"
    url = "/accounts/update/1"  

    def setUp(self):
        super().setUp()
        Account.objects.create(user=self.user,name="TestAccountUpdate",is_cash=False, id=1).save()
        self.post = {'name': ['TestAccountUpdated'],'is_cash': ['on']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Account.objects.last().name,'TestAccountUpdated')

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class TestSavingGoalUpdate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/account/saving_goal_form.html"
    url_name = "saving_goal_form_update"
    url = "/savings/update/1"  

    def setUp(self):
        super().setUp()
        Account.objects.create(user=self.user,name="TestSavingGoalUpdate",is_active_saving_goal=False, id=1,goal_value=1000,due_date='2022-03-25',is_cash=False).save()
        self.post = {'name':['TestSavingGoalUpdated'],'due_date':['26.03.2022'],'goal_value':['1000'],'is_active_saving_goal':['on']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Account.objects.last().name,'TestSavingGoalUpdated')

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class TestCategoryUpdate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "form.html"
    url_name = "category_form_update"
    url = "/categories/update/1"  

    def setUp(self):
        super().setUp()
        Category.objects.create(user=self.user,name="TestCategoryUpdate", id=1).save()
        self.post = {'name': ['TestCategoryUpdated']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Category.objects.last().name,'TestCategoryUpdated')

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class TestSubcategoryUpdate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "form.html"
    url_name = "subcategory_form_update"
    url = "/subcategories/update/2"  

    def setUp(self):
        super().setUp() 
        category = Category.objects.create(user=self.user,name="TestSubcategoryMaster",id=1)
        Category.objects.create(user=self.user,name="TestSubcategoryUpdate", id=2,master_category=category).save()
        self.post = {'name': ['TestSubcategoryUpdated']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Category.objects.last().name,'TestSubcategoryUpdated')

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(2,)))       
        self.assertEqual(response.status_code,200)

class TestTagUpdate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "form.html"
    url_name = "tag_form_update"
    url = "/tags/update/1"  

    def setUp(self):
        super().setUp()
        Tag.objects.create(user=self.user,name="TestTagUpdate", id=1).save()
        self.post = {'name': ['TestTagUpdated']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Tag.objects.last().name,'TestTagUpdated')

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class TestSavingGoalComplated(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transfer_form.html"
    url_name = "saving_goal_accomplished"
    url = "/savings/completed/1"  

    def setUp(self):
        super().setUp()
        Account.objects.create(user=self.user,name="TestAccount",is_cash=False, id=1).save()
        Account.objects.create(user=self.user,name="TestSavingGoal",is_active_saving_goal=False, id=2,goal_value=1000,due_date='2022-03-25',is_cash=False).save()
        self.post = {'value': ['1000.0'], 'date': ['26.03.2022'], 'account': ['2'], 'transfer_account': ['1']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Account.objects.get(id=1).value,1000)
        self.assertTrue(Account.objects.get(id=2).accomplished_date)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)   

class TestAccountDelete(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "delete.html"
    url_name = "account_form_delete"
    url = "/accounts/delete/1"  

    def setUp(self):
        super().setUp()
        Account.objects.create(user=self.user,name="TestAccountDelete",is_cash=False, id=1).save()
        self.post = {}

    def test_post(self):
        super().test_post()
        self.assertEqual(Account.objects.count(),0)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)  

class TestSavingGoalDelete(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "delete.html"
    url_name = "saving_goal_form_delete"
    url = "/savings/delete/1"  

    def setUp(self):
        super().setUp()
        Account.objects.create(user=self.user,name="TestSavingGoalDelete",is_active_saving_goal=False, id=1,goal_value=1000,due_date='2022-03-25',is_cash=False).save()
        self.post = {}

    def test_post(self):
        super().test_post()
        self.assertEqual(Account.objects.count(),0)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)   

class CategoryDelete(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "delete.html"
    url_name = "category_form_delete"
    url = "/categories/delete/1"  

    def setUp(self):
        super().setUp()
        Category.objects.create(user=self.user,name="TestCategoryDelete", id=1).save()
        self.post = {}

    def test_post(self):
        super().test_post()
        self.assertEqual(Category.objects.count(),0)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class SubcategoryDelete(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "delete.html"
    url_name = "subcategory_form_delete"
    url = "/subcategories/delete/2"  

    def setUp(self):
        super().setUp()
        category = Category.objects.create(user=self.user,name="TestSubcategoryMaster",id=1)
        Category.objects.create(user=self.user,name="TestSubcategoryUpdate", id=2,master_category=category).save()
        self.post = {}

    def test_post(self):
        super().test_post()
        self.assertEqual(Category.objects.count(),1)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)    

class TestTagDelete(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "delete.html"
    url_name = "tag_form_delete"
    url = "/tags/delete/1"  

    def setUp(self):
        super().setUp()
        Tag.objects.create(user=self.user,name="TestTagDelete", id=1).save()
        self.post = {}

    def test_post(self):
        super().test_post()
        self.assertEqual(Tag.objects.count(),0)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)  

class TestTransferCreate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transfer_form.html"
    url_name = "transfer_form"
    url = "/accounts/transfer/new"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,name="TestAccount",is_cash=False, id=1,value=1000)
        self.account2 = Account.objects.create(user=self.user,name="TestAccount2",is_cash=True, id=2,value=500)
        self.post = {'value': ['1000.0'], 'date': ['26.03.2022'], 'account': ['2'], 'transfer_account': ['1']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Transaction.objects.count(),1)
        self.assertEqual(Account.objects.get(id=1).value,2000)
        self.assertEqual(Account.objects.get(id=2).value,-500)

class TestTransferUpdate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transfer_form.html"
    url_name = "transfer_form_update"
    url = "/accounts/transfer/update/1"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,name="TestAccount",is_cash=False, id=1,value=1000)
        self.account2 = Account.objects.create(user=self.user,name="TestAccount2",is_cash=False, id=2,value=500)
        Transaction.objects.create(user=self.user,name="Transfer", id=1,value=500,type='transfer',account=self.account,transfer_account=self.account2,date=datetime.now()).save()
        self.post = {'value': ['1000.0'], 'date': ['26.03.2022'], 'account': ['2'], 'transfer_account': ['1']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Account.objects.get(id=1).value,2000)
        self.assertEqual(Account.objects.get(id=2).value,-500)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)    

class TestTransferDelete(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "delete.html"
    url_name = "transfer_form_delete"
    url = "/accounts/transfer/delete/1"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,name="TestAccount",is_cash=False, id=1,value=1000)
        self.account2 = Account.objects.create(user=self.user,name="TestAccount2",is_cash=False, id=2,value=500)
        Transaction.objects.create(user=self.user,name="Transfer", id=1,value=500,type='transfer',account=self.account,transfer_account=self.account2,date=datetime.now()).save()
        self.post = {}

    def test_post(self):
        super().test_post()
        self.assertEqual(Transaction.objects.count(),0)
        self.assertEqual(Account.objects.get(id=1).value,1500)
        self.assertEqual(Account.objects.get(id=2).value,0)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)                  

class TestCreateExpense(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transaction_form.html"
    url_name = "new_expense"
    url = "/transaction/expense/new"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()     
        self.post = {'name': ['Test'],
        'account': [self.account.id],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'image': [''],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5'], 
        'is_planned': ['True', 'False']}

    def test_post(self):
        super().test_post()       
        self.assertEqual(Account.objects.get(id=1).value,89.5)
        self.assertEqual(Transaction.objects.last().name,'Test')

class TestCreateIncome(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transaction_form.html"
    url_name = "new_income"
    url = "/transaction/income/new"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=True)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=True)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()     
        self.post = {'name': ['Test'],
        'account': [self.account.id],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'image': [''],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5'], 
        'is_planned': ['True', 'False']}

    def test_post(self):
        super().test_post()       
        self.assertEqual(Account.objects.get(id=1).value,110.5)
        self.assertEqual(Transaction.objects.last().name,'Test')

class TestCreatePlannedExpense(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transaction_form.html"
    url_name = "new_planned"
    url = "/transaction/planned/new"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()     
        self.post = {'name': ['Test'],
        'account': [self.account.id],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'image': [''],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5']
        }

    def test_post(self):
        super().test_post()
        self.assertEqual(Transaction.objects.last().name,'Test')

class TestCreateRecurringExpense(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transaction_form.html"
    url_name = "new_reccuring_expense"
    url = "/transaction/recurring/expense/new"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()     
        self.post = {'name': ['Test'],
        'account': [self.account.id],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'recurring_type': ['month'],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5']
        }

    def test_post(self):
        super().test_post()       
        self.assertEqual(Transaction.objects.last().name,'Test')

class TestCreateRecurringIncome(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transaction_form.html"
    url_name = "new_reccuring_income"
    url = "/transaction/recurring/income/new"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=True)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=True)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()     
        self.post = {'name': ['Test'],
        'account': [self.account.id],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],       
        'recurring_type': ['month'],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5'],
        }

    def test_post(self):
        super().test_post()       
        self.assertEqual(Transaction.objects.last().name,'Test')

class TestTransactionUpdate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transaction_form.html"
    url_name = "transaction_form_update"
    url = "/transaction/1/update"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()
        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=100,date=datetime.now(), type='expense')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=4.5, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()        
        self.post = {'name': ['TestExpenseUpdated'],
        'account': [self.account.id],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'image': [''],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5'], 
        'is_planned': ['True', 'False']}

    def test_post_expense(self):
        super().test_post()       
        self.assertEqual(Account.objects.get(id=1).value,189.5)
        self.assertEqual(Transaction.objects.last().name,'TestExpenseUpdated')

    def test_post_expense_changed_accounts(self):
        Account.objects.create(user=self.user,is_cash=False,name='Test',id=2, value=100).save()
        self.post = {'name': ['TestExpenseUpdated'],
        'account': ['2'],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'image': [''],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5'], 
        'is_planned': ['True', 'False']}
        super().test_post()       
        self.assertEqual(Account.objects.get(id=1).value,200)
        self.assertEqual(Account.objects.get(id=2).value,89.5)
        self.assertEqual(Transaction.objects.get(id=1).name,'TestExpenseUpdated')

    def test_post_income(self):
        self.category.is_income=True
        self.category.save()
        self.category2.is_income=True
        self.category2.save()
        self.transaction.type='income'
        self.transaction.save()
        self.post = {'name': ['TestIncomeUpdated'],
        'account': ['1'],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'image': [''],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5'], 
        'is_planned': ['True', 'False']}
        super().test_post()
        self.assertEqual(Account.objects.get(id=1).value,10.5)
        self.assertEqual(Transaction.objects.get(id=1).name,'TestIncomeUpdated')

    def test_post_income_changed_accounts(self):
        Account.objects.create(user=self.user,is_cash=False,name='Test',id=2, value=100).save()
        self.category.is_income=True
        self.category.save()
        self.category2.is_income=True
        self.category2.save()
        self.transaction.type='income'
        self.transaction.save()
        self.post = {'name': ['TestIncomeUpdated'],
        'account': ['2'],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'image': [''],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5'], 
        'is_planned': ['True', 'False']}
        super().test_post()
        self.assertEqual(Account.objects.get(id=1).value,0)
        self.assertEqual(Account.objects.get(id=2).value,110.5)
        self.assertEqual(Transaction.objects.get(id=1).name,'TestIncomeUpdated')

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)    

class TestRecurringUpdate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transaction_form.html"
    url_name = "recurring_form_update"
    url = "/transaction/recurring/1/update"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()
        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=100,date=datetime.now(), type='recurringExpense', recurring_type='month')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=4.5, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()        
        self.post = {'name': ['TestUpdated'],
        'account': [self.account.id],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'recurring_type': ['month'],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5'], 
        'is_planned': ['True', 'False']}

    def test_post(self):
        super().test_post()       
        self.assertEqual(Transaction.objects.get(id=1).name,'TestUpdated')

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class TestRecurringAdd(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transaction_form.html"
    url_name = "recurring_form_add"
    url = "/transaction/recurring/1/add"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()
        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=100,date='2022-02-01', type='recurringExpense', recurring_type='month')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=4.5, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()        
        self.post = {'name': ['TestAdd'],
        'account': [self.account.id],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5'], 
        'is_planned': ['True', 'False']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Transaction.objects.get(id=1).name,'test')
        self.assertEqual(str(Transaction.objects.get(id=1).date),'2022-03-01')       
        self.assertEqual(Transaction.objects.latest('id').name,'TestAdd')
        self.assertEqual(Account.objects.get(id=1).value,89.5)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class TestPlannedUpdate(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transaction_form.html"
    url_name = "planned_form_update"
    url = "/transaction/planned/1/update"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()
        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=100,date=datetime.now(), type='planned')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=4.5, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()        
        self.post = {'name': ['TestUpdated'],
        'account': [self.account.id],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'image': [''],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5'], 
        'is_planned': ['True', 'False']}

    def test_post(self):
        super().test_post()       
        self.assertEqual(Transaction.objects.get(id=1).name,'TestUpdated')

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)

class TestPlannedAdd(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "views/transaction/transaction_form.html"
    url_name = "planned_form_add"
    url = "/transaction/planned/1/add"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()
        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=100,date=datetime.now(), type='planned')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=4.5, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()        
        self.post = {'name': ['TestUpdated'],
        'account': [self.account.id],
        'value': ['10.5'],
        'description': [''],
        'date': ['25.03.2022'],
        'image': [''],
        'item_name': ['TestItem', 'TestItem2'],
        'category': [self.category.id, self.category2.id],
        'subcategory': ['-1', self.subcategory.id],
        'item_value': ['4.5', '5.5'], 
        'is_planned': ['True', 'False']}

    def test_post(self):
        super().test_post()
        self.assertEqual(Account.objects.get(id=1).value,89.5)       
        self.assertEqual(Transaction.objects.get(id=1).name,'TestUpdated')
        self.assertEqual(Transaction.objects.get(id=1).type,'expense')

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200)      
      
class TestTransactionDelete(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "delete.html"
    url_name = "transaction_form_delete"
    url = "/transaction/1/delete"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()
        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=100,date=datetime.now(), type='expense')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=4.5, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save() 
        self.post = {}

    def test_post(self):
        super().test_post()
        self.assertEqual(Tag.objects.count(),0)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200) 

class TestRecurringDelete(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "delete.html"
    url_name = "recurring_form_delete"
    url = "/transaction/recurring/1/delete"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=100,date=datetime.now(), type='recurringExpense', recurring_type='month')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=4.5, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save() 
        self.post = {}

    def test_post(self):
        super().test_post()
        self.assertEqual(Tag.objects.count(),0)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200) 

class TestPlannedDelete(AbstractTestCreateUpdateDeleteView,TestCase):
    template = "delete.html"
    url_name = "planned_form_delete"
    url = "/transaction/planned/1/delete"  

    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()
        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=100,date=datetime.now(), type='planned')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=4.5, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()   
        self.post = {}

    def test_post(self):
        super().test_post()
        self.assertEqual(Tag.objects.count(),0)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:'+self.url_name,args=(1,)))       
        self.assertEqual(response.status_code,200) 

class TestPlannedPDF(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1")
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")
        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save() 
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=2),id=3)
        self.subcategory.save()
        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=100,date=datetime.now(), type='planned')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=4.5, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()
    
    def test_get(self):
        response = self.client.get('/transaction/1/pdf')
        self.assertEquals(response.get('Content-Disposition'),'attachment; filename="test.pdf"')

    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get('/transaction/1/pdf')
        self.assertEqual(response.status_code, 302)

class TestAJAXSubcategory(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1",id=1)
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=Category.objects.get(id=1),id=3)
        self.subcategory.save()
    
    def test_get(self):
        response = self.client.get('/transaction/ajax/subcategories',{'category': ['1']},xhr=True)
        self.assertEqual(response.status_code,200)
        self.assertJSONEqual(response.content,{"subcategories": '[{"model": "financeAwareness.category", "pk": 3, "fields": {"name": "Test_subcategory", "user": 1, "master_category": 1, "is_income": null}}]'})

    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get('/transaction/ajax/subcategories',{'category': ['1']},xhr=True)
        self.assertEqual(response.status_code, 302)

class TestAJAXCategory(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1",id=1)
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")
        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test',id=2,is_income=True)
        self.category2.save()
    
    def test_get_income(self):
        response = self.client.get('/transaction/ajax/categories',{'transaction_type': ['True']},xhr=True)
        self.assertEqual(response.status_code,200)
        self.assertJSONEqual(response.content,{"categories": '[{"model": "financeAwareness.category", "pk": 2, "fields": {"name": "Test", "user": 1, "master_category": null, "is_income": true}}]'})

    def test_get(self):
        response = self.client.get('/transaction/ajax/categories',{'transaction_type': ['False']},xhr=True)
        self.assertEqual(response.status_code,200)
        self.assertJSONEqual(response.content,{"categories": '[{"model": "financeAwareness.category", "pk": 1, "fields": {"name": "Test", "user": 1, "master_category": null, "is_income": false}}]'})

    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get('/transaction/ajax/categories',{'transaction_type': ['False']},xhr=True)
        self.assertEqual(response.status_code, 302)
   
class TestReports(TestCase):
    url='/reports'
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1",id=1)
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")

        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()

        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=True)
        self.category2.save()
        self.category3 = Category.objects.create(user=self.user,name='Test3',id=3)
        self.category3.save()

        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=90,date=datetime.now(), type='expense')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=50, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()
        self.transaction_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem2', item_value=40, is_planned=False,category=Category.objects.get(id=3))
        self.transaction_item2.save()

        self.transaction2 = Transaction.objects.create(user=self.user,id=2,name="test2",account=Account.objects.get(id=1),value=120,date=datetime.now(), type='income')
        self.transaction2.save()
        self.transaction2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=2), item_name='TestItem3', item_value=120, is_planned=True,category=Category.objects.get(id=2))
        self.transaction2_item.save()

        self.transactionR = Transaction.objects.create(user=self.user,id=3,name="testR",account=Account.objects.get(id=1),value=110,date=datetime.now(), type='recurringExpense', recurring_type='month')
        self.transactionR.save()
        self.transactionR_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=3), item_name='TestItem4', item_value=110, is_planned=True,category=Category.objects.get(id=1))
        self.transactionR_item.save()

        self.tag = Tag(user=self.user,name='Test',id=1)
        self.tag.save()
        self.tag2 = Tag(user=self.user,name='Test2',id=2)
        self.tag2.save()

        self.transaction.tags.add(self.tag)
        self.transaction2.tags.add(self.tag2)
    
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['labels'],['Wydatek', 'Przychód'])
        self.assertEqual(response.context['data_exp_in'],[90, 120])
        self.assertEqual(response.context['labels_r'],['Wydatek', 'Przychód'])
        self.assertEqual(response.context['data_r_exp_in'],[110,0])
        self.assertEqual(response.context['labels_c_e'],['Test','Test3'])
        self.assertEqual(response.context['data_c_e'],[50,40])
        self.assertEqual(response.context['labels_planned'],['Zaplanowane', 'Nieplanowane'])
        self.assertEqual(response.context['data_planned'],[50, 40])
        self.assertEqual(response.context['labels_tags'],['Test', 'Test2'])
        self.assertEqual(response.context['data_tags'],[90, 120])
        self.assertTemplateUsed('views/report/reports.html')
        
    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:reports_list'))       
        self.assertEqual(response.status_code,200)

class TestReportExpenseIncome(TestCase):
    url='/reports/details'
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1",id=1)
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")

        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()

        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=True)
        self.category2.save()
        self.category3 = Category.objects.create(user=self.user,name='Test3',id=3)
        self.category3.save()

        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=90,date=datetime.now(), type='expense')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=50, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()
        self.transaction_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem2', item_value=40, is_planned=False,category=Category.objects.get(id=3))
        self.transaction_item2.save()

        self.transaction2 = Transaction.objects.create(user=self.user,id=2,name="test2",account=Account.objects.get(id=1),value=120,date=datetime.now(), type='income')
        self.transaction2.save()
        self.transaction2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=2), item_name='TestItem3', item_value=120, is_planned=True,category=Category.objects.get(id=2))
        self.transaction2_item.save()

        self.transactionD = Transaction.objects.create(user=self.user,id=3,name="test",account=Account.objects.get(id=1),value=10,date='2022-01-01', type='expense')
        self.transactionD.save()
        self.transactionD_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=3), item_name='TestItem', item_value=10, is_planned=True,category=Category.objects.get(id=1))
        self.transactionD_item.save()

        self.transactionD2 = Transaction.objects.create(user=self.user,id=4,name="test2",account=Account.objects.get(id=1),value=20,date='2022-01-31', type='income')
        self.transactionD2.save()
        self.transactionD2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=4), item_name='TestItem3', item_value=20, is_planned=True,category=Category.objects.get(id=2))
        self.transactionD2_item.save()
    
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['labels'],['Wydatek', 'Przychód'])
        self.assertEqual(response.context['data'],[90, 120])
        self.assertTemplateUsed('views/report/report_expense_income.html')

    def test_custom_date(self):
        response = self.client.get(self.url,{'date_from': ['01.01.2022'],'date_to': ['31.01.2022']})
        self.assertEqual(response.context['labels'],['Wydatek', 'Przychód'])
        self.assertEqual(response.context['data'],[10, 20])
        self.assertTemplateUsed('views/report/report_expense_income.html')
        
    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:report_expense_income_details'))       
        self.assertEqual(response.status_code,200)

class TestReportTags(TestCase):
    url='/reports/tags'
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1",id=1)
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")

        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()

        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=True)
        self.category2.save()
        self.category3 = Category.objects.create(user=self.user,name='Test3',id=3)
        self.category3.save()

        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=90,date=datetime.now(), type='expense')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=50, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()
        self.transaction_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem2', item_value=40, is_planned=False,category=Category.objects.get(id=3))
        self.transaction_item2.save()

        self.transaction2 = Transaction.objects.create(user=self.user,id=2,name="test2",account=Account.objects.get(id=1),value=120,date=datetime.now(), type='income')
        self.transaction2.save()
        self.transaction2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=2), item_name='TestItem3', item_value=120, is_planned=True,category=Category.objects.get(id=2))
        self.transaction2_item.save()

        self.tag = Tag(user=self.user,name='Test',id=1)
        self.tag.save()
        self.tag2 = Tag(user=self.user,name='Test2',id=2)
        self.tag2.save()

        self.transaction.tags.add(self.tag)
        self.transaction2.tags.add(self.tag2)

        self.transactionD = Transaction.objects.create(user=self.user,id=3,name="test",account=Account.objects.get(id=1),value=10,date='2022-01-01', type='expense')
        self.transactionD.save()
        self.transactionD_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=3), item_name='TestItem', item_value=10, is_planned=True,category=Category.objects.get(id=1))
        self.transactionD_item.save()

        self.transactionD2 = Transaction.objects.create(user=self.user,id=4,name="test2",account=Account.objects.get(id=1),value=20,date='2022-01-31', type='income')
        self.transactionD2.save()
        self.transactionD2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=4), item_name='TestItem3', item_value=20, is_planned=True,category=Category.objects.get(id=2))
        self.transactionD2_item.save()

        self.transactionD.tags.add(self.tag)
        self.transactionD2.tags.add(self.tag2)
    
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['labels'],['Test', 'Test2'])
        self.assertEqual(response.context['data'],[90, 120])
        self.assertTemplateUsed('views/report/report_tag.html')

    def test_custom_date(self):
        response = self.client.get(self.url,{'date_from': ['01.01.2022'],'date_to': ['31.01.2022']})
        self.assertEqual(response.context['labels'],['Test', 'Test2'])
        self.assertEqual(response.context['data'],[10, 20])
        self.assertTemplateUsed('views/report/report_tag.html')
        
    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:report_tags_details'))       
        self.assertEqual(response.status_code,200)

class TestReportPlanned(TestCase):
    url='/reports/planned'
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1",id=1)
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")

        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()

        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save()
        self.category3 = Category.objects.create(user=self.user,name='Test3',id=3)
        self.category3.save()

        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=90,date=datetime.now(), type='expense')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=50, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()
        self.transaction_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem2', item_value=40, is_planned=False,category=Category.objects.get(id=3))
        self.transaction_item2.save()

        self.transaction2 = Transaction.objects.create(user=self.user,id=2,name="test2",account=Account.objects.get(id=1),value=120,date=datetime.now(), type='expense')
        self.transaction2.save()
        self.transaction2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=2), item_name='TestItem3', item_value=120, is_planned=True,category=Category.objects.get(id=2))
        self.transaction2_item.save()

        self.tag = Tag(user=self.user,name='Test',id=1)
        self.tag.save()
        self.tag2 = Tag(user=self.user,name='Test2',id=2)
        self.tag2.save()

        self.transactionD = Transaction.objects.create(user=self.user,id=3,name="test",account=Account.objects.get(id=1),value=10,date='2022-01-01', type='expense')
        self.transactionD.save()
        self.transactionD_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=3), item_name='TestItem', item_value=10, is_planned=True,category=Category.objects.get(id=1))
        self.transactionD_item.save()

        self.transactionD2 = Transaction.objects.create(user=self.user,id=4,name="test2",account=Account.objects.get(id=1),value=20,date='2022-01-31', type='expense')
        self.transactionD2.save()
        self.transactionD2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=4), item_name='TestItem3', item_value=20, is_planned=False,category=Category.objects.get(id=2))
        self.transactionD2_item.save()
    
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['labels'],['Zaplanowane', 'Nieplanowane'])
        self.assertEqual(response.context['data'],[170, 40])
        self.assertTemplateUsed('views/report/report_planned.html')

    def test_custom_date(self):
        response = self.client.get(self.url,{'date_from': ['01.01.2022'],'date_to': ['31.01.2022']})
        self.assertEqual(response.context['labels'],['Zaplanowane', 'Nieplanowane'])
        self.assertEqual(response.context['data'],[10, 20])
        self.assertTemplateUsed('views/report/report_planned.html')
        
    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:report_planned_details'))       
        self.assertEqual(response.status_code,200)

class TestReportCategory(TestCase):
    url='/reports/category'
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1",id=1)
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")

        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()

        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=False)
        self.category2.save()
        self.category3 = Category.objects.create(user=self.user,name='Test3',master_category=Category.objects.get(id=1),id=3)
        self.category3.save()
        self.category4 = Category.objects.create(user=self.user,name='Test4',master_category=Category.objects.get(id=1),id=4)
        self.category4.save()
        self.category5 = Category.objects.create(user=self.user,name='Test5',master_category=Category.objects.get(id=2),id=5)
        self.category5.save()
        self.category6 = Category.objects.create(user=self.user,name='Test6',master_category=Category.objects.get(id=2),id=6)
        self.category6.save()

        self.transaction = Transaction.objects.create(user=self.user,id=1,name="test",account=Account.objects.get(id=1),value=250,date=datetime.now(), type='expense')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=10, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()
        self.transaction_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem2', item_value=120, is_planned=False,category=Category.objects.get(id=3))
        self.transaction_item2.save()
        self.transaction_item3 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem3', item_value=30, is_planned=False,category=Category.objects.get(id=4))
        self.transaction_item3.save()
        self.transaction_item4 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem4', item_value=40, is_planned=False,category=Category.objects.get(id=4))
        self.transaction_item4.save()
        self.transaction_item5 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem5', item_value=50, is_planned=False,category=Category.objects.get(id=4))
        self.transaction_item5.save()

        self.transaction2 = Transaction.objects.create(user=self.user,id=2,name="test2",account=Account.objects.get(id=1),value=200,date=datetime.now(), type='expense')
        self.transaction2.save()
        self.transaction2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=2), item_name='Test2Item', item_value=10, is_planned=True,category=Category.objects.get(id=4))
        self.transaction2_item.save()
        self.transaction2_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=2), item_name='Test2Item2', item_value=20, is_planned=False,category=Category.objects.get(id=5))
        self.transaction2_item2.save()
        self.transaction2_item3 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=2), item_name='Test2Item3', item_value=30, is_planned=True,category=Category.objects.get(id=5))
        self.transaction2_item3.save()
        self.transaction2_item4 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=2), item_name='Test2Item4', item_value=140, is_planned=False,category=Category.objects.get(id=6))
        self.transaction2_item4.save()

        self.categoryI = Category.objects.create(user=self.user,name='TestI',id=7,is_income=True)
        self.categoryI.save()
        self.categoryI2 = Category.objects.create(user=self.user,name='TestI2',id=8,is_income=True)
        self.categoryI2.save()
        self.categoryI3 = Category.objects.create(user=self.user,name='TestI3',master_category=Category.objects.get(id=7),id=9)
        self.categoryI3.save()
        self.categoryI4 = Category.objects.create(user=self.user,name='TestI4',master_category=Category.objects.get(id=7),id=10)
        self.categoryI4.save()
        self.categoryI5 = Category.objects.create(user=self.user,name='TestI5',master_category=Category.objects.get(id=8),id=11)
        self.categoryI5.save()
        self.categoryI6 = Category.objects.create(user=self.user,name='TestI6',master_category=Category.objects.get(id=8),id=12)
        self.categoryI6.save()

        self.transactionI = Transaction.objects.create(user=self.user,id=3,name="test",account=Account.objects.get(id=1),value=250,date=datetime.now(), type='income')
        self.transactionI.save()
        self.transactionI_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=3), item_name='TestIItem', item_value=10, is_planned=True,category=Category.objects.get(id=7))
        self.transactionI_item.save()
        self.transactionI_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=3), item_name='TestIItem2', item_value=120, is_planned=False,category=Category.objects.get(id=9))
        self.transactionI_item2.save()
        self.transactionI_item3 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=3), item_name='TestIItem3', item_value=30, is_planned=False,category=Category.objects.get(id=10))
        self.transactionI_item3.save()
        self.transactionI_item4 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=3), item_name='TestIItem4', item_value=40, is_planned=False,category=Category.objects.get(id=10))
        self.transactionI_item4.save()
        self.transactionI_item5 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=3), item_name='TestIItem5', item_value=50, is_planned=False,category=Category.objects.get(id=10))
        self.transactionI_item5.save()

        self.transactionI2 = Transaction.objects.create(user=self.user,id=4,name="test2",account=Account.objects.get(id=1),value=200,date=datetime.now(), type='income')
        self.transactionI2.save()
        self.transactionI2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=4), item_name='Test2IItem', item_value=10, is_planned=True,category=Category.objects.get(id=10))
        self.transactionI2_item.save()
        self.transactionI2_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=4), item_name='Test2IItem2', item_value=20, is_planned=False,category=Category.objects.get(id=11))
        self.transactionI2_item2.save()
        self.transactionI2_item3 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=4), item_name='Test2IItem3', item_value=30, is_planned=True,category=Category.objects.get(id=11))
        self.transactionI2_item3.save()
        self.transactionI2_item4 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=4), item_name='Test2IItem4', item_value=140, is_planned=False,category=Category.objects.get(id=12))
        self.transactionI2_item4.save()
    
        #Date check
        self.transaction = Transaction.objects.create(user=self.user,id=5,name="test",account=Account.objects.get(id=1),value=250,date='2022-01-01', type='expense')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=5), item_name='TestItem', item_value=10, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()
        self.transaction_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=5), item_name='TestItem2', item_value=120, is_planned=False,category=Category.objects.get(id=3))
        self.transaction_item2.save()
        self.transaction_item3 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=5), item_name='TestItem3', item_value=30, is_planned=False,category=Category.objects.get(id=4))
        self.transaction_item3.save()
        self.transaction_item4 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=5), item_name='TestItem4', item_value=40, is_planned=False,category=Category.objects.get(id=4))
        self.transaction_item4.save()
        self.transaction_item5 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=5), item_name='TestItem5', item_value=50, is_planned=False,category=Category.objects.get(id=4))
        self.transaction_item5.save()

        self.transaction2 = Transaction.objects.create(user=self.user,id=6,name="test2",account=Account.objects.get(id=1),value=200,date='2022-01-31', type='expense')
        self.transaction2.save()
        self.transaction2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=6), item_name='Test2Item', item_value=10, is_planned=True,category=Category.objects.get(id=4))
        self.transaction2_item.save()
        self.transaction2_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=6), item_name='Test2Item2', item_value=20, is_planned=False,category=Category.objects.get(id=5))
        self.transaction2_item2.save()
        self.transaction2_item3 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=6), item_name='Test2Item3', item_value=30, is_planned=True,category=Category.objects.get(id=5))
        self.transaction2_item3.save()
        self.transaction2_item4 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=6), item_name='Test2Item4', item_value=140, is_planned=False,category=Category.objects.get(id=6))
        self.transaction2_item4.save()

        self.transactionI = Transaction.objects.create(user=self.user,id=7,name="test",account=Account.objects.get(id=1),value=250,date='2022-01-01', type='income')
        self.transactionI.save()
        self.transactionI_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=7), item_name='TestIItem', item_value=10, is_planned=True,category=Category.objects.get(id=7))
        self.transactionI_item.save()
        self.transactionI_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=7), item_name='TestIItem2', item_value=120, is_planned=False,category=Category.objects.get(id=9))
        self.transactionI_item2.save()
        self.transactionI_item3 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=7), item_name='TestIItem3', item_value=30, is_planned=False,category=Category.objects.get(id=10))
        self.transactionI_item3.save()
        self.transactionI_item4 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=7), item_name='TestIItem4', item_value=40, is_planned=False,category=Category.objects.get(id=10))
        self.transactionI_item4.save()
        self.transactionI_item5 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=7), item_name='TestIItem5', item_value=50, is_planned=False,category=Category.objects.get(id=10))
        self.transactionI_item5.save()

        self.transactionI2 = Transaction.objects.create(user=self.user,id=8,name="test2",account=Account.objects.get(id=1),value=200,date='2022-01-31', type='income')
        self.transactionI2.save()
        self.transactionI2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=8), item_name='Test2IItem', item_value=10, is_planned=True,category=Category.objects.get(id=10))
        self.transactionI2_item.save()
        self.transactionI2_item2 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=8), item_name='Test2IItem2', item_value=20, is_planned=False,category=Category.objects.get(id=11))
        self.transactionI2_item2.save()
        self.transactionI2_item3 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=8), item_name='Test2IItem3', item_value=30, is_planned=True,category=Category.objects.get(id=11))
        self.transactionI2_item3.save()
        self.transactionI2_item4 = TransactionItem.objects.create(transaction=Transaction.objects.get(id=8), item_name='Test2IItem4', item_value=140, is_planned=False,category=Category.objects.get(id=12))
        self.transactionI2_item4.save()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['labels'],['Test', 'Test2'])
        self.assertEqual(response.context['data'],[260, 190])
        self.assertEqual(response.context['labels_subcategories'],['Test3', 'Test4'])
        self.assertEqual(response.context['data_subcategories'],[120, 130])
        self.assertEqual(response.context['labels_income'],['TestI', 'TestI2'])
        self.assertEqual(response.context['data_income'],[260, 190])
        self.assertEqual(response.context['labels_income_subcategories'],['TestI3','TestI4'])
        self.assertEqual(response.context['data_income_subcategories'],[120, 130])
        self.assertTemplateUsed('views/report/report_category.html')

    def test_custom_date(self):
        response = self.client.get(self.url,{'date_from': ['01.01.2022'],'date_to': ['31.01.2022'],'category_expense':[''],'category_income':['']})
        self.assertEqual(response.context['labels'],['Test', 'Test2'])
        self.assertEqual(response.context['data'],[260, 190])
        self.assertEqual(response.context['labels_subcategories'],['Test3', 'Test4'])
        self.assertEqual(response.context['data_subcategories'],[120, 130])
        self.assertEqual(response.context['labels_income'],['TestI', 'TestI2'])
        self.assertEqual(response.context['data_income'],[260, 190])
        self.assertEqual(response.context['labels_income_subcategories'],['TestI3','TestI4'])
        self.assertEqual(response.context['data_income_subcategories'],[120, 130])
        self.assertTemplateUsed('views/report/report_category.html')
        
    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:report_category_details'))       
        self.assertEqual(response.status_code,200)

class TestReportRecurring(TestCase):
    url='/reports/recurring'
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1",id=1)
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")

        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()

        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.transaction = Transaction.objects.create(user=self.user,id=1,name="TestW",account=Account.objects.get(id=1),value=10,date=datetime.now(), type='recurringExpense', recurring_type='week')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=1.5, is_planned=True,category=Category.objects.get(id=1))
        self.transaction_item.save()

        self.transaction2 = Transaction.objects.create(user=self.user,id=2,name="TestM",account=Account.objects.get(id=1),value=20,date=datetime.now(), type='recurringExpense', recurring_type='month')
        self.transaction2.save()
        self.transaction2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=2.5, is_planned=True,category=Category.objects.get(id=1))
        self.transaction2_item.save() 

        self.transaction3 = Transaction.objects.create(user=self.user,id=3,name="TestQ",account=Account.objects.get(id=1),value=30,date=datetime.now(), type='recurringExpense', recurring_type='quarter')
        self.transaction3.save()
        self.transaction3_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=3, is_planned=True,category=Category.objects.get(id=1))
        self.transaction3_item.save() 

        self.transaction4 = Transaction.objects.create(user=self.user,id=4,name="TestY",account=Account.objects.get(id=1),value=40,date=datetime.now(), type='recurringExpense', recurring_type='year')
        self.transaction4.save()
        self.transaction4_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=4, is_planned=True,category=Category.objects.get(id=1))
        self.transaction4_item.save()  

        #Date check
        self.transactionD = Transaction.objects.create(user=self.user,id=5,name="Test",account=Account.objects.get(id=1),value=10,date='2022-01-01', type='recurringExpense', recurring_type='month')
        self.transactionD.save()
        self.transactionD_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=10, is_planned=True,category=Category.objects.get(id=1))
        self.transactionD_item.save()



    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['labels'],['Wydatek'])
        self.assertEqual(response.context['data'],[100])
        self.assertEqual(response.context['labels_week'],['Wydatek'])
        self.assertEqual(response.context['data_week'],[10])
        self.assertEqual(response.context['labels_quarter'],['Wydatek'])
        self.assertEqual(response.context['data_quarter'],[30])
        self.assertEqual(response.context['labels_year'],['Wydatek'])
        self.assertEqual(response.context['data_year'],[40])
        self.assertEqual(response.context['labels_month'],['Wydatek'])
        self.assertEqual(response.context['data_month'],[30])
        self.assertEqual(response.context['labels_all'],['TestW', 'TestM', 'TestQ', 'TestY', 'Test'])
        self.assertEqual(response.context['data_all'],[10, 20, 30, 40, 10])
        self.assertTemplateUsed('views/report/report_recurring.html')

    def test_custom_date(self):
        response = self.client.get(self.url,{'date_from': ['01.01.2022'],'date_to': ['31.01.2022']})
        self.assertEqual(response.context['labels'],['Wydatek'])
        self.assertEqual(response.context['data'],[10])
        self.assertTemplateUsed('views/report/report_recurring.html')
        
    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:report_recurring_details'))       
        self.assertEqual(response.status_code,200)

class TestSearch(TestCase):
    url='/transaction/search'
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1",id=1)
        self.user.save()
        self.client = Client()
        self.client.login(username="PanTest", password="DjangoTest1")

        self.account = Account.objects.create(user=self.user,is_cash=False,name='Test',id=1, value=100)
        self.account.save()

        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',id=2,is_income=True)
        self.category2.save()
        self.category3 = Category.objects.create(user=self.user,name='Test3',master_category=Category.objects.get(id=1),id=3)
        self.category3.save()
        self.category4 = Category.objects.create(user=self.user,name='Test4',master_category=Category.objects.get(id=1),id=4)
        self.category4.save()
        self.category5 = Category.objects.create(user=self.user,name='Test5',master_category=Category.objects.get(id=2),id=5)
        self.category5.save()

        self.transaction = Transaction.objects.create(user=self.user,id=1,name="Test",account=Account.objects.get(id=1),value=10,date='2022-01-01', type='expense')
        self.transaction.save()
        self.transaction_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=1), item_name='TestItem', item_value=1.5, is_planned=True,category=Category.objects.get(id=3))
        self.transaction_item.save()

        self.transaction2 = Transaction.objects.create(user=self.user,id=2,name="Test2",account=Account.objects.get(id=1),value=10,date=datetime.now(), type='income')
        self.transaction2.save()
        self.transaction2_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=2), item_name='TestItem', item_value=1.5, is_planned=False,category=Category.objects.get(id=5))
        self.transaction2_item.save()

        self.transaction3 = Transaction.objects.create(user=self.user,id=3,name="Test3",account=Account.objects.get(id=1),value=10,date=datetime.now(), type='expense')
        self.transaction3.save()
        self.transaction3_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=3), item_name='TestItem', item_value=1.5, is_planned=False,category=Category.objects.get(id=3))
        self.transaction3_item.save()
        self.transaction4_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=3), item_name='TestItem', item_value=1.5, is_planned=True,category=Category.objects.get(id=4))
        self.transaction4_item.save()

        self.transactionR = Transaction.objects.create(user=self.user,id=4,name="TestR",account=Account.objects.get(id=1),value=10,date=datetime.now(), type='recurringExpense', recurring_type='week')
        self.transactionR.save()
        self.transactionR_item = TransactionItem.objects.create(transaction=Transaction.objects.get(id=4), item_name='TestItem', item_value=1.5, is_planned=True,category=Category.objects.get(id=1))
        self.transactionR_item.save()
        
        self.tag = Tag(user=self.user,name='Test',id=1)
        self.tag.save()
        self.tag2 = Tag(user=self.user,name='Test2',id=2)
        self.tag2.save()

        self.transaction.tags.add(self.tag)
        self.transaction2.tags.add(self.tag2)

    def test_planned(self):
        response = self.client.get(self.url,{'date_from': [''],'date_to': [''],'categories':['-1'],'subcategories':['-1'],'planned':['True'],'search':['']})
        self.assertTemplateUsed('views/transaction/transactions.html')
        self.assertEqual(response.context['transactions'].object_list,[self.transaction3,self.transaction])

    def test_categories(self):
        response = self.client.get(self.url,{'date_from': [''],'date_to': [''],'categories':['1'],'subcategories':['-1'],'planned':[''],'search':['']})
        self.assertTemplateUsed('views/transaction/transactions.html')
        self.assertEqual(response.context['transactions'].object_list,[self.transaction3,self.transaction])

    def test_subcategories(self):
        response = self.client.get(self.url,{'date_from': [''],'date_to': [''],'categories':['1'],'subcategories':['4'],'planned':[''],'search':['']})
        self.assertTemplateUsed('views/transaction/transactions.html')
        self.assertEqual(response.context['transactions'].object_list,[self.transaction3])

    def test_word(self):
        response = self.client.get(self.url,{'date_from': [''],'date_to': [''],'categories':['-1'],'subcategories':['-1'],'planned':[''],'search':['Test2']})
        self.assertTemplateUsed('views/transaction/transactions.html')
        self.assertEqual(response.context['transactions'].object_list,[self.transaction2])

    def test_tags(self):
        response = self.client.get(self.url,{'date_from': [''],'date_to': [''],'categories':['-1'],'subcategories':['-1'],'planned':[''],'search':[''],'tags':['1']})
        self.assertTemplateUsed('views/transaction/transactions.html')
        self.assertEqual(response.context['transactions'].object_list,[self.transaction])

    def test_custom_date(self):
        response = self.client.get(self.url,{'date_from': ['01.01.2022'],'date_to': ['31.01.2022'],'categories':[''],'subcategories':[''],'planned':[''],'search':['']})
        self.assertTemplateUsed('views/transaction/transactions.html')
        self.assertEqual(response.context['transactions'].object_list,[self.transaction])

    def test_empty(self):
        response = self.client.get(self.url,{'date_from': [''],'date_to': [''],'categories':[''],'subcategories':[''],'planned':[''],'search':['']})
        self.assertTemplateUsed('views/transaction/transactions.html')
        self.assertQuerysetEqual(response.context['transactions'].object_list,Transaction.objects.none())
        
    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_url(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed('views/transaction/transaction_search.html')
        self.assertEqual(response.status_code,200)

    def test_url_by_name(self):
        response = self.client.get(reverse('financeAwareness:search_transactions'))       
        self.assertEqual(response.status_code,200)
