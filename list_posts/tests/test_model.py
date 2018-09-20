# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from list_posts.models import Post
from django.utils import timezone
from django.urls import reverse


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

    def test_score_with_no_downvotes(self):
        """
        The score property of the Post model should be different to 0 when
        there is any downvote
        """
        post = Post(post_text='Post with no down.', up_votes=10, down_votes=0)
        score = post.compute_score()
        self.assertNotEqual(score, 0)

    def test_score_from_posts_with_same_ratio(self):
        """
        The score property of the Post model should be greater on a Post with
        1000/1000 up/down votes than on a Post with 100/100 up/down votes,
        despite of having the same ratio of up/down votes.
        """
        post_100 = Post(
            post_text='Post with 100/100 votes', up_votes=100, down_votes=100)
        score_100 = post_100.compute_score()

        post_1000 = Post(
            post_text='Post with 1000/1000 votes',
            up_votes=1000,
            down_votes=1000)
        score_1000 = post_1000.compute_score()

        self.assertGreater(score_1000, score_100)

    def test_score_from_posts_with_different_scores(self):
        """
        The score property of the Post model should be greater on a Post with
        1000/100 up/down votes than on a Post with 10/100 up/down votes.
        """
        post_1000 = Post(
            post_text='Post with 1000/100 votes', up_votes=1000, down_votes=100)
        score_1000 = post_1000.compute_score()

        post_10 = Post(
            post_text='Post with 10/100 votes', up_votes=10, down_votes=100)
        score_10 = post_10.compute_score()

        self.assertGreater(score_1000, score_10)

    def test_score_up_down_votes_when_post_is_created(self):
        """
        All the three properties (up/down votes and score) of the Post model
        should be equal to 0 on a Post that was recently created, and when there
        wasn't specified a different number of up/down votes than the default
        value (i.e., 0)
        """
        post_without_votes = Post(post_text='Post without votes.')

        self.assertEqual(post_without_votes.up_votes, 0)
        self.assertEqual(post_without_votes.down_votes, 0)
        self.assertEqual(post_without_votes.score, 0)
