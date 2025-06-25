###############################################
### NOMBRE DEL PROYECTO
###############################################
"""
SISTEMA DE VOTACIONES CON TABLAS HASH
"""

###############################################
### DATOS DEL GRUPO
###############################################
"""
01 AGUIRRE QUISPE, RALL ANDERSON Miembro
02 ALANYA VASQUEZ, ANTONY BRANDON  Responsable
84 TORRES PALOMINO, JOHAN FORTUNATO Miembro

HORARIO DE LABORATORIO:
DÍA: JUEVES
HORA: 7-9 AM

GRUPO: 1
"""

###############################################
### 1. Introducción
###############################################
"""
Objetivo del proyecto:
El presente proyecto tiene como objetivo diseñar e implementar un sistema de
votación electrónica básico, con un enfoque en la eficacia, seguridad e
integridad del proceso electoral. Este sistema permitirá gestionar de forma
eficiente tanto a los votantes como sus respectivos votos, mediante mecanismos
de verificación y almacenamiento que aseguren que cada ciudadano vote una sola
vez.

El sistema debe contemplar un registro rápido y único de votantes, garantizando
la no duplicidad mediante el uso de estructuras de datos eficientes,
particularmente una tabla hash como estructura principal, que permita
operaciones rápidas de inserción, búsqueda y eliminación. Además, se
incorporarán funcionalidades para añadir, consultar y eliminar datos, así como
obtener los resultados electorales de forma inmediata y precisa, conservando
siempre la integridad de la información procesada.

Este proyecto tiene como fin demostrar la aplicabilidad y ventajas del uso de
tablas hash en escenarios reales donde se requieren operaciones constantes en
tiempo eficiente, como es el caso de un proceso electoral automatizado.


Descripción breve:
El Sistema de Votaciones con Tablas Hash es una herramienta diseñada para
gestionar de forma eficiente un proceso electoral electrónico, permitiendo a
los usuarios registrarse como votantes, emitir su voto por candidatos
específicos y consultar los resultados en tiempo real. Para ello, el sistema
emplea una tabla hash como estructura de datos principal, utilizando el
identificador único del votante (como el DNI) como clave y su voto como valor
asociado.

Esta estructura permite realizar operaciones de inserción, búsqueda y
eliminación en tiempo constante promedio, lo que resulta ideal para manejar de
manera rápida y eficaz grandes volúmenes de datos. Además, se implementan
mecanismos para controlar colisiones y garantizar la unicidad de los registros,
contribuyendo así a la integridad, seguridad y confiabilidad del proceso
electoral.


Alcance:
Se implementará:

* Registro de votantes con su clave única(DNI).
* Verificación para evitar votos duplicados.
* Cálculo de resultados por candidato.
* Búsqueda y almacenamiento de datos.
* Presentación clara de los resultados parciales y finales.

No se incluirá:

* Autenticación biométrica o seguridad avanzada (solo DNI).
* Integración con sistemas de identificación nacional (RENIEC).
* Interfaz gráfica compleja.
  """

###############################################
### 2. Análisis del Problema
###############################################
"""
Entrada esperada:

* DNI del votante (string/clave primaria).
* Nombre del candidato votado (string).
* Voto (string o entero representando candidato/opción).

Salida esperada:

* Validación de votantes.
* Confirmación de registro o voto.
* Mensajes de error si ya se ha votado.
* Conteo final de votos por candidato.
* Número total de votantes registrados y votos emitidos.

Restricciones:

* 0% de votos duplicados (garantizado por la unicidad de claves DNI).
* Más de 1000 registros deberán ser manejados eficientemente.
* Uso eficiente de RAM (evitar colisiones excesivas que incrementen el
  tiempo a O(n)).

Casos de uso:

* Elecciones de representantes estudiantiles en la universidad.
* Votaciones internas de comités.
* Sistemas de encuestas rápidas.
* Votaciones en Asambleas de Comunidades o Cooperativas.
* Encuestas Internas en Empresas
  """

