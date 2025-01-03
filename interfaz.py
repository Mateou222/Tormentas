import sys
from tkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from Funciones_basicas import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Diccionario para guardar el estado de los checkboxes
estado_selecciones = {}
checkboxes = {}

# Variable global para almacenar el archivo seleccionado
archivo_seleccionado = None
analisis_seleccionado = None

def cerrar_ventana(ventana):
    ventana.quit()  # Finaliza el mainloop de la ventana
    ventana.destroy()  # Cierra la ventana
    sys.exit()  # Finalizar el programa

# Función que actualiza el estado al seleccionar/deseleccionar un checkbox
def actualizar_seleccion(pluvio, var):
    global estado_selecciones
    estado_selecciones[pluvio] = var
    
# Función para obtener pluviómetros seleccionados
def obtener_seleccionados():
    global checkboxes
    return [pluvio for pluvio, var in checkboxes.items() if var.get() == 1]

# Función que guarda el estado de los checkboxes
def guardar_selecciones(checkboxes):
    global estado_selecciones
    for pluvio, var in checkboxes.items():
        estado_selecciones[pluvio] = var.get()  # Guardamos el estado de cada checkbox
        
def actualizar_checkboxes(self):
    # Iterar sobre las checkboxes
    global checkboxes
    for checkbox, id_value in self.checkboxes.items():
        if id_value in self.estado_seleccionado:  # Si el valor está en el estado seleccionado
            checkbox.setChecked(True)  # Marcar la checkbox
        else:
            checkbox.setChecked(False)  # Desmarcar la checkbox
    
# Función que se ejecuta cuando el usuario selecciona un archivo
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if archivo:
        archivo_text.delete(0, END)  # Borrar texto previo
        archivo_text.insert(0, archivo)  # Rellenar con la ruta seleccionada
        global archivo_seleccionado
        archivo_seleccionado = archivo  # Guardar la ruta seleccionada en una variable global
        habilitar_boton_comenzar()  # Habilitar el botón "Comenzar" si se ha seleccionado un archivo

# Función para habilitar el botón "Comenzar" si hay una ruta seleccionada
def habilitar_boton_comenzar(event=None):
    if archivo_text.get() and analisis_seleccionado.get() != "":  # Si hay texto en el campo de archivo (es decir, si se ha seleccionado un archivo)
        comenzar_btn.config(state=NORMAL)  # Activar el botón "Comenzar"
    else:
        comenzar_btn.config(state=DISABLED)  # De lo contrario, desactivar el botón "Comenzar"

# Función para regresar a la ventana de inicio desde la ventana principal
def regresar_inicio(root):
    global checkboxes
    checkboxes = {}  # Limpiar los checkboxes
    estado_selecciones.clear()  # Limpiar el diccionario de selecciones
    root.destroy()  # Cierra la ventana actual
    ventana_inicio()  # Vuelve a crear la ventana de inicio
    
