from database import Database

def main():
    db = Database()
    db.conectar()

    while True:
        print("\n--- MENÚ OBJETOS PERDIDOS ---")
        print("1. Agregar objeto")
        print("2. Listar objetos")
        print("3. Actualizar objeto")
        print("4. Eliminar objeto")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre del objeto: ")
            lugar = input("Lugar donde se encontró: ")
            descripcion = input("Descripción: ")
            db.crear_objeto(nombre, lugar, descripcion)
        elif opcion == "2":
            db.listar_objetos()
        elif opcion == "3":
            id = int(input("ID del objeto a actualizar: "))
            nuevo_nombre = input("Nuevo nombre: ")
            nuevo_lugar = input("Nuevo lugar: ")
            nueva_descripcion = input("Nueva descripción: ")
            db.actualizar_objeto(id, nuevo_nombre, nuevo_lugar, nueva_descripcion)
        elif opcion == "4":
            id = int(input("ID del objeto a eliminar: "))
            db.eliminar_objeto(id)
        elif opcion == "5":
            db.cerrar_conexion()
            print("👋 Saliendo del programa...")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    main()
