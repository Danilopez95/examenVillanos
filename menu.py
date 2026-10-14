"""Menú de consola de la aplicación."""

import logging
from gestion import Gestion
from models import Jugador, CuerpoTecnico

logger = logging.getLogger(__name__)


class Menu:
    def __init__(self, gestion: Gestion):
        self.gestion = gestion

    def agregar_miembro(self):
        print("\n=== AGREGAR MIEMBRO ===")
        print("1. Jugador")
        print("2. Cuerpo técnico")

        opcion = input("¿Qué tipo de miembro quieres agregar?: ")

        if opcion == "1":
            tipo = "jugador"
            dato = "Posición"

        elif opcion == "2":
            tipo = "tecnico"
            dato = "Rol"

        else:
            print("Opción no válida.")
            return

        nombre = input("Nombre: ")
        apellidos = input("Apellidos: ")
        valor = input(f"{dato}: ")

        miembro = self.gestion.agregar_miembro(tipo, nombre, apellidos, valor)

        print(f"Miembro agregado correctamente con ID: {miembro.identificador}")



    def mostrar(self) -> None:
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Héroes y Villanos")
            print("2. Plantillas de Fútbol")
            print("0. Salir")

            opcion = input("Elige una opción: ")

            if opcion == "1":
                self.mostrar_menu_heroes()

            elif opcion == "2":
                while True:
                        print("\n=== PLANTILLAS DE FÚTBOL ===")
                        print("1. Agregar miembro")
                        print("2. Listar plantilla")
                        print("3. Crear plantilla")
                        print("4. Salir")

                        opcion = input("Elige una opción: ")

                        if opcion == "1":
                            self.agregar_miembro()

                        elif opcion == "2":
                            self.listar_plantilla()

                        elif opcion == "3":
                            self.gestion.generar_plantilla()

                        elif opcion == "4":
                            return

                        else:
                            print("Opción no válida.")


            elif opcion == "0":
                print("Hasta luego.")
                return

            else:
                print("Opción no válida.")

    def mostrar_menu_heroes(self) -> None:

        while True:

            print("\n=== HÉROES Y VILLANOS DEL VIRGEN ===")
            print("1. Crear héroe")
            print("2. Crear villano")
            print("3. Listar personajes")
            print("4. Buscar por atributo")
            print("5. Emparejar héroe y villano")
            print("6. Eliminar personaje")
            print("0. Salir")

            try:
                opcion = input("Elige una opción: ").strip()
                if opcion == "1":
                    self._crear("heroe")
                elif opcion == "2":
                    self._crear("villano")
                elif opcion == "3":
                    self._listar()
                elif opcion == "4":
                    self._buscar()
                elif opcion == "5":
                    self._emparejar()
                elif opcion == "6":
                    self._eliminar()
                elif opcion == "0":
                    logger.info("Aplicación cerrada por el usuario.")
                    print("Hasta luego.")
                    break
                else:
                    print("Opción no válida.")
                    logger.warning("Opción de menú no válida: %s", opcion)
            except (ValueError, TypeError) as exc:
                print(f"Error: {exc}")
                logger.warning("Entrada no válida: %s", exc)
            except (KeyboardInterrupt, EOFError):
                logger.info("Salida solicitada desde teclado.")
                print("\nAplicación finalizada.")
                break
            except Exception:
                logger.exception("Error no controlado en el menú.")
                print("Se ha producido un error. Consulta el archivo aplicacion.log.")

    def _crear(self, tipo: str) -> None:
        nombre = input("Nombre: ").strip()
        apellidos = input("Apellidos: ").strip()
        fecha = input("Fecha de nacimiento (AAAA-MM-DD): ").strip()
        personaje = self.gestion.crear_personaje(tipo, nombre, apellidos, fecha)
        print(f"Personaje creado: {personaje}")

    def _listar(self) -> None:
        tipo = input("¿Qué quieres listar? (heroe/villano/todos): ").strip()
        personajes = self.gestion.listar_personajes(tipo)
        if not personajes:
            print("No hay personajes para mostrar.")
            return
        for personaje in personajes:
            print(personaje)

    def _buscar(self) -> None:
        tipo = input("Tipo (heroe/villano): ").strip()
        print("Atributos: identificador, nombre, apellidos, fecha_nacimiento, edad,")
        print("          puntuacion_total y las cualidades propias de cada tipo.")
        atributo = input("Atributo: ").strip()
        operador = input("Operador (=, !=, >, >=, <, <=, contiene): ").strip()
        valor = input("Valor a buscar: ").strip()
        resultados = self.gestion.buscar_por_atributo(tipo, atributo, operador, valor)
        if not resultados:
            print("No se han encontrado coincidencias.")
        else:
            for personaje in resultados:
                print(personaje)

    def _emparejar(self) -> None:
        heroe, villano, diferencia, valoracion = self.gestion.emparejar_aleatoriamente()
        print(f"Héroe: {heroe}")
        print(f"Villano: {villano}")
        print(f"Diferencia de puntuación: {diferencia}")
        print(valoracion)

    def _eliminar(self) -> None:
        tipo = input("Tipo (heroe/villano): ").strip()
        identificador = int(input("Identificador: "))
        if self.gestion.eliminar_personaje(tipo, identificador):
            print("Personaje eliminado.")
        else:
            print("No existe un personaje con ese identificador.")

    def listar_plantilla(self):
        miembros = self.gestion.listar_plantilla()

        if not miembros:
            print("No hay miembros en la plantilla.")
            return

        print("\n========== PLANTILLA DE FÚTBOL ==========")

        for miembro in miembros:
            print(f"ID: {miembro.identificador}")
            print(f"Nombre: {miembro.nombre}")
            print(f"Apellidos: {miembro.apellidos}")

            if isinstance(miembro, Jugador):
                print("Tipo: Jugador")
                print(f"Posición: {miembro.posicion}")

            elif isinstance(miembro, CuerpoTecnico):
                print("Tipo: Cuerpo técnico")
                print(f"Rol: {miembro.rol}")

            print("-----------------------------------------")


