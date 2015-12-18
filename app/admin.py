from django.contrib import admin
from app.models import Post, Comment, AuthorProfile, Tag
from django.contrib.auth.models import User


class PostAdmin(admin.ModelAdmin):
    '''
        Admin View for Post
    '''
    list_display = ('title', 'date_posted', 'author', 'pk')
    search_fields = ['title', 'author']
    

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


class CommentAdmin(admin.ModelAdmin):
    '''
        Admin View for Comment
    '''
    list_display = ('post', 'date_posted', 'commenter_name')
    search_fields = ['post', 'commenter_name']


class AuthorProfileAdmin(admin.ModelAdmin):
    '''
        Admin View for AuthorProfile
    '''
    list_display = ('user', 'date_joined')
    search_fields = ['title']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(AuthorProfile, AuthorProfileAdmin)
admin.site.register(Tag, TagAdmin)