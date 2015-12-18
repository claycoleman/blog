from django import forms
from django.contrib.auth.models import User
from app.models import Comment, Post, AuthorProfile


class NewCommentForm(forms.Form):
    author = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'author', 'placeholder': 'Your name *', 'class': 'input-block-level form-control'}))
    comment = forms.CharField(required=True, widget=forms.Textarea(attrs={'id': 'comment', 'placeholder': 'Your message *', 'class': 'input-block-level form-control', 'rows': '3'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Your email *', 'class': 'input-block-level form-control'}))


class Search(forms.Form):
    search = forms.CharField(required=False, label='Search')

class UserLogin(forms.Form):
    """docstring for UserLogin"""
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'username *', 'class': 'input-block-level form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'username', 'placeholder': 'password *', 'class': 'input-block-level form-control'}), required=True)
    next_page = forms.CharField( required=False, widget=forms.HiddenInput())


class CreatePostForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'title', 'placeholder': 'Post Title *', 'class': 'input-block-level form-control'}))
    description = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'description', 'placeholder': 'Post Subtitle *', 'class': 'input-block-level form-control'}))
    body_text = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'body_text', 'placeholder': 'Body text *', 'class': 'input-block-level form-control'}))
    post_pic = forms.ImageField(required=False)


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'body_text', 'post_pic']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = AuthorProfile
        fields = ['short_description', 'bio']
    
