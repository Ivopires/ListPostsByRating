# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from list_posts.models import Post
from django.utils import timezone
from django.urls import reverse


def createPost(post_text, up_votes, down_votes):
    """
    Create a post with the given 'post_text' and published with the given
    number of up_votes and down_votes, which will aid in the assessment of the
    overall score.
    """
    now = timezone.now()
    post = Post.objects.create(
        pub_date=now,
        post_text=post_text,
        up_votes=up_votes,
        down_votes=down_votes)


class PostModelTests(TestCase):

    def test_score_with_no_upvotes(self):
        """
        The score property of the Post model should be equal to 0 when there
        is any upvote
        """
        post = Post(
            post_text='Post with no upvotes.', up_votes=0, down_votes=10)
        score = post.compute_score()
        self.assertEqual(score, 0)
