import threading
import time
from typing import Dict, List, Optional

class Card:
    """Represents a purchasable development card in the game of Splendor."""
    def __init__(self, card_id: str, cost: Dict[str, int], provides_bonus: Optional[str] = None):
        self.card_id = card_id
        self.cost = {color.lower(): amount for color, amount in cost.items() if amount > 0}
        self.provides_bonus = provides_bonus.lower() if provides_bonus else None


class Player:
    """Represents a player managing their dynamic wallet and card inventory."""
    def __init__(self, player_id: str):
        self.player_id = player_id
        self._standard_colors = {"red", "blue", "green", "white", "black"}
        self.coins: Dict[str, int] = {color: 0 for color in self._standard_colors}
        self.coins["gold"] = 0  
        self.owned_cards: List[Card] = []
        self.lock = threading.RLock() 

    def add_coins(self, color: str, amount: int) -> None:
        with self.lock:
            normalized_color = color.lower()
            if (normalized_color in self._standard_colors or normalized_color == "gold") and amount > 0:
                self.coins[normalized_color] += amount
            else:
                raise ValueError(f"Invalid coin color '{color}' or non-positive amount {amount}.")

    def get_discount(self, color: str) -> int:
        with self.lock:
            normalized_color = color.lower()
            return sum(1 for card in self.owned_cards if card.provides_bonus == normalized_color)

    def can_purchase(self, card: Card) -> bool:
        with self.lock:
            total_gold_needed = 0
            for color, total_cost in card.cost.items():
                discount = self.get_discount(color)
                net_cost_needed = total_cost - discount
                
                if net_cost_needed <= 0:
                    continue
                    
                player_standard_coins = self.coins.get(color, 0)
                if player_standard_coins < net_cost_needed:
                    deficit = net_cost_needed - player_standard_coins
                    total_gold_needed += deficit  
                    
            return self.coins["gold"] >= total_gold_needed

    def execute_deduction_and_receive(self, card: Card) -> None:
        with self.lock:
            for color, total_cost in card.cost.items():
                discount = self.get_discount(color)
                net_cost_needed = total_cost - discount
                
                if net_cost_needed <= 0:
                    continue
                    
                player_standard_coins = self.coins[color]
                if player_standard_coins >= net_cost_needed:
                    self.coins[color] -= net_cost_needed
                else:
                    gold_contribution_needed = net_cost_needed - player_standard_coins
                    self.coins[color] = 0  
                    self.coins["gold"] -= gold_contribution_needed  
                
            self.owned_cards.append(card)


class SplendorBoard:
    """Central coordinator managing the shared pool of available cards on the table."""
    def __init__(self, cards: List[Card]):
        self.available_cards: Dict[str, Card] = {card.card_id: card for card in cards}
        self.board_lock = threading.Lock()

    def purchase_card_from_board(self, player: Player, card_id: str) -> bool:
        with self.board_lock:
            if card_id not in self.available_cards:
                print(f"[Board Info] {player.player_id} tried to buy {card_id}, but it's ALREADY BOUGHT.")
                return False  
                
            card = self.available_cards[card_id]
            
            with player.lock:
                if not player.can_purchase(card):
                    print(f"[Board Info] {player.player_id} cannot afford {card_id}.")
                    return False
                
                player.execute_deduction_and_receive(card)
                del self.available_cards[card_id]
                print(f"🎉 SUCCESS: {player.player_id} bought {card_id}!")
                return True


# ==========================================
# MAIN EXECUTION ROUTINE
# ==========================================
def simulate_player_turn(board: SplendorBoard, player: Player, target_card_id: str):
    """Worker function to simulate parallel network/game interactions."""
    # Introduce a tiny, realistic microsecond jitter to make execution truly random
    time.sleep(0.001)
    board.purchase_card_from_board(player, target_card_id)


def main():
    print("=== Initializing Splendor Thread-Safety Simulation ===\n")
    
    # 1. Create a hot-commodity target card
    # Cost: 4 Red, 2 Blue. Generates a permanent Green discount once owned.
    valuable_card = Card(card_id="card_alpha", cost={"red": 4, "blue": 2}, provides_bonus="green")
    
    # Initialize the board with our high-value target card
    board = SplendorBoard([valuable_card])
    
    # 2. Setup Player 1: Has exactly enough standard coins to buy it outright
    player_1 = Player("Alice_Thread")
    player_1.add_coins("red", 4)
    player_1.add_coins("blue", 2)
    
    # 3. Setup Player 2: Deficient in standard coins, but relies heavily on Gold Wildcards
    player_2 = Player("Bob_Thread")
    player_2.add_coins("red", 2)   # Missing 2 Red
    player_2.add_coins("blue", 1)  # Missing 1 Blue
    player_2.add_coins("gold", 4)  # Has 4 Gold Wildcards (Needs 3 to buy)

    print(f"Initial Board Inventory: {list(board.available_cards.keys())}")
    print(f"Alice's Wallet: {player_1.coins}")
    print(f"Bob's Wallet: {player_2.coins}\n")
    print("--- Simulating Simultaneous Swipes for 'card_alpha' ---")

    # 4. Fire off two threads representing both players hitting the button at the exact same instant
    thread_alice = threading.Thread(target=simulate_player_turn, args=(board, player_1, "card_alpha"))
    thread_bob = threading.Thread(target=simulate_player_turn, args=(board, player_2, "card_alpha"))
    
    thread_alice.start()
    thread_bob.start()
    
    # Wait for both system processes to gracefully conclude
    thread_alice.join()
    thread_bob.join()
    
    print("\n--- Post-Simulation Engine Audit ---")
    print(f"Remaining Board Cards: {list(board.available_cards.keys())}")
    print(f"Alice's Final Wallet: {player_1.coins} | Cards: {[c.card_id for c in player_1.owned_cards]}")
    print(f"Bob's Final Wallet: {player_2.coins} | Cards: {[c.card_id for c in player_2.owned_cards]}")


if __name__ == "__main__":
    main()