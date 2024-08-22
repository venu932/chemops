from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from blog.models import Post,BlogComment
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login ,logout


# Create your views here.
def home(request):
    posts = Post.objects.filter(slug='tcs-info')

    return render(request, 'home/home.html',{'posts':posts})

def contact(request):
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):    
    search = request.GET['search']
    if len(search) >50:
        posts = Post.objects.none()
    else:
        posttitle = Post.objects.filter(title__icontains = search)
        postcontent = Post.objects.filter(content__icontains = search)
        posts = posttitle.union(postcontent)
    if posts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
        
    return render(request, 'home/search.html', {'posts':posts, 'search':search})



def handleSignUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname= request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # signup validation

        if len(username) > 10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, " Passwords do not match")
            return redirect('home')

        myuser = User.objects.create_user(username, fname, lname)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'your KDtek account has been successfully created')
        return redirect('home')
    else:
        return HttpResponse('404-Not Found')

def handleLogIn(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        
        user = authenticate(username = loginusername, password = loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')  
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect('home')

    else:
        return redirect('404-Not Found')



def handleLogOut(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

# def readContinue(request):
#     posts = Post.objects.filter(slug=slug).first()
#     comments = BlogComment.objects.filter(post=post, parent=None)
#     replies = BlogComment.objects.filter(post=post).exclude(parent=None)
#     replyDict = {}
#     for reply in replies:
#         if reply.parent.sno not in replyDict.keys():
#             replyDict[reply.parent.sno]=[reply]
#         else:
#             replyDict[reply.parent.sno].append(reply)   

#     context = {'posts':posts, 'comments':comments, 'replyDict':replyDict}
#     return render(request, 'blog/blogpost.html', context)
