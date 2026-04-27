# Evidencia.1.-Proyecto-Integrador-Sistemas-basados-en-conocimiento

# Descripción del Proyecto

Este proyecto implementa un sistema basado en Agentes Basados en Conocimiento para la asignación de espacios universitarios.

El sistema utiliza un motor de inferencia de encadenamiento hacia adelante (Forward Chaining), el cual, a partir de una base de hechos y reglas lógicas, permite procesar solicitudes, verificar disponibilidad y generar recomendaciones considerando criterios como capacidad, accesibilidad y ubicación.

# Instrucciones de Ejecución

Para ejecutar el sistema, siga los siguientes pasos:

### 1. Ubicación de archivos

Asegúrese de tener todos los archivos del proyecto en una misma carpeta.

### 2. Instalación de dependencias

Ejecute el siguiente comando en la terminal:

pip install streamlit pandas

### 3. Ejecución de la aplicación

En la terminal, dentro de la carpeta del proyecto, ejecute:

streamlit run app.py

### 4. Acceso

La aplicación se abrirá automáticamente en el navegador.

# Dependencias Necesarias

El proyecto fue desarrollado en Python 3.8 o superior.

Librerías requeridas:
* streamlit
* pandas

Instalación:
pip install streamlit pandas

# Archivos Modificados por el Equipo
Los siguientes archivos fueron modificados durante el desarrollo del proyecto:

* kb_v2.py

Contiene la versión extendida de la base de conocimiento, con nuevos hechos y reglas de inferencia.

* cases.py

Incluye nuevos casos de prueba para validar escenarios con requerimientos de accesibilidad.

# Diferencias entre KB_v1 y KB_v2
La versión KB_v2 introduce mejoras en la capacidad de razonamiento del sistema respecto a KB_v1.

## 1. Nuevos predicados y hechos
Se incorporaron nuevos predicados para modelar características del entorno y necesidades de los usuarios:

* **Accesible(s):** indica que un espacio cuenta con accesibilidad
* **Centrico(s):** indica que un espacio está bien ubicado
* **ReunionAccesible(g):** reuniones con requerimientos especiales
* **NecesitaAccesibilidad(g):** identifica grupos con necesidades específicas

## 2. Lógica de herencia y jerarquía 
Se añadieron reglas que permiten mayor flexibilidad en la asignación:

* Jerarquía de capacidad:
CapacidadAlta(s) → CapacidadMedia(s)

Esto permite asignar espacios grandes a grupos medianos si es necesario.

* Herencia de tipos de reunión:
ReunionAccesible → ReunionEquipo

Esto evita duplicación de reglas y mejora la generalización del sistema.

## 3. Recomendaciones contextuales
**KB_v1:**
Solo asigna espacios disponibles.

**KB_v2:**
Introduce el predicado Recomendable(s, g, t)
Considera accesibilidad, ubicación y tipo de reunión

Esto permite diferenciar entre asignaciones posibles y asignaciones óptimas.

# Conclusiones
La evolución de KB_v1 a KB_v2 representa una mejora significativa en la capacidad del sistema para tomar decisiones más informadas, incorporando nuevos criterios y reglas que permiten un razonamiento más completo y realista.

# Autores 
Abigail Godoy Araujo 

Montserrat Carrera Leal

Fermín Nieto
