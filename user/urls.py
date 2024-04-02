from django.urls import path
from .views import (
    PostListView,
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    ProfilePostListView,
    CommentDeleteView,
)
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('profile-posts/<str:username>', ProfilePostListView.as_view(), name='profile-posts'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_id>/like/', views.like_post, name='like-post'),
    path('post/<int:pk>/comment/', views.post_detail, name='add-comment'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment-edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    path('about/', views.about, name='about'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
