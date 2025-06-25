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

