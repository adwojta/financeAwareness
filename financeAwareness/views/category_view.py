from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import CategoryForm
from financeAwareness.models.category import Category

#Category
@login_required
def category_details(request,category_id):
    category = get_object_or_404(Category,id=category_id)
    if request.user != category.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        subcategories = category.subcategories.all()
        return render(request, 'views/category/category_details.html',{'subcategories': subcategories,'category':category})
        

@login_required
def category_list(request):
    expenses = Category.objects.filter(user_id=request.user.id, master_category=None,income=False)
    incomes = Category.objects.filter(user_id=request.user.id, master_category=None,income=True)
    return render(request, 'views/category/category.html',{'expenses': expenses,'incomes':incomes})

@login_required
def category_form(request, income=None):
    if request.method == 'POST':
        category_form = CategoryForm(data=request.POST,User=request.user)
        if category_form.is_valid():
            new_category = category_form.save(commit=False)
            if income == 'income':
                new_category.income = True
            else:
                new_category.income = False
            new_category.user_id = request.user
            new_category.save()
            return redirect('financeAwareness:categories')
    else:
        category_form = CategoryForm(User=request.user)
    return render(request, 'views/category/category_form.html',{'category_form': category_form})

@login_required
def category_form_update(request,category_id):   
    category = get_object_or_404(Category,id=category_id)        
    if request.user != category.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        category_form = CategoryForm(instance=category,User=request.user)
        if request.method == 'POST':
            category_form = CategoryForm(data=request.POST,instance=category,User=request.user)
            if category_form.is_valid():
                category_form.save()
                return redirect('financeAwareness:category_details',category_id)

        return render(request, 'views/category/category_update.html',{'category_form':category_form,'category_id':category_id})

    

def category_form_delete(request,category_id):
    category = get_object_or_404(Category,id=category_id)
    if request.user != category.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            category.delete()
            return redirect('financeAwareness:categories')
        return render(request, 'views/category/category_delete.html',{'category_id':category_id})