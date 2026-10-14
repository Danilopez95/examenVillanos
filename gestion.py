"""Operaciones de gestión de héroes y villanos."""

from datetime import date
import logging
import random
from typing import Dict, Optional, Type

from models import Heroe, Personaje, Villano, Miembro, Jugador, CuerpoTecnico
logger = logging.getLogger(__name__)


class Gestion:
    """Gestiona personajes y búsquedas usando diccionarios por identificador."""

    def __init__(self):
        self.heroes: Dict[int, Heroe] = {}
        self.villanos: Dict[int, Villano] = {}
        self._siguiente_id = 1

        self.plantilla = {}
        self._siguiente_id_miembro = 1

    def agregar_miembro(self,tipo,nombre,apellido,dato):
        identificador = self._siguiente_id_miembro
        if tipo.lower() == "jugador":
            miembro = Jugador(identificador, nombre, apellido, dato)
        elif tipo.lower() == "tecnico":
            miembro = CuerpoTecnico(identificador, nombre, apellido, dato)
        else:
            raise ValueError("Tipo de miembro no válido. Usa 'jugador' o 'tecnico'.")

        self.plantilla[identificador] = miembro
        self._siguiente_id_miembro += 1

        logger.info("Agregado %s id=%s nombre=%s %s", tipo, identificador, nombre, apellido)
        return miembro

    def listar_plantilla(self):
        try:
            miembros = list(self.plantilla.values())
            logger.info(
                "Listado de plantilla solicitado. Cantidad=%s",
                len(miembros)
            )
            return miembros

        except Exception:
            logger.exception("Error al listar la plantilla.")
            raise


    def _obtener_diccionario(self, tipo: str):
        tipo = tipo.strip().lower()
        if tipo in ("heroe", "héroe", "heroes", "héroes"):
            return self.heroes
        if tipo in ("villano", "villanos"):
            return self.villanos
        raise ValueError("Tipo no válido. Escribe 'heroe' o 'villano'.")

    @staticmethod
    def _leer_fecha(fecha_texto: str) -> date:
        try:
            return date.fromisoformat(fecha_texto.strip())
        except (ValueError, AttributeError) as exc:
            raise ValueError("Fecha no válida. Usa el formato AAAA-MM-DD.") from exc

    def crear_personaje(self, tipo: str, nombre: str, apellidos: str,
                        fecha_nacimiento: str) -> Personaje:
        """Crea un personaje y lo almacena en el diccionario correspondiente."""
        try:
            diccionario = self._obtener_diccionario(tipo)
            fecha = self._leer_fecha(fecha_nacimiento)
            identificador = self._siguiente_id
            clase: Type[Personaje] = Heroe if diccionario is self.heroes else Villano

            personaje = clase(identificador, nombre, apellidos, fecha)
            personaje.generar_cualidades()
            diccionario[identificador] = personaje
            self._siguiente_id += 1

            logger.info(
                "Creado %s id=%s nombre=%s %s",
                clase.__name__, identificador, nombre, apellidos
            )
            return personaje
        except (ValueError, TypeError):
            logger.exception("No se pudo crear el personaje.")
            raise
        except Exception:
            logger.exception("Error inesperado al crear un personaje.")
            raise

    def listar_personajes(self, tipo: Optional[str] = None) -> list:
        """Lista los personajes guardados."""
        try:
            if tipo is None or tipo.strip().lower() in ("todos", "todo"):
                personajes = list(self.heroes.values()) + list(self.villanos.values())
            else:
                personajes = list(self._obtener_diccionario(tipo).values())
            logger.info("Listado solicitado. Tipo=%s, cantidad=%s", tipo, len(personajes))
            return personajes
        except Exception:
            logger.exception("Error al listar personajes.")
            raise

    def buscar_por_atributo(self, tipo: str, atributo: str, operador: str,
                            valor_buscado: str) -> list:
        """
        Busca recorriendo el diccionario seleccionado.
        Operadores permitidos: =, !=, >, >=, <, <=, contiene.
        """
        try:
            diccionario = self._obtener_diccionario(tipo)
            atributo = atributo.strip().lower()
            operador = operador.strip().lower()
            resultados = []

            if operador not in ("=", "!=", ">", ">=", "<", "<=", "contiene"):
                raise ValueError("Operador no válido.")

            for personaje in diccionario.values():
                datos = personaje.obtener_datos()
                if atributo not in datos:
                    continue

                actual = datos[atributo]
                esperado = self._convertir_valor(valor_buscado, actual)

                coincide = {
                    "=": lambda: actual == esperado,
                    "!=": lambda: actual != esperado,
                    ">": lambda: actual > esperado,
                    ">=": lambda: actual >= esperado,
                    "<": lambda: actual < esperado,
                    "<=": lambda: actual <= esperado,
                    "contiene": lambda: str(esperado).lower() in str(actual).lower(),
                }[operador]()

                if coincide:
                    resultados.append(personaje)

            logger.info(
                "Búsqueda realizada: tipo=%s atributo=%s operador=%s resultados=%s",
                tipo, atributo, operador, len(resultados)
            )
            return resultados
        except Exception:
            logger.exception("Error durante la búsqueda.")
            raise

    @staticmethod
    def _convertir_valor(valor: str, actual):
        if isinstance(actual, bool):
            return valor.strip().lower() in ("true", "sí", "si", "1")
        if isinstance(actual, (int, float)):
            try:
                return type(actual)(valor)
            except ValueError as exc:
                raise ValueError("El valor de búsqueda debe ser numérico.") from exc
        return str(valor).strip()

    def emparejar_aleatoriamente(self) -> tuple:
        """Devuelve un héroe, un villano y una valoración del enfrentamiento."""
        try:
            if not self.heroes:
                raise ValueError("No hay héroes registrados.")
            if not self.villanos:
                raise ValueError("No hay villanos registrados.")

            heroe = random.choice(list(self.heroes.values()))
            villano = random.choice(list(self.villanos.values()))
            diferencia = abs(heroe.puntuacion_total - villano.puntuacion_total)

            if diferencia <= 10:
                valoracion = "Enfrentamiento equilibrado"
            elif diferencia >= 30:
                valoracion = "Alta desviación entre puntuaciones"
            else:
                valoracion = "Enfrentamiento con cierta diferencia"

            logger.info(
                "Emparejamiento: héroe=%s villano=%s diferencia=%s",
                heroe.identificador, villano.identificador, diferencia
            )
            return heroe, villano, diferencia, valoracion
        except Exception:
            logger.exception("Error al emparejar héroe y villano.")
            raise

    def eliminar_personaje(self, tipo: str, identificador: int) -> bool:
        """Elimina un personaje por su identificador."""
        try:
            diccionario = self._obtener_diccionario(tipo)
            if identificador not in diccionario:
                logger.warning("No existe personaje tipo=%s id=%s", tipo, identificador)
                return False
            del diccionario[identificador]
            logger.info("Eliminado personaje tipo=%s id=%s", tipo, identificador)
            return True
        except Exception:
            logger.exception("Error al eliminar personaje.")
            raise

