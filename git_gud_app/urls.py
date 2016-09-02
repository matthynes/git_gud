from django.conf.urls import url
import git_gud_app.views as views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/$', views.create_post, name='create_post'),
    url(r'^vote/(?P<post_id>\d+)/(?P<weight>\w+)/$', views.vote, name='vote'),
    url(r'^delete_post/(?P<post_id>\d+)/$', views.delete_post, name='delete_post'),
]
