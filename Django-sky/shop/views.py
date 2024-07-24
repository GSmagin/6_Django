from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory, BaseInlineFormSet, ModelForm
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from shop.forms import ProductForm, VersionForm, BaseVersionFormSet, ProductModeratorForm
from shop.models import Product, Version


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        if self.request.user.groups.filter(name='Moderator_Product').exists() or self.request.user.groups.filter(
                name='Admin').exists() or self.request.user.groups.filter(name='User_Product').exists():
            return Product.objects.all()
        return Product.objects.filter(is_published='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_with_versions = []

        for product in context['products']:
            current_version = product.versions.filter(is_current=True).first()
            products_with_versions.append((product, current_version))

        context['products_with_versions'] = products_with_versions
        return context


class ProductDetailView(DetailView):  # Переопределяем DetailView
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        current_version = product.versions.filter(is_current=True).first()
        context['current_version'] = current_version
        return context


# def product_create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('product_list')
#     else:
#         form = ProductForm()
#     return render(request, 'catalog/product_form.html', {'form': form})
#


class ProductCreateView(CreateView):  # Переопределяем CreateView для создания продукта
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_create.html'
    #    fields = ['name', 'description', 'price', 'weight', 'category', 'image']
    success_url = reverse_lazy('shop:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем текущего пользователя как владельца
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_update.html'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        # print(product.owner)
        # print(self.request.user)
        user = self.request.user

        has_permission = (
                user.groups.filter(name='Admin').exists() or
                user.groups.filter(name='Moderator_Product').exists() or
                product.owner == user
        )

        if not has_permission:
            # raise PermissionDenied("Вы не можете изменять этот продукт.")
            messages.success(self.request, 'Вы не может изменять не свои продукты,'
                                           'так как вы не являетесь его владельцем.')
            return redirect('main:not_found')
        return super().dispatch(request, *args, **kwargs)

        # if product.owner != self.request.user:
        #     # raise PermissionDenied("Вы не может изменять не свои продукты.")
        #     messages.success(self.request, 'Вы не может изменять не свои продукты,'
        #                                    'так как вы не являетесь его владельцем.')
        #     if self.request.user.groups.filter(name='Admin').exists():
        #         return super().dispatch(request, *args, **kwargs)
        #
        #     return redirect('main:not_found')
        #
        # return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Инициализируем формсет для версий продукта.
        #  Выбирает без сообщения последнюю отмеченную версию.
        # VersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        #  Не даст выбрать две версии продукта выводит сообщение.
        VersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1, formset=BaseVersionFormSet)

        if self.request.method in ['POST', 'PUT']:
            # Если есть POST-запрос, передаем данные формы и формсета
            context['formset'] = VersionFormSet(self.request.POST, instance=self.object)
        else:
            # Если GET-запрос, создаем формсет для текущего экземпляра продукта
            context['formset'] = VersionFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.is_current:
                    Version.objects.filter(product=self.object, is_current=True).exclude(pk=instance.pk).update(
                        is_current=False)
                instance.product = self.object
                instance.save()
            formset.save_m2m()

            # Удаление форм, помеченных для удаления
            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    # def get_object(self, queryset=None):
    #     return self.request.user

    def get_success_url(self):
        # return reverse_lazy('shop:product_update', kwargs={'pk': self.object.pk})
        return reverse_lazy('shop:product_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.groups.filter(name='Admin').exists():
            return ProductForm
        elif (user.has_perm('shop.can_edit_product_publication') and
              user.has_perm('shop.can_edit_product_description') and
              user.has_perm('shop.can_edit_product_category')):
            return ProductModeratorForm
        else:
            return PermissionDenied
            # return redirect('main:not_found')


class ProductDeleteView(DeleteView):
    model = Product  # Переопределяем DeleteView для удаления продукта
    fields = ['name', 'description', 'price', 'weight', 'category', 'image']
    template_name = 'shop/product_delete.html'
    success_url = reverse_lazy('shop:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        if product.owner != self.request.user:
            # raise PermissionDenied("Вы не может удалять не свои продукты")
            messages.success(self.request, 'Вы не может удалять не свои продукты, '
                                           'так как вы не являетесь его владельцем.')
            return redirect('main:not_found')

        return super().dispatch(request, *args, **kwargs)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name}, Телефон: {phone}, Сообщение: {message}')

    return render(request, 'main/contacts.html', {'contacts': contacts})
