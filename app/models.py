from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Description: Model Description
    """
    title = models.CharField(max_length=150)
    # description can also be the Post hook 
    description = models.CharField(max_length=255, null=True, blank=True)
    date_posted = models.DateTimeField(null=True, blank=True)
    body_text = models.TextField(null=True, blank=True)
    author = models.ForeignKey('AuthorProfile', null=True, blank=True)
    post_pic = models.ImageField(upload_to='post_pic', null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)


    class Meta:
        ordering = ['-date_posted']

    def __unicode__(self):
        return self.title[:20]

    @property
    def has_pic(self):
        return self.post_pic.url != None


class Tag(models.Model):
    name = models.CharField(max_length=255)
    post = models.ManyToManyField('app.Post')

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    """
    Description: Model Description
    """
    commenter_name = models.CharField(max_length=255, null=True, blank=True)
    commenter_email = models.EmailField(null=True, blank=True)
    post = models.ForeignKey('Post')
    comment_text = models.TextField(null=True, blank=True)
    parent_comment = models.ForeignKey('Comment', null=True, blank=True)
    date_posted = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_posted']
# self.commenter_name + ": " +
    def __unicode__(self):
        return self.comment_text[:15]


class AuthorProfile(models.Model):
    """
    Description: Model Description
    """
    user = models.OneToOneField(User)
    instagram = models.CharField(null=True, blank=True, max_length=255)
    picture = models.ImageField(upload_to='user_pics', null=True, blank=True)
    short_description = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(null=True, blank=True)
    access_token = models.CharField(null=True, blank=True, max_length=255)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def name(self):
        return self.first_name + " " + self.last_name
    
    # profile_picture = models.ImageField(null=True, blank=True)
    def __unicode__(self):
        return self.user.username

