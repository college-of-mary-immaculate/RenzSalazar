import time
import threading

class CoffeeMaker:
    def __init__(self):
        self.water_level = 100
        self.coffee_beans = 100
        self.milk_level = 100

    def check_resources(self, cup_size):
        if self.water_level < cup_size * 0.7:
            return False, "Not enough water! Please refill."
        if self.coffee_beans < cup_size * 0.5:
            return False, "Not enough coffee beans! Please refill."
        if self.milk_level < (cup_size // 2) * 0.5:
            return False, "Not enough milk! Please refill."
        return True, ""

    def brew_coffee(self, coffee_type, strength, cup_size):
        can_brew, message = self.check_resources(cup_size)
        if not can_brew:
            return message

        brew_time = int((cup_size / 30) + 5)
        print(f"Brewing your {strength} {coffee_type} coffee. Please wait...")

        for remaining in range(brew_time, 0, -1):
            time.sleep(1)
            print(f"{remaining} seconds remaining...")

        self.water_level -= cup_size * 0.7
        self.coffee_beans -= cup_size * 0.5
        if coffee_type in ["latte", "cappuccino"]:
            self.milk_level -= (cup_size // 2) * 0.5

        return f"Your {strength} {coffee_type} coffee is ready! Enjoy!"

    def refill_resources(self):
        print("Refilling resources...")
        while self.water_level < 100:
            time.sleep(0.03)
            self.water_level += 1
            if self.water_level > 100:
                self.water_level = 100

        while self.coffee_beans < 100:
            time.sleep(0.03)
            self.coffee_beans += 1
            if self.coffee_beans > 100:
                self.coffee_beans = 100

        while self.milk_level < 100:
            time.sleep(0.03)
            self.milk_level += 1
            if self.milk_level > 100:
                self.milk_level = 100
        
        print("Refill complete.")

    def update_resource_labels(self):
        print(f"Water Level: {self.water_level}%")
        print(f"Coffee Level: {self.coffee_beans}%")
        print(f"Milk Level: {self.milk_level}%")


def main():
    coffee_maker = CoffeeMaker()

    while True:
        print("\nWelcome to the Coffee Maker!")
        print("1. Brew Coffee")
        print("2. Refill Resources")
        print("3. Check Resources")
        print("4. Exit")
        choice = input("Select an option (1-4): ")

        if choice == '1':
            coffee_type = input("Select Coffee Type (1: espresso, 2: latte, 3: cappuccino): ").strip()
            coffee_types = {'1': 'espresso', '2': 'latte', '3': 'cappuccino'}
            coffee_type = coffee_types.get(coffee_type, 'espresso')  

            strength = input("Select Coffee Strength (1: mild, 2: medium, 3: strong): ").strip()
            strengths = {'1': 'mild', '2': 'medium', '3': 'strong'}
            strength = strengths.get(strength, 'medium') 

            cup_size = int(input("Enter Cup Size (ml): "))
            message = coffee_maker.brew_coffee(coffee_type, strength, cup_size)
            print(message)

        elif choice == '2':
            refill_thread = threading.Thread(target=coffee_maker.refill_resources)
            refill_thread.start()
            refill_thread.join()  
            coffee_maker.update_resource_labels()

        elif choice == '3':
            coffee_maker.update_resource_labels()

        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()