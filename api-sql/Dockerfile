# Usa la imagen oficial de Python 3 como base
FROM python:3

ENV APP_DIRECTORY api-sql
# Establecer DEBIAN_FRONTEND en modo no interactivo
ENV DEBIAN_FRONTEND=noninteractive
# Aceptar automáticamente la EULA
ENV ACCEPT_EULA=Y

# Instala herramientas necesarias para el proceso de instalación
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
    curl \
    apt-utils \
    unixodbc \
    unixodbc-dev \ 
    gnupg2 &&\
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip
        

# Install odbc SQL SERVER
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN apt-get install -q -y odbcinst
RUN apt-get install -y msodbcsql18

# CREATE DIRECTORY TRANSBANK
RUN mkdir -p /opt/app/$APP_DIRECTORY

# CHANGE DIRECTORY
WORKDIR /opt/app/

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación al contenedor
COPY . .

# Exponer el puerto 5000 para Flask
EXPOSE 6000

# Comando para ejecutar la aplicación Flask con ngrok
CMD ["python", "app.py"]