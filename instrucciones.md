
# Mini agente lógico para asignación de espacios

## Objetivo

Construir una webapp que reciba una solicitud de espacio, consulte una base de conocimiento, infiera qué espacios son asignables, muestre la traza de inferencia y permita reservar uno. Después de reservar, la KB debe cambiar y la app debe reflejar visualmente ese cambio.

 Lo importante es que quede claro:

- cómo se representa un dominio con hechos y reglas
- cómo se derivan conclusiones nuevas a partir de una KB
- cómo una acción cambia el estado del sistema
- cómo una KB mejorada produce un sistema mejor

---

## Enfoque del proyecto

En este proyecto trabajaremos con **forward chaining**.

Eso significa que el sistema parte de los hechos que ya conoce y aplica reglas para derivar nuevos hechos. El proceso se repite hasta que ya no aparecen hechos nuevos o hasta que la consulta que nos interesa ya puede responderse.


---

## Qué se evaluará

- representación del conocimiento con hechos y reglas
- inferencia automática elemental
- una consulta lógica
- una acción que modifique el mundo
- una interfaz visible
- una comparación clara entre una KB base y una KB mejorada


---

## Código base provisto

Se les entrega un **starter kit** con estos archivos:


- `engine.py`: motor básico de forward chaining
- `app.py`: webapp base en Streamlit
- `viz.py`: funciones para visualización
- `toy_example.py`: ejemplo pequeño para entender la lógica del motor
- `kb_v1.py`: versión base funcional
- `kb_v2.py`: archivo para extender la KB
- `cases.py`: casos de prueba base

### Qué deben hacer ustedes

1. Correr y entender la versión base.
1. Revisar cómo están representados los hechos y las reglas.
1. Usar `kb_v1.py` como punto de partida.
1. Construir una `kb_v2.py` mejorada.
1. Demostrar que la mejora vino de la KB.
1. Mostrar traza de inferencia y visualizaciones.
1. Entregar un proyecto que corra correctamente.

---

## Cómo correr el proyecto

Desde la carpeta del proyecto, ejecuta:

```bash
pip install streamlit pandas
streamlit run app.py
```




### Comandos útiles adicionales

Para probar la lógica sin abrir la app:

```bash
python toy_example.py
python cases.py
```

---


## Descripción general del sistema

La app representará un mini sistema de asignación de espacios del campus.

El usuario selecciona:

- un identificador de solicitud, por ejemplo `req1`
- una franja horaria
- un tipo de actividad

La app debe agregar hechos del usuario a la KB. Por ejemplo:

- `Solicita(req1,h2)`
- `Presentacion(req1)`

Después, el sistema debe contestar la consulta

$$
\exists s \; Asignable(s, req1, h2)
$$

Si hay espacios asignables, la app los muestra.

Si el usuario reserva uno, la KB debe actualizarse.

---

## Dominio fijo

Todos los equipos trabajarán con el mismo dominio.

### Espacios

- `AulaA`
- `AulaB`
- `Biblio1`
- `SalaReuniones`
- `AuditorioMini`

### Franjas

- `h1`
- `h2`
- `h3`
- `h4`

### Tipos de solicitud

- `EstudioIndividual`
- `ReunionEquipo`
- `Presentacion`
- `PresentacionGrande`

En `KB_v2` aparecerá además:

- `ReunionAccesible`

---

## Predicados obligatorios

### Predicados obligatorios en KB_v1

- `Libre(s,t)`
- `Ocupada(s,t)`
- `Solicita(g,t)`
- `EstudioIndividual(g)`
- `ReunionEquipo(g)`
- `Presentacion(g)`
- `PresentacionGrande(g)`
- `Silenciosa(s)`
- `Colaborativo(s)`
- `TieneProyector(s)`
- `CapacidadAlta(s)`
- `RequiereSilencio(g)`
- `RequiereColaboracion(g)`
- `Asignable(s,g,t)`
- `Recomendable(s,g,t)`
- `Reservada(s,g,t)`

