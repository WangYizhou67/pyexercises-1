"""Exercise 9.0 — Surviving what you did not expect

Useful for the final exam: two campaigns in the exam dataset have zero conversions.

WHAT THE PROGRAM MUST DO
    Ask the user for a number, divide something by it, and keep running whatever the
    user types. Never crash.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. Which two different failures can happen here, and should they produce the same
       message to the user? Decide before coding.

WHAT THE AI CANNOT KNOW
    Your answer to question 4, and how many attempts you allow before giving up.

    An assistant will often propose catching every error at once. Find out why catching
    each failure separately is better, and write the reason in a comment.

CHECK IT YOURSELF
    Run it with: a normal number, then zero, then the word "abc", then an empty line.
    Four runs, four behaviours, all described in a comment. If any of them stopped your
    program, it is not finished.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In:One line of text typed at the keyboard. It is *supposed* to be a number(the divisor), but the user can type anything: digits, a decimal point,a minus sign, nothing at all, letters, spaces, or a whole sentence.
# 2. Process:
# 3. Out:
# 4. The two failures, and whether they deserve the same message:


# Your code below


NUMERATOR = 100
MAX_ATTEMPTS = 3


def main() -> None:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        raw = input(f"Divide {NUMERATOR} by which number? ")

        # ---- Failure 1: the text is not a number at all ----------------
        try:
            divisor = float(raw)
        except ValueError:
            print(f"  '{raw}' is not a number — try digits like 4 or 2.5 "
                  f"(attempt {attempt} of {MAX_ATTEMPTS}).")
            continue

        # ---- Failure 2: the number is fine, but it is zero -------------
        try:
            result = NUMERATOR / divisor
        except ZeroDivisionError:
            print(f"  {divisor} is a fine number but you cannot divide by zero "
                  f"(attempt {attempt} of {MAX_ATTEMPTS}).")
            continue

        # ---- Success ---------------------------------------------------
        print(f"  {float(NUMERATOR)} / {divisor} = {result}")
        return

    print("  Too many bad inputs — giving up gracefully. Bye.")


if __name__ == "__main__":
    main()
