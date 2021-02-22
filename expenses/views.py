from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Expense


@login_required(login_url='/auth/login')
def index(request):
  expenses = Expense.objects.filter(owner=request.user).order_by('-date')
  context = {
    'expenses': expenses
  }
  return render(request, 'expenses/index.html', context)


@login_required(login_url='/auth/login')
def add_expense(request):
  categories = Category.objects.all()
  context = {
    'categories': categories,
    'values': request.POST
  }

  if request.method == 'GET':
    return render(request, 'expenses/add_expense.html', context)

  if request.method == 'POST':
    amount = request.POST['amount']
    description = request.POST['description']
    category = request.POST['category']
    date = request.POST['date']

    if not amount:
      messages.error(request, 'Amount is required.')
      return render(request, 'expenses/add_expense.html', context)
    if not description:
      messages.error(request, 'Description is required.')
      return render(request, 'expenses/add_expense.html', context)
    if not category:
      messages.error(request, 'Category is required.')
      return render(request, 'expenses/add_expense.html', context)

    Expense.objects.create(
      owner=request.user,
      amount=amount,
      date=date,
      category=category,
      description=description
    )
    messages.success(request, 'Expense saved successfully.')

    return render(request, 'expenses/add_expense.html')