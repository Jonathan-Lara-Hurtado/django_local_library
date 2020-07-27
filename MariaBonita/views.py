from django.shortcuts import render, HttpResponse
from django.views.generic import RedirectView,DetailView
from . models import Productos, Categoria

# Create your views here.
class Index(RedirectView):
    def get(self, request, *args, **kwargs):
        return render(request, "mariabonita/index.html")

    def post(self, request, *args, **kwargs):
        pass

class Productos(RedirectView):
    productos = Productos.objects.all()
    
    def get(self, request, *args, **kwargs):
        return render(request, "mariabonita/productos.html", {"productos": self.productos})

    def post(self, request, *args, **kwargs):
        pass

class Categorias(RedirectView):
    categorias = Categoria.objects.all()    
    
    def get(self, request, *args, **kwargs):
        return render(request, "mariabonita/categorias.html", {"categorias": self.categorias})

    def post(self, request, *args, **kwargs):
        pass
