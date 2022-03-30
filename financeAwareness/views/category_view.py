from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import CategoryForm
from financeAwareness.models.category import Category
from financeAwareness.views.site_view import AbstractDelete
from django.views.generic.edit import CreateView,UpdateView

#Category
@login_required
def category_details(request,category_id):
    category = get_object_or_404(Category,id=category_id) 
    if request.user != category.user:
        return redirect('financeAwareness:transactions')       
    else:
        subcategories = category.subcategories.all()
        return render(request, 'views/category/category_details.html',{'subcategories': subcategories,'category':category})
        
@login_required
def category_list(request):
    expenses = Category.objects.filter(user=request.user.id, master_category=None,is_income=False)
    incomes = Category.objects.filter(user=request.user.id, master_category=None,is_income=True)
    return render(request, 'views/category/category.html',{'expenses': expenses,'incomes':incomes})

@login_required
def category_form(request, income=None):
    title = 'Dodaj kategorie'
    type = 'category_form'
    if request.method == 'POST':
        form = CategoryForm(data=request.POST,User=request.user)
        if form.is_valid():
            new_category = form.save(commit=False)
            if income == 'income':
                new_category.is_income = True
            else:
                new_category.is_income = False
            new_category.user = request.user
            new_category.save()
            return redirect('financeAwareness:categories')
    else:
        form = CategoryForm(User=request.user)
    return render(request, 'form.html',{'form': form,'title':title,'type':type})

@login_required
def subcategory_form(request,master_category):
    title = 'Dodaj podkategorie'
    type = 'category'
    if request.method == 'POST':
        form = CategoryForm(data=request.POST,User=request.user)
        if form.is_valid():
            master = get_object_or_404(Category,id=master_category)
            new_subcategory = form.save(commit=False)
            new_subcategory.master_category=master
            new_subcategory.is_income = master.is_income
            new_subcategory.user = request.user
            new_subcategory.save()
            return redirect('financeAwareness:category_details',category_id=master.id)
    else:
        form = CategoryForm(User=request.user)
    return render(request, 'form.html',{'form': form,'category_id':master_category,'title':title,'type':type})

@login_required
def category_form_update(request,category_id):
    title = 'Zaktualizuj kategorie'
    type = 'category'   
    category = get_object_or_404(Category,id=category_id)        
    if request.user != category.user:
        return redirect('financeAwareness:transactions')       
    else:
        form = CategoryForm(instance=category,User=request.user)
        if request.method == 'POST':
            form = CategoryForm(data=request.POST,instance=category,User=request.user)
            if form.is_valid():
                form.save()
                return redirect('financeAwareness:category_details',category.id)

        return render(request, 'form.html',{'form':form,'category_id':category.id,'title':title,'type':type})

@login_required
def subcategory_form_update(request,subcategory_id):
    title = 'Zaktualizuj podkategorie'
    type = 'category'
    subcategory = get_object_or_404(Category,id=subcategory_id)
    category = subcategory.master_category.id
    if request.user != subcategory.user:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            form = CategoryForm(data=request.POST,instance=subcategory,User=request.user)
            if form.is_valid():
                updated_subcategory = form.save(commit=False)
                updated_subcategory.save()
                return redirect('financeAwareness:category_details',category)
        else:
            form = CategoryForm(instance=subcategory,User=request.user)
        return render(request, 'form.html',{'form':form,'category_id':category,'title':title,'type':type})

class CategoryDelete(AbstractDelete):
    redirect_view = 'financeAwareness:categories'
    model = Category
    delete_type = "Category"
    title = "Usuń kategorie"

class SubcategoryDelete(AbstractDelete):
    redirect_view = 'financeAwareness:category_details'
    model = Category
    delete_type = "Subcategory"
    title = "Usuń podkategorie"

    def post(self, request, *args, **kwargs):
        self.id = self.object.master_category.id
        if request.user != self.object.user:
            return redirect(self.redirect_view,self.id)      
        else:          
            self.object.delete()
            return redirect(self.redirect_view,self.id) 
        