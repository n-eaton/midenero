from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.



@login_required(login_url='auth/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    
    
    context={
        'expenses':expenses,
        'page_obj':page_obj,
        
    }
    return render(request, 'dashbapp/index.html', context)

def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        
    }
    if request.method =="POST":
        
        amount= request.POST['amount']
        

        
        description= request.POST['description']
        
        date= request.POST['expense_date']
        
        if not amount or not date:
            messages.error(request, 'Amount and Date are required')
            return render(request, 'dashbapp/add_expense.html', context)
        
        category= request.POST['category']
        
        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category,description=description)
        messages.success(request, 'Expence saved successfully')
        
        return redirect('expenses') 
    
    # Return the default render response for the GET request
    return render(request, 'dashbapp/add_expense.html', context)

   
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories':categories,
    }
    if request.method=="GET":
        
        return render(request, 'dashbapp/expense-edit.html', context)
    
    if request.method=="POST":
        
        category= request.POST['category']
        amount= request.POST['amount']
        description= request.POST['description']
        date= request.POST['expense_date']
        
        if not amount or not date:
            messages.error(request, 'Amount and Date are required')
            return render(request, 'dashbapp/expense-edit.html', context)
        
        
        
        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category,description=description)
        
        expense.user=request.user
        expense.amount=amount
        expense.date=date
        expense.category=category
        expense.description=description
        expense.save()
        
        messages.success(request, 'Expence updated successfully')        
   
        messages.info(request, 'Handling post form')
        
        return redirect('expenses')
    
def expense_delete(request, id):
    expense=Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense removed")
    return redirect('expenses')