from django.views.generic import ListView

from .models import Estado


# Create your views here.
class EstadoListView(ListView):
    model = Estado
    context_object_name = 'estado_list'
