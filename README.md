# ec.covid.19
Tu experiencia COVID-19


1. Pasos para empezar a desarrollar:
```
git clone https://github.com/bram70/ec.covid.19.git
```

2. Luego instalar Docker y docker-compose en tu maquina:

3. en el directorio principal hacer build de las imagenes de docker:
```
docker-compose up -d --build
```

4. Verificar que las imagenes estan ejecutandose:
```
docker ps
```

5.- Verificar que el proyecto se esta ejecutando en el puerto indicado
```
http://localhost:8000/home/
```

PS. Comandos utiles para docker:
```
Para ver logs:
docker-compose logs <nombre_imagen>

Para acceder al bash de la imagen:
docker-compose exec <nombre_imagen> bash

Para parar las imagenes, dentro del directorio principal:
docker-compose stop
```

