import tkinter as tk
from tkinter import messagebox
from typing import List

class AplicacionListaDeTareas:
    """
    Clase principal para la aplicación GUI de Lista de Tareas usando Tkinter.
    """
    def __init__(self, master: tk.Tk):
        # Configuración de la ventana principal (master)
        self.master = master
        master.title("📋 Lista de Tareas")
        master.geometry("450x450") # Establece un tamaño inicial para la ventana
        master.resizable(False, False) # Evita que se cambie el tamaño de la ventana

        # --- Variables y Estructuras de Datos ---
        # No se necesita una lista separada, el Listbox actuará como la fuente de datos.
        # El estado de completado se manejará directamente en el texto del Listbox.

        # --- Configuración de la Interfaz (Widgets) ---

        # 1. Marco Superior para la Entrada de Tareas
        self.frame_entrada = tk.Frame(master)
        self.frame_entrada.pack(pady=10)

        # Campo de entrada (Entry) para nuevas tareas
        self.campo_tarea = tk.Entry(
            self.frame_entrada,
            width=35,
            font=('Arial', 12)
        )
        self.campo_tarea.pack(side=tk.LEFT, padx=5)
        # Enlaza la tecla <Return> (Enter) a la función de añadir tarea.
        # Esto cumple con el requisito de añadir tareas con la tecla Enter.
        self.campo_tarea.bind("<Return>", self.añadir_tarea_evento)

        # Botón para Añadir Tarea
        self.boton_añadir = tk.Button(
            self.frame_entrada,
            text="Añadir Tarea",
            command=self.añadir_tarea,
            bg='#4CAF50', # Color de fondo (verde)
            fg='white'    # Color de texto
        )
        self.boton_añadir.pack(side=tk.LEFT, padx=5)

        # 2. Listbox para Mostrar Tareas
        # Se incluye un Scrollbar para manejar muchas tareas.
        self.frame_lista = tk.Frame(master)
        self.frame_lista.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame_lista)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lista_tareas = tk.Listbox(
            self.frame_lista,
            width=50,
            height=15,
            yscrollcommand=self.scrollbar.set,
            font=('Arial', 11),
            selectmode=tk.SINGLE # Permite seleccionar solo un elemento a la vez
        )
        self.lista_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.lista_tareas.yview)

        # Opcional: Implementación de evento adicional (Doble Clic)
        # Doble clic en una tarea la marca como completada/incompleta.
        self.lista_tareas.bind("<Double-Button-1>", self.alternar_estado_tarea_evento)


        # 3. Marco Inferior para Botones de Acción
        self.frame_acciones = tk.Frame(master)
        self.frame_acciones.pack(pady=10)

        # Botón para Marcar como Completada
        self.boton_completar = tk.Button(
            self.frame_acciones,
            text="✅ Completada",
            command=self.alternar_estado_tarea,
            bg='#2196F3', # Color de fondo (azul)
            fg='white'
        )
        self.boton_completar.pack(side=tk.LEFT, padx=10)

        # Botón para Eliminar Tarea
        self.boton_eliminar = tk.Button(
            self.frame_acciones,
            text="❌ Eliminar Tarea",
            command=self.eliminar_tarea,
            bg='#F44336', # Color de fondo (rojo)
            fg='white'
        )
        self.boton_eliminar.pack(side=tk.LEFT, padx=10)

    # --- Lógica de la Aplicación y Manejo de Eventos ---

    def añadir_tarea(self):
        """
        Obtiene el texto del campo de entrada, lo limpia y lo añade al Listbox.
        """
        tarea = self.campo_tarea.get().strip() # Obtener y limpiar espacios

        if tarea:
            # Inserta la tarea al final del Listbox
            self.lista_tareas.insert(tk.END, tarea)
            # Limpia el campo de entrada después de añadir
            self.campo_tarea.delete(0, tk.END)
        else:
            # Muestra un mensaje de advertencia si el campo está vacío
            messagebox.showwarning("Advertencia", "¡Debes ingresar una tarea!")

    def añadir_tarea_evento(self, event):
        """
        Manejador para el evento de pulsar Enter en el campo de texto.
        Llama a la función principal de añadir tarea.
        """
        self.añadir_tarea()

    def alternar_estado_tarea(self):
        """
        Cambia el estado visual de la tarea seleccionada (completada/incompleta).
        """
        try:
            # Obtiene el índice de la tarea actualmente seleccionada
            indice_seleccionado = self.lista_tareas.curselection()[0]
            tarea_actual = self.lista_tareas.get(indice_seleccionado)

            # Prefijo para indicar que la tarea está completada
            PREFIJO_COMPLETADO = "✅ "

            if tarea_actual.startswith(PREFIJO_COMPLETADO):
                # Si está completada, la marca como incompleta (quita el prefijo)
                nueva_tarea = tarea_actual.replace(PREFIJO_COMPLETADO, "", 1)
            else:
                # Si está incompleta, la marca como completada (añade el prefijo)
                nueva_tarea = PREFIJO_COMPLETADO + tarea_actual

            # 1. Elimina la versión antigua de la tarea
            self.lista_tareas.delete(indice_seleccionado)
            # 2. Inserta la nueva versión (con o sin prefijo) en la misma posición
            self.lista_tareas.insert(indice_seleccionado, nueva_tarea)
            # 3. Vuelve a seleccionar el elemento para mantener el foco visual
            self.lista_tareas.select_set(indice_seleccionado)

        except IndexError:
            # Se lanza si no hay ninguna tarea seleccionada
            messagebox.showwarning("Advertencia", "Debes seleccionar una tarea para marcarla.")

    def alternar_estado_tarea_evento(self, event):
        """
        Manejador para el evento de doble clic.
        Llama a la función principal de alternar el estado.
        """
        self.alternar_estado_tarea()


    def eliminar_tarea(self):
        """
        Elimina la tarea actualmente seleccionada del Listbox.
        """
        try:
            # Obtiene el índice de la tarea seleccionada
            indice_seleccionado = self.lista_tareas.curselection()[0]
            # Elimina la tarea por su índice
            self.lista_tareas.delete(indice_seleccionado)

        except IndexError:
            # Se lanza si no hay ninguna tarea seleccionada
            messagebox.showwarning("Advertencia", "Debes seleccionar una tarea para eliminarla.")


# --- Ejecución de la Aplicación ---
if __name__ == '__main__':
    # Crea la ventana raíz de Tkinter
    root = tk.Tk()
    # Crea una instancia de la aplicación
    app = AplicacionListaDeTareas(root)
    # Inicia el bucle principal de eventos de Tkinter (mainloop)
    # La aplicación permanece abierta y receptiva a los eventos del usuario.
    root.mainloop()