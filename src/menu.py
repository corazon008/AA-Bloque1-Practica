from random import choices
from typing import List
import os, sys
from datetime import datetime

from src.reservation_manager import ReservationManager
from src.service import SERVICES
from src.reservation import STATUS


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
                    for reservation in Menu.manager.get_all_reservations():
                        print(reservation)
                case 3:
                    # Ask to show all reservations first
                    show_reservations = input(
                        "Do you want to see all reservations before changing status? (y/n): "
                    ).lower()
                    if show_reservations in "yes":
                        for reservation in Menu.manager.get_all_reservations():
                            print(reservation)

                    reservation_id = int(
                        input("Enter reservation ID to change status: ")
                    )
                    status_list = [status.name for status in STATUS]
                    new_status = STATUS[
                        status_list[
                            Menu.ask_choices(
                                "Select new status:",
                                status_list,
                                clear_term=False,
                            )
                            - 1
                        ]
                    ]
                    if Menu.manager.change_reservation_status(
                        reservation_id, new_status
                    ):
                        print("Reservation status updated successfully.")
                    else:
                        print("Reservation not found.")

                case 4:
                    Menu.main_menu()
        except KeyError:
            print("Invalid choice. Please try again.")
            Menu.handle_reservation_menu()

    @staticmethod
    def handle_view_profits():
        sum = 0
        for reservation in Menu.manager.get_all_reservations():
            if reservation.status in (STATUS.completed, STATUS.confirmed):
                sum += reservation.cost
        print(f"Total profits from completed reservations: {sum:.2f}")

    @staticmethod
    def handle_exit():
        print("Exiting...")
        exit()


if __name__ == "__main__":
    Menu.main_menu()
