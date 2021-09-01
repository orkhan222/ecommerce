from time import time
from django.utils.text import slugify

def gen_slug(s):
    new_slug = slugify(s,allow_unicode=True)
    return new_slug + '-' + str(int(time()))