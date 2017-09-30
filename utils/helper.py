import urllib
from urlparse import urlparse

from random import choice
from string import ascii_lowercase

from django.core.files import File


def url_to_model_field(img_url, model_field):
    name = urlparse(img_url).path.split('/')[-1]
    if name == 'sddefault.jpg':
        extension = name.split('.')[-1]
        random = ''.join(choice(ascii_lowercase) for i in range(6))
        name = '{}.{}'.format(random, extension)
    content = urllib.urlretrieve(img_url)
    model_field.save(name, File(open(content[0])), save=True)
