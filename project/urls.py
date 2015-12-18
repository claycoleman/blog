"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings  
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^password/change/$', auth_views.password_change, name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, name='password_change_done'),
    url(r'^tinymce/', include('tinymce.urls')),
    # You can change your change password template. See here https://docs.djangoproject.com/en/1.8/topics/auth/default/#using-the-views
    url(r'^nimda/', include(admin.site.urls)),
    url(r'^post_view/(?P<pk>\d+)/$', 'app.views.post_view', name='post_view'),
    url(r'^post_list/([0-9]{4})/([0-9]{2})/$', 'app.views.monthly_post_list', name='monthly_post_list'),
    url(r'^post_list/(?P<slug>.+)/$', 'app.views.post_list', name='post_list'),
    url(r'^tag_posts/(?P<slug>.+)/$', 'app.views.tag_post_list', name='tag_post_list'),
    url(r'^post_list/$', 'app.views.family_post_list', name='family_post_list'),
    url(r'^author_post_list/(?P<pk>\d+)/$', 'app.views.author_post_list', name='author_post_list'),
    url(r'^about/(?P<slug>.+)/$', 'app.views.about_family_member', name='about_family_member'),
    url(r'^author_list/$', 'app.views.author_list', name='author_list'),
    url(r'^login/$', "app.views.login_user", name='login_user'),
    url(r'^logout/$', 'app.views.logout_user', name="logout_user"),
    url(r'^create_post/$', 'app.views.create_post', name='create_post'),
    url(r'^edit_post/(?P<post_pk>\d+)/$', 'app.views.edit_post', name='edit_post'),
    url(r'^delete_post/(?P<post_pk>\d+)/$', 'app.views.delete_post', name='delete_post'),
    url(r'^edit_author_info/$', "app.views.edit_author_info", name="edit_author_info"),
    url(r'^$', 'app.views.home', name='home'),
    url(r'^grab_access_token/$', 'app.views.grab_access_token', name='grab_access_token'),
    url(r'^grab_insta_pics/$', 'app.views.grab_insta_pics', name='grab_insta_pics'),
    url(r'^loading/$', 'app.views.loading_insta_pics', name='loading_insta_pics'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
