from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import  never_cache
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
@never_cache
def HomePage(request):  
   return render(request,'Home.html')

@never_cache
def SignupPage(request):
    if 'username' in request.session:
        return redirect('Home')
    
    if request.method=='POST':
           
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        if not (uname and email and pass1 and pass2 ):
            messages.error(request,"Please Fill Required Fields")
            return redirect('signup')
        
        elif pass1 != pass2:
            messages.error(request,"Password Mismatch")
            return redirect('signup')     
           
        else: 
            if User.objects.filter(username = uname).exists():
                messages.error(request,"Username Already Taken")
                return redirect('signup')
            elif User.objects.filter(email = email).exists():
                messages.info(request,"Email Already Taken")
                return redirect(request,'signup')
            else:       
                my_user=User.objects.create_user(uname,email,pass1)
                my_user.save()
                return redirect('login')

    return render(request,'signup.html')

@never_cache
def LogeinPage(request):
    if 'username' in request.session:
        print(request.session)
        return redirect('Home')
    
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            request.session['username'] = username
            login(request,user)
            return redirect('Home')
        else:
            messages.info(request,"Username or Password Incorrect")
            return redirect('login') 
    return render(request,'login.html')

@ never_cache
def LogoutPage(request):
    if 'username' in request.session:
        request.session.flush()
        logout(request)
        return redirect('login')