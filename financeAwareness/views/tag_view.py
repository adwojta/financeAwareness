from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import TagForm

from financeAwareness.models.tag import Tag
from financeAwareness.views.site_view import AbstractDelete

#Tags
@login_required
def tag_list(request):
    tags = Tag.objects.filter(user=request.user.id)
    return render(request, 'views/tags.html',{'tags': tags})

@login_required
def tag_form(request):
    title = 'Dodaj tag'
    type = 'tag'
    if request.method == 'POST':
        form = TagForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('financeAwareness:tags')
    else:
        form = TagForm()
    return render(request, 'form.html',{'form': form,'title':title,'type':type})

@login_required
def tag_form_update(request,tag_id):   
    tag = get_object_or_404(Tag,id=tag_id)
    title = 'Zaktualizuj tag'
    type = 'tag'
    if request.user != tag.user:
        return redirect('financeAwareness:transactions')       
    else:
        form = TagForm(instance=tag)
        if request.method == 'POST':
            form = TagForm(data=request.POST,instance=tag)
            if form.is_valid():
                form.save()
                return redirect('financeAwareness:tags')

        return render(request, 'form.html',{'form':form,'title':title,'type':type})

class TagDelete(AbstractDelete):
    redirect_view = 'financeAwareness:tags'
    model = Tag
    get_view = 'delete.html'
    delete_type = "Tag"
    title = "Usuń tag"