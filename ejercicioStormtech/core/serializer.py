from rest_framework import serializers
from .models import *


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class PaqueteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paquete
        fields = '__all__'
        read_only_fields = ['tipo_paquete']  


    
class ItemSerializer(serializers.ModelSerializer):
    paquete = serializers.PrimaryKeyRelatedField(queryset=Paquete.objects.all())

    class Meta:
        model = Item
        fields = '__all__'

    def validate(self, data): 
        planilla = data['planilla']
        peso_total = sum(i.paquete.peso for i in planilla.items.all())  #obtengo la suma del peso de todos los paquetes de esa planilla
        if peso_total + data['paquete'].peso > 25000:  #si al agregarle el paquete actual el peso pasa los 25kg, entonces envio mensaje de error
            raise serializers.ValidationError(
                "La planilla no puede superar los 25 kg en total."
            )
        return data


class PlanillaSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)   #para poder mostrar todos los items de la planilla

    class Meta:
        model = Planilla
        fields = '__all__'