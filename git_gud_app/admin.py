from django.contrib import admin

from git_gud_app.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('submitter', 'date_submitted', 'score')
    search_fields = ('submitter__first_name', 'submitter__last_name', 'text')


admin.site.register(Post, PostAdmin)
