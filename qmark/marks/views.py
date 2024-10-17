from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.shortcuts import render, get_object_or_404
from django.views import View

from PIL import Image, ImageEnhance, ImageOps, ImageGrab,ImageDraw, ImageFont
from .models import Post, Thing, Room, Comment, Company
from .forms import SignUpForm, SignInForm, CommentForm, AddThingForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

import os,qrcode

class MainView(View):
	def get(self, request, *args, **kwargs):
		posts = Post.objects.all().order_by('-created_at')
		paginator = Paginator(posts, 6)

		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
        
		if request.user.is_authenticated:
			things = Thing.objects.filter(author=request.user).order_by('-created_at')
			comps = Company.objects.filter(members=request.user).order_by('id')
		else:
			things = Thing.objects.filter(visible='a').order_by('-created_at')
			comps = Company.objects.filter(members=0).order_by('id')
		
		paginator = Paginator(things, 30)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		
		return render(request, 'marks/index.html', context={
            'page_obj': page_obj, 'comps': comps, 'things': things, 
        })

class HomeView(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			things = Thing.objects.filter(author=request.user).order_by('-created_at')
		else:
			things = Thing.objects.filter(visible='a').order_by('-created_at')
			
		return render(request, 'marks/home.html', context={
            'things': things, 
        })

class CompanyView(View):
	def get(self, request, *args, **kwargs):
		rooms = Room.objects.filter(company=request.id).order_by('name')
		return render(request, 'marks/rooms.html', context={
            'rooms': rooms
        })

class RoomsView(View):
	def get(self, request, *args, **kwargs):
		rooms = Room.objects.all().order_by('name')
		return render(request, 'marks/rooms.html', context={
            'rooms': rooms
        })

class RoomView(View):
	def make_labels(self, name, url):
		qr_img = "media/qr/"+url+'.png';
		lbl_img = "media/lbl/"+url+'.png';
		
		img=qrcode.make("https://qmarkit.ru/thing/"+url+"?src=qr")
		img.save(qr_img)
		
		w=img.size[0]*3
		h=img.size[1]
		im = Image.new("L", (w, h))
		
		im.paste(img)
			
		idraw = ImageDraw.Draw(im)
		idraw.rectangle( (h,0,w,h),	255)
		text = "https://qmarkit.ru/thing/"+url
			
		# подключаем Font и задаем высоту в пикселях
		font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", size=38)
		# вычисляем длину надписи 
		textlength = idraw.textlength(text, font)
		# вычисляем положение надписи на скриншоте, например по ширине
		# ширина скриншота - длина надписи - граница 2px + 10px
		size = (w, h-88)
			
		idraw.text(size, text, font=font, fill='black')
		idraw.text((w,40), name , font=font, fill='black')
			
		im.save(lbl_img)
		return
		
	def get(self, request, slug, *args, **kwargs):
		room = Room.objects.filter(number=slug)
		print (room[0].id)
		things = Thing.objects.filter(room=room[0].id).order_by('-created_at')
		for thing in things:
			qr_img = "media/qr/"+thing.url+'.png';
			lbl_img = "media/lbl/"+thing.url+'.png';
			if os.path.isfile(lbl_img):
				print(qr_img, "qr exists")
			else:
				self.make_labels(thing.name, thing.url)
				print("creating image", qr_img)
		return render(request, 'marks/room.html', context={
            'things': things, 'room': slug
        })
        
class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        return render(request, 'marks/post_detail.html', context={
            'post': post
    })

class ThingsView(View):
	def get(self, request, *args, **kwargs):
		things = Thing.objects.all().order_by('-created_at')
		return render(request, 'marks/room.html', context={
            'things': things, 'room': "any room"
    })

class AddView(View):
	def get(self, request, *args, **kwargs):
		print("add-get")
		things = Thing.objects.all().order_by('-created_at')
		thing_form = AddThingForm()
		return render(request, 'marks/add_thing.html', context={
            'thing_form': thing_form, 'room': "any room"
    })
    
    
	def post(self, request, *args, **kwargs):
		print("add-post")
		thing_form = AddThingForm(request.POST, request.FILES)
		if thing_form.is_valid():
			print("form is valid")
			if request.FILES:
				image = request.FILES['image']
			else:
				image=''
			name = request.POST['name']
			number = request.POST['number']
			url = number
			description = request.POST['description']
			visible = 'u'
			username = self.request.user
			if image!='':
				print("create thing with image")
				Thing.objects.create(name=name,number=number,visible=visible,
					url=url,description=description,image=image,author=username,
					tag='')
			else:
				print("create thing without image")
				Thing.objects.create(name=name,number=number,visible=visible,
					url=url,description=description,image='default.png',author=username,
					tag='')
		else:
			print("form is not valid")			
		things = Thing.objects.filter(author=request.user).order_by('-created_at')
		#comment_form = CommentForm()
		#return render(request, 'marks/thing_detail.html', context={
		#	'comment_form': comment_form })
		return render(request, 'marks/index.html', context={
             'things': things, 
        })
        

class ThingDetailView(View):
	def make_labels(self, name, url):
		qr_img = "media/qr/"+url+'.png';
		lbl_img = "media/lbl/"+url+'.png';
		
		img=qrcode.make("https://qmarkit.ru/thing/"+url+"?src=qr")
		img.save(qr_img)
		
		w=img.size[0]*3
		h=img.size[1]
		im = Image.new("L", (w, h))
		
		im.paste(img)
			
		idraw = ImageDraw.Draw(im)
		idraw.rectangle( (h,0,3*h,h),	255)
		text = "https://qmarkit.ru/thing/"+url
			
		# подключаем Font и задаем высоту в пикселях
		font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", size=38)
		# вычисляем длину надписи 
		textlength = idraw.textlength(text, font)
		# вычисляем положение надписи на скриншоте, например по ширине
		# ширина скриншота - длина надписи - граница 2px + 10px
		size = (400, im.size[1]-88)
			
		idraw.text(size, text, font=font, fill='black')
		idraw.text((400,40), name , font=font, fill='black')
			
		im.save(lbl_img)
		return
	
	def get(self, request, slug, *args, **kwargs):
		thing = get_object_or_404(Thing, url=slug)
		comment_form = CommentForm()
		
		print(thing)
		qr_img = "media/qr/"+thing.url+'.png';
		lbl_img = "media/lbl/"+thing.url+'.png';
		if os.path.isfile(lbl_img):
			print(qr_img, "qr exists")
		else:
			self.make_labels(thing.name, thing.url)
		
		return render(request, 'marks/thing_detail.html', context={
		'thing': thing, 'comment_form': comment_form })
    
	def post(self, request, slug, *args, **kwargs):
		comment_form = CommentForm(request.POST, request.FILES)
		if comment_form.is_valid():
			if request.FILES:
				image = request.FILES['image']
				print ("upload:",image)
			else:
				image=''
			text = request.POST['text']
			username = self.request.user
			thing = get_object_or_404(Thing, url=slug)
			if image!='':
				Comment.objects.create(thing=thing, username=username, text=text, image=image)
			else:
				Comment.objects.create(thing=thing, username=username, text=text)
			return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
		return render(request, 'marks/thing_detail.html', context={
			'comment_form': comment_form
        })

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'marks/signup.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'marks/signup.html', context={
            'form': form,
        })
        
class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'marks/signin.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, "Неправильный пароль или указанная учётная запись не существует!")
                return render(request, "marks/signin.html", {"form": form})
        return render(request, 'marks/signin.html', context={
            'form': form,
        })
