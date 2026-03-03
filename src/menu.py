from random import choices
from typing import List
import os, sys
from datetime import datetime

from src.reservation_manager import ReservationManager
from src.service import SERVICES


class Menu:

    manager = ReservationManager()

    @staticmethod
    def ask_choices(
        prompt: str, choices: List[str], clear_term: bool = True
    ) -> int:
        print(prompt)
        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")

        while True:
            try:
                selection = int(input("Enter your choice: "))
                if 1 <= selection <= len(choices):
                    if clear_term:
                        # Clear the console (works on Windows and Unix)
                        os.system("cls" if os.name == "nt" else "clear")
                    return selection
                else:
                    raise ValueError
            except ValueError:
                print("Invalid choice. Please try again.")

    @staticmethod
    def main_menu():
        choices = [
            "Manage reservations",
            "View profits",
            "Exit",
        ]
        print("Main Menu:")
        try:
            selected_choice = Menu.ask_choices(
                "Please choose an option:", choices
            )
            match selected_choice:
                case 1:
                    Menu.handle_reservation_menu()
                case 2:
                    Menu.handle_view_profits()
                case 3:
                    Menu.handle_exit()
        except KeyError:
            print("Invalid choice. Please try again.")
            Menu.main_menu()

    @staticmethod
    def handle_reservation_menu():
        choices = [
            "Create a new reservation",
            "View all reservations",
            "Change reservation status",
            "Back to main menu",
        ]
        print("Reservation Menu:")
        try:
            selected_choice = Menu.ask_choices(
                "Please choose an option:", choices
            )
            match selected_choice:
                case 1:
                    Menu.manager.new_reservation(
                        name=input("Enter reservation name: "),
                        service=SERVICES[
                            Menu.ask_choices(
                                "Select a service:",
                                [service.name for service in SERVICES],
                                clear_term=False,
                            )
                            - 1
                        ],
                        date=datetime.strptime(
                            input("Enter reservation date (YYYY-MM-DD): "),
                            "%Y-%m-%d",
                        ),
                        duration=float(
                            input("Enter reservation duration (hours): ")
                        ),
                    )
                case 2:
                    raise NotImplementedError(
                        "Viewing reservations not implemented yet."
                    )
                case 3:
                    raise NotImplementedError(
                        "Changing reservation status not implemented yet."
                    )
                case 4:
                    Menu.main_menu()
        except KeyError:
            print("Invalid choice. Please try again.")
            Menu.handle_reservation_menu()

    @staticmethod
    def handle_view_profits():
        raise NotImplementedError("Viewing profits not implemented yet.")

    @staticmethod
    def handle_exit():
        print("Exiting...")
        exit()


if __name__ == "__main__":
    Menu.main_menu()
