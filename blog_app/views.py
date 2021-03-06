from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import mixins as auth_mixins


from .forms import PostForm, EditPostForm, CommentForm
from .models import Post, Category, Comment


class CommentView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = Post.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post details',
                       kwargs={
                           'pk': self.object.post.pk,
                           'slug': self.object.post.slug,
                       })


class PostListView(generic.ListView):
    template_name = 'home.html'
    model = Post
    cats = Category.objects.all()

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super().get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu

        return context


class PostDetailView(generic.DetailView):
    template_name = 'post_details.html'
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = post.total_likes()
        liked = post.likes.filter(id=self.request.user.id).first()
        comments = post.comment_set.all().order_by('-id')

        context['cat_menu'] = Category.objects.all()
        context['total_likes'] = total_likes
        context['liked'] = liked
        context['form'] = CommentForm()
        context['comments'] = comments

        return context


class PostCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'post_create.html'
    model = Post
    form_class = PostForm

    # fields = ('title', 'content')

    def get_success_url(self):
        return reverse('post details',
                       kwargs={
                           'pk': self.object.pk,
                           'slug': self.object.slug,
                       })

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdateView(auth_mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'post_update.html'
    model = Post
    form_class = EditPostForm

    def get_success_url(self):
        return reverse('post details',
                       kwargs={
                           'pk': self.object.pk,
                           'slug': self.object.slug,
                       })


class PostDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    template_name = 'post_delete.html'
    model = Post
    success_url = reverse_lazy('home')


class CategoryCreateView(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'category_create.html'
    model = Category
    fields = '__all__'

    def get_success_url(self):
        return reverse('home')


def category_view(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    context = {
        'cats': cats.replace('-', ' '),
        'category_posts': category_posts
    }
    return render(request, 'categories.html', context)


def category_list_view(request):
    cat_list = Category.objects.all()

    context = {
        'cat_list': cat_list,
    }
    return render(request, 'category_list.html', context)


def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).first():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post details', kwargs={
        'pk': post.pk,
        'slug': post.slug,
    }))



