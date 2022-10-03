from django.urls import reverse_lazy
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Author, User
from .forms import PostForm
from .filters import PostFilter

from django.contrib.auth.mixins import PermissionRequiredMixin


class NewsList(ListView):
    model = Post    # Указываем модель, объекты которой мы будем выводить
    ordering = '-datetime'    # Поле, которое будет использоваться для сортировки объектов    #ordering = 'rating'
    # Указываем имя шаблона, в котором будут все инструкции о том, как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты. Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 2

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам. В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()        # К словарю добавим текущую дату в ключ 'time_now'.
        #context['next_sale'] = None        # Добавим ещё одну пустую переменную, чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['filterset'] = self.filterset
        return context


class PostSearch(DetailView):
    form_class = PostFilter
    model = Post
    template_name = 'search.html'
    # success_url = reverse_lazy('news')


class PostDetail(DetailView):
    model = Post    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    template_name = 'one_post.html'    # Используем другой шаблон
    context_object_name = 'one_post'    # Название объекта, в котором будет выбранная пользователем новость

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['comments'] = Comment.objects.filter(post=self.object.id)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        print("context['is_author'] = ", context['is_author'], self.request.user)
        return context


# def PostCreate(request):
#     form = PostForm()
#
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         print("form.is_valid - ", form.is_valid())
#         #print("form.text - ", form.title, form.value)
#         print("form.errors - ", form.errors)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#
#     return render(request, 'post_edit.html', {'form': form})


#     # def post(self, request, *args, **kwargs):
#     #     #id = request.id
#     #     #user = User.objects.get(id=request.user.id)
#     #     user = User.objects.get(id=request.user.id)
#     #     author = Author.objects.get(user=user)
#     #
#     #     if self.form.is_valid():
#     #         post = self.form.save(commit=False)
#     #         #post.author = author
#     #         #NEWS_TYPES = [('AR', 'статья'), ('NW', 'новость')]
#     #         url_str = self.form.get_absolute_url()
#     #         #news_type = self.form.
#     #         post.post_category = 'AR'
#     #         post.datetime = datetime.utcnow()
#     #         post.save()
#
#     return render(request, 'post_edit.html', {'form': form})

#class PostCreate(CreateView):
class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post', 'news.delete_post', 'news.change_post')

    def post(self, request, *args, **kwargs):
        #id = request.id
        #print("request.user.id = ", request.user.id)
        print("request - ", request)
        #     user = User.objects.get(id=request.user.id)
        user = User.objects.get(id=request.user.id)
        print("user = ", user, user.id)
        self.author = user   # Author.objects.get(user=user)
        self.author.id = 4
#         print("author = ", self.author, self.author.id)
#     #     #print("request.id = ", request.id)
#     #     # print("Author.objects.get(user=user) = ", Author.objects.get(user=user))
#         form = PostForm()
#         #print("form = ", form)
#         print("form.is_valid - ", form.is_valid())
#         print("form.text - ", form.title, form.value)
#         print("form.errors - ", form.errors)
#         #print("form.cleaned_data - ", form.cleaned_data)
#     #
#     #     if form.is_valid():
#     #         post = form.save(commit=False)
#     #         print("author = ", author)
#     #
#     #         post.author.user.set(author)
#     #         # print("post.author", post.author)  # = author
#     #         # NEWS_TYPES = [('AR', 'статья'), ('NW', 'новость')]
#     #         # url_str = form.get_absolute_url()
#     #         # news_type = self.form.
#     #         # post.post_category = 'AR'
#     #         post.datetime = datetime.utcnow()
#     #         post.save()
#     #
#     #     #print("PostCreate = ", PostCreate)
         return super(PostCreate, self).post(self, request, *args, **kwargs)
#     #    return
#     #
#     # def form_valid(self, form):
#     #     post = form.save(commit=False)
#     #     post.id = int(4)
#     #     #print("post", post)
#     #     post.postCategory.set('AR')
#     #     return super().form_valid(form)
#
    def get_success_url(self):
        return '/news/'


class PostEdit(PermissionRequiredMixin, UpdateView):    # Добавляем представление для изменения
#class PostEdit(UpdateView):  # Добавляем представление для изменения
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post')

    # def post(self, request, *args, **kwargs):
    #     user = User.objects.get(id=request.user.id)
    #     author = user   # Author.objects.get(user=user)
    #     form = PostForm()
    #     print("form = ", form)
    #     print("form.is_valid - ", form.is_valid())
    #
    #     #if form.is_valid():
    #     current_post = form.save(commit=False)
    #     print("current_post.post_category = ", current_post.postCategory)
    #     print("current_post.title = ", current_post.title)
    #     print("current_post.text = ", current_post.text)
    #     print("current_post = ", current_post)
    #     #print("author = ", author)
    #     #post.id=4
    #     #post.author.user.set(author)
    #     #post.postCategory.set('AR')
    #     current_post.datetime = datetime.utcnow()
    #     current_post.save()
    #
    #     return super(PostEdit, self).post(self, request, *args, **kwargs)

    def get_success_url(self):
        return '/news/'  #reverse('courses:video-detail', kwargs={'pk': self.object.pk})


class PostDelete(PermissionRequiredMixin, DeleteView):    # Добавляем представление для удаления
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')
    permission_required = ('news.delete_post')
