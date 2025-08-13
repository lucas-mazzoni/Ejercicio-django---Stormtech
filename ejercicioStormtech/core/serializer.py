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


class PaqueteEstadoSerializer(serializers.ModelSerializer): #util para el ejercicio 4
    class Meta:
        model = Paquete
        fields = ['tracking', 'estado']


class ItemSerializer(serializers.ModelSerializer):
    paquete = serializers.PrimaryKeyRelatedField(queryset=Paquete.objects.all())

    class Meta:
        model = Item
        fields = '__all__'

    def validate(self, data): 
        planilla = data['planilla']
        peso_total = sum(i.paquete.peso for i in planilla.items.all())  #obtengo la suma del peso de todos los paquetes de esa planilla
        if peso_total + data['paquete'].peso > 25000:  #si al agregarle el paquete actual el peso pasa los 25kg, entonces envio mensaje de error
            raise serializers.ValidationError("La planilla no puede superar los 25 kg en total.")
        return data


class PlanillaSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)   #para poder mostrar todos los items de la planilla

    class Meta:
        model = Planilla
        fields = '__all__'



class PlanillaAsignacionSerializer(serializers.Serializer):  #serializer para ejercicio 3
    tracking = serializers.ListField(child=serializers.UUIDField())
    numero_planilla = serializers.IntegerField()

    def validate_tracking(self, uuids_paquetes):
        paquetes_validos = Paquete.objects.filter(tracking__in=uuids_paquetes,estado='en_deposito') #filtro los paquetes que estan en deposito

        if len(paquetes_validos) != len(uuids_paquetes): #si falla es porque uno o mas paquetes no existen o no estan en el estado "en deposito"
            raise serializers.ValidationError("Solo se permiten paquetes cuyo estado sea: en deposito")

        return paquetes_validos    
    

class MotivoFallo(serializers.Serializer):  #serializer ejercicio 6 (otra opcion es no usar request y enviar los id por la url)
    numero = serializers.IntegerField()
    id_item = serializers.IntegerField()
    motivo_fallo = serializers.CharField(required=False, allow_blank=True)