# Función para crear la ventana de inicio
def ventana_inicio():
    global archivo_seleccionado
    inicio = tk.Tk()

    # Centrar la ventana
    screen_width = inicio.winfo_screenwidth()
    screen_height = inicio.winfo_screenheight()
    window_width = 500  # Ancho de la ventana
    window_height = 200  # Alto de la ventana
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)
    
    inicio.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
    inicio.title("Ventana de Inicio")

    # Etiqueta para seleccionar archivo
    archivo_label = tk.Label(inicio, text="Seleccionar archivo CSV: ", font=("Arial", 10, "bold"))
    archivo_label.pack(pady=5)

    # Crear un frame para la selección de archivo
    archivo_frame = tk.Frame(inicio)
    archivo_frame.pack(pady=5)

    # Caja de texto para mostrar la ruta del archivo
    global archivo_text
    archivo_text = tk.Entry(archivo_frame, font=("Arial", 12), width=40)
    archivo_text.pack(side=LEFT, padx=5)

    # Si ya se ha seleccionado un archivo previamente, restauramos la ruta
    if archivo_seleccionado:
        archivo_text.insert(0, archivo_seleccionado)
    
    # Botón para seleccionar el archivo
    archivo_btn = tk.Button(archivo_frame, text=" ... ", command=seleccionar_archivo, font=("Arial", 8, "bold"))
    archivo_btn.pack(side=LEFT)
    
    global analisis_seleccionado
    tk.Label(inicio, text="Seleccionar Tipo de análisis", font=("Arial", 8, "bold")).pack(pady=5)
    analisis_seleccionado = ttk.Combobox(inicio, values=["Tormenta", "Mensual"])
    analisis_seleccionado.pack(pady=5)
    analisis_seleccionado.set("")
    
    # Llamar a la función cada vez que se seleccione algo en la combobox
    analisis_seleccionado.bind("<<ComboboxSelected>>", habilitar_boton_comenzar)
        
    
    # Botón para comenzar
    global comenzar_btn
    comenzar_btn = tk.Button(inicio, text="Siguiente", command=lambda: [inicio.destroy(), iniciar_ventana_limite_temporal(archivo_seleccionado)], font=("Arial", 12, "bold"), state=DISABLED)
    comenzar_btn.pack(pady=5)
    
    # Vincular la función al perder el foco en la caja de texto del archivo
    archivo_text.bind("<FocusOut>", habilitar_boton_comenzar)

    # Verificar si hay archivo seleccionado para habilitar el botón al inicio
    habilitar_boton_comenzar()

    # Captura del evento de cierre global
    inicio.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(inicio))
    
    inicio.mainloop()

def iniciar_ventana_limite_temporal(archivo_seleccionado):
    global df_datos
    df_datos = leer_archivo(archivo_seleccionado)
    
    return ventana_limite_temporal()

def ventana_limite_temporal():
    # Grafico lo instantaneo y pregunto el inicio y el fin temporal, se pueden aplicar los cambios en la grafica y con el boton siguiente se hacen efectivos, antes no
    ventana_grafica_limite_temp = tk.Tk()
    
    ventana_grafica_limite_temp.state('zoomed')
    ventana_grafica_limite_temp.title("Ventana limite temporal")
    
    global df_datos
    
    pluvio_validos, pluvio_no_validos = obtener_pluviometros_validos(df_datos)
    df_lluvia_instantanea = calcular_instantaneos(df_datos)
    
    lluvia_filtrada = df_lluvia_instantanea[pluvio_validos]
    
    # Frame para gráfica
    frame_grafica = tk.Frame(ventana_grafica_limite_temp)
    frame_grafica.pack(side="top", expand=True, fill="both", padx=10)

    # Canvas para la gráfica
    canvas = tk.Canvas(frame_grafica)
    canvas.pack(fill="both", expand=True)
    def actualizar_grafica(lluvia_filtrada, limite_inf, limite_sup):
        lluvia_limitada_temp = limitar_df_temporal(lluvia_filtrada, limite_inf, limite_sup)
        fig = graficar_lluvia_instantanea(lluvia_limitada_temp)
        
        for widget in frame_grafica.winfo_children():
            widget.destroy()
            
        canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
           
    # Frame establecer limites
    frame_limites = tk.Frame(ventana_grafica_limite_temp)
    frame_limites.pack(side="bottom", fill="y", padx=10, pady=10)
    
    # Botón para regresar a la ventana de inicio
    reiniciar_btn = tk.Button(frame_limites, text="Reiniciar", command=lambda: regresar_inicio(ventana_grafica_limite_temp), font=("Arial", 10, "bold"))
    reiniciar_btn.pack(side="left",pady=10, padx=10)
    
    # Crear la etiqueta
    tk.Label(frame_limites, text="Seleccionar Limites:").pack(side="left", pady=10)
    # Crear el Entry para que el usuario ingrese el valor
    limite_inf_selector = tk.Entry(frame_limites)
    limite_inf_selector.pack(side="left", pady=10, padx=10)   
    limite_inf_selector.insert(0, df_datos.index.min())  # Establece el primer valor 
    
    # Crear el Entry para que el usuario ingrese el valor
    limite_sup_selector = tk.Entry(frame_limites)
    limite_sup_selector.pack(side="left",pady=10, padx=10)   
    limite_sup_selector.insert(0, df_datos.index.max())  # Establece el primer valor 
    
    actualizar_grafica(lluvia_filtrada, limite_inf_selector.get(), limite_sup_selector.get())
    
    # Botón de actualización de gráfica
    boton_aplicar = tk.Button(frame_limites, text="Aplicar", command=lambda: actualizar_grafica(lluvia_filtrada, limite_inf_selector.get(), limite_sup_selector.get()), font=("Arial", 10, "bold"))
    boton_aplicar.pack(side="left",pady=10, padx=10)
    
    def actualizar_df_datos(limite_inf, limite_sup):
        global df_datos
        df_datos = limitar_df_temporal(df_datos, limite_inf, limite_sup)
    
    # Botón de actualización de gráfica
    boton_siguiente = tk.Button(frame_limites, text="Siguiente", command=lambda: [actualizar_df_datos(limite_inf_selector.get(), limite_sup_selector.get()), ventana_grafica_limite_temp.destroy(), iniciar_ventana_principal()], font=("Arial", 10, "bold"))
    boton_siguiente.pack(side="left",pady=10, padx=10)
    
    # Captura del evento de cierre global
    ventana_grafica_limite_temp.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(ventana_grafica_limite_temp))
        
    ventana_grafica_limite_temp.mainloop()
    
    
