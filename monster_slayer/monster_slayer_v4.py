import random

# Base on v3, prompt: I would like to add difficulty levels to this game, for example: easy, normal and hard. Adjust damage & heal values based on chosen level

class Game:
    def __init__(self):
        self.username = ""
        self.player_health = 100
        self.monster_health = 100
        self.player_turn_count = 0
        self.player_strong_attack_count = 0
        self.player_heal_count = 0
        self.difficulty = ""
        self.damage_range = {
            "Easy": (15, 20),
            "Normal": (10, 25),
            "Hard": (5, 30)
        }
        self.heal_range = {
            "Easy": (18, 25),
            "Normal": (15, 30),
            "Hard": (10, 35)
        }

    def start(self):
        print("Welcome to Monster Slayer!")
        self.get_username()
        self.select_difficulty()

        while True:
            print("\n--- Player's Turn ---")
            self.player_turn()
            if self.check_game_over():
                break

            print("\n--- Monster's Turn ---")
            self.monster_turn()
            if self.check_game_over():
                break

        self.play_again()

    def get_username(self):
        self.username = input("Enter your username: ")

    def select_difficulty(self):
        print("\nSelect a difficulty level:")
        print("1. Easy")
        print("2. Normal")
        print("3. Hard")

        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            self.difficulty = "Easy"
        elif choice == '2':
            self.difficulty = "Normal"
        elif choice == '3':
            self.difficulty = "Hard"
        else:
            print("\nInvalid choice. Try again.")
            self.select_difficulty()

    def player_turn(self):
        self.player_turn_count += 1
        print(f"\n{self.username}'s Turn Menu (Difficulty: {self.difficulty}):")
        print("1. Regular Attack")
        if self.player_strong_attack_count < 3:
            print("2. Strong Attack")
        else:
            print("2. Strong Attack (available in the next turn)")
        if self.player_heal_count < 5:
            print("3. Heal")
        else:
            print("3. Heal (available in the next five turns)")

        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            damage = random.randint(*self.damage_range[self.difficulty])
            self.monster_health -= damage
            print(f"\n{self.username} hit the monster with a regular attack and dealt {damage} damage.")
        elif choice == '2':
            if self.player_strong_attack_count >= 3:
                print("\nYou need to wait for the next turn to use the strong attack.")
                self.player_turn()
                return
            damage = random.randint(*self.damage_range[self.difficulty])
            self.monster_health -= damage
            print(f"\n{self.username} used a strong attack and dealt {damage} damage.")
            self.player_strong_attack_count += 1
        elif choice == '3':
            if self.player_heal_count >= 5:
                print("\nYou need to wait for five turns to use the heal.")
                self.player_turn()
                return
            heal = random.randint(*self.heal_range[self.difficulty])
            self.player_health += heal
            print(f"\n{self.username} healed themselves for {heal} health points.")
            self.player_heal_count += 1
        else:
            print("\nInvalid choice. Try again.")
            self.player_turn()

    def monster_turn(self):
        damage = random.randint(10, 20)
        self.player_health -= damage
        print(f"The monster attacked {self.username} and dealt {damage} damage.")

    def check_game_over(self):
        if self.player_health <= 0:
            print(f"\n{self.username} lost the game. The monster defeated them!")
            return True
        elif self.monster_health <= 0:
            print(f"\nCongratulations, {self.username}! You defeated the monster and won the game!")
            return True
        else:
            print(f"\n{self.username}'s Health: {self.player_health}")
            print(f"Monster Health: {self.monster_health}")
            return False

    def play_again(self):
        choice = input("Do you want to play again? (y/n): ")
        if choice.lower() == 'y':
            self.__init__()
            self.start()
        else:
            print("\nThank you for playing Monster Slayer!")

# Start the game
game = Game()
game.start()