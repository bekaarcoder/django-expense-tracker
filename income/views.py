from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
from preferences.models import UserPreference
import datetime
import json

def search_income(request):
    if request.method == "POST":
        keyword = json.loads(request.body).get("searchText")
        income = (
            Income.objects.filter(amount__istartswith=keyword, owner=request.user)
            | Income.objects.filter(date__startswith=keyword, owner=request.user)
            | Income.objects.filter(description__icontains=keyword, owner=request.user)
            | Income.objects.filter(source__icontains=keyword, owner=request.user)
        )
        data = income.values()

        return JsonResponse(list(data), safe=False)


def index(request):
    incomes = Income.objects.filter(owner=request.user).order_by('-date')
    currency = UserPreference.objects.get(user=request.user).currency
    paginator = Paginator(incomes, 6)
    page_no = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_no)

    context = {
        'incomes': incomes,
        'currency': currency,
        'page_object': page_object
    }

    return render(request, 'income/index.html', context)


def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']

        if not amount:
            messages.error(request, "Amount is required.")
            return render(request, 'income/add_income.html', context)
        if not description:
            messages.error(request, "Description is required.")
            return render(request, 'income/add_income.html', context)
        if not source:
            messages.error(request, "Source is required.")
            return render(request, 'income/add_income.html', context)
        if not date:
            date = datetime.date.today()

        Income.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            source=source,
            date=date
        )
        messages.success(request, "Income added successfully.")

        return render(request, 'income/add_income.html')


def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'sources': sources
    }

    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']

        if not amount:
            messages.error(request, "Amount is required.")
            return render(request, 'income/add_income.html', context)
        if not description:
            messages.error(request, "Description is required.")
            return render(request, 'income/add_income.html', context)
        if not source:
            messages.error(request, "Source is required.")
            return render(request, 'income/add_income.html', context)
        if not date:
            date = datetime.date.today()

        income.owner = request.user
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        income.save()

        messages.success(request, "Income updated successfully.")
        return redirect('income:index')


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    context = {
        'income': income
    }
    
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income deleted successfully.')
        return redirect('income:index')

    return render(request, 'income/delete_income.html', context)
