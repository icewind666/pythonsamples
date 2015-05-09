from django.shortcuts import render
from rentv_crm.models import Client
from django.views.generic import ListView, DetailView

# Create your views here.
class ClientsListView(ListView):
    model = Client

class ClientDetailView(DetailView):
    model = Client