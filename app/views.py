from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponseNotFound
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    posts = Post.objects.all()
    pages = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = pages.get_page(page)
    context = {
        'posts': posts,
        'title': 'Главная страница',
        'students': ["Вася", "Петя", "Даня", "Маша"]
    }
    return render(request, 'index.html', context)


def about(request):
    context = {
        'title': 'О компании'
    }
    return render(request, 'about.html', context)


def contacts(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'contacts.html', context)


def post_detail(request, slug):
    post = Post.objects.filter(slug=slug)
    form = CommentForm(request.POST or None)
    parent_id = request.POST.get('parent_id')

    com = post[0].comment_set.filter(first_comment=None)
    pages = Paginator(com, 2)
    page = request.GET.get('page')
    comments = pages.get_page(page)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.post = post[0]
        if parent_id:
            main_comment = post[0].comment_set.get(pk=parent_id)
            instance.parent = main_comment

            if not main_comment.first_comment:
                instance.first_comment = main_comment
            else:
                instance.first_comment = main_comment.first_comment

        instance.save()
        return redirect('app:post', slug=slug)

    if not post:
        return HttpResponseNotFound(
            'Такой страницы не существует'
        )
    post = post[0]
    return render(request, 'post.html', {'post': post, 'form': form, 'comments': comments})


@login_required(login_url='/users/sign-in')
def post_create(request):
    post_form = PostForm(request.POST)

    if request.method == 'POST' and post_form.is_valid():
        images = request.FILES.getlist('images')

        instance = post_form.save(commit=False)
        instance.author = request.user
        instance.save()

        if images:
            for image in images:
                Photo.objects.create(post=instance, image=image)
        else:
            Photo.objects.create(post=instance)

        return redirect('app:index')

    post_form = PostForm()
    return render(request, 'post_create.html',
                  {'post_form': post_form})


def like(request):
    model = request.GET.get('model')
    action = request.GET.get('action')
    value = request.GET.get('value')

    if model == 'post':
        object = Post.objects.get(slug=value)
    else:
        object = Comment.objects.get(pk=value)

    user = request.user

    if action == 'like':
        if user not in object.likes.all():
            object.likes.add(user)
            object.dislikes.remove(user)
        elif user in object.likes.all():
            object.likes.remove(user)
    else:
        if user not in object.dislikes.all():
            object.dislikes.add(user)
            object.likes.remove(user)
        elif user in object.dislikes.all():
            object.dislikes.remove(user)

    slug = object.slug if not value.isdigit() else object.post.slug
    return redirect('app:post', slug=slug)


def delete_post(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('app:index')
    return render(request, 'delete_post.html', {'post': post})
