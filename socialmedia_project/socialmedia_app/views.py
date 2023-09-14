from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import messages
import re
from django.contrib.auth.decorators import login_required


# Create your views here.
# @login_required(login_url='signin')
def index(request):
    user=request.user.username
    posts=Post.objects.filter(published_status=True)
    return render(request,'index.html',{'user':user,'posts':posts})

# @login_required(login_url='signin')
def profile(request):
    user=request.user.username
    user_posts=Post.objects.filter(user=user)
    return render(request,'profile.html',{'user_posts':user_posts})

def signup(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        mobile=request.POST['mobile']
        username=request.POST['username']
        password=request.POST['password']
        repassword=request.POST['repassword']

        length_psw=len(password)

        if password==repassword:
            if Users.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect(signup)
            elif length_psw<8:
                messages.info(request,'Password must contain atleast 8 letters')
                return redirect(signup)
            elif not re.search("[a-z]", password):
                messages.info(request,'Password must contain atleast one small letter')
                return redirect(signup) 
            elif not re.search("[A-Z]", password):
                messages.info(request,'Password must contain atleast one capital letter')
                return redirect(signup)
            elif not re.search("[0-9]", password):
                messages.info(request,'Password must contain atleast one number')
                return redirect(signup)
            elif not re.search("[_@$#*]" , password):
                messages.info(request,'Password must contain atleast one special character')
                return redirect(signup)
             
            else:
                user=Users.objects.create_user(username=username,email=email,password=password,mobile=mobile,name=name) #creating user in User
                user.save()
                return render(request,'signin.html')
        else:
            messages.info(request,'Passwords are not equal')
            return redirect(signup)

    else:
        return render(request,'signup.html')

    
def signin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user= authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            request.session['user_id']=user.id  
            return redirect(profile)
        else:
            messages.info(request,'Credentials invalid')
            return redirect(signin)

    else:
        return render(request,'signin.html')

# @login_required(login_url='signin')
def signout(request):
    logout(request)
    request.session.flush()
    return redirect(signin)

# @login_required(login_url='signin')
def createpost(request):
    if request.method =='POST':
        user= request.user.username
        title=request.POST['title']
        description=request.POST['description']
        tags=request.POST['tags']
        new_post=Post.objects.create(user=user,description=description,tags=tags,title=title)
        print(new_post)
        new_post.save()
        return redirect(profile)

    else:
        return redirect(profile)

# @login_required(login_url='signin')
def deletepost(request,id):
    user=request.user.username
    user_post=Post.objects.get(id=id)
    user_post.delete()
    return redirect(profile)

# @login_required(login_url='signin')
def publish(request,id):
    user_post=Post.objects.get(id=id)
    if user_post.published_status==False:
        user_post.published_status=True
        user_post.save()
        posts=Post.objects.filter(published_status=True)
        return render(request,'index.html',{'posts':posts})
    else:
        messages.info(request,'Post is already published')
        return redirect(profile)

    

# @login_required(login_url='signin')
def unpublish(request,id):
    user_post=Post.objects.get(id=id)
    if user_post.published_status==True:
        user_post.published_status=False
        user_post.save()
        messages.info(request,'Post unpublished')
        return redirect(profile)
    else:
        messages.info(request,'Post is already unpublished')
        return redirect(profile)

# @login_required(login_url='signin')
def like(request):
    username=request.user.username
    post_id=request.GET.get('post_id')

    post=Post.objects.get(id=post_id)
    like_filter=Likepost.objects.filter(post_id=post_id,username=username).first()

    if like_filter ==None:
        new_like=Likepost.objects.create(post_id=post_id,username=username)
        new_like.save()

        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect(index)
    else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect(index)