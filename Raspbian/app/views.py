#coding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import Template
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from app.hardware import dht11
from app.models import TH_FORM
import os
import sys
import RPi.GPIO
import requests
import json
import time
import datetime
from picamera import PiCamera


RPi.GPIO.setmode(RPi.GPIO.BCM)

def thdata():
    while True:
        instance = dht11.DHT11(4)
        result = instance.read()
        if result.is_valid():
            temp=result.temperature
            hum =result.humidity
            RPi.GPIO.cleanup(4)
            now = time.strftime('%Y %m %d %H %M %S', time.localtime(time.time()))
            thd = TH_FORM(timeval=now,temperature=temp,humidity=hum)
            thd.save()
        time.sleep(120)




@login_required()
def face(request):
	return render(request,'face.html')


# 主页
@login_required()
def index(request):
	return render(request,'index.html')

#查看
@login_required()
def look(request):
	if request.method == 'POST':
		instance = dht11.DHT11(4)
		result = instance.read()

		if result.is_valid():
			temp = "%d ℃" % result.temperature
			hum = "%d %%" % result.humidity
			RPi.GPIO.cleanup(4)
			return JsonResponse({'temperature': temp, 'humidity': hum})
		else:
			return HttpResponse('error')

	else:
		instance = dht11.DHT11(4)
		result = instance.read()

		temp = "%d ℃" % result.temperature
		hum = "%d %%" % result.humidity
		RPi.GPIO.cleanup(4)


		return render(request, 'look.html', {'temperature': temp, 'humidity': hum})


def logout(request):
	auth.logout(request)
	return redirect('/login')

# 登录
def login(request):
	if request.method =='POST':
		username = request.POST['username']
		password = request.POST['password']
		#验证登录，正确则authenticate()返回一个User对象，错误则返回一个None类
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth.login(request, user)#登录用户
				return redirect('/',{'username':username})#使用重定向而不是render返回首页，可以避免刷新再次提交表单导致出错
			else:
				NOT_ACTIVE = '你的账户没有激活，请联系管理员Ck：ckxs1021@163.com'
				render(request,'login.html',{'NOT_ACTIVE':NOT_ACTIVE})
		else:
			ERROR = 'Typing Error'
			return render(request,'login.html',{'ERROR':ERROR })

	else:
		LOGIN = '智能家居系统'
	return render(request,'login.html',{'LOGIN':LOGIN})

#查看历史数据
@login_required()
def history(request):
	return render(request,'history.html')

#人脸比对的页面
@login_required()
def face(request):
	return render(request,'face.html')

@login_required()
def take_a_photo(request):
    # 实例化一个相机类
    camera = PiCamera()

    # 照片名由时间组成
    now = datetime.datetime.now()
    face_name = now.strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'

    # 拍好照片的存放地址
    face_address = 'app/static/face/'

    # 拍一个照片需要提供照片名和存放地址
    face = face_address + face_name

    # 需要把刚拍的照片返回给ajax以更新客户端的图片，但模板的img src不需要app/后缀
    img = "/static/face/" + face_name

    # 设置相机的分辨率
    camera.resolution = (1280, 720)
    camera.rotation = 180
    # 相机预览，很可惜只有接上显示屏才能预览，ssh方式无法预览
    camera.start_preview()
    # 相机启动需要点时间
    time.sleep(2)
    # 拍照，把大小裁剪为1024x768，太大不适合提交给人脸比对
    camera.capture(face, resize=(1024, 768))

    # 关闭相机，否则http一直在连接
    camera.close()
    # 返回照片名以更新客户端照片
    return HttpResponse(img)


# 人脸比对功能
@login_required()
def face_compare(request):
    # 获取要人脸比对的两张图片，加上app/后缀才能在服务端找到本地图片
    face1 = 'app/' + request.GET['img1']
    face2 = 'app/' + request.GET['img2']
    # face++的应用api_key和api_secret
    api_key = 'vigklkgJlKAFaSOuRfQGNcNAPz2Jrkfk'
    api_secret = 'rnLgNWHIACuE6KcpWIlxf13Bc6uDpqDW'
    # 接入face++ 人脸比对API
    url = 'https://api-cn.faceplusplus.com/facepp/v3/compare?api_key=%s&api_secret=%s' % (api_key, api_secret)
    # 载入两个本地图片进行比对
    files = {
        'image_file1': open(face1, 'rb'),
        'image_file2': open(face2, 'rb'),
    }

    # 二进制文件，需要用post multipart/form-data的方式上传
    r = requests.post(url=url, files=files)
    # 人脸比对的response，是一个json包
    data = r.json()
    # 人脸数据，若识别不出人脸则为空list
    faces1 = data.get('faces1')
    faces2 = data.get('faces2')
    # 格式化json数据，以便在html中展示
    JSON = json.dumps(data, indent=1)

    print(data)
    # 若人脸能识别出来，则face1/2是非空list
    if (len(faces1) != 0) and (len(faces2) != 0):
        # 认证系数，[0,100]，大于60则可认为是同一个人
        confidence = data.get('confidence')
        if confidence >= 60:

            compare_result = '是同一个人'
            result = {'compare_result': compare_result, 'JSON': JSON}
            return JsonResponse(result)

        elif confidence < 60:

            compare_result = '不是同一个人'
            result = {'compare_result': compare_result, 'JSON': JSON}
            return JsonResponse(result)
    else:

        compare_result = '未能检测到人脸'
        result = {'compare_result': compare_result, 'JSON': JSON}
        # 使用JsonResponse能更好的返回json数据
        return JsonResponse(result)
