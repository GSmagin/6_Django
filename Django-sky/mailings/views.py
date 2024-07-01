from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Client, Mailing, Attempt
from .forms import ClientForm, MailingForm
from django import forms


# Client views
class ClientListView(ListView):
    model = Client
    template_name = 'mailings/client_list.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailings/client_detail.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientCreateView(CreateView):
    model = Client
    fields = ('email', 'full_name', 'comment')
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('email', 'full_name', 'comment')
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailings/client_confirm_delete.html'
    success_url = reverse_lazy('mailings:client_list')


# Mailing views
class MailingListView(ListView):
    model = Mailing
#    form_class = MailingForm
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDetailView(DetailView):
    model = Mailing
#    form_class = MailingForm
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing_detail'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
#    fields = ('start_datetime', 'stop_datetime', 'periodicity', 'status')
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
#    form_class = MailingForm
    fields = ('start_datetime', 'stop_datetime', 'periodicity', 'status')
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
#    form_class = MailingForm
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')
