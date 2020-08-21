from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import RedirectView,DetailView
from django.utils.translation import gettext as _
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError,send_mail
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from django.templatetags.static import  static
from django.urls import reverse
from . models import Productos, Categoria
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Resultados(RedirectView):
    def get(self, request, *args, **kwargs):
        if request.GET["buscar"]:   
            producto = request.GET["buscar"]
            resultados = Productos.objects.filter(nombre__icontains= producto)
            return render(request, "mariabonita/resultados.html", {"resultados": resultados, "query": producto})

    def post(self, request, *args, **kwargs):
        pass


class Index(RedirectView):
    def get(self, request, *args, **kwargs):
        return render(request, "mariabonita/index.html")
    
    def post(self, request, *args, **kwargs):
        pass


class Producto(RedirectView):
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


class Registro(RedirectView):

    formularioRegistro = forms.FormularioRegistro()

    def get(self, request, *args, **kwargs):
        return render(request, "mariabonita/registro.html", {'formularioRegistro': self.formularioRegistro})
    
    def post(self, request, *args, **kwargs):
        formularioRegistro = forms.FormularioRegistro(request.POST)
        if formularioRegistro.is_valid():
            tmpUsuario = User.objects.create_user(formularioRegistro.data['correoElectronico'],
                                                  formularioRegistro.data['correoElectronico'],
                                                  formularioRegistro.data['contrasena'])
            tmpUsuario.first_name = formularioRegistro.data['nombres']
            tmpUsuario.last_name = formularioRegistro.data['apellidos']
            tmpUsuario.is_active = False
            tmpUsuario.save()
            '''
            Aqui inicia el proceso de autentificacion del la cuenta
            '''
            #tmpUsuario = User.objects.get(username=formularioRegistro.data['correoElectronico'])
            sitio = get_current_site(request)
            correoAsunto = _('Activacion de Cuenta Maria Bonita')
            token = PasswordResetTokenGenerator()
            mensaje = render_to_string('mariabonita/activacion_cuenta.html',{
                'usuario':tmpUsuario,
                'dominio':sitio.domain,
                'uid':urlsafe_base64_encode(force_bytes(tmpUsuario.pk)),
                'token':token.make_token(tmpUsuario)
            })
            destinatario = tmpUsuario.email
            correo = EmailMessage(correoAsunto,mensaje,to=[destinatario])
            correo.content_subtype ='html'
            correo.send()
            paginaRedireccionamiento  = render_to_string("mariabonita/redireccionamiento.html",{'respuesta': 'Active su cuenta al enlace que hemos enviado','vistaURL': 'mariabonita:acceso'})
            return HttpResponse(paginaRedireccionamiento)
        else:
            return render(request, "mariabonita/registro.html", {'formularioRegistro': formularioRegistro})


class VistaActivacionCuenta(RedirectView):

    def get(self, request, *args, **kwargs):
        try:
            uid = force_bytes(urlsafe_base64_decode(kwargs['uidb64']))
            token = kwargs['token']
            user = User.objects.get(pk=uid)
        except (TypeError,ValueError,OverflowError,User.DoesNotExist):
            user = None
        resultado = ''
        if user is not None:
            if user.is_active:
                resultado = '¡¡Usuario Activo!!'
            else:
                tmpRevision = PasswordResetTokenGenerator()
                if tmpRevision.check_token(user=user,token=token):
                    user.is_active = True
                    user.save()
                    resultado = '¡¡Usuario Activado!!'
                else:
                    resultado = 'El enlace de activacion no es valido!'
        else:
            resultado = 'El enlace de activacion no es valido!'
        pagina = render_to_string('mariabonita/redireccionamiento.html', {'respuesta': resultado})
        return HttpResponse(pagina)


class VistaAcceso(RedirectView):
    formularioAcceso = forms.FormularioAcceso()

    def get(self, request, *args, **kwargs):
        return render(request, "mariabonita/acceso.html",{'formularioAcceso':
                                                     self.formularioAcceso})

    def post(self, request, *args, **kwargs):
        formularioAcceso = forms.FormularioAcceso(request.POST)
        if formularioAcceso.is_valid():
            user = authenticate(request,username=formularioAcceso.data['correoElectronico'],password=formularioAcceso.data['contrasena'])
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('mariabonita:index'))
        else:
            return render(request, "mariabonita/acceso.html", {'formularioAcceso':
                                                              formularioAcceso})

class VistaDesconectar(RedirectView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('mariabonita:index'))

    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('mariabonita:index'))


class VistaCarritoCompras(LoginRequiredMixin,RedirectView):
    url = 'Tienda:acceso'

    def get(self, request, *args, **kwargs):
        return render(request,'mariabonita/carritoCompras.html',{})