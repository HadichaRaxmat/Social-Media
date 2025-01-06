from django.contrib import admin
from .models import MyUser, Post, Comment, Like, Follow


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'id', 'user', 'post_count', 'follower_count', 'following_count', 'created_at')
    list_display_links = ('user_id', 'user')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'comment_count', 'like_count', 'created_at')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following')


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin)
