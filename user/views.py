from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages 
from .models import Post, Profile, Like, Comment
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm, CommentEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def home (request):
    context = {
        'posts': Post.objects.all()
    }
    profile = Profile.objects.all()


    return render(request, 'home.html', context, {'profile': profile})



class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class ProfilePostListView(ListView):
    model = Post
    template_name = 'user/profile_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Assuming you have authentication
            
            comment.save()
            return redirect('post-detail', pk=pk)  # Redirect back to the post detail page
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'form': form})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'post_image', 'post_video']
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user.is_authenticated:
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            post.likes -= 1
        else:
            post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes})
    else:
        return render(request, 'user/login.html')

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def comment_edit(request, pk):  # Change 'comment_id' to 'pk'
    comment = get_object_or_404(Comment, id=pk)  # Use 'pk' instead of 'comment_id'
    if request.method == 'POST':
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=comment.post.pk)
    else:
        form = CommentEditForm(instance=comment)
    return render(request, 'comment_edit.html', {'form': form, 'comment': comment})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post-detail', kwargs={'pk': comment.post.pk})
    


def register (request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

def get_most_liked_posts(request):
    most_liked_posts = Post.objects.order_by('-likes')[:10]  # Adjust this as needed
    
    return render(request, 'popular.html', {'most_liked_posts': most_liked_posts})


@login_required
def profile (request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
  


    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('login') 