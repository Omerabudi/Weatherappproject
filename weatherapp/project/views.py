from django.shortcuts import render
from project.models import Weather,updateweather,Favorites
from project.forms import FormName
from django.contrib.auth.models import User
from django.contrib.auth import login
import django.contrib.messages as messages
from django.http import HttpRequest

# Create your views here.
def  display_weather(request):   # מפה מגיע המידע של המזג אוויר ומוצג באתר לפי העיר/ארץ שהמשתמש מכניס
        if request.method=="POST":
            location=request.POST['location']
            url=f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid=6ba95a89897c57ceb244bd5bcf6ddcdb&units=metric"
            information=updateweather(url)
            if information["cod"]=='404':
                location='location doesnt exist'
                return render(request,'weather.html',{'location':location})
            elif information['cod']=='400':
                location='please enter a location'
                return render(request,'weather.html',{'location':location})
            else:
                show_info=Weather(information)
                return render(request,'weather.html',{'show_info':show_info,'location':location})
        return render(request,'weather.html')
# 
def single_view(request): #הצגת מידע נוסף 
    request.session['location']=request.GET.get('location','')
    location=request.session['location']
    show_info_temp=request.GET.get('show_info_temp','1')
    show_info_maxtemp=request.GET.get('show_info_maxtemp','')
    show_info_mintemp=request.GET.get('show_info_mintemp','')
    show_info_feel=request.GET.get('show_info_feel','')
    show_info_humid=request.GET.get('show_info_humid','')
    show_info_description=request.GET.get('show_info_description','')
    myDict={'show_info_temp':show_info_temp,'show_info_maxtemp':show_info_maxtemp,'show_info_mintemp':show_info_mintemp,'show_info_feel':show_info_feel,'show_info_humid':show_info_humid,'show_info_description':show_info_description,'location':location}
    if  request.method=="POST": #נלחץ הכפתור של הוספה למועדפים 
        location=request.GET.get('location','')
        userid=request.user.id
        f=Favorites(favorites=location,user_id=userid)
        try:
            f.save() 
            messages.success(request,message='Location added to favorites.')
            render(request,'singleview.html', myDict)
        except:
            messages.error(request,message='Location already in favorites')
            render(request,'singleview.html', myDict)
    return render(request,'singleview.html', myDict)

    

def show_favorites(request): # הצגת המקומות המועדפים 
    user_id=request.user.id
    locations=Favorites.objects.all().filter(user_id=user_id)
    weatherinfo=[]
    for l in locations:
            url=f"http://api.openweathermap.org/data/2.5/weather?q={l}&appid=6ba95a89897c57ceb244bd5bcf6ddcdb&units=metric"
            information=updateweather(url)
            show_info=Weather(information,location=l)
            weatherinfo.append(show_info)
    if request.method=="POST":
        print(request.POST.getlist('location'))
        # entry=Favorites.objects.all().filter(user_id=user_id)
        # entry.delete()
    return render(request,'favorites.html',{'weatherinfo':weatherinfo})


def create_user(request): # יצירת משתמש חדש
    Form=FormName
    if request.method=="POST":
        Form=FormName(request.POST)
        if Form.is_valid():
            print("Validation Success")
            print("Name:"+Form.cleaned_data['name'])
            print("Email:"+Form.cleaned_data['email'])
            print("Password:"+Form.cleaned_data['password'])
            user=User.objects.create_user(Form.cleaned_data['name'],Form.cleaned_data['email'],Form.cleaned_data['password'])
            user.save()
            login(request, user)
            return render(request,'weather.html')
    return render(request,'forms.html',{'form':Form})

def homepage(request):
    return render(request,'base.html')