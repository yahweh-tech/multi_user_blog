from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import SignupForm, PostForm, CommentForm


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "home.html", {"posts": posts})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect("post_detail", pk=pk)
        else:
            return redirect("login")
    else:
        form = CommentForm()

    return render(request, "post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form
    })


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()

    return render(request, "create_post.html", {"form": form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return redirect("home")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, "create_post.html", {"form": form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user == post.author:
        post.delete()

    return redirect("home")