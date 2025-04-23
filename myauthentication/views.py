import re
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
# Create your views here.
from django.shortcuts import redirect

def handleSignUp(request):
    if request.method=="GET":
        return render(request,'auth/signup.html')
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        usertype=request.POST['usertype']
        usertype=str(usertype)
        usertype=usertype
        # validating the passwords 
        if (pass1!= pass2):
            #  messages.ERROR(request, " Passwords do not match")
             print("Passwords do not match")
             return redirect('/auth/signup')
        #  validting the email
        if(not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)):
            # messages.ERROR(request, " Passwords do not match")
            print("Invalid email")
            return redirect('/auth/signup')
        if usertype=="Teacher" or usertype=="Student":
            print("valid user type ")
        else:
            print("invalid user type")
        # print(username+" : "+email+" : "+fname+" : "+lname+" : "+pass1+" : "+pass2+" : "+usertype)
        # Create the user
        if(usertype=="Teacher"):
            myuser = User.objects.create_user(username=username, email=email, password=pass1, is_staff=True)
            myuser.first_name= fname
            myuser.last_name= lname
            myuser.save()
            User.is_superuser
        if(usertype=="Student"):
            myuser = User.objects.create_user(username=username, email=email, password=pass1, is_staff=False)
            myuser.first_name= fname
            myuser.last_name= lname
            myuser.save()
        # messages.success(request, " Your iCoder has been successfully created")
        return redirect('/auth/login')
        return HttpResponse(request,username+" : "+email+" : "+fname+" : "+lname+" : "+pass1+" : "+pass2+" : "+usertype)
    else:
        return HttpResponse("404 - Not found")
def handeLogin(request):
    if request.method=="GET":
        return render(request,'auth/login.html')
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username= loginusername, password= loginpassword)
        # HttpResponse(loginusername+" "+loginpassword)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/teacher/')
            else:
                return redirect('/student/')
                
        else:
            # messages.error(request, "Invalid credentials! Please try again")
            # return redirect("home")
            return HttpResponse("Invalid credential")

    return HttpResponse("404- Not found")
def handelLogout(request):
    logout(request)
    # messages.success(request, "Successfully logged out")
    return redirect('/auth/login/')
