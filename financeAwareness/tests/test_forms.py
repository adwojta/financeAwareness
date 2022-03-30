from datetime import datetime
from django.test import SimpleTestCase, TestCase
from financeAwareness.forms import LoginForm, RecurringForm,RegisterForm,TagForm,TransactionForm,TransactionItemForm,TransferForm,CategoryForm,SavingGoalForm,SearchForm,DateForm,AccountForm
from financeAwareness.models.category import Category
from financeAwareness.models.account import Account
from financeAwareness.models.transaction import Transaction
from financeAwareness.models.transactionItem import TransactionItem
from financeAwareness.models.tag import Tag
from django.contrib.auth.models import User


class TestLoginForm(TestCase):
    def test_valid_form(self):
        form = LoginForm(data={'username':'Test','password':'secretpassword'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)

class TestRegisterForm(TestCase):
    def test_valid_form(self):
        form = RegisterForm(data={'username':'Test','password1':'secretpassword','password1':'secretpassword','password2':'secretpassword'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = RegisterForm(data={'username':'Test','password1':'secretpassword'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),1)

class TestCategoryForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='PanTest',password='hasło')
    def test_valid_form(self):
        form = CategoryForm(data={'name':'TestCategory'},User=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CategoryForm(data={},User=self.user)
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),1)

class TestAccountForm(TestCase):
    def test_valid_form(self):
        form = AccountForm(data={'name':'cash','is_cash':True})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = AccountForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),1)

class TestSavingGoalForm(TestCase):
    def test_valid_form(self):
        form = SavingGoalForm(data={'name':'cash','due_date':datetime.now(),'goal_value':1000,'is_active_saving_goal':True})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = SavingGoalForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),3)

class TestTagForm(TestCase):
    def test_valid_form(self):
        form = TagForm(data={'name':'Tag'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = TagForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),1)

class TestTransactionForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='PanTest',password='hasło')
        self.account = Account.objects.create(user=self.user,name='Test',is_cash=True)

    def test_valid_form(self):
        form = TransactionForm(data={'name':'Test','account':self.account,'value':10.24,'date':'2022-02-02'},User=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = TransactionForm(data={},User=self.user)
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),4)

class TestRecurringForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='PanTest',password='hasło')
        self.account = Account.objects.create(user=self.user,name='Test',is_cash=True)

    def test_valid_form(self):
        form = RecurringForm(data={'name':'Test','account':self.account,'value':10.24,'date':'2022-02-02','recurring_type':'month'},User=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = RecurringForm(data={},User=self.user)
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),5)

class TestTransferForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='PanTest',password='hasło')
        self.account = Account.objects.create(user=self.user,name='Test',is_cash=True)
        self.account_to = Account.objects.create(user=self.user,name='Test2',is_cash=True)

    def test_valid_form(self):
        form = TransferForm(data={'account':self.account,'transfer_account':self.account_to,'value':10.24,'date':'2022-02-02'},User=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = TransferForm(data={},User=self.user)
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),4)

class TestTransactionItemForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='PanTest',password='hasło')
        self.account = Account.objects.create(user=self.user,name='Test',is_cash=True)
        self.category = Category.objects.create(user=self.user,name='Test',is_income=True)
        self.transaction = Transaction.objects.create(user=self.user,name='Test',account=self.account,value=10,date='2022-02-01')

    def test_valid_form(self):
        form = TransactionItemForm(data={'item_name':'test','category':self.category,'item_value':10.24,'is_planned':True},User=self.user,type='income')
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = TransactionItemForm(data={},User=self.user,type='income')
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),4)

class TestSearchForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='PanTest',password='hasło')

    def test_valid_form(self):
        form = SearchForm(data={},user=self.user)
        self.assertTrue(form.is_valid())

class TestDateForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='PanTest',password='hasło')

    def test_valid_form(self):
        form = DateForm(data={'date_from':'2022-02-01','date_to':'2022-02-02'},user=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = DateForm(data={},user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)


    