### Predicados nuevos obligatorios en KB_v2

- `ReunionAccesible(g)`
- `NecesitaAccesibilidad(g)`
- `Accesible(s)`
- `Centrico(s)`

Pueden agregar otros predicados si los necesitan.

---

## Representación recomendada

### Hechos

Representados como tuplas. Ejemplos:

```python
("Libre", "AulaA", "h2")
("Presentacion", "req1")
```

### Reglas

Representadas como diccionarios o estructuras equivalentes. Ejemplo:

```python
{
    "name": "R_presentacion",
    "if": [
        ("Libre", "s", "t"),
        ("Solicita", "g", "t"),
        ("Presentacion", "g"),
        ("TieneProyector", "s")
    ],
    "then": ("Asignable", "s", "g", "t")
}
```

### Convención recomendada

- usa nombres de variables como `"s"`, `"g"`, `"t"`
- usa constantes como `"AulaA"`, `"req1"`, `"h2"`
- no uses espacios dentro de los nombres de constantes

---

## KB_v1

La `KB_v1` ya se les entrega en el starter kit. Su obligación es:

- correrla
- entenderla
- verificar que funciona
- usarla como punto de partida



---




## KB_v2

La `KB_v2` debe mejorar a la `KB_v1`.


### Nuevos hechos obligatorios

- `Accesible(AulaA)`
- `Accesible(SalaReuniones)`
- `Centrico(SalaReuniones)`
- `Centrico(AulaA)`

### Nuevas reglas obligatorias

$$
\forall g \; (ReunionAccesible(g) \Rightarrow ReunionEquipo(g))
$$

$$
\forall g \; (ReunionAccesible(g) \Rightarrow NecesitaAccesibilidad(g))
$$

$$
\forall s \forall g \forall t \; (Asignable(s,g,t) \land NecesitaAccesibilidad(g) \land Accesible(s) \Rightarrow Recomendable(s,g,t))
$$

$$
\forall s \forall g \forall t \; (Asignable(s,g,t) \land Presentacion(g) \land Centrico(s) \Rightarrow Recomendable(s,g,t))
$$

### Qué debe demostrar KB_v2

- la app distingue mejor entre espacios posibles y espacios preferibles
- la app puede atender un nuevo tipo de requerimiento
- la mejora vino de agregar conocimiento nuevo



---
### Tareas obligatorias

1. Ejecutar correctamente la versión base.
1. Entender y explicar al menos una traza de inferencia en `KB_v1`.
1. Construir una `KB_v2` mejorada.
1. Mostrar que `KB_v2` mejora el comportamiento del sistema.
1. Asegurarse de que la app siga corriendo bien con `KB_v2`.
1. Entregar visualizaciones y reporte.

---
## Qué debe hacer la app

### Entrada

La app debe tener un formulario con:

- id de solicitud
- franja horaria
- tipo de actividad

### Actualización de KB con la solicitud

Cuando el usuario envía el formulario, la app debe agregar hechos a la KB.

Ejemplo:

- `Solicita(req2,h3)`
- `PresentacionGrande(req2)`

### Inferencia

La app debe correr forward chaining y mostrar:

- todos los hechos derivados `Asignable`
- todos los hechos derivados `Recomendable`

### Consulta respondida

Debe quedar explícito si la consulta

$$
\exists s \; Asignable(s,g,t)
$$

es verdadera o falsa.

### Acción

Si el usuario reserva un espacio, la KB debe cambiar.

Ejemplo, si reserva `SalaReuniones` en `h2`:

- se elimina `Libre(SalaReuniones,h2)`
- se agrega `Ocupada(SalaReuniones,h2)`
- se agrega `Reservada(SalaReuniones,req1,h2)`

### Re-ejecución

