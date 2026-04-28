# Mini Agente Lógico para Asignación de Espacios

Sistema basado en conocimiento que utiliza **forward chaining** para asignar espacios universitarios (aulas, biblioteca, sala de reuniones, auditorio) según disponibilidad, tipo de actividad y criterios de calidad como accesibilidad, centralidad y capacidad.

---

## Instrucciones de Ejecución

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
```

### 2. Instalar dependencias

```bash
pip install streamlit pandas
```

### 3. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en el navegador en `http://localhost:8501`.

### 4. Pruebas sin interfaz gráfica

Para verificar la lógica del motor de inferencia:

```bash
python toy_example.py
```

Para correr todos los casos de prueba:

```bash
python cases.py
```

---

## Dependencias

| Librería | Uso |
|---|---|
| `streamlit` | Interfaz web interactiva |
| `pandas` | Manipulación de datos y visualización de tablas |

Python **3.8 o superior** requerido.

---

## Estructura del Proyecto

```
.
├── app.py          # Aplicación principal en Streamlit
├── engine.py       # Motor de forward chaining 
├── kb_v1.py        # Base de conocimiento versión 1 (base)
├── kb_v2.py        # Base de conocimiento versión 2 (mejorada) 
├── cases.py        # Casos de prueba ← modificado
├── viz.py          # Funciones de visualización 
├── toy_example.py  # Ejemplo mínimo del motor 
├── README.md       # Este archivo 
└── reporte.pdf     # Reporte del proyecto
```

---

## Archivos Modificados por el Equipo

| Archivo | Cambios realizados |
|---|---|
| `kb_v2.py` | KB extendida con nuevos hechos, predicados y reglas (R9–R30) |
| `cases.py` | Nuevos casos de prueba exclusivos de KB V2 (V2-C1 a V2-Prioridad) |
| `engine.py` | Modificado para soportar el override del Director (parámetro `allow_override` en `reserve_space`) |
| `viz.py` | Modificado para mostrar el ID de la solicitud en celdas reservadas de la matriz de disponibilidad |
| `README.md` | Documentación completa del proyecto |

---

## Dominio del Sistema

### Espacios disponibles
`AulaA` · `AulaB` · `Biblio1` · `SalaReuniones` · `AuditorioMini`

### Franjas horarias
`h1` · `h2` · `h3` · `h4`

### Tipos de solicitud
**KB V1:** `EstudioIndividual` · `ReunionEquipo` · `Presentacion` · `PresentacionGrande`

**KB V2 (adicionales):** `ReunionAccesible` · `ReunionLarga`

---

## Cómo Funciona el Sistema

El usuario ingresa en el formulario:
- **ID de solicitud** (ej. `req1`)
- **Franja horaria** (ej. `h2`)
- **Tipo de actividad** (ej. `Presentacion`)

El sistema agrega hechos a la KB:
```
Solicita(req1, h2)
Presentacion(req1)
```

Luego ejecuta **forward chaining** y responde la consulta:
```
∃s Asignable(s, req1, h2)
```

Si el usuario reserva un espacio, la KB se actualiza:
- Se elimina `Libre(SalaReuniones, h2)`
- Se agrega `Ocupada(SalaReuniones, h2)`
- Se agrega `Reservada(SalaReuniones, req1, h2)`

---

## Diferencias entre KB V1 y KB V2

### KB V1 — Base

Contiene 8 reglas (R1–R8) que cubren los tipos de solicitud básicos:

| Regla | Descripción |
|---|---|
| R1 | `EstudioIndividual` → requiere silencio |
| R2 | `ReunionEquipo` → requiere colaboración |
| R3 | Asignar espacio silencioso a estudio individual |
| R4 | Asignar espacio colaborativo a reunión |
| R5 | Asignar espacio con proyector a presentación |
| R6 | Asignar espacio con proyector y capacidad alta a presentación grande |
| R7 | Recomendar espacios silenciosos |
| R8 | Recomendar espacios colaborativos |


---

### KB V2 — Mejorada

Extiende KB V1 con nuevos hechos, predicados y 22 reglas adicionales (R9–R30):

#### Nuevos hechos
```python
("Accesible", "AulaA"), ("Accesible", "SalaReuniones")
("Centrico", "AulaA"),  ("Centrico", "SalaReuniones")
("CapacidadMedia", "AulaA"), ("CapacidadMedia", "SalaReuniones")
("CapacidadBaja", "AulaB"),  ("CapacidadBaja", "Biblio1")
("CapacidadAlta", "SalaReuniones"), ("CapacidadAlta", "AuditorioMini")
("EsDirector", "Director1")
("Consecutivo", "h1", "h2"), ("Consecutivo", "h2", "h3"), ("Consecutivo", "h3", "h4")
```

