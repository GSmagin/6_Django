from django.shortcuts import render
import transliterate
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, TemplateView, CreateView

from blog.models import Blog
from blog.utils.mail_newsletter import congratulate_mail_newsletter


# Create your views here.


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        congratulate_mail_newsletter(obj)
        return obj


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blog'
    paginate_by = 10

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blogpost_form.html'
    fields = ["title", "content", "preview_image", "is_published"]
    success_url = reverse_lazy('blog:blogpost_list')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_post = form.save(commit=False)
    #         new_post.slug = slugify(new_post.title)
    #         new_post.save()
    #     return super().form_valid(form)

    def form_valid(self, form,):
        slug = transliterate.slugify(form.cleaned_data['title'])
        if self.model.objects.filter(slug=slug).exists():
            form.add_error('title', 'Пост с таким slug уже существует')
            return self.form_invalid(form=form)

        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog:blogpost_detail", args=[self.object.pk])


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ("title", "content", "preview_image", "is_published")
    template_name = 'blog/blogpost_form.html'
    context_object_name = 'blog'
    success_url = reverse_lazy('blog:blogpost_detail')

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog:blogpost_detail", args=[self.object.pk])


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:blogpost_list')



