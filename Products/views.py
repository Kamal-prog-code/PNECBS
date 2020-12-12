from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from .forms import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
import json

# Create your views here.
def products(request):
    items = Items.objects.all()
    return render(request, 'items/list.html',{'items':items})  

def home(request):
    form = MediaForm()    
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'home.html',context)

def contact(request):
    return render(request,'contact.html')

def contents(request,pk):
    item = Items.objects.get(id=pk) 
    overset = item.content_set.get(item_id=pk)
    context={'item':item,'overset':overset}
    return render(request,'content.html',context)    
#Authentication
def signup(request):
    if request.method == 'POST':
        fm = UserForm(request.POST)
        if fm.is_valid():
            user = User.objects.create_user(username=fm.cleaned_data['User_Name'],
                                            password=fm.cleaned_data['Password'],
                                            email=fm.cleaned_data['Email'])

            user.save()
            fm.save()
            return redirect('login')
    else:
        fm = UserForm()
    return render(request,'signup.html',{'form':fm})

def login(request):
    if request.method=='POST':        
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            if user.is_staff:
                return redirect('home')
            else:
                return redirect('products')
        else:
            msg = "Invalid username or password."    
            return HttpResponse(msg)    
    else:
        return render(request,'login.html')  


def get_content(request):
    data = json.loads(request.body)
    iid = str(data['itemid'])
    inf = info.objects.all()
    if len(inf) == 0:
        newi = info.objects.get_or_create(itemid=iid,usern=str(request.user))
    fir = info.objects.first()    
    upd = info.objects.filter(itemid=fir).update(itemid=iid,usern=str(request.user))
    return JsonResponse(iid, safe=False)   


@api_view(['GET'])
def itemdetail(request,pk):
    item = Items.objects.get(id=pk)
    serializer = ItemsSerializer(item)
    return Response(serializer.data)

@api_view(['GET'])
def contentdetail(request,pk):
    content = Content.objects.get(id=pk)
    serializer = ContentSerializer(content)
    return Response(serializer.data)

@api_view(['GET'])
def contentid(request):
    itemid = info.objects.first()
    serializer = infoSerializer(itemid)
    return Response(serializer.data)    

