from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django import forms
from django.contrib.gis import forms as gis_forms
from django.forms.models import modelform_factory
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Item
from .forms import ItemForm


def index(request):
    latest_advert_list = Item.objects.order_by('-modified')[:5]
    context = {
        'latest_advert_list': latest_advert_list,
    }
    return render(request, 'items/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Item, pk=advert_id)
    return render(request, 'items/detail.html', {'advert': advert})


class ItemList(ListView):
    queryset = Item.objects.filter(point__isnull=False)


class ItemCreate(CreateView):
    model = Item
    form_class = ItemForm
    login_required = True
    success_url = reverse_lazy('items:index')

    # def get_form(self, form_class):
    #     form = super(ItemCreate, self).get_form(form_class)
    #     form.fields['password'].widget = forms.PasswordInput()
    #     return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ItemUpdate(UpdateView):
    model = Item
    fields = '__all__'
    success_url = reverse_lazy('items:index')


class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('items:index')
