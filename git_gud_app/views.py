from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from git_gud_app.forms import PostForm
from git_gud_app.models import Post


def index(request):
    post_objects = Post.objects.all().order_by('-date_submitted', )

    paginator = Paginator(post_objects, 12)
    page = request.GET.get('page')

    post_form = PostForm()

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'post_objs': post_objects, 'paginator': paginator,
                                          'posts': posts, 'page': page, 'post_form': post_form})


def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.submitter = request.user
            post.save()

            return HttpResponseRedirect(reverse('index'))


def delete_post(request, post_id):
    if request.method == 'GET':
        # I really hate to use GET for this but bootstrap-confirmation fought me
        post = Post.objects.get(id=post_id)
        if post.submitter == request.user or request.user.is_staff:
            post.delete()

        return HttpResponseRedirect(reverse('index'))


def vote(request, post_id, weight):
    post = Post.objects.get(id=post_id)
    user = request.user

    # manually sets the post's score since django-vote downvote is weird
    # but still adds the user to post.votes to check for duplicate voting and so the template tag
    # doesn't break
    if not post.votes.exists(user):
        if weight == 'up':
            post.votes.up(user)
            post.score += 1
        elif weight == 'down':
            post.votes.up(user)
            post.score -= 1

    response_data = {}
    try:
        post.full_clean()
        post.save()
        response_data['voted'] = True
    except ValidationError as e:
        response_data['voted'] = False

    response_data['score'] = post.score

    return JsonResponse(response_data)
