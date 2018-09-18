from django.conf.urls import url
from . import views

app_name = 'list_posts'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='post'),
    url(r'^vote/(?P<post_id>[0-9]+)/$', views.vote, name='vote'),
    url(r'^upvote/(?P<post_id>[0-9]+)/$', views.up_vote, name='up_vote'),
    url(r'^downvote/(?P<post_id>[0-9]+)/$', views.down_vote, name='down_vote'),
    url(r'^posts/', views.list_posts, name='list_posts'),
]
