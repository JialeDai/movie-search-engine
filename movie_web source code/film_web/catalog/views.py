import hashlib
import pymongo
import re
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from catalog import forms
from catalog.models import Users, Movies
from bson.json_util import dumps
from bson import ObjectId
from django.urls import reverse
from catalog.RS import movie_recommend
from catalog.plot_search import plot_search


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

# Create your views here.
def login(request):
    client = pymongo.MongoClient("mongodb://Song:a931021@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.movie_web   
    login_form = forms.LoginForm()
    message = ''

    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')

    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            name = login_form.cleaned_data.get('name')
            password = login_form.cleaned_data.get('password')
            try:
                user = db.catalog_users.find({'name': name})[0]
                if user['password'] == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_name'] = user['name']
                    return redirect('/index/')
                else:
                    message = 'wrong password!'
            except:
                message = 'no username!'
        else:
            message = 'please enter the vaild content!'

    context = {
        'login_form': login_form,
        'message': message
    }

    return render(request, 'login.html', context=context)


def register(request):
    register_form = forms.RegisterForm()
    message = ''

    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            name = register_form.cleaned_data.get('name')
            password = register_form.cleaned_data.get('password')
            confirm_pw = register_form.cleaned_data.get('confirm_pw')
            email = register_form.cleaned_data.get('email')

            if password != confirm_pw:
                message = 'wrong confirm password!'
            else:
                same_email_user = Users.objects.filter(email=email)
                same_name_user = Users.objects.filter(name=name)
                if same_email_user:
                    message = 'email already exist'
                elif same_name_user:
                    message = 'name already exist'
                else:
                    new_user = Users()
                    new_user.name = name
                    new_user.password = hash_code(password)
                    new_user.email = email
                    new_user.save()
                    
                    return redirect('/login/')

    context = {
        'register_form': register_form,
        'message': message
    }

    return render(request, 'register.html', context=context)


@csrf_exempt
def index(request):
    client = pymongo.MongoClient("mongodb://Song:a931021@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.movie_web
    recommand_list = []
    user_name = request.session.get('user_name')

    if request.session.get('is_login', None):
        user = db.catalog_users.find({'name': user_name})[0]
        if 'ratings' in user:
            recommand_oids = movie_recommend(request.session.get('user_name'))
            for recommand_oid in recommand_oids:
                movie = db.catalog_movies.find({'_id': recommand_oid})[0]
                movie['id'] = movie.pop('_id')
                recommand_list.append(movie)

    context = {
        'recommand_list': recommand_list,
    }

    return render(request, 'index.html', context=context)


@csrf_exempt
def result(request):
    client = pymongo.MongoClient("mongodb://Song:a931021@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.movie_web   
    result_movies = []

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        type_input = request.POST.get('type_input')
        option_id = request.POST.get('option_id')
        request.session['option_id'] = option_id
        results = db.catalog_movies.find({'title': re.compile(user_input, re.I)})

        if type_input == 'genre':
            results = db.catalog_movies.find({'genres': {'$regex': user_input, '$options': '$i'}})
        elif type_input == 'cast':
            results = db.catalog_movies.find({'cast': {'$regex': user_input, '$options': '$i'}})
        elif type_input == 'director':
            results = db.catalog_movies.find({'directors': {'$regex': user_input, '$options': '$i'}})
        elif type_input == 'year':
            results = db.catalog_movies.find({'year': int(user_input)})
        elif type_input == 'fullplot':
            results = []
            movie_oids = plot_search(user_input)
            for movie_oid in movie_oids:
                movie = db.catalog_movies.find({'_id': movie_oid})[0]
                results.append(movie)

        for result in results:
            result['id'] = result.pop('_id')
            result_movies.append(result)

    context = {
        'result_movies': result_movies,
    }

    return render(request, 'result.html', context=context)


@csrf_exempt
def result_detail(request, pk):
    client = pymongo.MongoClient("mongodb://Song:a931021@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.movie_web
    request.session['pk'] = pk
    detail_movie = db.catalog_movies.find({'_id': ObjectId(pk)})[0]
    detail_movie_id = detail_movie['_id']
    s_detail_movie_id = str(detail_movie_id)
    rate_value = 0

    if request.session.get('is_login', None):
        user_name = request.session['user_name']
        user = db.catalog_users.find({'name': user_name})[0]
        if 'ratings' in user and s_detail_movie_id in user['ratings']:
            rate_value = user['ratings'][s_detail_movie_id]

    if request.method == 'POST':
        rate_value = int(request.POST.get('rate_value'))
        user_movie_rating = { s_detail_movie_id : rate_value }

        # user ratings index exist
        if 'ratings' in user:
            ratings = user['ratings']
            ratings[s_detail_movie_id] = rate_value
            db.catalog_users.update_one(
                {'name': user_name},
                {'$set': {'ratings': ratings}}
            )
        else:
            db.catalog_users.update_one(
                {'name': user_name},
                {'$set': {'ratings': user_movie_rating}}
            )
    
    context = {
        'detail_movie': detail_movie,
        'detail_movie_id': detail_movie_id,
        'rate_value': rate_value,
    }

    return render(request, 'result_detail.html', context)


def logout(request):
    if not request.session.get('is_login', None):
        
        return redirect("/index/")
    request.session.flush()

    return redirect('/index/')