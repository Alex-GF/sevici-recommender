# BICICATOR

## Introducción

Bicicator es un proyecto que busca recopilar datos en tiempo real sobre las estaciones de SEVICI con el objetivo de ofrecer al usuario final un sistema de recomendaciones que prediga la mejor estación en relación distancia/bicis para el usuario.

También ofrece servicios para filtrar las estaciones de la compañía en función de su estado en un momento determinado, tanto de manera general como en un radio de distancia desde una dirección.

### Índice

1. [Demo](#demo)
2. [Máquina](#local)
3. [Contenedor Docker](#docker)

## Demo<a name="demo"></a>

Existe una demo de la aplicación disponible en la siguiente dirección: [https://bicicator.javiercavlop.com/](https://bicicator.javiercavlop.com/)

## Máquina<a name="local"></a>

### Requisitos

- NodeJS: 20.0.0
- npm: 9.6.4
- PostgreSQL: 14.7
- Python: 3.8.13
- pip: 23.1.2
- PostGIS: 3.1.4

### Enlaces de interés

- [NodeJS](https://nodejs.org/es/)
- [npm](https://www.npmjs.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Python](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)
- [GeoDjango y PostGIS](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/tutorial/#setting-up)
- [JCDecaux](https://developer.jcdecaux.com)

### Pasos previos

1. Clonar el repositorio

```
git clone https://github.com/Alex-GF/sevici-recommender.git
```

### Backend

1. Crear una base de datos en PostgreSQL y un usuario con todos los permisos sobre ella. (De ahora en adelante, nos referiremos a esta BD con el nombre: `sevici_db`):

- Accedemos a la consola de PostgreSQL:

```
psql postgres
```

- Creamos la base de datos y el usuario:

```
CREATE DATABASE sevici_db;
CREATE USER sevici_user WITH ENCRYPTED PASSWORD 'sevici_password';
GRANT ALL PRIVILEGES ON DATABASE sevici_db TO sevici_user;
```

- Salimos de la consola de PostgreSQL:

```
\q
```

2. Accedemos a la base de datos recien creada, y habilitamos la extensión PostGIS:

```
psql sevici_db
```
```
CREATE EXTENSION PostGIS;
```
```
\q
```

3. Accedemos a la carpeta `backend` del proyecto y creamos un archivo `.env` siguiendo el ejemplo del archivo `.env.example`.

NOTA IMPORTANTE: es necesario contar con una API key de desarrollador en [JCDecaux](https://developer.jcdecaux.com). Sigue los pasos para create una cuenta y activarla. Esta API key deberá colocarla como valor de la variable `API_KEY` en el archivo `.env` del paso 3.

4. Instalamos todos los requisitos (recomendamos hacerlo dentro de un entorno virtual):

```
pip install -r requirements.txt
```

5. Creamos y ejecutamos todas las migraciones de los modelos de django a la base de datos:

```
python manage.py makemigrations
python manage.py migrate
```

6. Lanzamos el backend de la aplicación en el puerto 8000:

```
python manage.py runserver --noreload
```

### Frontend

Una vez lanzado el backend, dejamos corriendo la tarea y, desde otra terminal, accedemos a la carpeta `frontend` del proyecto. A continuación:

1. Instalamos el gestor de paquetes `yarn` de manera global en nuestro equipo:

```
npm i -g yarn
```

2. Instalamos todos los paquetes necesarios para el frontend:

```
yarn install
```

3. Lanzamos el frontend de la aplicación en el puerto 3000:

```
yarn start
```

### Anotaciones finales

Una vez lanzados los dos servidores, podemos acceder a la aplicación desde el navegador en la dirección `http://localhost:3000/`. Cabe destacar que no se podrán ver datos de las estaciones ni usar las funcionalidades hasta 10 minutos después del lanzamiento del backend, ya que es el tiempo que tarda en lanzarse la primera tarea periódica de recopiación de datos.

## Contenedor Docker<a name="docker"></a>

### Requisitos

- Docker: 20.10.20
- Docker-compose: 2.12.1

### Pasos

1. Clonar el repositorio

```
git clone https://github.com/Alex-GF/sevici-recommender.git
```

2. Accedemos a la carpeta `sevici-recommender/docker`: 

```
cd sevici-recommender/docker
```

3. Creamos un archivo `.env` siguiendo el ejemplo del archivo `.env.example`.

NOTA IMPORTANTE: es necesario contar con una API key de desarrollador en [JCDecaux](https://developer.jcdecaux.com). Sigue los pasos para create una cuenta y activarla. Esta API key deberá colocarla como valor de la variable `API_KEY` en el archivo `.env` del paso 3.
NOTA IMPORTANTE 2: debe tener en cuenta que las variables del archivo `.env.example` cuyos valores se encuentran separados por una barra `/` deben ser sustituidos por un único valor, por ejemplo: `DJANGO_ENV="/production"` en lugar de `DJANGO_ENV="development/production"`.

4. Construimos la arquitectura de contenedores con Docker:

```
docker-compose up
```

NOTA: si se desea lanzar los contenedores en segundo plano, especificar el flag `-d` al final del comando anterior.

### Anotaciones finales

Una vez lanzados los dos servidores, podemos acceder a la aplicación desde el navegador en la dirección `http://localhost/`. Cabe destacar que no se podrán ver datos de las estaciones ni usar las funcionalidades hasta 10 minutos después del lanzamiento del backend, ya que es el tiempo que tarda en lanzarse la primera tarea periódica de recopiación de datos.