###############################################
### 3. Selección de Estructuras de Datos
###############################################
"""
Estructura principal: La estructura de datos principal es la Tabla Hash (Hash
Table).

Justificación:
Se requiere rápido acceso a los datos de los votantes, verificar si ya han
votado y actualizar el conteo. La tabla hash es ideal por su eficiencia en
búsqueda e inserción.

* Eficiencia en Tiempo: Verificar si un DNI ya votó toma microsegundos.
* Unicidad de Claves: El DNI como clave única evita votos duplicados por
diseño.

Estructuras auxiliares:
* Maps: para conteo de votos por candidato y almacenar algunos datos.
* Arrays: Para manejar colisiones en la tabla hash (encadenamiento).
  """

###############################################
### 4. Diseño del Algoritmo
###############################################
"""
Descripción del algoritmo:

1. Registrar votante en la tabla hash.
2. Verificar si ya votó.
3. Registrar voto si es válido.
4. Incrementar contador del candidato en el diccionario.
5. Mostrar resultados cuando se solicite.

Complejidad Temporal:
* registrar_voto:
    Promedio: O(1+c)
    Peor caso: O(n+c)
* total_votantes: O(n)O(n)
* mostrar_resultados: O(c)
* eliminar_votante: O(b+c)

Complejidad Espacial:
* Tabla hash de votantes: 0(n+b)
* Tabla de resultados: 0(c)
* Total del sistema: 0(n+c+b)

Donde n: numero de votantes
      c: numero de candidatos
      b: colisiones en una cubeta
  """


###############################################
### 5. Implementación y documentación
###############################################

###############################################
### MODULO 1 Definicon de clases(Map, TableHash y SistemaVotacion)
###############################################

import time
import random
import tkinter as tk
from tkinter import messagebox

class UnsortedTableMap:
    """Implementación simple de un diccionario mediante una lista desordenada."""
    
    class _Item:
        """Clase interna que representa una entrada clave-valor."""
        def __init__(self, k, v):
            self._key = k
            self._value = v

    def __init__(self):
        """Inicializa una tabla vacía."""
        self._table = []

    def __getitem__(self, k):
        """Retorna el valor asociado a la clave k."""
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError("Key Error: " + repr(k))

    def __setitem__(self, k, v):
        """Asigna el valor v a la clave k. Si ya existe, actualiza el valor."""
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        self._table.append(self._Item(k, v))
    
    def __delitem__(self, k):
        """Elimina el elemento con clave k."""
        for i in range(len(self._table)):
            if k == self._table[i]._key:
                del self._table[i]
                return
        raise KeyError("Key Error: " + repr(k))

    def __len__(self):
        """Retorna el número de elementos almacenados."""
        return len(self._table)

    def __iter__(self):
        """Itera sobre las claves almacenadas."""
        for item in self._table:
            yield item._key

    def items(self):
        """Itera sobre los pares clave-valor."""
        for item in self._table:
            yield item._key, item._value

    def __str__(self):
        """Representación como string del mapa."""
        return "{" + ", ".join(f"'{k}': {v}" for k, v in self.items()) + "}"


class HashMapBase:
    """Mapa hash que utiliza una lista de UnsortedTableMap para manejar
    colisiones (encadenamiento).
    """
    
    def __init__(self):
        self._table = 11 * [None]  # Tabla con 11 cubetas inicialmente

    def _hash_function(self, k):
        """Función hash simple basada en suma de códigos ASCII."""
        return sum(ord(c) for c in k) % len(self._table)

    def __setitem__(self, k, v):
        """Inserta o actualiza el valor v en la clave k."""
        i = self._hash_function(k)
        if self._table[i] is None:
            self._table[i] = UnsortedTableMap()
        self._table[i][k] = v

    def __getitem__(self, k):
        """Retorna el valor asociado a la clave k si existe."""
        i = self._hash_function(k)
        if self._table[i] is not None:
            try:
                return self._table[i][k]
            except KeyError:
                return None
        return None

    def __contains__(self, k):
        """Verifica si la clave k está en el mapa."""
        return self.__getitem__(k) is not None

    def __iter__(self):
        """Itera sobre todas las claves almacenadas."""
        for bucket in self._table:
            if bucket:
                for key in bucket:
                    yield key

    def items(self):
        """Itera sobre todos los pares clave-valor del mapa."""
        for bucket in self._table:
            if bucket:
                for k, v in bucket.items():
                    yield k, v

