# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.shortcuts import get_object_or_404, render
from list_posts.models import Post


class PostView(generic.DetailView):
    model = Post
    template_name = 'list_posts/post.html'


def index(request):
    latest_posts_list = Post.objects.all()[:10]
    template = loader.get_template('list_posts/index.html')
    context = {
        'latest_posts_list': latest_posts_list,
    }
    return HttpResponse(template.render(context, request))


def vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    try:
        vote_type = request.POST['vote']
    except (KeyError, Post.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'list_posts/post.html', {
            'post': post,
            'error_message': "You didn't select a choice.",
        })
    else:
        if vote_type == 'upvote':
            post.up_votes += 1
        elif vote_type == 'downvote':
            post.down_votes += 1
        post.save()
        return HttpResponseRedirect(reverse('list_posts:post', args=(post_id,)))


def list_posts(request):
    return HttpResponse("Here are the posts listed by top rating")


def up_vote(request, post_id):
    return HttpResponse(
        "You just upvoted the post with the ID {}".format(post_id))


def down_vote(request, post_id):
    return HttpResponse(
        "You just downvoted the post with the ID {}".format(post_id))
