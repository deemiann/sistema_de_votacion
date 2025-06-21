\###############################################

### NOMBRE DEL PROYECTO

\###############################################

### Sistema de votaciones con tablas hash

\###############################################

### DATOS DEL GRUPO

\###############################################
"""
NumOrden APELLIDOS Y NOMBRES  Responsable
NumOrden APELLIDOS Y NOMBRES  Miembro
HORARIO DE LABORATORIO:
DÍA:
HORA:
"""

\###############################################

### 1. Introducción

\###############################################
"""
Objetivo del proyecto:
Diseñar e implementar un sistema de votaciones electrónico básico que permita registrar votantes, almacenar sus votos y obtener resultados de forma eficiente, utilizando como estructura principal una tabla hash.

Descripción breve:
Las tablas hash permiten realizar operaciones de inserción, búsqueda y eliminación en tiempo constante promedio, lo cual es ideal para manejar rápidamente registros de votantes y votos en un proceso electoral. La clave será el identificador del votante y el valor asociado, su voto.

Alcance:
Se implementará:

* Registro de votantes con su identificador único.
* Almacenamiento y modificación de votos.
* Cálculo de resultados por candidato.
* Validación de votos únicos.

No se incluirá:

* Interfaces gráficas.
* Validación biométrica ni cifrado de datos.
  """

\###############################################

### 2. Análisis del Problema

\###############################################
"""
Entrada esperada:

* ID de votante (string o entero).
* Nombre del candidato votado (string).
* Comando de operación (registrar, votar, consultar resultados).

Salida esperada:

* Confirmación de registro o voto.
* Mensajes de error si ya se ha votado.
* Conteo final de votos por candidato.

Restricciones:

* Un voto por ID.
* Más de 1000 registros deberán ser manejados eficientemente.

Casos de uso:

* Elecciones de representantes estudiantiles en la universidad.
* Votaciones internas de comités.
* Sistemas de encuestas rápidas.
  """

\###############################################

### 3. Selección de Estructuras de Datos

\###############################################
"""
Estructura principal: Tabla Hash.

Justificación:
Se requiere rápido acceso a los datos de los votantes, verificar si ya han votado y actualizar el conteo. La tabla hash es ideal por su eficiencia en búsqueda e inserción.

Estructuras auxiliares:

* Diccionarios para conteo de votos por candidato.
* Listas para mostrar resultados ordenados.
  """

\###############################################

### 4. Diseño del Algoritmo

\###############################################
"""
Descripción del algoritmo:

1. Registrar votante en la tabla hash.
2. Verificar si ya votó.
3. Registrar voto si es válido.
4. Incrementar contador del candidato en el diccionario.
5. Mostrar resultados cuando se solicite.

Complejidad:

* Inserción y búsqueda: promedio O(1)
* Conteo de votos: O(n)
  """

\###############################################
\###############################################

### 5. Implementación y documentación

\###############################################

\###############################################

### MODULO 1

\###############################################

\###############################################

### MODULO 2

\###############################################

\###############################################

### MODULO  ..

\###############################################

\###############################################

### 6. Evaluación y Conclusiones

\###############################################
"""
Pruebas de rendimiento:

* Tiempo de inserción y búsqueda para 1000+ votantes.

Casos extremos:

* Todos los votos a un solo candidato.
* IDs duplicados o vacíos.

Comparación:

* Versión con lista simple: tiempo de búsqueda crece linealmente.

Resultados obtenidos:

* Sistema rápido y funcional.
* Acceso y conteo eficiente con tabla hash.

Lecciones aprendidas:

* Tablas hash mejoran significativamente el rendimiento.
* Es vital controlar colisiones y validar entradas.

Mejoras futuras:

* Autenticación de votantes.
* Exportación de resultados.
* Interfaz web o app gráfica.
  """

\###############################################

###

\###############################################
