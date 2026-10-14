"""Punto de entrada de la aplicación."""

import logging
from gestion import Gestion
from menu import Menu
import faker
import os


def configurar_logging() -> None:
    # Crear la carpeta logs si no existe
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(
                "logs/villanoYHeroe.log",
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )


def main() -> None:
    configurar_logging()
    logger = logging.getLogger(__name__)
    logger.info("Inicio de la aplicación.")

    try:
        gestion = Gestion()
        menu = Menu(gestion)
        menu.mostrar()
    except Exception:
        logger.exception("Error fatal en la aplicación.")
        print("La aplicación ha finalizado por un error. Consulta aplicacion.log.")
    finally:
        logger.info("Fin de la aplicación.")


if __name__ == "__main__":
    main()
