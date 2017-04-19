import urllib
from urlparse import urlparse
from django.core.files import File


def url_to_model_field(img_url, model_field):
    name = urlparse(img_url).path.split('/')[-1]
    content = urllib.urlretrieve(img_url)
    model_field.save(name, File(open(content[0])), save=True)