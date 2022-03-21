from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from abc import ABC

class AbstractDelete(LoginRequiredMixin,TemplateView,ABC):
    redirect_view = ""
    get_view = "delete.html"
    model = None
    delete_type = ""
    title = ""
    id = 0

    def setup(self, request, *args, **kwargs):
        self.id = kwargs['id']
        self.object = get_object_or_404(self.model,id=self.id)        
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user != self.object.user:
            return redirect(self.redirect_view)       
        else:          
            self.object.delete()
            return redirect(self.redirect_view)

    def get(self, request, *args, **kwargs):
        return render(request, self.get_view,{'delete_type':self.delete_type,"title":self.title,'id':self.id})

def index(request):
    return render(request,'index.html')