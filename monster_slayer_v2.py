import random

# Prompt:
# You are a python developer, and your task is to build a text-based/command-line based game: "Monster Slayer", and following is the description of the game:

# It's a turn-based game where the user (= player) fights a monster (= computer).
# During every turn, the player can perform a regular or strong attack or heal.
# The strong attack should only be available every three player turns. Healing should only be available every five player turns.
# After each turn, the monster attacks.
# Damage & heal values are calculated randomly.
# The first participant to go below 0 health loses.
# Both participants start with 100 health.
# Once the game is over, the winner should be displayed on the screen and the player should be asked if a new game should be started.

class Game:
    def __init__(self):
        self.player_health = 100
        self.monster_health = 100
        self.player_turn_count = 0
        self.player_strong_attack_count = 0
        self.player_heal_count = 0

    def start(self):
        print("Welcome to Monster Slayer!")

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

    def player_turn(self):
        self.player_turn_count += 1
        print("Player's Turn Menu:")
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
            damage = random.randint(18, 25)
            self.monster_health -= damage
            print(f"\nYou hit the monster with a regular attack and dealt {damage} damage.")
        elif choice == '2':
            if self.player_strong_attack_count >= 3:
                print("\nYou need to wait for the next turn to use the strong attack.")
                self.player_turn()
                return
            damage = random.randint(10, 35)
            self.monster_health -= damage
            print(f"\nYou used a strong attack and dealt {damage} damage.")
            self.player_strong_attack_count += 1
        elif choice == '3':
            if self.player_heal_count >= 5:
                print("\nYou need to wait for five turns to use the heal.")
                self.player_turn()
                return
            heal = random.randint(18, 25)
            self.player_health += heal
            print(f"\nYou healed yourself for {heal} health points.")
            self.player_heal_count += 1
        else:
            print("\nInvalid choice. Try again.")
            self.player_turn()

    def monster_turn(self):
        damage = random.randint(10, 20)
        self.player_health -= damage
        print(f"The monster attacked you and dealt {damage} damage.")

    def check_game_over(self):
        if self.player_health <= 0:
            print("\nYou lost the game. The monster defeated you!")
            return True
        elif self.monster_health <= 0:
            print("\nCongratulations! You defeated the monster and won the game!")
            return True
        else:
            print(f"\nPlayer Health: {self.player_health}")
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