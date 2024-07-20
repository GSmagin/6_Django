from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, inlineformset_factory, ModelForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, Version


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['owner']
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get('name')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in forbidden_words:
            if word in name.lower():
                raise forms.ValidationError(f'Название содержит запрещенное слово: {word}')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        for word in forbidden_words:
            if word in description.lower():
                raise forms.ValidationError(f'Описание содержит запрещенное слово: {word}')
        return description


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['version_name', 'version_number', 'is_current']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.fields['is_current'].widget.attrs.update({'class': 'form-check-input'})

    def clean(self):
        cleaned_data = super().clean()
        version_name = cleaned_data.get('version_name')
        version_number = cleaned_data.get('version_number')
        product = self.instance.product
        if Version.objects.filter(product=product, version_number=version_number, version_name=version_name).exclude(
                pk=self.instance.pk).exists():
            raise ValidationError(
                f'Версия с названием "{version_name}" и номером "{version_number}" уже существует для данного продукта.')
        return cleaned_data


class BaseVersionFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        current_count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_current'):
                current_count += 1
        if current_count > 1:
            raise ValidationError('Вы можете выбрать только одну текущую версию продукта.')


class ProductModeratorForm(LoginRequiredMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published')
