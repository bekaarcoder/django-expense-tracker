from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Category, Expense
from preferences.models import UserPreference
import datetime
import json


def search_expenses(request):
    if request.method == "POST":
        keyword = json.loads(request.body).get("searchText")
        expenses = (
            Expense.objects.filter(amount__istartswith=keyword, owner=request.user)
            | Expense.objects.filter(date__startswith=keyword, owner=request.user)
            | Expense.objects.filter(description__icontains=keyword, owner=request.user)
            | Expense.objects.filter(category__icontains=keyword, owner=request.user)
        )
        data = expenses.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url="/auth/login")
def index(request):
    expenses = Expense.objects.filter(owner=request.user).order_by("-date")
    paginator = Paginator(expenses, 2)
    page_no = request.GET.get("page")
    page_object = Paginator.get_page(paginator, page_no)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {"expenses": expenses, "page_object": page_object, "currency": currency}
    return render(request, "expenses/index.html", context)


@login_required(login_url="/auth/login")
def add_expense(request):
    categories = Category.objects.all()
    context = {"categories": categories, "values": request.POST}

    if request.method == "GET":
        return render(request, "expenses/add_expense.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        category = request.POST["category"]
        date = request.POST["date"]

        if not amount:
            messages.error(request, "Amount is required.")
            return render(request, "expenses/add_expense.html", context)
        if not description:
            messages.error(request, "Description is required.")
            return render(request, "expenses/add_expense.html", context)
        if not category:
            messages.error(request, "Category is required.")
            return render(request, "expenses/add_expense.html", context)

        Expense.objects.create(
            owner=request.user,
            amount=amount,
            date=date,
            category=category,
            description=description,
        )
        messages.success(request, "Expense saved successfully.")

        return render(request, "expenses/add_expense.html")


def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {"expense": expense, "categories": categories}

    if request.method == "GET":
        return render(request, "expenses/edit-expense.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        category = request.POST["category"]
        date = request.POST["date"]

        if not amount:
            messages.error(request, "Amount is required.")
            return render(request, "expenses/add_expense.html", context)
        if not description:
            messages.error(request, "Description is required.")
            return render(request, "expenses/add_expense.html", context)
        if not category:
            messages.error(request, "Category is required.")
            return render(request, "expenses/add_expense.html", context)
        if not date:
            date = datetime.date.today()

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()

        messages.success(request, "Expense updated successfully.")
        return redirect("expenses:index")


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    context = {"expense": expense}
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted successfully.")
        return redirect("expenses:index")

    return render(request, "expenses/delete_expense.html", context)
