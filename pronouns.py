# pronouns.py
# Single source of truth for all gender-based wording.
# Every one of the 1000+ templates will use ONLY these variables.

PRONOUNS = {
    "Male": {
        "subject_pronoun": "He",
        "subject_pronoun_lower": "he",
        "possessive_pronoun": "His",
        "possessive_pronoun_lower": "his",
        "object_pronoun": "him",
        "relationship_term": "son",
    },
    "Female": {
        "subject_pronoun": "She",
        "subject_pronoun_lower": "she",
        "possessive_pronoun": "Her",
        "possessive_pronoun_lower": "her",
        "object_pronoun": "her",
        "relationship_term": "daughter",
    },
}


def get_pronouns(gender: str) -> dict:
    """Return pronoun set for Male/Female.
    Raises ValueError on any other value."""
    if gender not in PRONOUNS:
        raise ValueError(f"Invalid gender: {gender}. Must be 'Male' or 'Female'.")
    return PRONOUNS[gender]


if __name__ == "__main__":
    for g in ("Male", "Female"):
        p = get_pronouns(g)
        print(f"\n--- {g} ---")
        print(f"{p['subject_pronoun']} / {p['subject_pronoun_lower']}")
        print(f"{p['possessive_pronoun']} / {p['possessive_pronoun_lower']}")
        print(f"{p['object_pronoun']}")
        print(f"my {p['relationship_term']}")