"""People Age Analyzer - Python course project.

Enter any number of people in the format: name, dd-mm-yyyy
Leave the input loop by typing DONE. No external packages required.
"""

from datetime import date
import re
import sys


def parse_birth_date(date_text, today):
    """Return a valid past-or-present date, or None for an invalid date."""
    if not re.fullmatch(r"[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}", date_text):
        return None

    day, month, year = map(int, date_text.split("-"))
    try:
        birthday = date(year, month, day)
    except ValueError:
        return None

    if birthday > today:
        return None
    return birthday


def calculate_age(birthday, today):
    """Calculate complete years of age as of the reference date."""
    return today.year - birthday.year - (
        (today.month, today.day) < (birthday.month, birthday.day)
    )


def analyze_people(*entries, today=None):
    """Analyze any number of 'name, dd-mm-yyyy' entries."""
    if today is None:
        today = date.today()

    valid_people = []
    original_entries = list(entries)

    print(f"\nAge calculations as of {today.isoformat()}")
    print("=" * 47)

    for entry in original_entries:
        if "," not in entry:
            name = entry.strip() or "Unknown person"
            print(f"Invalid date: {name}")
            continue

        name, date_text = entry.split(",", 1)
        name = name.strip()
        date_text = date_text.strip()
        birthday = parse_birth_date(date_text, today)

        if not name or birthday is None:
            print(f"Invalid date: {name or 'Unknown person'}")
            continue

        age = calculate_age(birthday, today)
        weekday = birthday.strftime("%A")
        valid_people.append(
            {"name": name, "birthday": birthday, "age": age, "weekday": weekday}
        )
        print(f"{name} is {age} years old and she/he was born on {weekday}")

    # Use actual dates (not rounded whole-year ages) to determine oldest/youngest.
    if len(valid_people) < 2:
        print("There is no oldest or youngest person")
    else:
        oldest = min(valid_people, key=lambda person: person["birthday"])
        youngest = max(valid_people, key=lambda person: person["birthday"])
        print(f"The oldest one is {oldest['name']} ({oldest['age']} years old)")
        print(f"The youngest one is {youngest['name']} ({youngest['age']} years old)")

    print(f"Total People: {len(original_entries)}")

    # Additional task 1: sort from oldest to youngest.
    print("\nPeople sorted from oldest to youngest:")
    if valid_people:
        for person in sorted(valid_people, key=lambda item: item["birthday"]):
            print(f"{person['name']} - {person['age']} years old")
    else:
        print("No valid people")

    # Additional task 2: print the submitted inputs in reverse order.
    print("\nOriginal inputs in reverse order:")
    if original_entries:
        for entry in reversed(original_entries):
            print(entry)
    else:
        print("No inputs")

    # Additional task 3: show only people born on Sunday (weekday 6).
    print("\nPeople born on Sunday:")
    sunday_people = [person["name"] for person in valid_people if person["birthday"].weekday() == 6]
    if sunday_people:
        for name in sunday_people:
            print(name)
    else:
        print("None")


def main():
    # Optional demonstration with the assignment's reference date (01-01-2021).
    if "--demo" in sys.argv:
        analyze_people(
            "Khalid, 1-2-1989",
            "Nouf, 2-9-2004",
            "Ali, 9-12-2009",
            today=date(2021, 1, 1),
        )
        return

    print("People Age Analyzer")
    print("Enter: name, dd-mm-yyyy")
    print("Enter DONE to finish. You can enter as many people as you like.\n")

    entries = []
    while True:
        entry = input("Person: ").strip()
        if entry.upper() == "DONE":
            break
        if not entry:
            continue
        entries.append(entry)

    analyze_people(*entries)


if __name__ == "__main__":
    main()