from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
from preferences.models import UserPreference
import datetime
import json
from django.db.models import Sum
from django.template.loader import get_template
from xhtml2pdf import pisa

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
        context = {
            'sources': sources
        }
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

        return render(request, 'income/add_income.html', context)


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


def income_summary(request):
    todays_date = datetime.date.today()
    six_months_before = todays_date - datetime.timedelta(days=30*6)
    incomes = Income.objects.filter(date__gte=six_months_before, date__lte=todays_date, owner=request.user)
    result = {}

    def get_source(income):
        return income.source

    source_list = list(set(map(get_source, incomes)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount

        return amount

    for source in source_list:
        result[source] = get_income_source_amount(source)
        print(result)

    return JsonResponse({'income_summary': result}, safe=False)


def get_monthly_income_summary(request):
    current_month = datetime.date.today().month
    result = {}
    check_month = current_month

    i = 1
    while i <= 6:
        if check_month == 0:
            check_month = 12
        incomes = Income.objects.filter(date__month=check_month, owner=request.user)
        month_income = 0
        for income in incomes:
            month_income += income.amount
        datetime_obj = datetime.datetime.strptime(str(check_month), '%m')
        key_month = datetime_obj.strftime('%B')

        result[i] = {
            "month": key_month,
            "amount": month_income
        }
        check_month -= 1
        i += 1

    return JsonResponse({'income_summary': result}, safe=False)


def view_income_summary(request):
    return render(request, 'income/income_summary.html')


def export_pdf(request):
    template_path = 'income/pdf_output.html'
    incomes = Income.objects.filter(owner=request.user)
    sum = incomes.aggregate(Sum('amount'))
    context = {
        'incomes': incomes,
        'total': sum['amount__sum']
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    filename = 'Expenses' + datetime.datetime.now().strftime('%d%m%Y%H%M%S') + '.pdf'
    response['Content-Disposition'] = 'attachment; filename=' + filename
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