Después de reservar, la app debe volver a correr la inferencia con la KB actualizada.

---

## Evidencia de inferencia

La app debe mostrar una traza clara. 

Debe ser posible reconstruir el razonamiento paso a paso.

### Formato sugerido

Una tabla con estas columnas:

- paso
- regla aplicada
- sustitución $ \theta $
- hecho derivado

### Ejemplo

1. `Presentacion(req1)`
1. `Solicita(req1,h2)`
1. `Libre(AulaA,h2)`
1. `TieneProyector(AulaA)`
1. aplicar `R_presentacion` con $ \theta = \{s \mapsto AulaA, g \mapsto req1, t \mapsto h2\} $
1. derivar `Asignable(AulaA,req1,h2)`

### Obligación mínima en el reporte

Deben explicar:

- una traza de inferencia en `KB_v1`
- una traza de inferencia en `KB_v2`

---

## Visualizaciones obligatorias

### Matriz de disponibilidad

Debe mostrarse una matriz o heatmap con:

- filas = espacios
- columnas = franjas
- color = libre / ocupada / reservada

Debe verse antes y después de reservar.

### Comparación entre KB_v1 y KB_v2

Deben correr las mismas solicitudes con ambas KB y mostrar una comparación visual.

Solicitudes mínimas obligatorias:

- `EstudioIndividual(reqA)` en `h1`
- `Presentacion(reqB)` en `h2`
- `PresentacionGrande(reqC)` en `h3`

La comparación puede mostrar:

- número de espacios `Asignable`, o
- número de espacios `Recomendable`

Lo importante es que se vea que `KB_v2` cambia el comportamiento del sistema.

---

## Casos de prueba esperados

### Caso 1

Solicitud: `EstudioIndividual(req1)` en `h1`

Salida esperada: debe aparecer al menos `AulaB` y `Biblio1` como asignables.

### Caso 2

Solicitud: `ReunionEquipo(req2)` en `h2`

Salida esperada: debe aparecer al menos `AulaA` y `SalaReuniones` como asignables.

### Caso 3

Solicitud: `Presentacion(req3)` en `h2`

Salida esperada: debe aparecer al menos `AulaA` y `SalaReuniones` como asignables.

### Caso 4

Solicitud: `PresentacionGrande(req4)` en `h3`

Salida esperada: debe aparecer `AuditorioMini` como asignable.

### Caso 5

Después de reservar `AuditorioMini` en `h3`, ya no debe volver a aparecer como libre en esa franja.

### Caso 6

En `KB_v2`, una `ReunionAccesible` debe producir recomendaciones mejores que en `KB_v1`.

---

## Qué archivos pueden modificar

### Pueden modificar

- `kb_v1.py` solo si encuentran un detalle menor que corregir
- `kb_v2.py` obligatoriamente
- `app.py` si necesitan pequeños ajustes de presentación
- `cases.py` para agregar o mejorar pruebas
- `README.md`
- `reporte.pdf`

### No deberían modificar

- `engine.py`
- `viz.py`
- `toy_example.py`


---

## Entregables

La entrega tendrá **dos partes**.

### Carpeta comprimida con el proyecto

Deben entregar una carpeta comprimida `.zip` que incluya, como mínimo:

- `app.py`
- `engine.py`
- `viz.py`
- `kb_v1.py`
- `kb_v2.py`
- `cases.py`
- `README.md`
- `reporte.pdf`

### Condición obligatoria

El proyecto debe correr correctamente con:

```bash
streamlit run app.py
```

El código se entrega para verificar que el sistema funciona.

### Documento principal 

El entregable principal será un PDF titulado:

**`reporte.pdf`**

Este documento debe evidenciar claramente que el equipo entendió:

- cómo está representado el dominio
- qué significan los predicados, hechos y reglas
- cómo opera el forward chaining
- cómo se deriva una conclusión a partir de la KB
- cómo cambia el comportamiento del sistema al pasar de `KB_v1` a `KB_v2`
- cómo una acción del usuario modifica el estado del sistema


