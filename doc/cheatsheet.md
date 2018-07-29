#### Crear proyecto `mysite`

```bash
django-admin startproject mysite
```


#### Iniciar servidor

Normal
```bash
./manage.py runserver
```

En un puerto diferente
```bash
./manage.py runserver 8080
```

Determinar la visibilidad diferente
```bash
./manage.py runserver 0:8000
```
> `0`: es un sortcut de `0.0.0.0`


#### Crear aplicación `polls`

```bash
./manage.py startapp polls
```


#### Generar archivos de migraciones

```bash
./manage.py makemigrations polls
```


#### Visualizar sql a ejecutar del fichero `0001` de migración

```bash
./manage.py sqlmigrate polls 0001
```


#### Instalar migraciones pendientes

```bash
./manage.py migrate
```


#### Verificar que el proyecto no tiene problemas de ningún tipo (no modifica migraciones ni DDBB)

```bash
./manage.py check
```


# Ejecución de Tests

```bash
./manage.py test polls
```

 * Ejecutará los tests de la aplicación llamada *polls*
 * Ejecutará las subclases de la clase: django.test.TestCase
 * Crea una DDBB especial para la ejecución de los tests.
 * Busca métodos de pruebas; **aquellos cuyos nombres comienzan con test**.


#### Manejo de zonas horarias en django

```py
from django.utils import timezone
```

[reference](https://docs.djangoproject.com/es/2.0/topics/i18n/timezones/)



#### Crear portal de administrador

```bash
./manage.py createsuperuser
```


#### Registrar módulos en el admin site

Agregar estas líneas en `polls/admin.py`

```py
from django.contrib import admin
from .models import Question

admin.site.register(Question)
```


#### Buena práxis en POST

* Todos los formularios **POST** que están dirigidos a las URLs internas deben utilizar la etiqueta de plantilla `{% csrf_token %}`.

* La vista siempre debe devolver un objeto `HttpResponseRedirect`, el cual espera recibir un único parámetro, el nombre de la vista. Dejamos un ejemplo:

```python
# Imports
from django.http import HttpResponseRedirect
from django.urls import reverse

# Code
return HttpResponseRedirect(reverse(
        'polls:results',
        args=(question.id,)
    ))  # reverse return: '/polls/3/results/'
```


#### ¿Dónde está mí Django?

```bash
python -c "import django; print(django.__path__)"
# ['/home/$USER/Proyectos/django/.env/lib/python3.5/site-packages/django']
```


#### Empaquetando el app

1. Generar un directorio

  ```
  django-<name>
  ```

2. Meter el app dentro de `django-<name>`

3. Crear los ficheros

  ```
  django-<name>/README.rst
  django-<name>/LICENSE
  django-<name>/setup.py
  django-<name>/MANIFEST.in
  django-<name>/docs/
  ```
  > Revisar [documentación](https://docs.djangoproject.com/es/2.0/intro/reusable-apps/)para más detalle del contenido de cada fichero.

4. Ejecutar el comando

  ```bash
  python setup.py sdist
  ```
  > Se generará un fichero tar.gz

5. Instalar el empaquetado con pip

  ```bash
  pip install django-polls/dist/django-polls-0.1.tar.gz
  ```
  > Nota: Lo ideal sería hacer uso de entornos virtuales para la instalación de las dependencias requeridas por el proyecto.
