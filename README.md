![Portada](https://github.com/JesusJiga/VIAD/blob/main/Resources/portada.png)

## **Introducción**
VIAD (Vigilante inteligente atenuador de decesos) es el proyecto final de IA y Big Data. Realizado por Jose Pérez Soler y Jesús Jiménez García.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Enlaces

- [Presentación Genially](https://view.genial.ly/6408bf1d1221aa0018adfbb3/presentation-proyecto-final-master-salud)

- [VIAD - Streamlit](https://jesusjiga-viad-websrcapp-hn890g.streamlit.app/)

- [Video](https://github.com/JesusJiga/VIAD/blob/main/Resources/Video.mp4)

## **Justificación y descripción del proyecto.**

### **Justificación:**

  Se ha elegido este proyecto para ayudar a las administraciones sanitarias y a futuros residentes a saber la causa de la mortalidad que es más probable en una provincia.

  Así, un futuro residente podrá ver que es una provincia segura si las causas se deben a motivos naturales o bien se deben a patológias graves, para lo cual las autoridades sanitarias deberían tomar medidas para minimizar dicha probabilidad.

### **Descripción:**

  En el proyecto podrás encontrar:

   - Un modelo de predicción.
   - Un chatbot.
   - Una web donde poder visualizar datos.

## **Obtención de datos.**


Elaboración propia con datos extraídos del sitio web del [INE 23/02/203](https://www.ine.es/index.htm).

## **Almacenamiento.**

  Los datos se han almacenado en S3.
  
  ![S3](https://raw.githubusercontent.com/JesusJiga/VIAD/master/Resources/S3.png)
  
Datos de acceso
Al ser la cuenta de amazon perteneciente a awsacademy habrá que iniciar la sesión
del laboratorio previamiente a su uso y estas claves tendrán que modificarse.

## **Limpieza de datos.**

[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zsp8nuiLN9127ZI_bDfBBajlQ5441-Wd)

## **Exploración y visualización de los datos.**

![Visualización](https://github.com/JesusJiga/VIAD/blob/main/Web/src/images/pltDeathsSex2021.png)

## **Preparación de los datos para los algoritmos de Machine Learning.**

![Preparación](https://github.com/JesusJiga/VIAD/blob/main/Resources/Preparacion.png)

## **Entrenamiento del modelo y comprobación del rendimiento.**

![Entrenamiento](https://github.com/JesusJiga/VIAD/blob/main/Resources/Entrenamiento.png)

## **Aplicación web.**

![InicioWeb](https://github.com/JesusJiga/VIAD/blob/main/Resources/InicioWeb.png)

## **Procesamiento de Lenguaje Natural**

![Monath](https://github.com/JesusJiga/VIAD/blob/main/Resources/Monath.png)

## **Conclusiones.**

A pesar de no haber podido acceder a ciertas estadísticas de tipo mensual para realizar una predicción más concisa en el tiempo hemos llegado a una conclusión.
En el año 2020 con la llegad del Covid19 la mortalidad aumentó drásticamente, pero no
únicamente por el propio Covid19, otras causas también aumentaron, puede ser que fueran
fallecimientos ocasionados por el propio Covid19 o por debilitamiento de personas que quedaron con las defensas bajas tras el padecimiento de esta enfermedad.
Hemos aprendido también un nuevo algoritmo de entrenamiento llamado ARIMA, es un
modelo de series de tiempo muy para analizar y predecir datos de series, como en este caso. Este algoritmo ha sido la base de nuestro modelo, ya que de otra manera no hubiera sido posible.
Si hubiéramos tenido estadísticas mensuales podría haber sido muy útil para hospitales, ya que de esta manera el modelo hubiera podido predecir picos por tipos de fallecimientos y de esa manera preparar a los profesionales de la salud para hacer frente a estas circunstancias.
