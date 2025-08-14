# Sistema de Logística - Ejercicio Django

Este repositorio contiene la solución al ejercicio de desarrollo de un sistema de logística, construido con Django y Django REST Framework. El proyecto implementa una API REST para la gestión de paquetes, planillas y clientes, además de una interfaz de usuario simple para la interacción y prueba.

**Nota:** Para facilitar la revision, este repositorio incluye el archivo de base de datos SQLite (`db.sqlite3`) con datos de ejemplo ya cargados. Por esta razon no es necesario realizar una migracion

---
# Endpoints


  -   `GET /paquetes/listar/`: Listar y filtrar paquetes por estado, cliente y tipo.
  -   `POST /paquetes/crear/`: Crear un nuevo paquete. El tipo de paquete (`P`, `M`, `G`) se calcula automáticamente según el peso.
  -   `GET /planillas/<pk>/resumen/`: Obtener un resumen de una planilla específica.
  -   `POST /planillas/asignar-paquetes/`: Asignar múltiples paquetes a una planilla.
  -   `POST /planillas/<planilla_id>/pasar-a-distribucion/`: Cambiar el estado de los paquetes de una planilla.
  -   `PATCH /planillas/item/actualizar-fallo/`: Asignar un motivo de fallo a un ítem.

# Interfaz de Usuario (UI)

-   **Pagina Principal (`/`)**: Página de inicio con una botonera para acceder a las funcionalidades de la API explorable.
-   **Listado y Filtrado de Paquetes (`/front/paquetes/listar/`)**: Página HTML para visualizar y filtrar todos los paquetes.
-   **Resumen de planilla: (`front/planillas/<int:pk>/resumen/`)**: Pagina HTML para poder visualizar el resumen de una planilla.




# Configuración


## 1. Clonar el repositorio


## 2. Crear y activar el entorno virtual
  ### Crear el entorno virtual
    python -m venv env

  ### Activar el entorno virtual
   #### En Windows:
    .\env\Scripts\activate
   #### En macOS/Linux:
    source env/bin/activate


  
## 3. Instalar dependencias
     pip install -r requirements.txt



## 4. Ir a la carpeta del proyecto
     cd ejercicioStormtech


## 5. Ejecutar 
    python manage.py runserver


# Admin
Si se quiere acceder a la seccion de admin para poder crear/actualizar o borrar datos, se puede acceder a traves de la url http://localhost:8000/admin 

Usuario:lucas

Contraseña:123456



