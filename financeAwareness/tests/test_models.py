from datetime import datetime
from django.test import SimpleTestCase, TestCase
from financeAwareness.models.category import Category
from financeAwareness.models.account import Account
from financeAwareness.models.transaction import Transaction
from financeAwareness.models.transactionItem import TransactionItem
from financeAwareness.models.tag import Tag
from django.contrib.auth.models import User

class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='PanTest',password='hasło')
        self.account = Account.objects.create(user=self.user,is_cash=False)
        self.cash = Account.objects.create(user=self.user,is_cash=True)
        self.tag = Tag.objects.create(user=self.user,name='Tag A')
        self.category = Category.objects.create(user=self.user,name='Test')
        self.subcategory = Category.objects.create(user=self.user,name='Test_subcategory',master_category=self.category)
        self.transaction = Transaction.objects.create(user=self.user,name='Sklep A', account=self.account,value = 123.45,date=datetime.now(),type='expense')

    def test_category(self):
        self.c = Category(user=self.user,name='Test')
        self.s = Category(user=self.user,name='Test_subcategory',master_category=self.category)
        self.assertIsInstance(self.c,Category)
        self.assertIsInstance(self.s,Category)

    def test_account(self):
        self.a = Account(user=self.user,is_cash=False)
        self.c = Account(user=self.user,is_cash=True)
        self.assertIsInstance(self.a,Account)
        self.assertIsInstance(self.c,Account)

    def test_tag(self):
        self.t = Tag(user=self.user,name='Tag A')
        self.assertIsInstance(self.t,Tag)

    def test_transaction(self):
        self.transactionIncome = Transaction(user=self.user,name='Sklep A', account=self.account,value = 123.45,date=datetime.now(),type='income')
        self.recurring = Transaction(user=self.user,name='Rachunek B', account=self.account,value = 123.45,date=datetime.now(),type='recurringExpense',recurring_type=('month'))
        self.planned = Transaction(user=self.user,name='Sklep C', account=self.cash,value = 123.45,date=datetime.now(),type='planned')
        self.transfer = Transaction(user=self.user,name='account->cash', account=self.account,value = 123.45,date=datetime.now(),type='transfer',transfer_account=self.cash)
        self.assertIsInstance(self.transaction,Transaction)
        self.assertIsInstance(self.recurring,Transaction)
        self.assertIsInstance(self.planned,Transaction)
        self.assertIsInstance(self.transfer,Transaction)

    def test_transactionItem(self):
        self.product = TransactionItem(transaction=self.transaction,category=self.category,item_name='Test',item_value=123.45,is_planned=True)
        self.assertIsInstance(self.product,TransactionItem)


