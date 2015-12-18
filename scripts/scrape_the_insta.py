#! /usr/bin/env python 
import lxml, requests, re, os, sys, json
from datetime import datetime
from bs4 import BeautifulSoup
from pprint import pprint
from unidecode import unidecode
from tzlocal import get_localzone 
import pytz
from requests.auth import HTTPBasicAuth


sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "project.settings")

from app.models import Post, AuthorProfile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from project.local import INSTAGRAM_CLIENT, INSTAGRAM_SECRET

import django
django.setup()   

# response = requests.get('https://api.instagram.com/v1/users/self/media/recent/?access_token=%s' % AUTH)
# print response.text

for author in AuthorProfile.objects.all():
    if author.instagram:
        if not author.access_token:
            continue

        print author.instagram


        response = requests.get('https://api.instagram.com/v1/users/self/media/recent/?access_token=%s' % author.access_token)
        images = response.json().get('data')

        image_response = requests.get(images[0].get('user').get('profile_picture'))
        tempImage = NamedTemporaryFile(delete=True)
        tempImage.write(image_response.content)
        author.picture.save("%s.jpg" % author.instagram, File(tempImage))    
        for image in images:
            new_post, created = Post.objects.get_or_create(body_text=str(unidecode(image.get('caption').get('text'))))
            new_post.date_posted = datetime.fromtimestamp(float(image.get('created_time')))

            image_response = requests.get(image.get('images').get('standard_resolution').get('url'))
            tempImage = NamedTemporaryFile(delete=True)
            tempImage.write(image_response.content)
            new_post.post_pic.save("%s.jpg" % new_post.body_text[:10],File(tempImage))

            new_post.author = author
            new_post.likes = image.get('likes').get('count')
            new_post.save()


        # soup = BeautifulSoup(response.text, "lxml")
        # script_tag = soup.find('script', text=re.compile('window\._sharedData'))
        # shared_data = script_tag.string.partition('=')[-1].strip(' ;')
        # result = json.loads(shared_data)

        # pprint(result)
        # posts = result.get("entry_data").get("ProfilePage")[0].get('user').get('media').get('nodes')


        # for post in posts:
        #     if post.get('is_video'):
        #         print "Cannot"
        #     else:
        #         new_post, created = Post.objects.get_or_create(body_text=str(unidecode(post.get('caption'))))
        #         new_post.date_posted = datetime.datetime.fromtimestamp(post.get('date'))

        #         image_response = requests.get(post.get('display_src'))
        #         tempImage = NamedTemporaryFile(delete=True)
        #         tempImage.write(image_response.content)
        #         new_post.post_pic.save("%s.jpg" % new_post.body_text[:10],File(tempImage))
        #         new_post.author = author
        #         new_post.likes = post.get('likes').get('count')
        #         new_post.save()
        #         print "yep"

        # for count, post in enumerate(author.post_set.order_by('-date_posted')):
        #     print post.date_posted, count
    