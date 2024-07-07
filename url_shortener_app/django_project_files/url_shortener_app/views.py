from django.contrib.auth.models import auth, User
from django.shortcuts import redirect, render
from .shortener_engine import encoding
from .models import Urls


# Create your views here.

def get_url_list(request):
    url_list = []
    url_query_set = Urls.objects.filter(username=request.user.username).values()

    for x in url_query_set:
        url_dict = {
            "website_name": x["website_name"],
            "hashed_url": x["hashed_url"]
        }
        url_list.append(url_dict)

    return url_list
def home(request):
    if request.user.is_authenticated:
        return redirect("landing_page")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("landing_page")
            else:
                return render(request, "login.html", {'error': 'Invalid username or password!'})
        else:
            return render(request, "login.html")
def landing_page(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            website_name = request.POST["website_name"]
            website_url = request.POST["url"]
            url_list = get_url_list(request)

            if website_name and website_url:
                encoded_url = encoding(website_url)

                for x in url_list:
                    if x['hashed_url'] == encoded_url:
                        website_name = x['website_name']
                        duplicate_entry = {
                            "error": "URL already added",
                            "website_name": website_name,
                            "url_list": url_list
                        }
                        return render(request, "landing_page.html", duplicate_entry)
                url = Urls(url=website_url, hashed_url=encoded_url, website_name=website_name,
                           username=request.user.username)
                url.save()
                return redirect("landing_page")
            else:
                missing_input = {
                    "error": "Enter both website name and URL!",
                    "url_list": url_list
                }
                return render(request, "landing_page.html", missing_input)
        else:
            url_list = get_url_list(request)
            return render(request, "landing_page.html", {"url_list": url_list})
    else:
        return redirect("home")
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect("home")
        else:
            return render(request, "signup.html", {"error": "Passwords are not matching!"})
    else:
        return render(request, "signup.html")
def delete_multiple(request):
    delete_list = request.POST.getlist("url_list[]")
    if delete_list:
        for i in delete_list:
            url = Urls.objects.filter(username=request.user.username, hashed_url=i).first()
            url.delete()
        return redirect("landing_page")
    else:
        url_list = get_url_list(request)
        empty_list = {
            "error": "Select at-least one stock from the list before clicking delete!",
            "url_list": url_list
        }

        return render(request, "landing_page.html", empty_list)
def re_routing(request, hash_value):
    if request.method == "POST" or request.method == "GET":
        url_query_set = Urls.objects.filter(hashed_url=hash_value).first()
        print(url_query_set)
        url = url_query_set.url
        return redirect(url)
def user_profile(request):
    if request.user.is_authenticated:
        return render(request, "user_profile_page.html", {'user': request.user})
def logout(request):
    auth.logout(request)
    return redirect("home")
