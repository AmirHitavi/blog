from django.shortcuts import render
from .models import Post, WebsiteMeta
from .forms import SubscribeForm


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
    print(website_info.title)

    return render(request, 'app/index.html', context)
