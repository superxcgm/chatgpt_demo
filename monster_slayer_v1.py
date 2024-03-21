import random

# Prompt:
# You are a python developer, and your task is to build a text-based/command-line based game: "Monster Slayer", and following is the description of the game:

# It's a turn-based game where the user (= player) fights a monster (= computer).
# During every turn, the player can perform a regular or strong attack or heal.
# The strong attack should only be available every three turns. Healing should only be available every five turns.
# After each turn, the monster attacks.
# Damage & heal values are calculated randomly.
# The first participant to go below 0 health loses.
# Both participants start with 100 health.
# Once the game is over, the winner should be displayed on the screen and the player should be asked if a new game should be started.



class Game:
    def __init__(self):
        self.player_health = 100
        self.monster_health = 100
        self.player_turn = True
        self.turn_count = 0

    def start(self):
        print("Welcome to Monster Slayer!")
        print("Defeat the monster to win the game.")

        while self.player_health > 0 and self.monster_health > 0:
            self.next_turn()

        self.end_game()

    def next_turn(self):
        self.turn_count += 1
        print("\n--- Turn", self.turn_count, "---")
        self.print_stats()

        if self.player_turn:
            self.player_action()
        else:
            self.monster_action()

        self.player_turn = not self.player_turn

    def player_action(self):
        print("\nPlayer's turn:")
        print("1. Regular Attack")
        print("2. Strong Attack")
        print("3. Heal")

        choice = self.get_valid_choice(1, 3)
        if choice == 1:
            damage = random.randint(10, 20)
            self.monster_health -= damage
            print("You hit the monster with a regular attack, dealing", damage, "damage.")
        elif choice == 2:
            if self.turn_count % 3 != 0:
                print("You can only use the strong attack every third turn.")
                self.player_action()
                return
            damage = random.randint(20, 30)
            self.monster_health -= damage
            print("You hit the monster with a strong attack, dealing", damage, "damage.")
        else:
            if self.turn_count % 5 != 0:
                print("You can only heal every fifth turn.")
                self.player_action()
                return
            heal = random.randint(10, 20)
            self.player_health += heal
            print("You healed yourself, gaining", heal, "health.")

    def monster_action(self):
        print("\nMonster's turn:")
        damage = random.randint(5, 15)
        self.player_health -= damage
        print("The monster attacked you, dealing", damage, "damage.")

    def print_stats(self):
        print("\nPlayer Health:", self.player_health)
        print("Monster Health:", self.monster_health)

    def end_game(self):
        print("\n--- Game Over ---")
        if self.player_health <= 0:
            print("You were defeated by the monster. Better luck next time!")
        else:
            print("Congratulations! You defeated the monster!")

        choice = input("Do you want to start a new game? (yes/no): ")
        if choice.lower() == "yes":
            self.reset()
            self.start()
        else:
            print("Thank you for playing Monster Slayer!")

    def get_valid_choice(self, min_choice, max_choice):
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if min_choice <= choice <= max_choice:
                    return choice
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def reset(self):
        self.player_health = 100
        self.monster_health = 100
        self.player_turn = True
        self.turn_count = 0


# Start the game
game = Game()
game.start()
