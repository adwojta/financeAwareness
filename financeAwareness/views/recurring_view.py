from django.contrib.auth.decorators import login_required
from django.shortcuts import render


#recurring
@login_required
def recurring_list(request):
    pass