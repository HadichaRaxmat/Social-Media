from django.urls import path
from .views import (home_view, login_view, signup_view, logout_view, like_view,
                    comment_view, follow_view, post_upload_view, setting_view, profile_view, profile_image_view)

urlpatterns = [
    path('', home_view),
    path('login/', login_view),
    path('signup/', signup_view),
    path('logout/', logout_view),
    path('like/', like_view),
    path('comment/', comment_view),
    path('follow/', follow_view),
    path('post/upload/', post_upload_view),
    path('profile/', profile_view),
    path('setting/', setting_view),
    path('profile/image/', profile_image_view)
]