def iniciar_ventana_principal():
    global df_datos
    global checkboxes
    global df_datos
    checkboxes = {}
    
    pluvio_validos, pluvio_no_validos = obtener_pluviometros_validos(df_datos)

    global estado_selecciones
    # Solo inicializamos si no hay datos previos
    if not estado_selecciones:
        estado_selecciones = {pluvio: 1 for pluvio in pluvio_validos}
    ventana_principal()
    
# Función para mostrar la gráfica de lluvia instantánea
def mostrar_grafica_instantanea(lluvia_instantanea):
    seleccionados = obtener_seleccionados()
    if not seleccionados:
        messagebox.showwarning("Advertencia", "Seleccione al menos un pluviómetro.")
        return

    lluvia_filtrada = lluvia_instantanea[seleccionados]

    ventana_grafica_inst = tk.Toplevel()
    ventana_grafica_inst.state('zoomed')
    ventana_grafica_inst.title("Gráfico de Lluvia Instantánea")

    fig = graficar_lluvia_instantanea(lluvia_filtrada)
    canvas = FigureCanvasTkAgg(fig, master=ventana_grafica_inst)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    volver_btn = Button(ventana_grafica_inst, text="Regresar", command=ventana_grafica_inst.destroy, font=("Arial", 10, "bold"))
    volver_btn.pack(pady=10)

# Función para mostrar la gráfica de lluvia acumulada
def mostrar_grafica_acumulada(lluvia_acumulada):
    seleccionados = obtener_seleccionados()
    if not seleccionados:
        messagebox.showwarning("Advertencia", "Seleccione al menos un pluviómetro.")
        return

    lluvia_filtrada = lluvia_acumulada[seleccionados]

    ventana_grafica_acum = tk.Toplevel()
    ventana_grafica_acum.state('zoomed')
    ventana_grafica_acum.title("Gráfico de Lluvia Acumulada")

    fig = graficar_lluvia_acumulado(lluvia_filtrada)
    canvas = FigureCanvasTkAgg(fig, master=ventana_grafica_acum)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    volver_btn = Button(ventana_grafica_acum, text="Regresar", command=ventana_grafica_acum.destroy, font=("Arial", 10, "bold"))
    volver_btn.pack(pady=10)
    