class SistemaVotacion:
    """Clase principal que gestiona el sistema de votación."""

    def __init__(self):
        self.votantes = HashMapBase()         # Claves: DNI, Valores: candidato votado
        self.resultados = UnsortedTableMap()  # Claves: candidato, Valores: conteo de votos

    def registrar_voto(self, dni, candidato):
        """Registra el voto de un votante identificado por su DNI."""

        # Validación del formato de DNI
        if not isinstance(dni, str) or not dni.isdigit() or len(dni) != 8:
            return f"Error: el DNI '{dni}' no es válido. Debe tener 8 dígitos numéricos."

        if self.votantes[dni] is not None:
            return f"Error: el DNI {dni} ya ha votado."

        self.votantes[dni] = candidato
        votos_actuales = self.resultados[candidato] if candidato in self.resultados else 0
        self.resultados[candidato] = votos_actuales + 1
        return f"Voto registrado exitosamente para {candidato}."

    def total_votantes(self):
        """Devuelve el número total de votantes únicos registrados."""
        return len(list(self.votantes))

    def mostrar_resultados(self):
        """Devuelve los resultados de la votación en forma de diccionario."""
        return dict(self.resultados.items())

    def eliminar_votante(self, dni):
        """Permite eliminar un votante (por ejemplo, para pruebas o errores)."""
        if self.votantes[dni] is None:
            return f"El DNI {dni} no está registrado."
        candidato = self.votantes[dni]
        del self.votantes._table[self.votantes._hash_function(dni)][dni]
        self.resultados[candidato] = self.resultados[candidato] - 1
        return f"Votante con DNI {dni} eliminado correctamente."

###############################################
### MODULO 2 Pruebas
###############################################

def generar_dni():
    """Genera un DNI aleatorio válido de 8 dígitos como string."""
    return ''.join(str(random.randint(0, 9)) for _ in range(8))

def prueba_insercion(sistema, cantidad):
    """Prueba el tiempo de inserción de muchos votantes."""
    candidatos = ["A", "B", "C"]
    start = time.time()
    for _ in range(cantidad):
        dni = generar_dni()
        candidato = random.choice(candidatos)
        sistema.registrar_voto(dni, candidato)
    end = time.time()
    print(f"[Inserción] Tiempo para registrar {cantidad} votantes: {end - start:.6f} segundos")

def prueba_busqueda(sistema, muestras=100):
    """Prueba el tiempo de búsqueda de DNIs ya registrados."""
    dnis = list(sistema.votantes)
    dnis_muestra = random.sample(dnis, min(muestras, len(dnis)))

    start = time.time()
    for dni in dnis_muestra:
        _ = sistema.votantes[dni]
    end = time.time()
    print(f"[Búsqueda] Tiempo para verificar {len(dnis_muestra)} DNIs: {end - start:.6f} segundos")


def caso_extremo_dnis_invalidos(sistema):
    """Se prueban DNIs vacíos o con caracteres inválidos."""
    print("\n[Prueba extrema] DNIs inválidos:")
    print(sistema.registrar_voto("", "A"))
    print(sistema.registrar_voto("ABC12345", "B"))
    print(sistema.registrar_voto("-0000001", "C"))


def comparacion_con_array(n):
    """Comparación con lista simple (array) para búsquedas."""
    print("\n[Comparación] Uso de arrays vs tablas hash")
    lista_votantes = []

    for _ in range(n):
        lista_votantes.append((generar_dni(), "Candidato X"))

    # Buscar 100 DNIs aleatorios
    dnis_existentes = random.sample([dni for dni, _ in lista_votantes], 100)

    # Búsqueda en lista (O(n))
    start = time.time()
    for dni in dnis_existentes:
        found = any(dni == x[0] for x in lista_votantes)
    end = time.time()
    print(f"[Array] Búsqueda de 100 DNIs en lista de {n}: {end - start:.6f} segundos")

    # Búsqueda en tabla hash (O(1) promedio)
    sistema = SistemaVotacion()
    for dni, candidato in lista_votantes:
        sistema.registrar_voto(dni, candidato)

    start = time.time()
    for dni in dnis_existentes:
        _ = sistema.votantes[dni]
    end = time.time()
    print(f"[Tabla Hash] Búsqueda de 100 DNIs en hash de {n}: {end - start:.6f} segundos")


