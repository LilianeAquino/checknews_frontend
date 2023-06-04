import pymongo
from os import getenv
from dotenv import load_dotenv
from django.shortcuts import redirect, render
from django.contrib.auth.models import User


load_dotenv(verbose=True)


client = pymongo.MongoClient(getenv('URL_MONGO'))
dbname = client[getenv('DB_NAME')]


def delete_user(request, user_id):
    collection = dbname[getenv('COLLECTION_USERS')]
    collection.delete_one({'id': int(user_id)})
    return redirect('app:users_listing')


def update_user_form(request, user_id):
    user = User.objects.get(id=int(user_id))
    context = {'user': user}
    return render(request, 'app/crud/update_user_form.html', context)


def update_user(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=int(user_id))

        new_username = request.POST.get('username')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        is_staff = request.POST.get('is_staff') == 'on'
        is_active = request.POST.get('is_active') == 'on'

        user.username = new_username
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.is_staff = is_staff
        user.is_active = is_active
        user.save()
        return redirect('app:users_listing')


def create_user_form(request):
    return render(request, 'app/crud/create_user_form.html')


def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') == 'on'

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, is_staff=is_staff)
        user.save()
    return redirect('app:users_listing')
