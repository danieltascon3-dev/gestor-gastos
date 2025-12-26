import json
import tkinter as tk
from tkinter import messagebox
import datetime

ventana = tk.Tk()
ventana.geometry("800x600")
ventana.title()

mostrar_lista = []
contador = 0

def cargar_gastos():
    global contador,mostrar_lista
    try:
        with open('gastos.json', 'r') as archivo:
            resultado = json.load(archivo)
            contador = resultado['total']
            etiqueta_total.config(text=contador)
            mostrar_lista = resultado['gastos']
            mostrar.delete(0, tk.END)
            for gastos in mostrar_lista:
                mostrar.insert(tk.END,gastos)

    except PermissionError:
        messagebox.showerror("error", "error de permiso")
    except FileNotFoundError:
        messagebox.showerror("error", "Archivo no encontrado")
    except Exception:
        messagebox.showerror("error", "error inesperado")
    else:
        messagebox.showinfo("exito", "se cargo con exito")

def guardar_gastos():
    global mostrar_lista, contador
    diccionario = {'gastos': mostrar_lista,
                   'total': contador}
    try:
        with open('gastos.json', 'w') as archivo:
            json.dump(diccionario, archivo)
    except PermissionError:
        messagebox.showerror("error", "error de permiso")
    except FileNotFoundError:
        messagebox.showerror("error", "Archivo no encontrado")
    except Exception:
        messagebox.showerror("error", "error inesperado")
    else:
        messagebox.showinfo("exito", "se guardo con exito")


def agregar(categoria):
    global mostrar_lista, contador

    try:
        desc = descripicion.get()
        mont = int(monto.get())
        fecha = datetime.datetime.now().strftime("%Y - %m - %d %H:%M")
        if not desc.strip():
            messagebox.showwarning("error","no puede estar en blanco")
            return
        if mont <= 0:
            messagebox.showwarning("error","no puedes poner un monto negativo")
            return
        mostrar_lista.append(f"categoria {categoria} descripcion {desc} monto {mont} fecha {fecha}")
        texto_mostrar = f"{categoria}: {desc} - ${mont} {fecha}"
        mostrar.insert(tk.END, texto_mostrar)
        monto.delete(0, tk.END)
        descripicion.delete(0, tk.END)
        contador += mont
        etiqueta_total.config(text=contador)
    except ValueError:
        messagebox.showwarning("advertencia", "tienes que rellenar los campos")


def limpiar():
    global contador
    mostrar.delete(0, tk.END)
    mostrar_lista.clear()
    contador = 0
    etiqueta_total.config(text=contador)


def cerrar():
    close = messagebox.askyesno("cerrar", "¿esta seguro que quiere cerrar?")
    if close:
        ventana.destroy()


mostrar = tk.Listbox(ventana, width=100)
mostrar.pack()

etiqueta_descripcion = tk.Label(ventana, text="descripcion")
etiqueta_descripcion.pack()
descripicion = tk.Entry()
descripicion.pack()
etiqueta_monto = tk.Label(ventana, text="monto")
etiqueta_monto.pack()
monto = tk.Entry()
monto.pack()

boton_categoria_transoporte = tk.Button(ventana, text='transporte', command=lambda: agregar("trasporte"))
boton_categoria_transoporte.pack()

boton_categoria_comida = tk.Button(ventana, text='comida', command=lambda: agregar("comida"))
boton_categoria_comida.pack()

boton_categoria_entretenimiento = tk.Button(ventana, text='entretenimiento', command=lambda: agregar("entretenimiento"))
boton_categoria_entretenimiento.pack()

etiqueta_total = tk.Label(ventana, text='')
etiqueta_total.pack()

boton_cargar = tk.Button(ventana,text="cargar",command=cargar_gastos)
boton_cargar.pack()

boton_guardar = tk.Button(ventana,text="guardar",command=guardar_gastos)
boton_guardar.pack()
boton_limpiar = tk.Button(ventana, text='Limpiar', command=limpiar)
boton_limpiar.pack()

boton_cerrar = tk.Button(ventana, text="Cerrar", command=cerrar)
boton_cerrar.pack()


ventana.mainloop()
