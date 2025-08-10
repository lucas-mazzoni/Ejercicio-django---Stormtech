import uuid
from django.db import models

ESTADOS = (('en_deposito', 'En deposito'), ('en_distribucion', 'En distribucion'))

def verificar_peso(peso):   #asumo que los pesos se cargan en gramos y no en kilos
    peso = float(peso)
    if peso < 1000:
        return "P"
    elif peso < 3000:
        return "M"
    else: return "G" 


class Cliente(models.Model): 
    nombre = models.CharField(max_length=60)
    direccion = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nombre


class Paquete(models.Model):
    tracking = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #uso uuid para crear un tracking unico para cada paquete
    direccion = models.CharField(max_length=60)
    telefono = models.CharField(max_length=20)
    nombre = models.CharField(max_length=60)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    altura = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='en_deposito',)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_paquete = models.CharField(max_length=1)
    
    def save(self, *args, **kwargs):  #asi verifico que sin importar que se envie en un req, siempre se llamara a la logica de peso correspondiente
       self.tipo_paquete = verificar_peso(self.peso)
       super().save(*args, **kwargs)

    def __str__(self):
        return f"Paquete {self.tracking}"



class Planilla(models.Model):
    numero = models.IntegerField(primary_key=True, unique=True)
    fecha = models.DateField()

    def __str__(self):
        return f"Planilla {self.numero}"



class Item(models.Model):
    planilla = models.ForeignKey(Planilla, on_delete=models.CASCADE, related_name="items")
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    posicion = models.IntegerField()
    motivo_fallo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Paquete {self.paquete.tracking}"
