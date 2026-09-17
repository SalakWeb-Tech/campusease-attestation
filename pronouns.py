# pronouns.py
# Single source of truth for all gender-based wording.
# Every one of the 1000+ templates will use ONLY these variables.

PRONOUNS = {
    "Male": {
        "subject_pronoun": "He",
        "possessive_pronoun": "His",
        "object_pronoun": "him",
        "relationship_term": "son",
    },
    "Female": {
        "subject_pronoun": "She",
        "possessive_pronoun": "Her",
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
        print(f"{p['subject_pronoun']} is of good conduct.")
        print(f"{p['subject_pronoun']} will be dedicated to {p['possessive_pronoun'].lower()} studies.")
        print(f"Please kindly give {p['object_pronoun']} all necessary assistance.")
        print(f"Relationship: my {p['relationship_term']}")