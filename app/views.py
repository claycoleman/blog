import requests
from unidecode import unidecode
from datetime import datetime

from django.shortcuts import render, render_to_response, redirect, resolve_url
from django.http import JsonResponse

from app.models import Post, Comment, AuthorProfile, Tag
from django.template import RequestContext
from app.forms import NewCommentForm, Search, UserLogin, CreatePostForm, EditPostForm, EditUserForm, EditProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from project.local import INSTAGRAM_CLIENT, INSTAGRAM_SECRET, URL


# Create your views here.


def home(request):
    context = {}
    context['URL'] = URL
    context['posts'] = Post.objects.all()[:9]
    context['recentposts'] = Post.objects.all()[:4]
    context['tags'] = Tag.objects.all()
    context['number_of_posts'] = len(Post.objects.all())
    context['married'] = (datetime.now() - datetime(1986, 10, 16, 0, 0, 0)).days / 7
    return render_to_response('home.html', context, context_instance=RequestContext(request))


def create_post(request):
    if (request.user.is_authenticated()):
        context = {}
        context['recentposts'] = Post.objects.all()[:4]
        context['tags'] = Tag.objects.all()
        
        author = AuthorProfile.objects.get(user=request.user)
        context['author'] = author
        if request.method == 'POST':
                form = CreatePostForm(request.POST, request.FILES)
                context['form'] = form
                if form.is_valid():
                    new_post = Post.objects.create(author=author)
                    new_post.title = form.cleaned_data['title']
                    new_post.description = form.cleaned_data['description']
                    new_post.body_text = form.cleaned_data['body_text']
                    new_post.date_posted = datetime.now()
                    new_post.post_pic = form.cleaned_data['post_pic']
                    print 'worked!'

                    author.save()
                    new_post.save()

                    return redirect('post_view', new_post.pk)
        else:
            form = CreatePostForm()
            context['form'] = form
            

        return render_to_response('create_post.html', context, context_instance=RequestContext(request))
    else:
        return render(request, 'not_logged_in.html')

def edit_post(request, post_pk):
    post = Post.objects.get(pk=post_pk) 
    if (request.user.is_authenticated() and post.author.user == request.user):
        context = {}
    
        context['recentposts'] = Post.objects.all()[:4]
        context['tags'] = Tag.objects.all()

        author = AuthorProfile.objects.get(user=request.user)
        context['author'] = author
        
        context['post'] = post
        if (author.user.is_authenticated()):
            if request.method == 'POST':
                form = EditPostForm(request.POST, request.FILES, instance=post)
                context['form'] = form
                if form.is_valid():
                    form.save()
                    return redirect('post_view', post.pk)
            else:
                form = EditPostForm(None, instance=post)
                context['form'] = form
        else:
            return render('not_logged_in.html')

        return render_to_response('edit_post.html', context, context_instance=RequestContext(request))
    else:
        return render(request, 'not_logged_in.html')

def delete_post(request, post_pk):
    context = {}

    context['recentposts'] = Post.objects.all()[:4]
    context['tags'] = Tag.objects.all()

    post = Post.objects.get(pk=post_pk)

    if (request.user.is_authenticated() and post.author.user == request.user):
        context['post'] = post
        context['request'] = request

        if (request.method == "POST"):
            post.delete()
            return redirect('post_list')
       
        return render_to_response('delete_post.html', context, context_instance=RequestContext(request))
    else:
        return render(request, 'not_logged_in.html')


def edit_author_info(request):
    if (request.user.is_authenticated()):
        context = {}
        context['request'] = request

    
        context['recentposts'] = Post.objects.all()[:4]
        context['tags'] = Tag.objects.all()
        user_form = EditUserForm(request.POST or None, instance=request.user)
        profile_form = EditProfileForm(request.POST or None, instance=request.user.authorprofile)
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        if user_form.is_valid() or profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('about_family_member', request.user.first_name)

        return render_to_response('edit_author_info.html', context, context_instance=RequestContext(request))

    else:
        return render(request, 'not_logged_in.html')



def author_post_list(request, pk):
    context = {}

    
    context['recentposts'] = Post.objects.all()[:4]
    context['tags'] = Tag.objects.all()
    author = AuthorProfile.objects.get(pk=pk)
    context['posts'] = author.post_set.all()
    context['author'] = author

    return render_to_response('author_post_list_no_base.html', context, context_instance=RequestContext(request))


def author_list(request):
    context = {}
    
    
    context['recentposts'] = Post.objects.all()[:4]
    context['tags'] = Tag.objects.all()
    if request.method == 'POST':
        form = Search(request.POST)
        context['form'] = form
        if form.is_valid():
            search = form.cleaned_data('search')
            context['authors'] = AuthorProfile.objects.filter(user__username__istartswith=search)
    else:
        form = Search()
        context['form'] = form
        context['authors'] = AuthorProfile.objects.all()

    return render_to_response('author_list.html', context, context_instance=RequestContext(request))


def about_family_member(request, slug):
    context = {}

    
    context['recentposts'] = Post.objects.all()[:4]
    context['tags'] = Tag.objects.all()
    family_member = AuthorProfile.objects.get(user__first_name__istartswith=slug)
    context['family_member'] = family_member

    return render_to_response('about_family_member.html', context, context_instance=RequestContext(request))


