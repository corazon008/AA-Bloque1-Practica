from random import choices
from typing import List
import os, sys


class Menu:
    @staticmethod
    def ask_choices(prompt: str, choices: List[str]) -> int:
        print(prompt)
        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")

        while True:
            try:
                selection = int(input("Enter your choice: "))
                if 1 <= selection <= len(choices):
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
            "Manage services",
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
                    Menu.handle_service_menu()
                case 3:
                    Menu.handle_view_profits()
                case 4:
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
                    print("Creating a new reservation...")
                case 2:
                    print("Viewing all reservations...")
                case 3:
                    print("Changing reservation status...")
                case 4:
                    Menu.main_menu()
        except KeyError:
            print("Invalid choice. Please try again.")
            Menu.handle_reservation_menu()

    @staticmethod
    def handle_service_menu():
        print("Service Menu")

    @staticmethod
    def handle_view_profits():
        print("Viewing profits")

    @staticmethod
    def handle_exit():
        print("Exiting...")
        exit()


if __name__ == "__main__":
    Menu.main_menu()
