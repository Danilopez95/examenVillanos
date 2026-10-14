"""Modelos de datos para la aplicación Héroes y Villanos."""

from abc import ABC, abstractmethod
from datetime import date
import logging
import random

logger = logging.getLogger(__name__)


class Personaje(ABC):
    """Clase base común para héroes y villanos."""

    def __init__(self, identificador: int, nombre: str, apellidos: str,
                 fecha_nacimiento: date):
        if not isinstance(identificador, int) or identificador <= 0:
            raise ValueError("El identificador debe ser un entero positivo.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if not apellidos or not apellidos.strip():
            raise ValueError("Los apellidos no pueden estar vacíos.")
        if not isinstance(fecha_nacimiento, date):
            raise TypeError("La fecha de nacimiento debe ser un objeto date.")
        if fecha_nacimiento > date.today():
            raise ValueError("La fecha de nacimiento no puede estar en el futuro.")

        self.identificador = identificador
        self.nombre = nombre.strip()
        self.apellidos = apellidos.strip()
        self.fecha_nacimiento = fecha_nacimiento
        self.cualidades = {}
        self.puntuacion_total = 0

    @property
    def edad(self) -> int:
        """Calcula la edad teniendo en cuenta si ya ha cumplido años."""
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month,
                                    self.fecha_nacimiento.day)
        )

    def generar_cualidades(self) -> None:
        """Asigna valores aleatorios entre 0 y 100 a las cualidades."""
        self.cualidades = {
            nombre: random.randint(0, 100)
            for nombre in self.nombres_cualidades()
        }
        self.calcular_puntuacion()
        logger.info(
            "Cualidades generadas para %s id=%s",
            self.__class__.__name__, self.identificador
        )

    @abstractmethod
    def nombres_cualidades(self) -> tuple:
        """Devuelve los nombres de las cualidades de la subclase."""

    def calcular_puntuacion(self) -> None:
        """Calcula la media de las cualidades como puntuación total."""
        if not self.cualidades:
            self.puntuacion_total = 0
        else:
            self.puntuacion_total = round(
                sum(self.cualidades.values()) / len(self.cualidades), 2
            )

    def obtener_datos(self) -> dict:
        """Devuelve los datos del personaje en un diccionario."""
        return {
            "identificador": self.identificador,
            "tipo": self.__class__.__name__,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat(),
            "edad": self.edad,
            **self.cualidades,
            "puntuacion_total": self.puntuacion_total,
        }

    def __str__(self) -> str:
        cualidades = ", ".join(
            f"{nombre}={valor}" for nombre, valor in self.cualidades.items()
        )
        return (
            f"[{self.__class__.__name__} #{self.identificador}] "
            f"{self.nombre} {self.apellidos} | Edad: {self.edad} | "
            f"Puntuación: {self.puntuacion_total} | {cualidades}"
        )


class Heroe(Personaje):
    """Personaje con cualidades propias de un héroe."""

    def nombres_cualidades(self) -> tuple:
        return (
            "codigo_limpio",
            "bien_documentado",
            "gitgod",
            "arquitecto",
            "detallista",
        )


class Villano(Personaje):
    """Personaje con cualidades propias de un villano."""

    def nombres_cualidades(self) -> tuple:
        return (
            "chagepeteador",
            "entregadortardio",
            "ausencias",
            "hablador",
        )

class Miembro:
    def __init__(self, identificador, nombre, apellidos):
        self.identificador = identificador
        self.nombre = nombre
        self.apellidos = apellidos


class Jugador(Miembro):
    def __init__(self, identificador, nombre, apellidos, posicion):
        super().__init__(identificador, nombre, apellidos)
        self.posicion = posicion


class CuerpoTecnico(Miembro):
    def __init__(self, identificador, nombre, apellidos, rol):
        super().__init__(identificador, nombre, apellidos)
        self.rol = rol
