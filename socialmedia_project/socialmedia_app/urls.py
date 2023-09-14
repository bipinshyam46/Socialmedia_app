from django.urls import path
from . import views

urlpatterns = [
    path('index',views.index),
    path('profile',views.profile),
    path('',views.signup),
    path('signin',views.signin),
    path('signout',views.signout),
    path('createpost',views.createpost),
    path('deletepost/<str:id>',views.deletepost),
    path('publish/<str:id>',views.publish),
    path('unpublish/<str:id>',views.unpublish),
    path('like',views.like),
    path('postlist',views.post_list)


]