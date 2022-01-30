from django.contrib.auth.models import User
from financeAwareness.forms import registerForm
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.models.account import Account

from financeAwareness.models.category import Category

income = ('Przychód',('Wynagrodzenie','Wynajem','Zwroty','Sprzedaż','Inne'))

expense = (('Zakupy',('Sprzęt elektroniczny','Sport','Odzież','Obuwie','Prezenty','Biżuteria')),
('Samochód',('Parking','Paliwo','Ubezpieczenie','Serwis','Inne')),
('Rozrywka',('Kino','Teatr','Gry','Książki','Koncert','Bar','Kawiarnia')),
('Używki',('Tytoń','Alkohol')),
('Usługi',('Fryzjer','Kosmetyczka','Prawnik','Inne')),
('Zdrowie',('Lekarz','Dentysta','Leki')),
('Rachunki',('Prąd','Czynsz','Woda','Telefon','Gaz','Ogrzewanie','Internet','Opłaty bankowe','Telewizja')),
('Jedzenie i picie',('Restauracje','Pieczywo','Warzywa','Owoce','Herbata','Kawa','Napoje gazowane')))



def register(request):
    if request.method == 'POST':
        user_form = registerForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            new_user = User.objects.latest('date_joined')

            #Creating basic categories for user
            new = Category(income=False,user_id=new_user, name='Ogólna kategoria')
            new.save()            
            for category in expense:
                new = Category(income=False,user_id=new_user, name=category[0])
                new.save()
                subcategories = category[1]

                for subcategory in subcategories:                    
                    master = Category.objects.get(user_id=new_user, name=category[0], master_category=None)
                    new = Category(income=False,user_id=new_user, name=subcategory, master_category=master)
                    new.save()
            
            new = Category(income=True,user_id=new_user, name=income[0])
            new.save()

            subcategories = income[1]
            master = Category.objects.get(user_id=new_user,name=income[0])

            for subcategory in subcategories:
                print(subcategory)               
                new = Category(income=True, user_id=new_user, name=subcategory, master_category=master)
                new.save()

            #Creating basic accounts for user
            new = Account(user_id=new_user,is_cash=True,name='Gotówka')
            new.save()

            new = Account(user_id=new_user,is_cash=False,name='Konto bankowe')
            new.save()
            
            return render(request,'registration/register_done.html',{'new_user':new_user})

    else:
        user_form = registerForm()
    return render(request,'registration/register.html',{'user_form':user_form})


def index(request):
    return render(request,'index.html')