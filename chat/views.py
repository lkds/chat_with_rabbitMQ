from django.shortcuts import render

def gotoLogin(request):
    return render(request,'login.html')


# Create your views here.
def login(request):
    #接收登录页面传来的用户id
    loginId = request.Post.get('loginId',None)

    return render(request, 'login.html', {'msg':' 登录成功'})