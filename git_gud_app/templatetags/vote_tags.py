from django import template
from django.contrib.auth.models import AnonymousUser

register = template.Library()


# template tag in django-vote library wouldn't load for some reason I had to make my own
@register.simple_tag
def vote_exists(model, user=AnonymousUser()):
    if user.is_anonymous():
        return False
    return model.votes.exists(user)
