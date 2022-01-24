from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import SubcategoryForm
from financeAwareness.models.category import Category



#Subcategory
@login_required
def subcategory_details(request,subcategory_id):
    subcategory = get_object_or_404(Category,id=subcategory_id)
    if request.user != subcategory.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        return render(request, 'views/category/subcategory_details.html',{'subcategory':subcategory})

@login_required
def subcategory_form(request,master_category):
    if request.method == 'POST':
        subcategory_form = SubcategoryForm(data=request.POST)
        if subcategory_form.is_valid():
            master = get_object_or_404(Category,id=master_category)
            new_subcategory = subcategory_form.save(commit=False)
            new_subcategory.master_category=master
            new_subcategory.user_id = request.user
            new_subcategory.save()
            return redirect('financeAwareness:category_details',category_id=master.id)
    else:
        subcategory_form = SubcategoryForm()
    return render(request, 'views/category/subcategory_form.html',{'subcategory_form': subcategory_form})

@login_required
def subcategory_form_update(request,subcategory_id):
    subcategory = get_object_or_404(Category,id=subcategory_id)
    if request.user != subcategory.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            subcategory_form = SubcategoryForm(data=request.POST,instance=subcategory)
            if subcategory_form.is_valid():
                updated_subcategory = subcategory_form.save(commit=False)
                updated_subcategory.save()
                return redirect('financeAwareness:subcategory_details',subcategory_id)
        else:
            subcategory_form = SubcategoryForm(instance=subcategory)
        return render(request, 'views/category/subcategory_update.html',{'subcategory_form':subcategory_form,'subcategory_id':subcategory_id})

def subcategory_form_delete(request,subcategory_id):
    subcategory = get_object_or_404(Category,id=subcategory_id)
    if request.user != subcategory.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            master = subcategory.master_category
            subcategory.delete()
            return redirect('financeAwareness:category_details',category_id=master.id)

        return render(request, 'views/category/subcategory_delete.html',{'subcategory_id':subcategory_id})