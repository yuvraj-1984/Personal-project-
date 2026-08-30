PUZZLES = [
    {
        "id": "garden_gate",
        "title": "The Garden Gate",
        "description": "A locked gate blocks your path. There is a riddle inscribed: 'I have keys but no locks, space but no room. You can enter but not go inside.' What am I?",
        "puzzle_type": "text",
        "answer": "keyboard",
        "hints": [
            "It's an object you use every day with a computer.",
            "It has letters and numbers on it."
        ],
        "points": 10,
        "required_items": [],
        "reward_item": "rusty_key",
        "next_puzzle": "greenhouse_lock"
    },
    {
        "id": "greenhouse_lock",
        "title": "Greenhouse Lock",
        "description": "The greenhouse door has a padlock. It seems you need a key.",
        "puzzle_type": "item_use",
        "answer": "rusty_key",
        "hints": [
            "Maybe you found something earlier that could open a lock.",
            "The rusty key from the gate might fit."
        ],
        "points": 15,
        "required_items": ["rusty_key"],
        "reward_item": "seed_packet",
        "next_puzzle": "flower_code"
    },
    {
        "id": "flower_code",
        "title": "Flower Code",
        "description": "Inside the greenhouse, you see a panel with four flower symbols: Rose, Tulip, Daisy, Lily. Each has a number: Rose=3, Tulip=5, Daisy=2, Lily=8. What is the four-digit code?",
        "puzzle_type": "code",
        "answer": "3528",
        "hints": [
            "Match the flowers in order: Rose, Tulip, Daisy, Lily.",
            "The code is formed by the numbers in that order."
        ],
        "points": 20,
        "required_items": [],
        "reward_item": "secret_map",
        "next_puzzle": "mystery_letter"
    },
    {
        "id": "mystery_letter",
        "title": "The Mystery Letter",
        "description": "You find a letter with missing words: 'The ______ is in the library.' What word completes the sentence?",
        "puzzle_type": "multiple_choice",
        "answer": "clue",
        "options": ["clue", "key", "answer", "secret"],
        "hints": [
            "It's something that helps you solve a mystery.",
            "It rhymes with 'blue'."
        ],
        "points": 25,
        "required_items": [],
        "reward_item": "library_key",
        "next_puzzle": None
    }
]

def get_puzzle(puzzle_id):
    for p in PUZZLES:
        if p["id"] == puzzle_id:
            return p
    return None
