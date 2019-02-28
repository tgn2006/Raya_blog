from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post

# Create your views here.
def home_view(request):
    posts = Post.objects.all()
    return render(request, 'blogsapp/home.html', {'posts': posts})

class PostListView(ListView):
    model = Post
    template_name = 'blogsapp/home.html'
    context_object_name ='posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blogsapp/user_posts.html'
    context_object_name ='posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        #This is to get a user from the User model with the username passed  as a query parameter
        #(username = self.kwargs.get('username')
        return Post.objects.filter(author=user).order_by('-date_posted')




class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):   # if we dont override this method  as follows, we will have
    #integrity error because auther will be none
        form.instance.author = self.request.user #this is to get the current logged user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user #this is to get the current logged user
        return super().form_valid(form)

    def test_func(self): #to validate that only the user who created the post can edit the post.
        post = self.get_object() # to get the post object which will be editted
        if self.request.user == post.author: # to check if the current user is the author of the post
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self): #to validate that only the user who created the post can edit the post.
        post = self.get_object() # to get the post object which will be editted
        if self.request.user == post.author: # to check if the current user is the author of the post
            return True
        return False





def about_view(request):
    return render(request, 'blogsapp/about.html', {'title': 'about'})
