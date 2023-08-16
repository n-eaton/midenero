from django.shortcuts import render

# Create your views here.


def base(request):
    return render(request, 'base.html')

def expenses(request):
    return render(request, 'dashbapp/expenses.html')

def add_expense(request):
    return render(request, 'dashbapp/add_expense.html')