# Función para mostrar interfaz de selección y gráficas
def mostrar_interfaz_tr(lluvia_instantanea):
    seleccionados = obtener_seleccionados()
    
    if not seleccionados:
        messagebox.showwarning("Advertencia", "Seleccione al menos un pluviómetro.")
        return
    
    lluvia_filtrada = lluvia_instantanea[seleccionados]

    # Crear la ventana principal
    ventana_tr = tk.Toplevel()
    ventana_tr.state('zoomed')
    ventana_tr.title("Precipitación vs. Duración de Tormenta")
    
    # Frame izquierdo para selección
    frame_izq = tk.Frame(ventana_tr)
    frame_izq.pack(side="left", fill="y", padx=10, pady=10)

    # Frame izquierdo para selección
    frame_bottom = tk.Frame(ventana_tr)
    frame_bottom.pack(side="bottom", fill="y", padx=10, pady=10)
    
    # Checkboxes para TRs
    lista_tr = [tk.IntVar(value=v) for v in [1, 1, 1, 1, 0, 1, 0]]
    tr_labels = ["TR 2 años", "TR 5 años", "TR 10 años", "TR 20 años", "TR 25 años", "TR 50 años", "TR 100 años"]
    tk.Label(frame_izq, text="Seleccionar TRs", font="bold").pack(pady=10, padx=10)
    for i, tr in enumerate(tr_labels):
        tk.Checkbutton(frame_izq, text=tr, variable=lista_tr[i]).pack(anchor="w")
        
    tk.Label(frame_izq, text=" ", font="bold").pack()

    # Frame derecho para gráfica
    frame_graficas = tk.Frame(ventana_tr)
    frame_graficas.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    # Canvas para la gráfica
    canvas = tk.Canvas(frame_graficas)
    canvas.pack(fill="both", expand=True)
    
    # Crear la etiqueta
    tk.Label(frame_izq, text="Seleccionar Limites", font="bold").pack(pady=5)
    
    # Crear la etiqueta
    tk.Label(frame_izq, text="Precipitacion de al Grafica:").pack(pady=5)
    # Crear el Entry para que el usuario ingrese el valor
    limite_precipitacion_selector = tk.Entry(frame_izq)
    limite_precipitacion_selector.pack(pady=5)   
    # Establecer un valor predeterminado (si lo deseas)
    limite_precipitacion_selector.insert(0, 150)  # Establece el primer valor 
    
    tk.Label(frame_izq, text="Tiempo de la Grafica:").pack(pady=5)
    # Crear el Entry para que el usuario ingrese el valor
    limite_tiempo_selector = tk.Entry(frame_izq)
    limite_tiempo_selector.pack(pady=5)   
    # Establecer un valor predeterminado (si lo deseas)
    limite_tiempo_selector.insert(0, 1480)  # Establece el primer valor
    
    
    tk.Label(frame_izq, text="Precipitacion de la Grafica Ampliada:").pack(pady=5)
    # Crear el Entry para que el usuario ingrese el valor
    limite_precipitacion_selector_ampliada = tk.Entry(frame_izq)
    limite_precipitacion_selector_ampliada.pack(pady=5)   
    # Establecer un valor predeterminado (si lo deseas)
    limite_precipitacion_selector_ampliada.insert(0, 80)  # Establece el primer valor 
    
    tk.Label(frame_izq, text="Tiempo de la Grafica Ampliada:").pack(pady=5)
    # Crear el Entry para que el usuario ingrese el valor
    limite_tiempo_selector_ampliada = tk.Entry(frame_izq)
    limite_tiempo_selector_ampliada.pack(pady=5)   
    # Establecer un valor predeterminado (si lo deseas)
    limite_tiempo_selector_ampliada.insert(0, 120)  # Establece el primer valor
    
    
    tk.Label(frame_izq, text="Seleccionar Pluviómetro").pack(pady=5)
    pluv_selector = ttk.Combobox(frame_izq, values=list(lluvia_filtrada.columns))
    pluv_selector.pack(pady=5)
    pluv_selector.set(lluvia_filtrada.columns[0])

    # Variable para rastrear el tipo de gráfica mostrada
    ultima_grafica = "ninguna"  # Puede ser "pluviómetro" o "total"
    
    # Función para actualizar gráfica
    def graficar_pluv():
        global ultima_grafica
        
        pluvio = pluv_selector.get()
        precipitaciones = calcular_precipitacion_pluvio(lluvia_filtrada, pluvio)
        fig = grafica_tr([var.get() for var in lista_tr], precipitaciones, float(limite_precipitacion_selector.get()), float(limite_tiempo_selector.get()), pluvio, "Precipitación vs. Duración de Tormenta")
        fig_ampliada  = grafica_tr([var.get() for var in lista_tr], precipitaciones, float(limite_precipitacion_selector_ampliada.get()), float(limite_tiempo_selector_ampliada.get()), pluvio, "Grafica ampliada")

        for widget in frame_graficas.winfo_children():
            widget.destroy()

        canvas1 = FigureCanvasTkAgg(fig, master=frame_graficas)
        canvas1.get_tk_widget().pack(fill="both", expand=True)
        canvas1.draw()
        
        canvas2 = FigureCanvasTkAgg(fig_ampliada, master=frame_graficas)
        canvas2.get_tk_widget().pack(fill="both", expand=True)
        canvas2.draw()
        
        # Actualizamos la variable de estado
        ultima_grafica = "pluviómetro"

    tk.Label(frame_izq, text=" ", font="bold").pack()
    # Botón de actualización de gráfica
    tk.Button(frame_izq, text="Graficar pluviometro", command=graficar_pluv, font=("Arial", 10, "bold")).pack(pady=10)

    # Botón para mostrar todos los pluviómetros
    def graficar_todos():
        global ultima_grafica
        
        precipitaciones = calcular_precipitacion_para_tr(lluvia_filtrada)
        fig = grafica_tr([var.get() for var in lista_tr], precipitaciones, float(limite_precipitacion_selector.get()), float(limite_tiempo_selector.get()), "RHM", "Precipitación vs. Duración de Tormenta")
        fig_ampliada  = grafica_tr([var.get() for var in lista_tr], precipitaciones, float(limite_precipitacion_selector_ampliada.get()), float(limite_tiempo_selector_ampliada.get()), "RHM", "Grafica ampliada")

        for widget in frame_graficas.winfo_children():
            widget.destroy()

        canvas1 = FigureCanvasTkAgg(fig, master=frame_graficas)
        canvas1.get_tk_widget().pack(fill="both", expand=True)
        canvas1.draw()
        
        canvas2 = FigureCanvasTkAgg(fig_ampliada, master=frame_graficas)
        canvas2.get_tk_widget().pack(fill="both", expand=True)
        canvas2.draw()
        # Actualizamos la variable de estado
        ultima_grafica = "total"

    graficar_todos()
    
    def guardar_graficas():
        # Cuadro de diálogo para seleccionar directorio y nombre del archivo
        directorio = filedialog.askdirectory(title="Selecciona un directorio para guardar las gráficas")
        ventana_tr.lift()
        
        if directorio:
            # Determinar el nombre del archivo dependiendo del tipo de gráfica mostrada
            if ultima_grafica == "pluviómetro":
                pluvio = pluv_selector.get()
                nombre_archivo = f"grafica_{pluvio}.png"
                nombre_archivo_ampliada = f"grafica_ampliada_{pluvio}.png"
                precipitaciones = calcular_precipitacion_pluvio(lluvia_filtrada, pluvio)
                fig = grafica_tr([var.get() for var in lista_tr], precipitaciones, 
                                float(limite_precipitacion_selector.get()), float(limite_tiempo_selector.get()), pluvio, "Precipitación vs. Duración de Tormenta")
                fig_ampliada = grafica_tr([var.get() for var in lista_tr], precipitaciones, 
                                      float(limite_precipitacion_selector_ampliada.get()), float(limite_tiempo_selector_ampliada.get()), pluvio, "Grafica ampliada")
            else:
                nombre_archivo = "grafica_total.png"
                nombre_archivo_ampliada = "grafica_ampliada_total.png"
                precipitaciones = calcular_precipitacion_para_tr(lluvia_filtrada)
                fig = grafica_tr([var.get() for var in lista_tr], precipitaciones, float(limite_precipitacion_selector.get()), float(limite_tiempo_selector.get()), "RHM", "Precipitación vs. Duración de Tormenta")
                fig_ampliada  = grafica_tr([var.get() for var in lista_tr], precipitaciones, float(limite_precipitacion_selector_ampliada.get()), float(limite_tiempo_selector_ampliada.get()), "RHM", "Grafica ampliada")

            # Guardar la primera gráfica
            fig.savefig(f"{directorio}/{nombre_archivo}")

            # Guardar la gráfica ampliada
            
            fig_ampliada.savefig(f"{directorio}/{nombre_archivo_ampliada}")
            
            messagebox.showinfo("Éxito", "Las gráficas se han guardado correctamente.")
            ventana_tr.lift()
    
    tk.Button(frame_izq, text="Graficar Todos", command=graficar_todos, font=("Arial", 10, "bold")).pack(pady=5)
    
    # Botón para regresar (cerrar la ventana de gráfica)
    tk.Button(frame_bottom, text="Regresar",command= lambda: ventana_tr.destroy(), font=("Arial", 10, "bold")).pack(side="left", padx=20)
    
    # Botón para regresar (cerrar la ventana de gráfica)
    tk.Button(frame_bottom, text="Guardar graficas", command=guardar_graficas, font=("Arial", 10, "bold")).pack(side="left", pady=10)

    ventana_tr.mainloop()
 
