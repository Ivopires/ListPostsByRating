# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Your posts will be posted here")


def list_posts(request):
    return HttpResponse("Here are the posts listed by top rating")


def up_vote(request, post_id):
    return HttpResponse(
        "You just upvoted the post with the ID {}".format(post_id))


def down_vote(request, post_id):
    return HttpResponse(
        "You just downvoted the post with the ID {}".format(post_id))
