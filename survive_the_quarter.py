"""
SURVIVE THE QUARTER — Croissant Rocket
Student: <Yizhou Wang>
Group: B

Q1 — What goes in?
scenarios_B.csv is separated by semicolons. The first row is a header.
Each data row has 14 columns: scenario number, situation, and for A/B/C:
choice text, budget change, reputation change, feedback text.
Budget and reputation changes are integers (positive or negative).

Q2 — What happens?
1. Ask the player's name.
2. Load all scenarios from scenarios_B.csv.
3. Shuffle and keep 10 days.
4. Each day: show day, gauges, situation and options A/B/C.
5. Ask for A/B/C until valid (a,b,c accepted).
6. Apply budget and reputation changes, print feedback line.
7. Reputation capped at 100.
8. If budget or reputation <= 0, stop immediately.

Q3 — What comes out?
At the end: "Fired" with the reason, or the final score and title.
Best and worst move (by reputation change) are displayed.
One line is appended to results.csv:
name,budget,reputation,title,date

Q4 — What could go wrong?
- Player types a wrong key -> get_valid_choice() loops until A/B/C.
- scenarios_B.csv missing -> load_scenarios() prints a clear message and returns [].
- A CSV row has bad numbers or too few columns -> the row is skipped with a warning.
- Budget or reputation <= 0 -> the game stops immediately with reason.
- Reputation above 100 -> capped by apply_choice().

Feature chosen: (d) Difficulty.
Why: it is simple to implement, cannot break the game, and it makes the game replayable.
"""

import csv
import random
from datetime import date


# ---------- Read the scenario file ----------
def load_scenarios(filename):
    """Read scenarios_B.csv and return a list of
    (situation, option_a, option_b, option_c) tuples.
    Each option is (text, budget_change, reputation_change, feedback)."""
    scenarios = []
    try:
        with open(filename, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=";")
            header = next(reader, None)  # skip header line
            for line_no, row in enumerate(reader, start=2):
                if len(row) < 14 or not row[1].strip():
                    continue
                try:
                    situation = row[1].strip()
                    a = (row[2].strip(), int(row[3].strip()),
                         int(row[4].strip()), row[5].strip())
                    b = (row[6].strip(), int(row[7].strip()),
                         int(row[8].strip()), row[9].strip())
                    c = (row[10].strip(), int(row[11].strip()),
                         int(row[12].strip()), row[13].strip())
                except ValueError:
                    print(f"[warning] skipping bad row at line {line_no}")
                    continue
                scenarios.append((situation, a, b, c))
    except FileNotFoundError:
        print(f"[error] file not found: {filename}")
        return []
    return scenarios


# ---------- Feature (d): difficulty ----------
def choose_difficulty():
    """Ask for difficulty. Return (starting_budget, starting_reputation)."""
    while True:
        answer = input(
            "Choose difficulty — E = easy (15000 EUR) / H = hard (6000 EUR): "
        ).strip().upper()
        if answer == "E":
            return 15000, 50
        if answer == "H":
            return 6000, 50
        print("Please type E or H.")


# ---------- Read the player's choice safely ----------
def get_valid_choice():
    """Loop until the player types A, B or C (lowercase accepted)."""
    while True:
        answer = input("Your choice (A, B or C): ").strip().upper()
        if answer in ("A", "B", "C"):
            return answer
        print("Please type A, B or C.")


# ---------- Apply an option, return the new gauges ----------
def apply_choice(budget, reputation, option):
    """option is (text, budget_change, reputation_change, feedback).
    Return (new_budget, new_reputation); reputation capped at 100."""
    text, budget_change, rep_change, feedback = option
    new_budget = budget + budget_change
    new_reputation = min(100, reputation + rep_change)
    return new_budget, new_reputation


# ---------- Title from the final score ----------
def get_title(score):
    """Return the title given a final score."""
    if score < 95:
        return "Eternal Intern"
    if score < 120:
        return "Growth Hacker"
    if score < 140:
        return "CMO Material"
    return "Viral Legend"


# ---------- Best and worst move ----------
def find_best_worst(history):
    """history: list of (rep_change, day, option_text) tuples.
    Return (best, worst) using Python tuple comparison on the first element."""
    if not history:
        return None, None
    return max(history, key=lambda x: x[0]), min(history, key=lambda x: x[0])


# ---------- Append one line to results.csv ----------
def save_result(name, budget, reputation, title):
    """Append name,budget,reputation,title,date to results.csv."""
    with open("results.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, budget, reputation, title, date.today().isoformat()])


# ---------- Main game ----------
def main():
    print("=== SURVIVE THE QUARTER — Croissant Rocket ===")
    name = input("Your name: ").strip() or "Anonymous"

    scenarios = load_scenarios("scenarios_B.csv")
    if not scenarios:
        print("No scenarios loaded — cannot start. Check scenarios_B.csv.")
        return
    if len(scenarios) < 10:
        print(f"[warning] only {len(scenarios)} scenarios available.")

    budget, reputation = choose_difficulty()

    random.shuffle(scenarios)
    days = scenarios[:10]

    history = []           # (rep_change, day_number, option_text)
    game_over = False
    reason = ""

    for day_number, (situation, a, b, c) in enumerate(days, start=1):
        print()
        print(f"--- Day {day_number} ---")
        print(f"[Budget: {budget} EUR | Reputation: {reputation}/100]")
        print(situation)
        print(f"A: {a[0]}")
        print(f"B: {b[0]}")
        print(f"C: {c[0]}")

        choice = get_valid_choice()
        option = {"A": a, "B": b, "C": c}[choice]

        old_reputation = reputation
        budget, reputation = apply_choice(budget, reputation, option)
        actual_rep_change = reputation - old_reputation

        print(option[3])  # feedback line
        print(f"Budget {option[1]:+d} EUR, Reputation {actual_rep_change:+d}")

        history.append((actual_rep_change, day_number, option[0]))

        if budget <= 0:
            game_over = True
            reason = "budget hit zero"
            break
        if reputation <= 0:
            game_over = True
            reason = "reputation hit zero"
            break

    print()
    print("=" * 30)

    if game_over:
        print(f"You are fired! ({reason})")
        title = "Fired"
    else:
        print("Quarter survived!")
        print(f"Budget left: {budget} EUR, reputation: {reputation}/100")
        score = reputation + budget // 200
        print(f"Final score: {score}")
        title = get_title(score)
        print(f"{name}, your title: {title}")

    best, worst = find_best_worst(history)
    if best is not None:
        print(f'Best move: day {best[1]}, "{best[2]}" ({best[0]:+d})')
    if worst is not None:
        print(f'Worst move: day {worst[1]}, "{worst[2]}" ({worst[0]:+d})')

    save_result(name, budget, reputation, title)
    print("Saved in results.csv")


if __name__ == "__main__":
    main()