#### Nuevos predicados
| Predicado | Significado |
|---|---|
| `Accesible(s)` | El espacio tiene accesibilidad física |
| `Centrico(s)` | El espacio está bien ubicado en el campus |
| `ReunionAccesible(g)` | La reunión requiere espacio accesible |
| `NecesitaAccesibilidad(g)` | La solicitud necesita accesibilidad |
| `CapacidadMedia(s)` / `CapacidadBaja(s)` | Jerarquía de capacidad de espacios |
| `AltaPrioridad(g)` | La solicitud tiene prioridad elevada |
| `AltamenteRecomendable(s,g,t)` | Espacio de máxima calidad para la solicitud |
| `AsignablePrioritario(s,g,t)` | Espacio que puede asignarse con prioridad de director |
| `EsDirector(g)` | La solicitud proviene de un director |
| `LibreLargo(s,t)` | El espacio tiene dos franjas consecutivas libres |

#### Nuevas reglas destacadas

| Regla | Descripción |
|---|---|
| R9 | `ReunionAccesible` hereda `ReunionEquipo` |
| R10 | `ReunionAccesible` → necesita accesibilidad |
| R11 | Espacio accesible + necesita accesibilidad → recomendable |
| R12 | Espacio céntrico + presentación → recomendable |
| R13 | `CapacidadAlta` → `CapacidadMedia` (jerarquía) |
| R14–R15 | `PresentacionGrande` → alta prioridad → altamente recomendable |
| R16a | Director siempre tiene alta prioridad |
| R16 | Director + espacio libre → asignable prioritario |
| R17 | Director puede tomar espacios reservados por otros |
| R17a–R17c | Asignable prioritario → asignable + recomendable + altamente recomendable |
| R28–R30 | Soporte para reuniones largas con slots consecutivos |

#### ¿Qué mejora concretamente?

- **KB V1** asigna si un espacio *puede* usarse.  
- **KB V2** además distingue si es *recomendable* o *altamente recomendable*, considera accesibilidad, ubicación, capacidad y prioridad del solicitante.
- Un director puede desplazar reservas existentes (override).
- Reuniones largas solo se asignan en franjas consecutivas disponibles.

---

## Casos de Prueba

### Casos compartidos V1 y V2

| Caso | Solicitud | Franja | Espacios esperados |
|---|---|---|---|
| Caso 1 | `EstudioIndividual(reqA)` | h1 | AulaB, Biblio1 |
| Caso 2 | `ReunionEquipo(reqB)` | h2 | AulaA, SalaReuniones |
| Caso 3 | `Presentacion(reqC)` | h2 | AulaA, SalaReuniones |
| Caso 4 | `PresentacionGrande(reqD)` | h3 | AuditorioMini |
| Caso 5 | `ReunionAccesible(reqE)` | h2 | AulaA, SalaReuniones |

### Casos exclusivos KB V2

| Caso | Descripción | Reglas ejercitadas |
|---|---|---|
| V2-C1 | ReunionAccesible filtra solo espacios accesibles | R9, R10, R11 |
| V2-C2 | PresentacionGrande en h1 con capacidad alta derivada | R13, R6 |
| V2-C3 | PresentacionGrande activa alta prioridad | R14, R15 |
| V2-C4 | Presentación céntrica recomendable | R12 |
| V2-C6 | Director con prioridad sobre espacios libres | R16, R16a |
| V2-Prioridad | Director toma espacio reservado por otro | R17, R17a–R17c |

---

## Visualizaciones en la App

- **Matriz de disponibilidad:** tabla espacios × franjas con estado 🟩 Libre / 🟥 Ocupada / 🟦 Reservada
- **Comparación V1 vs V2:** gráfica de barras con asignables y recomendables por caso
- **Métricas exclusivas KB V2:** impacto de reglas de prioridad, accesibilidad y centralidad
- **Tasa de verificación:** qué porcentaje de casos pasan el mínimo esperado
- **Traza de inferencia:** tabla con ronda, regla aplicada, sustitución θ y hecho derivado

---

## Autores

- Abigail Godoy Araujo
- Montserrat Carrera Leal
- Fermín Nieto
