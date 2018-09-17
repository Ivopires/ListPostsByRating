from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^posts/', views.list_posts, name='list_posts'),
    url(r'^upvote/(?P<post_id>[0-9]+)/$', views.up_vote, name='list_posts'),
    url(r'^downvote/(?P<post_id>[0-9]+)/$', views.down_vote, name='list_posts'),
]
