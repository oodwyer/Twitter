

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from core.models import Tweet, Hashtag
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# Create your views here.
def splash(request): 
    if request.method == "POST":
        print("request")
        body = request.POST["body"]
        t = Tweet.objects.create(body=body, author=request.user)
        t.save()
        return redirect(request.META['HTTP_REFERER'])
    return render(request, "splash.html", {})

def profile(request, username): 
    person = User.objects.get(username=username)
    tweets = Tweet.objects.filter(author=person).order_by('-created_at')
    return render(request, "profile.html", {"person": person, "tweets": tweets})

def accounts(request): 
    return render(request, "accounts.html", {})

def login_view(request): 
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else: 
            print("not work")
            messages.error(request,'username or password not correct')
    return render(request, 'accounts.html', {})

def logout_view(request):
    logout(request)
    return redirect("/login/")

def signup_view(request): 
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("/")
    return render(request, 'accounts.html', {})

def delete_view(request): 
    tweet = Tweet.objects.get(id=request.GET['id'])
    if (tweet.author == request.user):
        tweet.delete()
    else: 
        messages.error(request,'You may not delete a tweet that is not yours.')
    return redirect(request.META['HTTP_REFERER'])

def like_view(request): 
    tweet = Tweet.objects.get(id=request.GET['id'])
    tweet.num_likes = tweet.num_likes + 1
    tweet.save()
    return redirect(request.META['HTTP_REFERER'])

def home(request): 
    if request.method == "POST":
        print("request")
        body = request.POST["body"]
        t = Tweet.objects.create(body=body, author=request.user)
        t.save()
        return redirect(request.META['HTTP_REFERER'])
    tweets = Tweet.objects.all().order_by('-created_at')
    hashtags = Hashtag.objects.all()
    for h in hashtags: 
        print(h.name)
        related = h.tweets.all()
        if len(related) == 0:
                h.delete()
    for t in tweets: 
        text = t.body
        print(text)
        num = 0
        while num < len(text):
            if text[num] == '#': 
                x = '' 
                num = num + 1
                while num < len(text): 
                    if (text[num] == ' ') | (num == (len(text) - 1)): 
                        if num == len(text) - 1: 
                            x = x + text[num]
                        tracking = False
                        try:
                            h=Hashtag.objects.get(name=x)
                        except MultipleObjectsReturned as e:
                            print("multiple objects")
                            break
                        except ObjectDoesNotExist as e:
                            newHash = Hashtag.objects.create(name=x)
                            newHash.tweets.add(t)
                            break
                        else:
                            h.tweets.add(t)
                            break  
                    else: 
                        x = x + text[num]
                        print(x)
                        num = num + 1
            else: 
                num = num + 1
    return render(request, "home.html", {"tweets": tweets, "hashtags": hashtags})

def hashtag(request, name): 
    h = Hashtag.objects.get(name=name)
    tweets = h.tweets.all().order_by('-created_at')
    hashtags = Hashtag.objects.all()
    return render(request, "hashtag.html", {"h": h, "hashtags": hashtags, "tweets": tweets})