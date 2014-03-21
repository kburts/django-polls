from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/$', views.About.as_view(), name='about'),
    url(r'^makepoll/$', views.MakePollView, name="makepoll"),
    url(r'^newpoll/$', views.MakePollView, name="makepoll"),
    url(r'^makechoices/(?P<poll_id>\d+)/$', views.MakeChoicesView, name="makepoll"),
    url(r'^user/(?P<user>\w+)/$', views.UserView, name="view_user"),

    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    #Authentication/Authorization
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
)
