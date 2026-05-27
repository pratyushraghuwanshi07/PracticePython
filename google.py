import random
from typing import List, Set, Dict, Optional

class Person:
    """
    Represents a Person who picks a random thing from a list of things
    and can answer whether a question is related to that thing.
    """
    def __init__(self, things: List[str], relations: Dict[str, Set[str]]):
        if not things:
            raise ValueError("The list of things cannot be empty.")
        self.things = things
        self.relations = relations
        # The person selects a random thing from the list
        self.selected_thing = random.choice(things)
        # Keep track of how many questions were asked
        self.questions_asked_count = 0

    def ask(self, question: str) -> bool:
        """
        Ask the person a question. Returns True if the question is related
        to their selected thing, and False otherwise.
        """
        self.questions_asked_count += 1
        related_questions = self.relations.get(self.selected_thing, set())
        return question in related_questions

def find_selected_thing(
    things: List[str],
    questions: List[str],
    relations: Dict[str, Set[str]],
    person: Person,
    verbose: bool = False
) -> Optional[str]:
    """
    Finds the thing that the person selected from the list of things.
    
    This function uses an optimal filtering strategy by selecting the question
    at each step that splits the remaining candidates closest to 50/50 (maximizing information gain).
    
    Args:
        things: The list of possible things.
        questions: The list of possible questions.
        relations: A mapping of each thing to its set of related questions.
        person: The Person object to ask questions to.
        verbose: If True, prints the decision process step-by-step.
        
    Returns:
        The identified thing, or None if it cannot be determined.
    """
    candidates = set(things)
    asked_questions = set()
    
    if verbose:
        print(f"\n[Search] Starting search. Remaining candidates: {len(candidates)}")

    while len(candidates) > 1:
        best_question = None
        min_diff = len(candidates) + 1
        
        # Select the question that splits candidates most evenly
        for q in questions:
            if q in asked_questions:
                continue
            
            # Count how many remaining candidates are related to this question
            yes_count = sum(1 for c in candidates if q in relations.get(c, set()))
            no_count = len(candidates) - yes_count
            diff = abs(yes_count - no_count)
            
            # We want to minimize the difference between YES and NO counts
            if diff < min_diff:
                min_diff = diff
                best_question = q
        
        # If we can't find any question that splits candidates, or run out of questions, stop
        if best_question is None or min_diff == len(candidates):
            if verbose:
                print("[Search] No more informative questions to ask.")
            break
            
        # Ask the person
        answer = person.ask(best_question)
        asked_questions.add(best_question)
        
        if verbose:
            print(f"  Asked: '{best_question}' -> Answer: {answer}")
            
        # Filter candidates based on response
        if answer:
            candidates = {c for c in candidates if best_question in relations.get(c, set())}
        else:
            candidates = {c for c in candidates if best_question not in relations.get(c, set())}
            
        if verbose:
            print(f"  Remaining candidates ({len(candidates)}): {list(candidates)}")
            
    if len(candidates) == 1:
        return list(candidates)[0]
    elif len(candidates) > 1:
        if verbose:
            print(f"[Search] Multiple candidates remaining: {candidates}. Unable to narrow down further.")
        return list(candidates)[0] # Return one of the remaining options as a guess
    else:
        if verbose:
            print("[Search] Error: 0 candidates remaining. Relations database might be inconsistent.")
        return None

# Demonstration and validation code
if __name__ == "__main__":
    # Define our dataset of things, questions, and relations
    things = [
        "Apple", "Banana", "Eagle", "Lion", "Shark", 
        "Salmon", "Rose", "Cactus"
    ]
    
    questions = [
        "Is it an animal?",
        "Can it fly?",
        "Does it live in water?",
        "Is it a plant?",
        "Is it a fruit?",
        "Does it have thorns/spines?",
        "Is it a mammal?",
        "Is it round?",
        "Is it long and curved?",
        "Is it yellow?",
        "Is it typically red?",
        "Is it a king of the jungle?",
        "Does it have sharp teeth?"
    ]
    
    relations = {
        "Apple": {"Is it a plant?", "Is it a fruit?", "Is it round?", "Is it typically red?"},
        "Banana": {"Is it a plant?", "Is it a fruit?", "Is it long and curved?", "Is it yellow?"},
        "Eagle": {"Is it an animal?", "Can it fly?"},
        "Lion": {"Is it an animal?", "Is it a mammal?", "Is it a king of the jungle?"},
        "Shark": {"Is it an animal?", "Does it live in water?", "Does it have sharp teeth?"},
        "Salmon": {"Is it an animal?", "Does it live in water?"},
        "Rose": {"Is it a plant?", "Does it have thorns/spines?", "Is it typically red?"},
        "Cactus": {"Is it a plant?", "Does it have thorns/spines?"}
    }
    
    print("=" * 60)
    print(" 20 Questions Game Solver Demo ")
    print("=" * 60)
    
    # Run the game 10 times to test
    success_count = 0
    rounds = 10
    
    for i in range(1, rounds + 1):
        print(f"\n--- Round {i} ---")
        person = Person(things, relations)
        actual = person.selected_thing
        print(f"[Person] Selected thing (hidden from searcher): {actual}")
        
        guessed = find_selected_thing(things, questions, relations, person, verbose=True)
        
        print(f"[Result] Guessed: {guessed} | Actual: {actual}")
        print(f"[Stats] Questions asked: {person.questions_asked_count}")
        
        if guessed == actual:
            print("Verdict: SUCCESS! Correctly guessed.")
            success_count += 1
        else:
            print("Verdict: FAILURE! Incorrect guess.")
            
    print("\n" + "=" * 60)
    print(f"Demo Summary: {success_count}/{rounds} correct guesses ({success_count / rounds * 100:.1f}%)")
    print("=" * 60)
