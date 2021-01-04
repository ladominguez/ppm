# ppm - Proyecto de monitoreo de la calidad del aire. 
## Introducción
Este proyecto tiene como objetivo crear un protocolo para el monitorio de la calidad del aire que permite conocer a quien lo construye la cantidad de particulas suspendidas en el aire. En algunas ciudades como la Ciudad de México, se cuenta desde hace varios años con un sistema de monitoreo que permite informar a la población y a las autoridades de la calidad del aire de la ciudad. A este sistema se le conoce como **Indice Metropolitano de la Calidad del Aire (IMECA)**. En este proyecto vamos a generar un sistema de monitorio que permita medir la concentración de partículas suspendidas en el aire, las cuales se almacenarán en una base de datos y generará un reporte díario de la concentración de partículas. La siguiente gráfica muestra la clasificación de la calidad. <br>
![IMECAS](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Imeca.svg/1000px-Imeca.svg.png)
(Fuente: https://es.wikipedia.org/wiki/%C3%8Dndice_metropolitano_de_la_calidad_del_aire)
## Materiales
* Raspberry pi.
* Protoboard.
* 4 cables dupont.
* <a href="https://www.espruino.com/PMS7003">Sensor de partículas PMS7003</a>
## Paso 1 - Configuración de la Raspberry Pi.
El primer paso consiste en instalar el sistema operativo a la computadora **Raspberry Pi**. Existen múltiples formas de hacerlo, sin embargo la más simple consiste en utilizar el software <a href="https://www.raspberrypi.org/software/">Raspberry Pi Imager</a>. El programa es muy fácil de utilizar simplemente tienes que elegir el sistema operativo insertar tu tarjeta y seguir los pasos que se te indican. Existe un sistema operativo especialmente diseñado para el uso con la Raspberry Pi, que está señalado como la opción por defecto (*Raspberry Pi OS (32-bit)*). Lo siguientes pasos asumen que tienes instalado este sistema operativo.
<div style="text-align:center"><img src="./img/pi_imager.png"></div>
Una vez que hayas instalado el sistema operativo en la tarjeta SD, insertalo en tu **Raspberry Pi** y conectalo a la corriente, a tu monitor y tu teclado. La primera vez que lo utilices tendrás que configurar el sistema como se indica a través de los cuadros de dialogo. 
## Paso 2 - Habilita el puerto serial y la conexión SSH
Los puertos seriales y de conexión SSH están desabilitados por defectos, para poder desarrollar este proyecto deberás de habilitar de la siguiente forma. Primero abra la terminal y escribe el siguiente comando. 
```
sudo raspi-config
```
