from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


def base(request):
    return render(request, 'base.html')

@login_required(login_url='auth/login')
def expenses(request):
    return render(request, 'dashbapp/expenses.html')

def add_expense(request):
    return render(request, 'dashbapp/add_expense.html')