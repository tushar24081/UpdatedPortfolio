from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import CreatePost, CommentForm
from .filters import PostFilter
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.

def home(request):
	posts = Post.objects.filter(active = True, featured = True)[0:3]
	tags = Tag.objects.all()[0:5]
	context = {'posts' : posts, 'tags':tags}	
	print(tags)
	return render(request, 'base/index.html', context)

def posts(request):
	posts = Post.objects.filter(active = True)
	myFilter = PostFilter(request.GET, queryset = posts)
	posts = myFilter.qs

	page = request.GET.get('page')
	paginator = Paginator(posts, 3)

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	print(posts.number)
	context = {'posts' : posts, 'myFilter' : myFilter}
	return render(request, 'base/posts.html', context)

def post(request, slug):
	post = Post.objects.get(slug = slug)
	c_form = CommentForm()
	if request.method == "POST":
		c_form = CommentForm(request.POST)
		if c_form.is_valid():
			instance = c_form.save(commit = False)
			instance.post = Post.objects.get(id = request.POST.get('post-id'))
			instance.user = request.POST.get('user')
			instance.email = request.POST.get('email')
			instance.save()
			c_form = CommentForm()

			email = EmailMessage(
				instance.user + ' Commented On ' + instance.post.headline,
				instance.body + ' Email: ' + instance.email,
				settings.EMAIL_HOST_USER,
				['tushar24081@gmail.com']
				)
			email.fail_silently = False
			email.send()
			print("Mail sent")
	context = {'posts' : post, 'c_form': c_form}
	return render(request, 'base/post.html', context)

def profile(request):
	return render(request, 'base/profile.html')

def tagPosts(request, name):
	posts = Post.objects.filter(tags__name = name)
	print(posts)
	myFilter = PostFilter(request.GET, queryset = posts)
	posts = myFilter.qs
	context = {'posts': posts, 'name':name}
	return render(request, 'base/posts.html', context)

@login_required(login_url = 'home')
def createPost(request):
	form = CreatePost()
	if request.method == "POST":
		form = CreatePost(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return redirect('posts')
	context = {'form' : form}
	return render(request, 'base/post_form.html', context)

@login_required(login_url = 'home')
def updatePost(request, slug):
	post = Post.objects.get(slug = slug)
	form = CreatePost(instance = post)
	if request.method == "POST":
		form = CreatePost(request.POST, request.FILES, instance = post)
		if form.is_valid():
			form.save()
		return redirect('posts')
	context = {'form' : form}
	return render(request, 'base/post_form.html', context)


@login_required(login_url = 'home')
def deletePost(request, slug):
	post = Post.objects.get(slug=slug)
	if request.method == 'POST':
		post.delete()
		return redirect('posts')
	context = {'item' : post}
	return render(request, 'base/delete_confirm.html', context)


def send_email(request):
	print("It's here..")
	if request.method == 'POST':
		template = render_to_string('base/email_template.html', {
			'name': request.POST['name'],
			'email': request.POST['email'],
			'message': request.POST['message'],
			})

		print(template)

		email = EmailMessage(
			request.POST['subject'],
			template,
			settings.EMAIL_HOST_USER,
			['tushar24081@gmail.com']
			)
		email.fail_silently = False
		email.send()

	return render(request, 'base/email_sent.html')
def sendMail(request):
	if request.method == "POST":
		email = request.POST.get('email')
		name = request.POST.get('name')

		if SendMail.objects.filter(email = email).exists():
			exist = True
		else:
			se = SendMail.objects.create(email = email, name=name)
			se.save()
			exist = False
		print("PROCESS DONE!!")
		print(exist)
		context = {
		'exist': exist
		}
	return render(request, 'base/mail.html', context)

def mail(request):
	if request.method == "POST":
		se = SendMail.objects.all()
		email_list = []

		for email in se:
			email_list.append(email.email)
		subject = request.POST.get('subject')
		html_content = request.POST.get('html_content')
		from_email = "tushar24081@gmail.com"
		text_content = ""
		to = email_list

		msg = EmailMultiAlternatives(subject, text_content, from_email, to)
		msg.attach_alternative(html_content, "text/html")
		msg.send()


	return render(request, 'base/sending_mail.html')