def login_user(request):
    context = {}
    context['recentposts'] = Post.objects.all()[:4]
    context['tags'] = Tag.objects.all()
    next_page = request.GET.get('next')
    form = UserLogin(request.POST or None)
    context['form'] = form
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    login(request, user)
                    print next_page is not None and next_page is not ""
                    print next_page is not ""
                    print next_page is not None
                    if next_page is not None and next_page != "":
                        return redirect(next_page)
                    else:
                        return redirect('home')
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                pass
                # the authentication system was unable to verify the username and password


    return render_to_response('login_user.html', context, context_instance=RequestContext(request))


def logout_user(request):
    logout(request)

    next = request.GET.get('next')
    if next is not None:
        return redirect(next)
    else:
        return redirect('home')



def post_view(request, pk):
    context = {}
    context['request'] = request
    context['recentposts'] = Post.objects.all()[:4]
    context['tags'] = Tag.objects.all()


    post = Post.objects.get(pk=pk)
    context['post'] = post
    if len(post.tag_set.all()) > 0:
        tag = (post.tag_set.all()[0])
        context['relatedposts'] = tag.post.exclude(pk=post.pk)[:3]
    context['num_comments'] = len(post.comment_set.all())
    posts = post.author.post_set.all()
    post_index = list(posts).index(post)
    if post_index is not 0:
        context['previous'] = (list(posts)[post_index-1]).pk
    if post_index is not (len(posts)-1):
        context['next'] = (list(posts)[post_index+1]).pk

    if (request.method == "POST"):
        print 'POST'
        form = NewCommentForm(request.POST)
        context['form'] = form
        if form.is_valid():
            comment = form.cleaned_data['comment'].strip(" ").strip('\n')
            author = form.cleaned_data['author'].strip(" ").strip('\n')
            email = form.cleaned_data['email'].strip(" ").strip('\n')
            if comment is not "":
                new_comment = Comment.objects.create(post=post)
                new_comment.comment_text = comment
                new_comment.post = post
                new_comment.commenter_name = author
                new_comment.email = email

                new_comment.date_posted = datetime.now()            
                post.save()
                new_comment.save()
                return redirect('post_view', pk=post.pk)
            else:
                pass
    else:
        print 'GET'
        form = NewCommentForm()
        context['form'] = form


    return render_to_response('post_view.html', context, context_instance=RequestContext(request))


def post_list(request, slug):
    context = {}
    author = AuthorProfile.objects.get(instagram=slug)
    context['author'] = author
    context['posts'] = author.post_set.all()
    context['recentposts'] = author.post_set.all()[:4]
    context['tags'] = Tag.objects.all()

    return render_to_response('post_list_masonry.html', context, context_instance=RequestContext(request))


def monthly_post_list(request, year, month):
    context = {}
    posts = Post.objects.filter(date_posted__year=year)
    # posts = posts.filter(date_posted__icontains='/%s/' % (month))
    context['posts'] = posts[:20]
    context['recentposts'] = Post.objects.all()[:4]
    context['tags'] = Tag.objects.all()

    return render_to_response('post_list_masonry.html', context, context_instance=RequestContext(request))


def family_post_list(request):
    context = {}
    context['author'] = None
    context['posts'] = Post.objects.all()[:20]
    context['recentposts'] = Post.objects.all()[:4]
    context['tags'] = Tag.objects.all()

    return render_to_response('post_list_masonry.html', context, context_instance=RequestContext(request))    


def tag_post_list(request, slug):
    context = {}
    tag = Tag.objects.get(name=slug)
    posts = tag.post.all()

    context['recentposts'] = Post.objects.all()[:4]
    context['tags'] = Tag.objects.all()
    context['tag'] = tag
    context['posts'] = posts

    return render_to_response('tag_post_list.html', context, context_instance=RequestContext(request))


def grab_access_token(request):
    code = request.GET.get('code')

    data = {'client_id': INSTAGRAM_CLIENT, 'client_secret': INSTAGRAM_SECRET, 'grant_type': 'authorization_code', 'redirect_uri': '%s/grab_access_token/' % URL, 'code': code }    

    response = requests.post('https://api.instagram.com/oauth/access_token', data=data)
    json = response.json()

    request.user.authorprofile.access_token = json.get('access_token')

    request.user.authorprofile.save()
    return redirect('loading_insta_pics')


def loading_insta_pics(request):
    return render(request, 'loading.html')


def grab_insta_pics(request):
    response = requests.get('https://api.instagram.com/v1/users/self/media/recent/?access_token=%s' % request.user.authorprofile.access_token)
    images = response.json().get('data')

    image_response = requests.get(images[0].get('user').get('profile_picture'))
    tempImage = NamedTemporaryFile(delete=True)
    tempImage.write(image_response.content)
    request.user.authorprofile.picture.save("%s.jpg" % request.user.authorprofile.instagram, File(tempImage))    
    for image in images:
        new_post, created = Post.objects.get_or_create(body_text=str(unidecode(image.get('caption').get('text'))))
        new_post.date_posted = datetime.fromtimestamp(float(image.get('created_time')))

        image_response = requests.get(image.get('images').get('standard_resolution').get('url'))
        tempImage = NamedTemporaryFile(delete=True)
        tempImage.write(image_response.content)
        new_post.post_pic.save("%s.jpg" % new_post.body_text[:10],File(tempImage))

        new_post.author = request.user.authorprofile
        new_post.likes = image.get('likes').get('count')
        new_post.save()

    return JsonResponse([resolve_url('post_list', slug=request.user.authorprofile.instagram),], safe=False)