# =======================
# EJECUCIÓN DE PRUEBAS
# =======================
if __name__ == "__main__":
    sistema = SistemaVotacion()

    # Pruebas solicitadas
    prueba_insercion(sistema, 1000)
    prueba_busqueda(sistema, 100)
    print("Total de votantes:", sistema.total_votantes())
    print("Resultados:", sistema.mostrar_resultados())

    # Casos extremos
    caso_extremo_dnis_invalidos(SistemaVotacion())

    # Comparación con array
    comparacion_con_array(1000)

###############################################
### MODULO 3 Interfaz Grafica
###############################################

class InterfazVotacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Votación con Tablas Hash")
        self.sistema = SistemaVotacion()

        # Etiquetas e inputs
        self.label_dni = tk.Label(root, text="DNI del votante:")
        self.label_dni.pack()
        self.entry_dni = tk.Entry(root)
        self.entry_dni.pack()

        self.label_candidato = tk.Label(root, text="Nombre del candidato:")
        self.label_candidato.pack()
        self.entry_candidato = tk.Entry(root)
        self.entry_candidato.pack()

        # Botón de votar
        self.btn_votar = tk.Button(root, text="Registrar Voto", command=self.registrar_voto)
        self.btn_votar.pack(pady=5)

        # Botón de mostrar resultados
        self.btn_resultados = tk.Button(root, text="Mostrar Resultados", command=self.mostrar_resultados)
        self.btn_resultados.pack(pady=5)

        # Área de resultados
        self.text_resultados = tk.Text(root, height=10, width=50)
        self.text_resultados.pack(pady=10)
        self.text_resultados.config(state='disabled')

    def registrar_voto(self):
        dni = self.entry_dni.get().strip()
        candidato = self.entry_candidato.get().strip()

        if not dni or not candidato:
            messagebox.showerror("Error", "Por favor, ingrese DNI y candidato.")
            return

        mensaje = self.sistema.registrar_voto(dni, candidato)
        messagebox.showinfo("Resultado", mensaje)
        self.entry_dni.delete(0, tk.END)
        self.entry_candidato.delete(0, tk.END)

    def mostrar_resultados(self):
        resultados = self.sistema.mostrar_resultados()
        self.text_resultados.config(state='normal')
        self.text_resultados.delete(1.0, tk.END)

        if not resultados:
            self.text_resultados.insert(tk.END, "Aún no hay votos registrados.\n")
        else:
            self.text_resultados.insert(tk.END, "Resultados de la votación:\n")
            for candidato, votos in resultados.items():
                self.text_resultados.insert(tk.END, f"{candidato}: {votos} votos\n")

        self.text_resultados.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazVotacion(root)
    root.mainloop()


###############################################
### 6. Evaluación y Conclusiones
###############################################
"""
Pruebas de rendimiento:

* Tiempo de Inserción: Registrar 1000 votantes con DNIs aleatorios.
* Tiempo de Búsqueda: Verificar la existencia de 100 DNIs en una tabla con 1000
  registros.


Casos extremos:
* IDs duplicados o vacíos.
* DNIs Inválidos o Erróneos: Entrada de DNIs con letras o valores negativos

Comparación:

* Frente a Arrays: Registro y Búsqueda de Votantes
  (requerirían una búsqueda O(N)).

Resultados obtenidos:

* Sistema rápido y funcional.
* Acceso y conteo eficiente con tabla hash.
* Registrar nuevos votantes y verificar su unicidad de manera eficiente.
* Prevención de votos duplicados mediante la unicidad del DNI.
* Presentar los resultados de la votación de forma clara y accesible.

Lecciones aprendidas:

* Tablas hash mejoran significativamente el rendimiento.
* Control de colisiones y validar entradas.
* Importancia del Diseño de la Función de Hash.
* Modularización del código.
* Aprendizaje de la Validación de Datos Crítica.

Mejoras futuras:

* Exportación de resultados.
* Seguridad Reforzada: Añadir autenticación biométrica.
* Interfaz Gráfica: Desarrollar una interfaz web o móvil.
* Integración con Blockchain: Almacenar votos en una blockchain para
  garantizar la transparencia pública.
  """
