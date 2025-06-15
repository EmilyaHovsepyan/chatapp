from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import User
from .models import groupinfo, userinfo


def MainPage(request):
    return render(request, 'MainPage.html')

def SignInPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('reg')
    else:
        return render(request, 'SignInPage.html')
    
def cool(request):
    res = groupinfo.objects.filter(members__username = request.user.username)
    # print(res)
    result = []
    alluserinfo = []
    # groupids = []
    for i in res:
        members = list(i.members.values_list('username', flat=True))
        if i.groupimg:
            result.append({'groupname':i.groupname, 'groupid':i.id, 'groupimgurl':i.groupimg.url, 'members':members, 'bgname':i.bgname})
        else:
            result.append({'groupname':i.groupname, 'groupid':i.id, 'groupimgurl':'nourl', 'members': members, 'bgname':i.bgname})
            
    print(result)
    print('result from views printed on top')
    # print(request.user.username)
    info = userinfo.objects.get(username = request.user)

    allinfo = userinfo.objects.all()
    for i in allinfo:
        alluserinfo.append({
            'username':i.username.username,
            'name':i.name if i.name else 'noname',
            'bio': i.bio if i.bio else 'nobio',
            'url':i.photo.url if i.photo else 'nourl',
        })
    
    print(alluserinfo)
    return render(request, 'ChatPage.html', {'groupinfo':result, 'userinfo':info, 'alluserinfo':alluserinfo})

# def profilepicimg(request): 
#     if request.method == 'POST':
#         photo = request.FILES['imageinput']
#         res = userinfo.objects.get(username__username = request.user.username)
#         oldphoto = res.photo.name
#         default_storage.delete(oldphoto)
#         instance = default_storage.save('profilepic/'+ photo.name, ContentFile(photo.read()))
#         print('our instance is ')
#         print(instance) 
#         res.photo = instance
#         res.save()
#         url = default_storage.url(instance)
#         print('our url is')
#         print(url)
        
#         print('photo saved to folder and model')
#         return JsonResponse({'profilepic':True, 'url':url})
#     else:
#         return HttpResponse("something went wrong")
    

def profilepicimg(request):
    if request.method == 'POST':
        img = request.FILES['photo']
        print(img)
        instance = default_storage.save('profilepic/' + img.name, ContentFile(img.read()))
        print(instance)
        url = default_storage.url(instance)
        print(url)
        user = userinfo.objects.get(username = request.user)
        default_storage.delete(user.photo.name)
        user.photo = instance
        user.save()
        
        return JsonResponse({'profilepic':True, 'url':url})
    else:
        return HttpResponse('something went wrong')

def usernamenew(request):
    if request.method == 'POST':
        if request.POST['username']:
            username = request.POST['username']
            user = User.objects.get(username = request.user.username)
            user.username = username
            user.save()
            return JsonResponse({'username':username})
           
        return HttpResponse('done ig')
    else:
        return HttpResponse('smth went wrong in usernamenew')
    
def namenew(request):
    if request.method == 'POST':
        name = request.POST['name']

        userrinfo = userinfo.objects.get(username = request.user)
        print(userinfo)
        userrinfo.name = name
        print(userrinfo.name)
        userrinfo.save()
        return JsonResponse({'name':name})
    else:
        print('something went wrong')

def bionew(request):
    if request.method == 'POST':
        print('mtav')
        bio = request.POST['bio']
        user = userinfo.objects.get(username = request.user)
        user.bio = bio
        user.save()
        return JsonResponse({'bio':bio})
    else:
        return HttpResponse('smth went wrong((')
