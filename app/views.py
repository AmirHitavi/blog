from django.shortcuts import render, redirect
from .models import Post, WebsiteMeta, Comment, Tag, Profile
from .forms import SubscribeForm, CommentForm
from django.db.models import Count
from django.contrib.auth.models import User

def index(request):
    top_posts = Post.objects.all().order_by("-view_count")[:3]
    recent_posts = Post.objects.all().order_by("-last_updated")[:3]
    featured_post = None
    website_info = None
    subscribe_form = SubscribeForm()
    subscribe_successful = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if Post.objects.filter(is_featured=True).exists():
        featured_post = Post.objects.filter(is_featured=True)[0]

    if request.method == "POST":
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            request.session["subscribed"] = True
            subscribe_successful = 'Subscribed Successfully'
            subscribe_form = SubscribeForm()

    context = {
        'featured_post': featured_post,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'website_info': website_info,
        'subscribe_form': subscribe_form,
        'subscribe_successful': subscribe_successful
    }

    return render(request, 'app/index.html', context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post, parent=None).order_by("-date")
    count_comment = Comment.objects.filter(post=post).count()
    comment_form = CommentForm()
    top_posts = Post.objects.exclude(slug=slug).order_by("-view_count")[:3]
    recent_posts = Post.objects.exclude(slug=slug).order_by("-last_updated")[:3]
    top_tags = Tag.objects.annotate(post_count=Count("post")).order_by("-post_count")[:10]

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_object = None
            if request.POST.get("parent"):
                parent = request.POST.get("parent")
                parent_object = Comment.objects.get(id=parent)
                if parent_object:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_object
                    comment_reply.post = post
                    comment_reply.save()
                    return redirect("post_page", slug=slug)
            else:
                comment = comment_form.save(commit=False)
                post_id = request.POST.get("post_id")
                post = Post.objects.get(id=post_id)
                comment.post = post
                comment.save()
                return redirect("post_page", slug=slug)

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1

    post.save()

    context = {
        "post": post,
        "comments": comments,
        "count_comments": count_comment,
        "comment_form": comment_form,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
        "top_tags": top_tags
    }
    return render(request, "app/post.html", context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by("-view_count")[:3]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by("-last_updated")[:3]
    top_tags = Tag.objects.exclude(slug=slug).annotate(post_count=Count('post')).order_by('-post_count')[:10]
    other_tags = Tag.objects.exclude(slug=slug)[:10]

    context = {
        "tag": tag,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
        "top_tags": top_tags,
        "other_tags": other_tags
    }
    return render(request, "app/tag.html", context)


def author_page(request, slug):
    author = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(author=author.user).order_by("-view_count")[:3]
    recent_posts = Post.objects.filter(author=author.user).order_by("-last_updated")[:3]
    top_authors = User.objects.filter(is_staff=True).exclude(profile=author)\
                      .annotate(post_count=Count("post")).order_by("-post_count")[:5]
    other_authors = User.objects.filter(is_staff=True).exclude(profile=author)[:5]

    context = {
        "author": author,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
        "top_authors": top_authors,
        "other_authors": other_authors
    }
    return render(request, "app/author.html", context)


def search_posts(request):
    search_query = ''
    if request.GET.get("q"):
        search_query = request.GET.get("q")

    posts = Post.objects.filter(title__icontains=search_query)

    context = {
        "search_query": search_query,
        "posts": posts
    }
    return render(request, 'app/search.html', context)


def about(request):
    website_info = None
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    context = {
        "website_info": website_info
    }
    return render(request, "app/about.html", context)