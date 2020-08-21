from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Productos(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=25)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='mariabonita') #, storage='https://s3.us-east-2.amazonaws.com/media/mariabonita/'
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=25)
    apellidos = models.CharField(max_length=50)
    sexo = models.CharField(max_length=10)
    telefono = models.CharField(max_length=12)
    email = models.EmailField()
    fechaNacimiento = models.DateField()




class CarritoCompras(models.Model):
    propietario = models.ForeignKey(User,on_delete=models.CASCADE)

class CestaCarrito(models.Model):
    fkCarritoCompras = models.ForeignKey(CarritoCompras,on_delete=models.CASCADE)
    fkProducto = models.ForeignKey(Productos,on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        try:
            tmpCesta = CestaCarrito.objects.get(fkCarritoCompras=self.fkCarrito, fkProducto=self.fkProducto)
            self.id = tmpCesta.pk
            self.cantidad += tmpCesta.cantidad
            return super(Cesta, self).save(*args, **kwargs)
        except:
            return super(Cesta, self).save(*args, **kwargs)