---

## Estructura obligatoria del reporte

### Representación del conocimiento

Deben explicar, con sus propias palabras, cómo está representado el dominio en la KB.

Debe incluir:

1. una tabla con al menos **6 predicados**
1. el significado de cada predicado
1. un ejemplo concreto de uso de cada uno
1. una explicación breve de la diferencia entre:
   - hechos base
   - hechos derivados
   - reglas

### Una inferencia completa en KB_v1

Deben escoger **uno** de los casos de prueba de `KB_v1` y explicar, paso a paso, cómo se llega a la conclusión.

Debe incluir:

1. la solicitud inicial del usuario
1. los hechos agregados por esa solicitud
1. las reglas que se activan
1. la sustitución usada en cada paso relevante
1. el hecho derivado final
1. la respuesta que recibe el usuario

### Cambio de KB_v1 a KB_v2

Deben explicar qué agregaron en `KB_v2` y por qué eso mejora el sistema.

Debe incluir:

1. los nuevos hechos agregados
1. los nuevos predicados agregados
1. las nuevas reglas agregadas
1. una justificación breve de cada cambio

### Una inferencia completa en KB_v2

Deben escoger **un caso** en el que `KB_v2` se comporte mejor que `KB_v1` y explicarlo paso a paso.

Debe incluir:

1. la solicitud inicial
1. qué hechos se agregan
1. qué nuevas reglas se activan en `KB_v2`
1. qué nuevo hecho o recomendación aparece
1. por qué eso no ocurría igual en `KB_v1`

### Evidencia de actualización del mundo

Deben mostrar que entienden que el sistema no solo infiere, sino que también cambia su estado cuando el usuario actúa.

Debe incluir:

1. una captura o tabla **antes** de reservar
1. una captura o tabla **después** de reservar
1. una explicación breve de qué cambió en la KB

### Comparación entre KB_v1 y KB_v2

Deben comparar ambas versiones usando los casos de prueba definidos en la consigna.

Deben incluir:

1. una tabla comparativa o una gráfica
1. número de espacios `Asignable` en cada versión, o número de espacios `Recomendable`
1. una interpretación breve del resultado

### Reflexión breve

El reporte debe cerrar con una reflexión breve titulada:

**“Qué mejoraría si mi KB creciera”**

---

## README obligatorio

El `README.md` debe incluir:

1. instrucciones exactas de ejecución
1. dependencias necesarias
1. qué archivos modificó el equipo
1. qué cambia entre `KB_v1` y `KB_v2`

---

## Rúbrica

### Documento de evidencia de comprensión — 35 puntos

Se evaluará si el PDF demuestra claramente que el equipo entendió:

- la representación del dominio
- la diferencia entre hechos, reglas y hechos derivados
- una inferencia completa en `KB_v1`
- una inferencia completa en `KB_v2`
- la actualización de la KB tras una reserva
- la diferencia entre `KB_v1` y `KB_v2`

### Calidad de KB_v2 — 25 puntos

Se evaluará:

- si agrega conocimiento nuevo y relevante
- si las reglas son correctas
- si la mejora es real y no superficial
- si la KB sigue siendo coherente y clara

### Funcionamiento del sistema — 20 puntos

Se evaluará:

- si la app corre correctamente
- si el formulario funciona
- si la reserva funciona
- si la KB se actualiza bien
- si las visualizaciones aparecen correctamente

### Traza e interpretación — 10 puntos

Se evaluará:

- si la traza es clara
- si la sustitución está bien entendida
- si la explicación del razonamiento es correcta

### Reproducibilidad y orden de entrega — 10 puntos

Se evaluará:

- si el proyecto corre sin problemas
- si el `README.md` es claro
- si la carpeta está ordenada
- si los nombres de archivos son correctos

---

