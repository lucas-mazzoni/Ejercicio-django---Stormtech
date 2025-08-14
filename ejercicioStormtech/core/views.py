from django.shortcuts import get_object_or_404, render
from .serializer import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from django.db.models import Sum

class PaqueteListar(ListAPIView):   #endpoint para traer y filtrar paquetes (ejercicio 1)
#Metodo GET
    queryset = Paquete.objects.all()
    serializer_class = PaqueteSerializer

    def get_queryset(self):
        query = Paquete.objects.all()
        estado = self.request.query_params.get("estado")  #obtengo los campos del request
        cliente = self.request.query_params.get("cliente")
        tipo_paquete = self.request.query_params.get("tipo_paquete")

        if estado:
            query = query.filter(estado=estado)   #si los campos existe, quiere decir que se quiere filtrar
        if cliente:
            query = query.filter(cliente__nombre__icontains=cliente) #asi filtro por nombre de cliente
        if tipo_paquete:
            query = query.filter(tipo_paquete=tipo_paquete)

        return query
    
        
    

class PaqueteCrear(CreateAPIView):  #Create de Paquete (ejercicio 2)
#Metodo POST
    serializer_class = PaqueteSerializer


class AsignarPaquetes(APIView):  #uso APIView ya que la entrada es diferente a un create normal
#es un metodo POST que ira creando items para una planilla
    serializer_class = PlanillaAsignacionSerializer

    def post(self, request, *args, **kwargs):
        planilla = get_object_or_404(Planilla, numero=request.data.get("numero_planilla")) #obteno la planilla que se quiere actualizar

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        paquetes_a_asignar = serializer.validated_data['tracking'] #si la validacion esta bien, tomo los trackings

        peso_actual = Item.objects.filter(planilla=planilla).aggregate(total_peso=Sum("paquete__peso")) 
        peso_actual = peso_actual['total_peso'] or 0

        peso_nuevos = sum(p.peso for p in paquetes_a_asignar)

        if peso_actual + peso_nuevos > 25000:  #sigo manteniendo la regla del peso, ya que voy a usar  bulk_create
            return Response(
                {"La planilla no puede superar los 25 kg en total."},
                status=status.HTTP_400_BAD_REQUEST
            )

        ultima_posicion = planilla.items.order_by("-posicion").first()
        posicion = ultima_posicion.posicion if ultima_posicion else 0 #obtengo la ultima posicion en la que se agrego un item a esa planilla

        items_para_agregar = []

        for paquete in paquetes_a_asignar:
            items_para_agregar.append(Item(planilla=planilla,paquete=paquete,posicion=posicion+1)) #asocio cada paquete de la lista a la planilla, e incremento la posicion 
            posicion += 1 
                
        Item.objects.bulk_create(items_para_agregar)  #bulk_create para una unica consulta a la bdd

        return Response(
            {"Paquetes asignados correctamente a la planilla."},
            status=status.HTTP_200_OK)


class PlanillaResumenView(RetrieveAPIView): #ejercicio 4, se accede a traves del id gracias a la url
#metodo GET
    queryset = Planilla.objects.all()
    serializer_class = PlanillaSerializer



class PlanillaADistribucion(APIView):    #ejecricio 5
    def post(self, request, planilla_id):  #hago un POST ya que modifico masivamente varias tuplas
        paquetes_actualizar = Paquete.objects.filter(item__planilla_id=planilla_id,estado="en_deposito") #asi obtengo solo los paquetes que estan en deposito y no actualizo paquetes de mas
        cambios = paquetes_actualizar.update(estado="en_distribucion")
        return Response(
            { f"se actualizaron {cambios} paquetes paquetes"},
            status=status.HTTP_200_OK)
    

class ModificarMotivoFallo(APIView):   #ejercicio 6
    serializer_class = MotivoFallo
    
    def patch(self,request):  #uso un PATCH porque solo cambio un atributo de un solo item
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        datos_validados = serializer.validated_data
        try:    #uso el bloque try/except para ver si existe el item

            item_actualizar = Item.objects.get(id=datos_validados.get("id_item"),planilla__numero=datos_validados.get("numero"))
            item_actualizar.motivo_fallo=request.data.get("motivo_fallo")
            item_actualizar.save()     #ya que solo se modifica un campo de un solo objeto, uso un save
            return Response({"motivo de fallo actualizado correctamente"},status=status.HTTP_200_OK)
        
        except Item.DoesNotExist:
                return Response({"no se encontro el item seleccionado"},status=status.HTTP_400_BAD_REQUEST)
        



#---------------------------------aca voy a poner funciones frontend simples para dos ejercicios-------------------------

#Los metodos que defino aca abajo son para poder visualizar las consultas del ejercicio 1 y el ejercicio 4, ya que son los metodos
#GET  que hay en el enunciado. Opte por usar los templates que brinda django, creando una estructura html y css simple, las funciones
#para el front son iguales a la de sus endpoints, pero las defino nuevamente con el metodo render, para separar la estructura back/front



def front_listar_paquetes(request):

    query = Paquete.objects.all()

    estado = request.GET.get("estado")
    cliente = request.GET.get("cliente")
    tipo_paquete = request.GET.get("tipo_paquete")

    if estado:
        query = query.filter(estado=estado)   
    if cliente:
        query = query.filter(cliente__nombre__icontains=cliente)
    if tipo_paquete:
        query = query.filter(tipo_paquete=tipo_paquete)
    
    context = {
        "paquetes": query,
        "filtro_estado": estado,
        "filtro_cliente": cliente,
        "filtro_tipo_paquete": tipo_paquete,
    }

    return render(request, "lista_paquetes.html", context)


def front_resumen_planilla(request, pk):

    planilla = get_object_or_404(Planilla, pk=pk)

    paquetes_asociados = Paquete.objects.filter(item__planilla=planilla)
    context = {
        'planilla': planilla,
        'paquetes': paquetes_asociados
    }

    return render(request, 'resumen_planilla.html', context)   


def page_principal(request):

    context = {} 
    return render(request, 'principal.html', context)