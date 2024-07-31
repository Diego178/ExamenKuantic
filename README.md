Comandos para ejecutar la aplicacion:
docker build -t app_movies .
docker run -d -p 8000:8000 --name movies_container app_movies

