from abc import ABC
from selenium import webdriver
from selenium.webdriver.support.select import Select
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from financeAwareness.models.account import Account
from financeAwareness.models.category import Category
from financeAwareness.models.tag import Tag

class Register(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.browser.maximize_window()

    def tearDown(self):
        self.browser.close()

    def test(self):
        self.browser.get(self.live_server_url)
        self.assertEqual(self.browser.title,'financeAwareness')
        self.browser.find_element_by_link_text('Zarejestruj się').click()
        self.assertEqual(self.browser.title,'Rejestracja')
        self.browser.find_element_by_id('id_username').send_keys("PanTest")
        self.browser.find_element_by_id('id_first_name').send_keys("Pan")
        self.browser.find_element_by_id('id_last_name').send_keys("Test")
        self.browser.find_element_by_id('id_email').send_keys("test@test.pl")
        self.browser.find_element_by_id('id_password1').send_keys("DjangoTest1")
        self.browser.find_element_by_id('id_password2').send_keys("DjangoTest1")
        self.browser.find_element_by_name("Rejestracja").click()

        self.assertEqual(self.browser.title,'Utworzono konto')
        self.browser.find_element_by_link_text('Zaloguj').click()
        self.assertEqual(self.browser.title,'Logowanie')
        username = self.browser.find_element_by_id('id_username')
        username.send_keys("PanTest")
        password = self.browser.find_element_by_id('id_password')
        password.send_keys("DjangoTest1")
        self.browser.find_element_by_name("Zaloguj").click()
        self.assertEqual(self.browser.title,'Transakcje')

        self.browser.find_element_by_link_text("Kategorie").click()
        self.assertEqual(self.browser.title,'Kategorie')
        self.browser.find_element_by_link_text("Przychód")
        self.browser.find_element_by_link_text("Zakupy")
        self.browser.find_element_by_link_text("Dom").click()
        self.assertEqual(self.browser.title,'Dom')
        self.assertTrue(self.browser.page_source,'Narzędzia')

        self.browser.find_element_by_link_text("Konta i cele").click()
        self.assertEqual(self.browser.title,'Konta i cele')
        self.assertTrue(self.browser.page_source,'Konto bankowe')
        self.assertTrue(self.browser.page_source,'Gotówka')

class Login(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1",id=1)
        self.user.save()
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')

    def tearDown(self):
        self.browser.close()

    def test(self):
        self.browser.get(self.live_server_url)
        self.assertEqual(self.browser.title,'financeAwareness')
        self.browser.find_element_by_link_text('Zaloguj').click()
        self.assertEqual(self.browser.title,'Logowanie')
        username = self.browser.find_element_by_id('id_username')
        username.send_keys("PanTest")
        password = self.browser.find_element_by_id('id_password')
        password.send_keys("DjangoTest1")
        self.browser.find_element_by_name("Zaloguj").click()
        self.assertEqual(self.browser.title,'Transakcje')

class AbstractCreateTest(ABC):
    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.browser.maximize_window()
        self.user = User.objects.create_user(username="PanTest", password="DjangoTest1",id=1)
        self.user.save()
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text('Zaloguj').click()
        username = self.browser.find_element_by_id('id_username')
        username.send_keys("PanTest")
        password = self.browser.find_element_by_id('id_password')
        password.send_keys("DjangoTest1")
        self.browser.find_element_by_name("Zaloguj").click()

    def tearDown(self):
        self.browser.close()

class CreateCategory(AbstractCreateTest,StaticLiveServerTestCase):
    def test(self):
        self.browser.find_element_by_link_text('Kategorie').click()
        self.assertEqual(self.browser.title,'Kategorie')
        categories_add = self.browser.find_elements_by_link_text('Dodaj')
        categories_add[0].click()
        name = self.browser.find_element_by_id('id_name')
        name.send_keys("Test")
        self.browser.find_element_by_xpath("//input[@value='Wyślij']").click()
        self.browser.find_element_by_link_text('Test').click()
        self.assertEqual(self.browser.title,'Test')
        self.assertTrue(self.browser.page_source,'Kategoria Test')
        self.browser.find_element_by_link_text('Zmień').click()
        name = self.browser.find_element_by_id('id_name')
        name.send_keys("Tested")
        self.browser.find_element_by_xpath("//input[@value='Wyślij']").click()
        self.assertTrue(self.browser.page_source,'Kategoria Tested')

        self.browser.find_element_by_link_text('Usuń').click()
        self.browser.find_element_by_xpath("//input[@value='Tak']").click()
        self.assertEqual(self.browser.title,'Kategorie')

class CreateTag(AbstractCreateTest,StaticLiveServerTestCase):
    def test(self):
        self.browser.find_element_by_link_text('Tagi').click()
        self.assertEqual(self.browser.title,'Tagi')
        self.browser.find_element_by_link_text('Dodaj tag').click()
        name = self.browser.find_element_by_id('id_name')
        name.send_keys("Test")
        self.browser.find_element_by_xpath("//input[@value='Wyślij']").click()

        self.assertEqual(self.browser.title,'Tagi')
        self.assertTrue(self.browser.page_source,'Test')
        self.browser.find_element_by_link_text('Zmień').click()
        name = self.browser.find_element_by_id('id_name')
        name.send_keys("Tested")
        self.browser.find_element_by_xpath("//input[@value='Wyślij']").click()
        self.assertTrue(self.browser.page_source,'Tested')

        self.browser.find_element_by_link_text('Usuń').click()
        self.browser.find_element_by_xpath("//input[@value='Tak']").click()
        self.assertEqual(self.browser.title,'Tagi')

class CreateAccount(AbstractCreateTest,StaticLiveServerTestCase):
    def test(self):
        self.browser.find_element_by_link_text('Konta i cele').click()
        self.assertEqual(self.browser.title,'Konta i cele')
        self.browser.find_element_by_link_text('Dodaj konto').click()
        name = self.browser.find_element_by_id('id_name')
        name.send_keys("Test")
        self.assertTrue(self.browser.find_element_by_id('id_is_cash'))
        self.browser.find_element_by_xpath("//input[@value='Wyślij']").click()

        self.assertEqual(self.browser.title,'Konta i cele')
        self.assertTrue(self.browser.page_source,'Test')
        self.browser.find_element_by_link_text('Edytuj').click()
        name = self.browser.find_element_by_id('id_name')
        name.send_keys("Tested")
        self.browser.find_element_by_xpath("//input[@value='Wyślij']").click()
        self.assertTrue(self.browser.page_source,'Konta i cele')
        self.assertTrue(self.browser.page_source,'Tested')

        self.browser.find_element_by_link_text('Usuń').click()
        self.browser.find_element_by_xpath("//input[@value='Tak']").click()
        self.assertEqual(self.browser.title,'Konta i cele')

class CreateGoal(AbstractCreateTest,StaticLiveServerTestCase):
    def test(self):
        self.browser.find_element_by_link_text('Konta i cele').click()
        self.assertEqual(self.browser.title,'Konta i cele')
        self.browser.find_element_by_link_text('Dodaj cel').click()
        name = self.browser.find_element_by_id('id_name')
        name.send_keys("Test")
        date = self.browser.find_element_by_id('id_due_date')
        date.send_keys("30.06.2030")
        value = self.browser.find_element_by_id('id_goal_value')
        value.send_keys("10000")
        self.browser.find_element_by_xpath("//input[@value='Wyślij']").click()

        self.assertEqual(self.browser.title,'Konta i cele')
        self.assertTrue(self.browser.page_source,'Test')
        self.browser.find_element_by_link_text('Edytuj').click()
        name = self.browser.find_element_by_id('id_name')
        name.send_keys("Tested")
        self.browser.find_element_by_xpath("//input[@value='Wyślij']").click()
        self.assertTrue(self.browser.page_source,'Konta i cele')
        self.assertTrue(self.browser.page_source,'Tested')

        self.browser.find_element_by_link_text('Usuń').click()
        self.browser.find_element_by_xpath("//input[@value='Tak']").click()
        self.assertEqual(self.browser.title,'Konta i cele')

class CreateTransaction(AbstractCreateTest,StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='TestAccount',id=1, value=100)
        self.account.save()

        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',master_category=Category.objects.get(id=1),id=2)
        self.category2.save()
        self.category3 = Category.objects.create(user=self.user,name='Test3',master_category=Category.objects.get(id=1),id=3)
        self.category3.save()
        self.category4 = Category.objects.create(user=self.user,name='Test4',master_category=Category.objects.get(id=1),id=4)
        self.category4.save()

        self.tag = Tag(user=self.user,name='TestTag',id=1)
        self.tag.save()
        self.tag2 = Tag(user=self.user,name='TestTag2',id=2)
        self.tag2.save()

    def test(self):
        self.browser.find_element_by_link_text('Dodaj wydatek').click()
        self.assertEqual(self.browser.title,'Dodaj wydatek')
        
        name = self.browser.find_element_by_id('id_name')
        name.send_keys("TestTransaction")
        self.browser.find_element_by_id('id_date').click()
        self.browser.find_element_by_link_text('10').click()
        select = Select(self.browser.find_element_by_id('id_account'))
        select.select_by_visible_text('TestAccount')

        self.browser.execute_script("arguments[0].click();",self.browser.find_element_by_id('id_tags_0'))
        self.browser.execute_script("arguments[0].click();",self.browser.find_element_by_xpath("//input[@value='Usuń element']"))
        self.browser.execute_script("arguments[0].click();",self.browser.find_element_by_xpath("//input[@value='Dodaj element']"))
        self.browser.execute_script("arguments[0].click();",self.browser.find_element_by_xpath("//input[@value='Dodaj element']"))

        items_name = self.browser.find_elements_by_id('id_item_name')
        items_value = self.browser.find_elements_by_id('id_item_value')
        items_category = self.browser.find_elements_by_id('id_category')
        items_subcategory = self.browser.find_elements_by_id('id_subcategory')

        items_name[0].send_keys('TestItem1')
        items_name[1].send_keys('TestItem2')

        items_value[0].send_keys('4,5')
        items_value[1].send_keys('5,5')

        
        select = Select(items_category[0])
        select.select_by_visible_text('Test')
        self.browser.implicitly_wait(10)
        select = Select(items_subcategory[0])
        select.select_by_visible_text('Test2')

        select = Select(items_category[1])
        select.select_by_visible_text('Test')
        self.browser.implicitly_wait(10)
        select = Select(items_subcategory[1])
        select.select_by_visible_text('Test3')
        self.browser.execute_script("arguments[0].click();",self.browser.find_element_by_xpath("//input[@value='Wyślij']"))

        self.assertEqual(self.browser.title,'Transakcje')
        self.browser.find_element_by_link_text('TestTransaction').click()
        self.assertTrue(self.browser.page_source,'Test')
        self.assertTrue(self.browser.page_source,'Test2')
        self.assertTrue(self.browser.page_source,'Test3')
        self.assertTrue(self.browser.page_source,'TestTransaction')
        self.assertTrue(self.browser.page_source,'TestAccount')
        self.assertTrue(self.browser.page_source,'10,0')
        self.assertTrue(self.browser.page_source,'TestTag')
        self.assertTrue(self.browser.page_source,'TestTag2')
        self.assertTrue(self.browser.page_source,'TestItem1')
        self.assertTrue(self.browser.page_source,'TestItem2')
        self.assertTrue(self.browser.page_source,'4,5')
        self.assertTrue(self.browser.page_source,'5,5')

class CreateRecurring(AbstractCreateTest,StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.account = Account.objects.create(user=self.user,is_cash=False,name='TestAccount',id=1, value=100)
        self.account.save()

        self.category = Category.objects.create(user=self.user,name='Test',id=1,is_income=False)
        self.category.save()
        self.category2 = Category.objects.create(user=self.user,name='Test2',master_category=Category.objects.get(id=1),id=2)
        self.category2.save()
        self.category3 = Category.objects.create(user=self.user,name='Test3',master_category=Category.objects.get(id=1),id=3)
        self.category3.save()
        self.category4 = Category.objects.create(user=self.user,name='Test4',master_category=Category.objects.get(id=1),id=4)
        self.category4.save()

        self.tag = Tag(user=self.user,name='TestTag',id=1)
        self.tag.save()
        self.tag2 = Tag(user=self.user,name='TestTag2',id=2)
        self.tag2.save()

    def test(self):
        self.browser.find_element_by_link_text('Stałe transakcje').click()
        self.browser.find_element_by_link_text('Dodaj stały wydatek').click()
        self.assertEqual(self.browser.title,'Dodaj stały wydatek')
        
        name = self.browser.find_element_by_id('id_name')
        name.send_keys("TestTransaction")
        self.browser.find_element_by_id('id_date').click()
        self.browser.find_element_by_link_text('10').click()
        select = Select(self.browser.find_element_by_id('id_account'))
        select.select_by_visible_text('TestAccount')

        select = Select(self.browser.find_element_by_id('id_recurring_type'))
        select.select_by_visible_text('Miesiąc')

        self.browser.execute_script("arguments[0].click();",self.browser.find_element_by_id('id_tags_0'))
        self.browser.execute_script("arguments[0].click();",self.browser.find_element_by_xpath("//input[@value='Usuń element']"))
        self.browser.execute_script("arguments[0].click();",self.browser.find_element_by_xpath("//input[@value='Dodaj element']"))
        self.browser.execute_script("arguments[0].click();",self.browser.find_element_by_xpath("//input[@value='Dodaj element']"))

        items_name = self.browser.find_elements_by_id('id_item_name')
        items_value = self.browser.find_elements_by_id('id_item_value')
        items_category = self.browser.find_elements_by_id('id_category')
        items_subcategory = self.browser.find_elements_by_id('id_subcategory')

        items_name[0].send_keys('TestItem1')
        items_name[1].send_keys('TestItem2')

        items_value[0].send_keys('4,5')
        items_value[1].send_keys('5,5')

        
        select = Select(items_category[0])
        select.select_by_visible_text('Test')
        self.browser.implicitly_wait(10)
        select = Select(items_subcategory[0])
        select.select_by_visible_text('Test2')

        select = Select(items_category[1])
        select.select_by_visible_text('Test')
        self.browser.implicitly_wait(10)
        select = Select(items_subcategory[1])
        select.select_by_visible_text('Test3')
        self.browser.execute_script("arguments[0].click();",self.browser.find_element_by_xpath("//input[@value='Wyślij']"))

        self.assertEqual(self.browser.title,'Stałe transakcje')
        self.browser.find_element_by_link_text('TestTransaction').click()
        self.assertTrue(self.browser.page_source,'Test')
        self.assertTrue(self.browser.page_source,'Test2')
        self.assertTrue(self.browser.page_source,'Test3')
        self.assertTrue(self.browser.page_source,'TestTransaction')
        self.assertTrue(self.browser.page_source,'TestAccount')
        self.assertTrue(self.browser.page_source,'10,0')
        self.assertTrue(self.browser.page_source,'TestTag')
        self.assertTrue(self.browser.page_source,'TestTag2')
        self.assertTrue(self.browser.page_source,'TestItem1')
        self.assertTrue(self.browser.page_source,'TestItem2')
        self.assertTrue(self.browser.page_source,'4,5')
        self.assertTrue(self.browser.page_source,'5,5')
        self.assertTrue(self.browser.page_source,'Miesięczna')
