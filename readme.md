# Supervisor

This project contains a script to monitor your network traffic.

## Autores

Carlos A. Cancino Escobar: [C4ncino](https://github.com/C4ncino)

Emilio Rivera Macías: [EmilioRivera0](https://github.com/EmilioRivera0)

Juan Pablo Gómez Haro Cabrera: [JuanPabloGHC](https://github.com/JuanPabloGHC)

Manuel Adolfo Darío Escobedo Cortés

## Introducción

La red es un componente crítico en cualquier entorno tecnológico, y su monitoreo y análisis son esenciales para garantizar un funcionamiento óptimo. En este informe, se utilizan herramientas avanzadas para llevar a cabo un análisis profundo de la red y obtener información valiosa sobre el tráfico, velocidad de transmisión  y consumo de ancho de banda.

## Herramientas

* Wireshark: 
    - Se utilizó Wireshark para la captura de paquetes en la red, permitiendo el análisis detallado del tráfico y la identificación de posibles anomalías.
* PyShark: 
    - Se implementó PyShark, una interfaz Python para Wireshark, para procesar y extraer datos específicos de los paquetes capturados de forma programática.
* Plotly: 
    - Se empleó Plotly, una biblioteca de visualización de datos en Python, para crear gráficos interactivos y dinámicos que representan el tráfico de red y otros parámetros relevantes.
* Dash:
    - Permite crear un tablero completo con múltiples componentes, interactividad y múltiples gráficos.
* Postgres:
    - Base de datos relacional para el almacenamiento y gestión de datos.
* Sqlalchemy:
    - ORM para la creación de las tablas en la base de datos y mayor facilidad para las consultas.

## Configuración de router

1. Conectar el moden a la corriente.
2. Verificar que el modem esté con los valores de fábrica, si no tiene los valores de fábrica; presionar el botón con un clip 📎 aguja 🪡 durante 10 segundos hasta que los foquitos del router parpaden.
3. Volteas el moden y tiene una etiqueta que viene el ssid de la red wifi y la contraseña,nos conectamos a la red wifi y mete la contraseña. 
4. En el celular no vamos a "configuración de la red wifi" y buscamos algo que diga puerta de enlace y copiamos la IP.
5. Abrimos el navegador y pegamos en la URL la IP y nos muestra una pantalla de tp-link.
6. El usuario y contraseña también vienen en la etiqueta de atrás del router. El usuario y contraseña es admin para ambos.
7. Una vez que estemos dentro nos muestra una pantalla de configuración rápida donde te dice "que quieres hacer con el router", ya que tiene varias funciones como por ejemplo: extensor de wifi o routeador. Vamos a  configurarlo como routeador, le damos siguiente y te pide nombre de red wifi, le escribimos el nombre de "internesito", después te pide la seguridad o usamos wapa2 Enterprise y le metemos la contraseña "nada123", le damos siguiente y salvamos los valores (El modem se va a reiniciar).

## Configuración de Raspberry Pi

1.	Preparación del hardware
    * Conectar la tarjeta microSD a tu computadora.
    * Descargar e instalar el software de Raspberry Pi Imager desde el sitio web oficial de Raspberry Pi (https://www.raspberrypi.org/software/).
    * Abrir Raspberry Pi Imager y seleccionar el sistema operativo que se desea instalar en el Raspberry Pi.
    * Seleccionar la tarjeta microSD y hacer click en “Write” para escribir la imagen del sistema operativo en la tarjeta microSD.
2.	Inicialización de la Raspberry Pi
    * Insertar la tarjeta microSD en la ranura correspondiente de la Raspberry Pi.
    * Conectar el teclado, el mouse y el monitor a la Raspberry Pi.
    * Conectar la Raspberry Pi a una fuente de alimentación utilizando un cable micro USB.
    * La Raspberry Pi se iniciará y se deberá ver la pantalla de inicio del sistema operativo que instalaste.
3.	Configuración inicial
    * La primera vez que se inicie la Raspberry Pi, se abrirá el asistente de configuración.
    * Sigue las instrucciones en pantalla para configurar la configuración regional, la contraseña de usuario, la conexión Wi-Fi y otras configuraciones básicas.
    * Una vez que se haya completado la configuración inicial, la Raspberry Pi se reiniciará automáticamente.
    * Ejemplo

```plain
-----------------------------------------------------------------------------------------
|Bienvenido al asistente de configuración de Raspberry Pi.				|
|											|
|Por favor, sigue los pasos a continuación para configurar tu Raspberry Pi.     	|
|											|
|1. Configuración regional:								|
|   - Selecciona tu país/región: [México]						|
|											|
|2. Configuración de red:								|
|   - Selecciona tu red Wi-Fi: [Nombre de la red] (internecito)		        	|
|   - Introduce la contraseña: [**********] (nose1234)					|
|											|
|3. Configuración de la contraseña del usuario:					        |
|   - Introduce una nueva contraseña para el usuario 'pi': [**********]			|
|   - Confirma la contraseña: [**********]						|	
|											|
|4. Actualización del software:						        	|
|   - Instalando actualizaciones del sistema... [Progreso]				|
|											|
|Configuración completada. La Raspberry Pi se reiniciará automáticamente.       	|
-----------------------------------------------------------------------------------------

```
4.	Actualización del sistema
    * Después de la configuración inicial, es recomendable actualizar el sistema operativo y los paquetes instalados para asegurarse de que estén al día. Se puede hacer ejecutando los siguientes comandos en la terminal

```plain
---------------------
|sudo apt update    |
|sudo apt upgrade   |
---------------------
```

## Base de datos

NODE

| Id        | Ip         | Consumption                     | Timestamp   | Active       | 
| --------- | ---------- | ------------------------------- | ----------- | ------------ |
| Integer() | String(15) | DECIMAL (precision=16, scale=8) | TIMESTAMP() | Boolean()    |

SPEED

| Id        | Speed                          | Timestamp   |
| --------- | ------------------------------ | ----------- |
| Integer() | DECIMAL(precision=10, scale=8) | TIMESTAMP() |

## Procedimiento

Se capturaron y analizaron datos de tráfico de red durante un período de tiempo específico.
Se extrajeron métricas clave, como el ancho de banda por nodo y total y la velocidad de transmisión de datos.
Se generaron gráficos interactivos utilizando Plotly y dash para visualizar los resultados de manera clara y comprensible.

## Arquitectura

```plain
├──📁/database          
│   ├──🐍__init__.py
|   ├──🐍base.py
|   ├──🐍database.py
|   ├──🐍node.py
|   └──🐍speed.py
│
├──🐍graphics.py
├──📝.env
├──📝output
├──🐍supervisor.py
└──📝requirements.txt
```

- /database: 
    - Componente de la base de datos.
    * /__init__.py:
        - Inicialiador de la base de datos.
    * /base.py:
        - La base declarativa para el ORM de SQLAchemy.
    * /database.py:
        - La clase de base de datos con los métodos correspondientes al CRUD.
    * /node.py:
        - Clase node para la creación de la tabla a través del ORM.
    * /speed.py:
        - Clase speed para la creación de la tabla a través del ORM.
- graphics.py:
    - Código que consume la base de datos para la generación de gráficas para las métricas previamente mencionadas.
- .env:
    - Se almacenan las variables de entorno, para almacenar la información necesaria para la base de datos.
- output:
    - Archivo que sirve para escribir el resultado del comando nmap, que busca todas las ips de la red.
- supervisor.py:
    - Código para consultar todos los nodos dentro de una red e ir almacenando en la base de datos la información acerca a la velocidad de transmisión, consumo de ancho de banda y fechas en los que estos se almacenan.
- requirements.txt:
    - Las dependencias que se utilizarón en el proyecto.

## Instalación

- Clonar el repositorio.
- Moverte a la carpeta del proyecto.
- Instalar todas las dependencias.

```bash
git clone https://github.com/C4ncino/supervisor.git

cd supervisor
```

En la instalación de dependencias recomendamos tener un entorno virtual en caso de que no desees uno puedes ir directo a la instalación de [dependencias](#dependencies), para crearlo ejecuta lo siguiente:

```bash
python -m venv venv
```

La activación del entorno virtual depende de su sistema operativo:

Linux:
```bash
source venv/bin/activate
```
Windows:
```bash
venv\Scripts\activate
```

Windows con bash:
```bash
source venv\Scripts\activate
```

<span id="dependencies" ></span>

Una vez activado el entorno virtual, se instalan las dependencias:

```bash
pip install -r requirements.txt
```

## IP Attributes

- `version` 
- `hdr_len` 
- `dsfield` 
- `dsfield_dscp` 
- `dsfield_ecn` 
- `len` 
- `id` 
- `flags` 
- `flags_rb` 
- `flags_df` 
- `flags_mf` 
- `frag_offset` 
- `ttl` 
- `proto` 
- `checksum` 
- `checksum_status` 
- `src` 
- `addr` 
- `src_host` 
- `host` 
- `dst` 
- `dst_host`