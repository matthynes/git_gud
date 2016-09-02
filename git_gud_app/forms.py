from django.forms import ModelForm

from git_gud_app.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = 'text',
