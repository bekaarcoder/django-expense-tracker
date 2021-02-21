from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
import os
import json
from .models import UserPreference


def index(request):
  currency_data = []
  file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
  
  with open(file_path, 'r') as json_file:
    data = json.load(json_file)
    for k,v in data.items():
      currency_data.append({'name': k, 'value': v})

  user_preferences = None
  if UserPreference.objects.filter(user=request.user).exists():
    user_preferences = UserPreference.objects.get(user=request.user)

  if request.method == 'GET':
    context = {
      'currency_data': currency_data,
      'user_preferences': user_preferences
    }
    return render(request, 'preferences/index.html', context)

  else:
    currency = request.POST['currency']

    if currency:

      if UserPreference.objects.filter(user=request.user).exists():
        user_preferences.currency = currency
        user_preferences.save()
      else:
        UserPreference.objects.create(user=request.user, currency=currency)
      user_preferences = UserPreference.objects.get(user=request.user)
      context = {
        'currency_data': currency_data,
        'user_preferences': user_preferences
      }
      messages.success(request, 'Preference have been saved successfully.')
      return render(request, 'preferences/index.html', context)

    else:
      context = {
        'currency_data': currency_data
      }
      messages.error(request, 'Please select a currency.')
      return render(request, 'preferences/index.html', context)
