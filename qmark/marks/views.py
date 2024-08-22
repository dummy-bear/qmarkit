from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Post, Thing, Room, Comment
from .forms import SignUpForm, SignInForm, CommentForm, AddThingForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


class MainView(View):
	def get(self, request, *args, **kwargs):
		posts = Post.objects.all().order_by('-created_at')
		paginator = Paginator(posts, 6)

		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
        
		if request.user.is_authenticated:
			things = Thing.objects.filter(author=request.user).order_by('-created_at')
		else:
			things = Thing.objects.filter(visible='a').order_by('-created_at')
			
		return render(request, 'marks/index.html', context={
            'page_obj': page_obj, 'things': things, 
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

class RoomsView(View):
	def get(self, request, *args, **kwargs):
		rooms = Room.objects.all().order_by('-created_at')
		return render(request, 'marks/rooms.html', context={
            'rooms': rooms
        })

class RoomView(View):
	def get(self, request, slug, *args, **kwargs):
		things = Thing.objects.all().order_by('-created_at')
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
		things = Thing.objects.all().order_by('-created_at')
		return render(request, 'marks/room.html', context={
            'things': things, 'room': "any room"})
		

class ThingDetailView(View):
	def get(self, request, slug, *args, **kwargs):
		thing = get_object_or_404(Thing, url=slug)
		comment_form = CommentForm()
		
		print(thing)
		
		return render(request, 'marks/thing_detail.html', context={
		'thing': thing, 'comment_form': comment_form })
    
	def post(self, request, slug, *args, **kwargs):
		comment_form = CommentForm(request.POST, request.FILES)
		if comment_form.is_valid():
			if request.FILES:
				image = request.FILES['image']
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
