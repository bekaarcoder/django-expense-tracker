from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category


@login_required(login_url='/auth/login')
def index(request):
  return render(request, 'expenses/index.html')

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
    if not description:
      messages.error(request, 'Description is required.')
    if not category:
      messages.error(request, 'Category is required.')

    return render(request, 'expenses/add_expense.html', context)