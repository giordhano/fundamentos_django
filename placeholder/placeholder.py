# django-admin.py startproject placeholder --template=template_reusable

import os
import sys

from django.conf import settings

DEBUG = os.environ.get('DEBUG','on')  == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY','2%&6s(o0*e$wd)@viy(!7fttu0tm&y3b7db4-wr3h!9nstxaw=')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')

settings.configure(

    DEBUG = DEBUG,

    SECRET_KEY = SECRET_KEY,

    ALLOWED_HOSTS = ALLOWED_HOSTS,

    ROOT_URLCONF = __name__,

    MIDDLEWARE_CLASSES = (

        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

    ),

)

from django import forms
from django.conf.urls import url
from django.http import HttpResponse,HttpResponseBadRequest

from io import BytesIO
from PIL import Image, ImageDraw


class ImageForm(forms.Form):
    """ Form para validar los datos recibidos """
    height = forms.IntegerField(min_value = 1, max_value = 2000)
    width = forms.IntegerField(min_value=1, max_value =2000)

    def generate(self, image_format = 'PNG'):

        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        image = Image.new('RGB',(width,height))
        draw = ImageDraw.Draw(image)

        text = '{} X {}'.format(width,height)

        textwidth,textheight = draw.textsize(text)

        if textwidth < width and textheight < height:
            texttop = (height - textheight) // 2
            textleft = (width - textwidth) // 2
            draw.text((textleft, texttop), text, fill = (255,255,255))

        content = BytesIO()
        image.save(content, image_format)
        content.seek(0)
        return content


def placeholder(request, width, height):

    form = ImageForm({'height' : height, 'width' : width })

    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('Algo no esta bien') # Envia error 404


def index(request):
    return HttpResponse('Hola estoy vivo')


urlpatterns = (

    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
    url(r'^$',index),

)


if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)