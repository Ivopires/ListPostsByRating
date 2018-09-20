# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.test import TestCase
from list_posts.models import Post
from django.utils import timezone
from django.urls import reverse


def create_post(post_text, days, up_votes=0, down_votes=0):
    """
    Create a post with the given 'post_text' and published with the given
    number of up_votes and down_votes, and published the given
    number of 'days' offset to now (negative for posts published in the past
    and positive for posts that have yet to be published).
    """
    date = timezone.now() + datetime.timedelta(days=days)
    post = Post.objects.create(
        pub_date=date,
        post_text=post_text,
        up_votes=up_votes,
        down_votes=down_votes)
    return post


class PostIndexViewTest(TestCase):

    def test_no_posts(self):
        """
        If no posts exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('list_posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No posts are available.')
        self.assertQuerysetEqual(response.context['latest_posts_list'], [])

    def test_past_post(self):
        """
        Posts with a pub_date in the past are displayed on the index page.
        """
        create_post(post_text='Past post.', days=-30)
        response = self.client.get(reverse('list_posts:index'))
        self.assertQuerysetEqual(response.context['latest_posts_list'],
                                 ['<Post: Past post.>'])

    def test_future_post(self):
        """
        Posts with a pub_date in the future aren't displayed on the index
        page.
        """
        create_post(post_text='Future post.', days=30)
        response = self.client.get(reverse('list_posts:index'))
        self.assertContains(response, 'No posts are available.')
        self.assertQuerysetEqual(response.context['latest_posts_list'], [])

    def test_future_post_and_past_post(self):
        """
        Even if both, past and future, posts exist, only past posts are
        displayed.
        """
        create_post(post_text='Past post.', days=-30)
        create_post(post_text='Future post.', days=30)
        response = self.client.get(reverse('list_posts:index'))
        self.assertQuerysetEqual(response.context['latest_posts_list'],
                                 ['<Post: Past post.>'])

    def test_two_past_posts(self):
        """
        The posts index page may display multiple questions.
        """
        create_post(post_text='Past post 2.', days=-5)
        create_post(post_text='Past post 1.', days=-30)
        response = self.client.get(reverse('list_posts:index'))
        self.assertQuerysetEqual(
            response.context['latest_posts_list'],
            ['<Post: Past post 2.>', '<Post: Past post 1.>'])


class PostDetailViewTest(TestCase):

    def test_future_post(self):
        """
        The detail view of a post with a pub_date in the future returns a
        404 not found
        """
        future_post = create_post(post_text='Future post.', days=5)
        url = reverse('list_posts:post', args=(future_post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_post(self):
        """
        The detail view of a post with a pub_date in the past displays the
        post's text.
        """
        past_post = create_post(post_text='Past post.', days=-5)
        url = reverse('list_posts:post', args=(past_post.id,))
        response = self.client.get(url)
        self.assertContains(response, past_post.post_text)
