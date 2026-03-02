from datetime import datetime

from src.reservation_manager import ReservationManager
from src.services import Service, SERVICE_TYPE
from src.menu import Menu

if __name__ == "__main__":
    manager = ReservationManager()

    Menu.main_menu()
