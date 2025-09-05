# Proyecto Backend

Este proyecto contiene el backend de una aplicación desarrollada con Django. A continuación, se detallan los pasos para ejecutar el contenedor Docker y poner en marcha el servidor.

## 🚀 Desplegar el contenedor

Para ejecutar el contenedor desde Docker Hub, utiliza el siguiente comando:

```
docker run -d --name backend_api -p 8000:8000 marianaruge/backend-proyecto
```

**-d: ** Ejecuta el contenedor en segundo plano (modo detached).

**--name backend_api**: Asigna el nombre backend_api al contenedor.

**-p 8000: 8000:** Mapea el puerto 8000 del contenedor al puerto 8000 de tu máquina local.

Una vez ejecutado, podrás acceder al servidor Django en http://localhost:8000
.