# Función que se ejecuta cuando el usuario da click en "Procesar"
def guardar_graficas(lluvia_acumulada, lluvia_instantanea):
    seleccionados = obtener_seleccionados()
        
    if not seleccionados:
        messagebox.showwarning("Advertencia", "Seleccione al menos un pluviómetro.")
        return

    # Aquí puedes llamar a la función que procesa los pluviómetros seleccionados
    # por ejemplo: guardar las graficas y esas manos
    lluvia_filtrada_inst = lluvia_instantanea[seleccionados]
    
    # Cuadro de diálogo para seleccionar directorio y nombre del archivo
    directorio = filedialog.askdirectory(title="Selecciona un directorio para guardar las gráficas")
        
    fig_inst = graficar_lluvia_instantanea(lluvia_filtrada_inst)
    fig_inst.savefig(f"{directorio}/grafica instantaneas.png")
    
    lluvia_filtrada_acum = lluvia_acumulada[seleccionados]
    
    fig_acum = graficar_lluvia_acumulado(lluvia_filtrada_acum)
    # Guardar la primera gráfica
    fig_acum.savefig(f"{directorio}/grafica acumulado.png")
    
    messagebox.showinfo("Exito", "Procesado correctamente.")

# Función para crear la ventana interfaz principal
def ventana_principal():
    global checkboxes
    global estado_selecciones
    global df_datos
    
    principal = tk.Tk()
    
    principal.state('zoomed')
    principal.title("Ventana principal")
    
    # Obtener pluviómetros válidos
    pluvio_validos, pluvio_no_validos = obtener_pluviometros_validos(df_datos)
        
    df_acumulados = acumulado(df_datos)
    
    df_instantaneos = calcular_instantaneos(df_datos)
    
    df_saltos = detectar_saltos_temporales(df_datos[pluvio_validos])

    df_porcentaje_vacio = calcular_porcentaje_vacios(df_datos[pluvio_validos])
    
    # Parte superior: Información 
    info_frame = Frame(principal)
    info_frame.pack(side="top", fill="both", padx=20, pady=20)

    # Mostrar la información en el frame izquierdo
    info_label = tk.Label(info_frame, text="Información sobre los datos de precipitación:", font=("Arial", 16, "bold"))
    info_label.pack(fill="both", padx=10, pady=10)

    # Mostrar pluviómetros no válidos
    # Crear la etiqueta
    tk.Label(info_frame, text="Pluviómetros no válidos", font=("Arial", 14, "bold")).pack(pady=15)
    
    pluvios_no_validos_label = tk.Label(info_frame, text=f"{', '.join(pluvio_no_validos)}", font=("Arial", 12), justify="left")
    pluvios_no_validos_label.pack(fill="both", padx=10, pady=5)
    
    # Crear la etiqueta
    tk.Label(info_frame, text="Saltos temporales", font=("Arial", 14, "bold")).pack(pady=15)

    # Crear un Frame para contener la tabla y la barra de desplazamiento
    frame_tabla = tk.Frame(info_frame)
    frame_tabla.pack(fill="both", expand=True)

    # Crear un Treeview con columnas para los saltos
    tabla = ttk.Treeview(frame_tabla, columns=("Pluviómetro", "Cantidad de saltos", "Duración total (min)", "Duración máx (min)", "Inicio máx", "Fin máx"), show="headings")

    # Definir los encabezados
    tabla.heading("Pluviómetro", text="Pluviómetro")
    tabla.heading("Cantidad de saltos", text="Cantidad de saltos")
    tabla.heading("Duración total (min)", text="Duración total (min)")
    tabla.heading("Duración máx (min)", text="Duración máx (min)")
    tabla.heading("Inicio máx", text="Inicio máximo")
    tabla.heading("Fin máx", text="Fin máximo")

    # Configurar las columnas para que se ajusten y centrar el texto
    tabla.column("Pluviómetro", width=150, anchor="center")
    tabla.column("Cantidad de saltos", width=100, anchor="center")
    tabla.column("Duración total (min)", width=150, anchor="center")
    tabla.column("Duración máx (min)", width=150, anchor="center")
    tabla.column("Inicio máx", width=150, anchor="center")
    tabla.column("Fin máx", width=150, anchor="center")

    # Crear una barra de desplazamiento vertical para la tabla
    scrollbar = tk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    scrollbar.pack(side="right", fill="y")
    tabla.configure(yscrollcommand=scrollbar.set)

    # Inicializar la lista para almacenar los datos
    data = []

    # Verificar si df_saltos no está vacío
    if not df_saltos.empty:
        # Extraer los datos del DataFrame
        for index, row in df_saltos.iterrows():
            data.append((row["Pluviómetro"], row["Cantidad de saltos"], row["Duración total (min)"], row["Duración máx (min)"], row["Inicio máx"], row["Fin máx"]))

        # Ordenar los datos por "Duración total (min)" de mayor a menor
        data.sort(key=lambda x: x[2], reverse=True)  # x[2] es la "Duración total (min)"

        # Insertar los datos ordenados en la tabla
        for row in data:
            tabla.insert("", "end", values=row)
    else:
        tabla.insert("", "end", values=("No se detectaron saltos temporales", "", "", "", "", ""))

    # Empaquetar la tabla
    tabla.pack(fill="both", expand=True)
    
    # Crear la etiqueta para la segunda tabla (Porcentaje de nulos)
    tk.Label(info_frame, text="Porcentaje de nulos por pluviómetro", font=("Arial", 14, "bold")).pack()
    
    # Crear un Treeview con columnas para el porcentaje de nulos
    tabla_nulos = ttk.Treeview(frame_tabla, columns=("Pluviómetro", "Porcentaje_Nulos"), show="headings")

    # Definir los encabezados de la segunda tabla
    tabla_nulos.heading("Pluviómetro", text="Pluviómetro")
    tabla_nulos.heading("Porcentaje_Nulos", text="Porcentaje Nulos (%)")

    # Configurar las columnas para que se ajusten y centrar el texto
    tabla_nulos.column("Pluviómetro", width=150, anchor="center")
    tabla_nulos.column("Porcentaje_Nulos", width=150, anchor="center")

    # Crear una barra de desplazamiento vertical para la tabla de nulos
    scrollbar_nulos = tk.Scrollbar(frame_tabla, orient="vertical", command=tabla_nulos.yview)
    scrollbar_nulos.pack(side="right", fill="y")
    tabla_nulos.configure(yscrollcommand=scrollbar_nulos.set)

    # Ordenar los datos por porcentaje de nulos de mayor a menor
    df_porcentaje_vacio = df_porcentaje_vacio.sort_values(by="Porcentaje_Nulos", ascending=False)

    # Insertar los datos ordenados en la tabla de porcentaje de nulos
    for index, row in df_porcentaje_vacio.iterrows():
        tabla_nulos.insert("", "end", values=(row["Pluviómetro"], round(row["Porcentaje_Nulos"], 2)))

    # Empaquetar la tabla de porcentaje de nulos
    tabla_nulos.pack(fill="both", expand=True, pady=5)
    

    check_frame = Frame(principal)
    check_frame.pack()
    
    # Crear un checkbox por cada pluviómetro válido en formato de cuadrícula
    row, col = 0, 0
    for pluvio in pluvio_validos:
        estado = estado_selecciones.get(pluvio, 1)
        var = tk.IntVar(value=estado)
        checkboxes[pluvio] = var
        checkbutton = tk.Checkbutton(check_frame, text=pluvio, variable=var, font=("Arial", 10, "bold"),
                                     command=lambda: actualizar_seleccion(pluvio, var.get()))
        checkbutton.grid(row=row, column=col, padx=10, pady=10, sticky="w")

        col += 1
        if col > 6:
            col = 0
            row += 1
    
    # Parte inferior: Botones
    botonera_frame = Frame(principal)
    botonera_frame.pack(side="bottom", fill="y", padx=10, pady=10)
    
    # Botón para regresar a la ventana de inicio
    volver_btn = tk.Button(botonera_frame, text="Volver", command=lambda: [principal.destroy(), ventana_limite_temporal()], font=("Arial", 10, "bold"))
    volver_btn.pack(side="left", padx=10, pady=10)

    # Botón para mostrar la gráfica de lluvia instantánea
    grafica_instantanea_btn = Button(botonera_frame, text="Ver Gráfico Lluvia Instantánea", 
                                     command=lambda: mostrar_grafica_instantanea(df_instantaneos),
                                     font=("Arial", 10, "bold"))
    grafica_instantanea_btn.pack(side="left", padx=10, pady=10)

    # Botón para mostrar la gráfica de lluvia acumulada
    grafica_acumulada_btn = Button(botonera_frame, text="Ver Gráfico Lluvia Acumulada", 
                                   command=lambda: mostrar_grafica_acumulada(df_acumulados),
                                   font=("Arial", 10, "bold"))
    grafica_acumulada_btn.pack(side="left", padx=10, pady=10)
    
    # Botón para mostrar la interfaz de tr
    grafica_tr_btn = Button(botonera_frame, text="Ver Gráfico Tr", 
                                   command=lambda: mostrar_interfaz_tr(df_instantaneos),
                                   font=("Arial", 10, "bold"))
    grafica_tr_btn.pack(side="left", padx=10, pady=10)

    # Botón para procesar selección
    procesar_btn = tk.Button(botonera_frame, text="Guardar Graficas", command=lambda: guardar_graficas(df_acumulados, df_instantaneos), font=("Arial", 10, "bold"))
    procesar_btn.pack(side="left", padx=10, pady=10)
    
    # Captura del evento de cierre global
    principal.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(principal))

    principal.mainloop()


# Crear la ventana inicial (ventana de inicio)
# Llamada inicial a la ventana
if __name__ == "__main__":
    ventana_inicio()
