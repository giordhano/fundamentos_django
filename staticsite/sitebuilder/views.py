import json
import os

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader_tags import BlockNode
from django.utils._os import safe_join


def get_page_or_404(name):

    try:
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY,name)
        print(file_path)
    except ValueError:
        raise Http404('Page Not Found')
    else:
        if not os.path.exists(file_path):
            raise Http404('Page not Found')


    with open(file_path, 'r') as f:
        page = Template(f.read())


    meta = None
 
    for i,node in enumerate(list(page.nodelist)): # crea una tupla (1,e1) , (2,e2) 
        if isinstance(node,BlockNode) and node.name =='context':
            meta = page.nodelist.pop(i)
            break

    print(type(page.nodelist))
    page._meta = meta # Add la propiedad _meta que es un Node 

    return page


def page(request, slug = 'index'):
    file_name = '{}.html'.format(slug)
    page = get_page_or_404(file_name)

    context = {
        'slug' : slug,
        'page' : page,
    }

    if page._meta is not None:
        meta = page._meta.render(Context())
        extra_content = json.loads(meta) # Parsea el texto JSON a un dicionario 
        context.update(extra_content) 

    return render(request, 'page.html', context )

