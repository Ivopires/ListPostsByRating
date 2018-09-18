# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.shortcuts import get_object_or_404, render
from list_posts.models import Post


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'list_posts/post.html'


def index(request):
    latest_posts_list = Post.objects.order_by('-pub_date')
    context = {'latest_posts_list': latest_posts_list}
    return render(request, 'list_posts/index.html', context=context)


def vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    try:
        vote_type = request.POST['vote']
    except (KeyError, Post.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'list_posts/post.html', {
            'post': post,
            'error_message': "You didn't voted.",
        })
    else:
        if vote_type == 'upvote':
            post.up_votes += 1
        elif vote_type == 'downvote':
            post.down_votes += 1
        post.score = post.compute_score()
        post.save()
        return HttpResponseRedirect(reverse('list_posts:post', args=(post_id,)))


def list_posts(request):
    ordered_posts_list = Post.objects.order_by('-score')
    context = {'latest_posts_list': ordered_posts_list}
    return render(request, 'list_posts/index.html', context=context)


def up_vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.up_votes += 1
    post.score = post.compute_score()
    post.save()

    return render(request, 'list_posts/results.html', {'post': post})


def down_vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.down_votes += 1
    post.score = post.compute_score()
    post.save()

    return render(request, 'list_posts/results.html', {'post': post})
