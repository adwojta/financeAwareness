from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from financeAwareness.forms import TagForm

from financeAwareness.models.tag import Tag

#Tags
@login_required
def tag_list(request):
    tags = Tag.objects.filter(user_id=request.user.id)
    return render(request, 'views/tag/tags.html',{'tags': tags})

@login_required
def tag_form(request):
    if request.method == 'POST':
        tag_form = TagForm(data=request.POST)
        if tag_form.is_valid():
            new_tag = tag_form.save(commit=False)
            new_tag.user_id = request.user
            new_tag.save()
            return redirect('financeAwareness:tags')
    else:
        tag_form = TagForm()
    return render(request, 'views/tag/tag_form.html',{'tag_form': tag_form})

@login_required
def tag_form_update(request,tag_id):   
    tag = get_object_or_404(Tag,id=tag_id)

    if request.user != tag.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        tag_form = TagForm(instance=tag)
        if request.method == 'POST':
            tag_form = TagForm(data=request.POST,instance=tag)
            if tag_form.is_valid():
                tag_form.save()
                return redirect('financeAwareness:tags')

        return render(request, 'views/tag/tag_update.html',{'tag_form':tag_form,'tag_id':tag_id})

    

def tag_form_delete(request,tag_id):
    tag = get_object_or_404(Tag,id=tag_id)
    if request.user != tag.user_id:
        return redirect('financeAwareness:transactions')       
    else:
        if request.method == 'POST':
            tag.delete()
            return redirect('financeAwareness:tags')
        return render(request, 'views/tag/tag_delete.html',{'tag_id':tag_id})