from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from shop.forms import ProductForm, VersionForm, BaseVersionFormSet
from shop.models import Product, Version


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 3

# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {"product": product}
#     return render(request, 'catalog/product_detail.html', context)

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


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_update.html'


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

    def get_success_url(self):
        # return reverse_lazy('shop:product_update', kwargs={'pk': self.object.pk})
        return reverse_lazy('shop:product_list')

class ProductDeleteView(DeleteView):
    model = Product  # Переопределяем DeleteView для удаления продукта
    fields = ['name', 'description', 'price', 'weight', 'category', 'image']
    template_name = 'shop/product_delete.html'
    success_url = reverse_lazy('shop:product_list')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name}, Телефон: {phone}, Сообщение: {message}')

    return render(request, 'main/contacts.html', {'contacts': contacts})

