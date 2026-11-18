"""Exercise 7.1 — Loading a file, cleaning it, saving the result (homework)

This is the direct rehearsal for the final exam. Session 8 starts with it.

WHAT THE PROGRAM MUST DO
    Load names.txt, clean what is inside, sort it by last name, and write the result to
    a new file. The original file must not be modified.

DO THIS BEFORE ANYTHING ELSE
    Open names.txt and read it with your eyes. Then write, in comments at the top of
    your file, everything that is wrong with it. There are at least four different
    problems. Find them yourself.

    This step is not optional and it is graded. An assistant cannot see your file.

ANSWER THESE, in comments, after the list of problems
    1. What goes in?
    2. What happens to it?  (one line per problem you found, and how you deal with it)
    3. What comes out?
    4. What does "sort by last name" mean when a line contains two words, and how do you
       know which one is the last name?

WHAT THE AI CANNOT KNOW
    The actual content of names.txt. If you paste this brief into an assistant without
    describing the file, it will write a program for a clean file, and that program will
    crash or produce nonsense on the real one.

    Describe the file to it. That description is the exercise.

CHECK IT YOURSELF
    Count the lines in names.txt, then in your output file. The numbers should differ,
    and you should be able to say exactly why. Then check the first and last name of
    your sorted list by hand.

DELIVERABLE
    This file, plus the output file your program produced.
"""

# What is wrong with names.txt (found by reading it, not by guessing):
# -
# -
# -
# -

# 1. In:
# 2. Process, problem by problem:
# 3. Out:
# 4. How I decide which word is the last name:


# Your code below
"""
Exercise 7.1 — Loading a file, cleaning it, saving the result (homework)

==============================================================================
HONEST NOTE BEFORE ANYTHING ELSE
==============================================================================
I (the assistant) have NOT seen names.txt. The brief says explicitly that
this is the one thing an AI cannot know, and that the exercise IS the act
of describing the file. So instead of inventing four "problems" that might
not exist, I am giving you:

  (a) the answer template with every question answered *as far as it can
      be answered without seeing the file*, and
  (b) a program that is robust to the most common real-world problems in
      files of this kind, with the exact line to change if your file
      has a different problem than the ones covered.

Fill in the four dashes below by reading names.txt with your own eyes.
Then delete any code path that does not apply, and keep the ones that do.
That is the exercise.
==============================================================================

==============================================================================
WHAT IS WRONG WITH names.txt (fill in with what YOU saw — examples of
what to look for, in decreasing order of frequency in real files)
==============================================================================
Typical problems to check for, one line each:
  - [ ] blank lines in the middle or at the end
  - [ ] leading/trailing spaces or tabs on some lines
  - [ ] a header row like "First Last" or "name"
  - [ ] the same person listed twice (case differences count)
  - [ ] separator is sometimes a comma ("Smith, John" or "John, Smith")
  - [ ] one line has three words (a middle name, a nickname in quotes,
        a suffix like "Jr." or "III")
  - [ ] mixed case: "john smith" next to "John Smith"
  - [ ] Windows line endings (\\r\\n) mixed with Unix (\\n) — invisible
        but turns "Smith\\r" into a name whose last char is a CR
  - [ ] non-breaking spaces (U+00A0) pasted from a web page
  - [ ] accented letters (José, Müller) that might have been mangled

I cannot check any of these for you. What follows is the shape of the
answer you must write.

# What is wrong with names.txt (found by reading it, not by guessing):
# 1. <your finding 1 — e.g. "There are 3 empty lines, one between lines 5
#    and 6, two at the end.">
# 2. <your finding 2 — e.g. "Lines 8 and 12 start with a space.">
# 3. <your finding 3 — e.g. "Line 4 uses a comma, the rest use spaces.">
# 4. <your finding 4 — e.g. "Line 15 has three words: 'Mary Ann Smith'.">
# (add more if you found more)

==============================================================================
1. What goes in?
==============================================================================
The file `names.txt` in the working directory, read as UTF-8 text, one
name per line. Encoding is opened explicitly (see code) so that accented
letters do not blow up on Windows.

==============================================================================
2. What happens to it?  (one line per problem, and how I deal with it)
==============================================================================
The four lines below must be rewritten to match YOUR four findings above.
Each finding gets exactly one fix in the pipeline.

  - <problem 1>  ->  <fix 1>
      e.g. blank lines           -> skip lines whose .strip() is empty
      e.g. trailing CR from \\r\\n -> .strip() removes it
  - <problem 2>  ->  <fix 2>
      e.g. leading spaces        -> .strip() on every line
  - <problem 3>  ->  <fix 3>
      e.g. comma-separated lines -> split on ',' when present, else ' '
  - <problem 4>  ->  <fix 4>
      e.g. three-word names      -> treat the LAST token as the surname
                                    (see question 4 for the defence)

Anything I do NOT list above, I do NOT fix. If your file has a problem
that is not in this list, the program below will trip on it loudly, and
that is on purpose — I would rather see the bug than hide it.

==============================================================================
3. What comes out?
==============================================================================
A new file, `names_cleaned.txt`. It is written, not printed, so the
original `names.txt` is never opened for writing and therefore cannot be
modified. The count of lines written should equal
    (lines in names.txt)
    minus (blank lines)
    minus (header row, if any)
    minus (duplicate names after normalisation)
and you should be able to say that number out loud.

==============================================================================
4. How I decide which word is the last name?
==============================================================================
My rule, stated before looking at any code:

    After stripping the line, split it on commas if a comma is present,
    otherwise split it on whitespace. The surname is the LAST field.

  - For "John Smith"  -> surname is "Smith".
  - For "Mary Ann Smith" (three tokens, no comma) -> surname is "Smith";
    "Ann" is assumed to be a middle name, because English naming puts
    the family name last. This is a CONVENTION, not a fact. If your file
    uses "Smith, Mary Ann" then the comma branch kicks in and the surname
    is still the first field of the split — which for that format is
    correct.
  - I do NOT attempt to detect "surname first" files automatically.
    Detecting that from data alone is ambiguous ("Van Morrison" — is Van
    the surname?). If your file is surname-first, change the key function
    to `key[0]` and add a comment saying so.

The sort is case-insensitive (I lowercase for the comparison only, I do
not change the stored value) so that "smith" and "Smith" end up adjacent
rather than in two separate alphabetical runs.
==============================================================================
"""

from pathlib import Path


INPUT_PATH  = Path("names.txt")
OUTPUT_PATH = Path("names_cleaned.txt")


def split_name(line: str) -> tuple[str, str] | None:
    """Return (first, last) for a cleaned line, or None if not a real name.

    Adjust the body of this function ONLY where your four findings above
    demand it, and leave a comment next to each change pointing back to
    the finding by number.
    """
    # --- Finding 1 / 2: strip surrounding whitespace (also kills \\r) ---
    cleaned = line.strip()

    # --- Finding 1: skip blank lines -----------------------------------
    if not cleaned:
        return None

    # --- Finding 3: comma separator takes priority over whitespace -----
    # "Smith, John" -> ["Smith", "John"] -> first="John", last="Smith"
    # "John Smith"  -> ["John", "Smith"] -> first="John", last="Smith"
    if "," in cleaned:
        parts = [p.strip() for p in cleaned.split(",", 1)]
        # After split("," , 1): parts[0] is surname, parts[1] is given names
        last, given = parts[0], parts[1]
        return given, last

    # --- Finding 4: whitespace-separated; last token is the surname ----
    parts = cleaned.split()
    if len(parts) < 2:
        # One token: cannot decide which half is the surname. Skip it and
        # note it — silently inventing a surname is worse than dropping it.
        return None
    first = " ".join(parts[:-1])   # keeps middle names with the given name
    last  = parts[-1]
    return first, last


def main() -> None:
    # -------- Load ----------------------------------------------------
    # encoding="utf-8-sig" also strips a UTF-8 BOM if the file was saved
    # by Notepad on Windows — a common invisible first character.
    raw_lines = INPUT_PATH.read_text(encoding="utf-8-sig").splitlines()
    original_count = len(raw_lines)

    # -------- Clean ---------------------------------------------------
    # Finding on header row: if the first line is literally "First Last"
    # or "name", drop it. Check for it in YOUR file before leaving this on.
    if raw_lines and raw_lines[0].strip().lower() in {"first last", "name"}:
        raw_lines = raw_lines[1:]
        header_dropped = 1
    else:
        header_dropped = 0

    cleaned: list[tuple[str, str]] = []
    dropped_short: list[str] = []

    for line_no, line in enumerate(raw_lines, start=1 + header_dropped):
        pair = split_name(line)
        if pair is None:
            if line.strip():                      # not blank -> real loss
                dropped_short.append(f"line {line_no}: {line!r}")
            continue
        cleaned.append(pair)

    # Finding on duplicates: same (first, last) after stripping, compared
    # case-insensitively, is a duplicate. Keep the first occurrence.
    seen: set[tuple[str, str]] = set()
    unique: list[tuple[str, str]] = []
    duplicates = 0
    for first, last in cleaned:
        key = (first.casefold(), last.casefold())
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        unique.append((first, last))

    # -------- Sort ----------------------------------------------------
    # Case-insensitive, then first name as a tiebreaker so the order is
    # deterministic across runs. Only the comparison is lowercased; the
    # stored value is untouched.
    unique.sort(key=lambda p: (p[1].casefold(), p[0].casefold()))

    # -------- Save ----------------------------------------------------
    # write_text opens in mode "w" (truncate) and creates the file if
    # missing. INPUT_PATH is only ever read, never opened for writing,
    # so names.txt cannot be modified by this program.
    output_body = "\n".join(f"{first} {last}" for first, last in unique) + "\n"
    OUTPUT_PATH.write_text(output_body, encoding="utf-8")

    # -------- Self-check report ---------------------------------------
    print(f"Read          : {original_count} lines from {INPUT_PATH}")
    print(f"Header dropped: {header_dropped}")
    print(f"Duplicates    : {duplicates}")
    print(f"Unusable lines: {len(dropped_short)}")
    for d in dropped_short:
        print(f"                 {d}")
    print(f"Wrote         : {len(unique)} lines to {OUTPUT_PATH}")
    expected = original_count - header_dropped - duplicates - len(dropped_short) \
               - (original_count - header_dropped - len(dropped_short) - len(cleaned))
    # The ugly formula above is just a reminder: run the program, then
    # manually check that
    #     lines_out == lines_in - blanks - header - duplicates - unusable
    # matches what the printout says. If it does not, one of your four
    # findings is wrong, or you have a fifth problem you missed.
    if unique:
        print(f"First entry   : {unique[0][1]}, {unique[0][0]}")
        print(f"Last entry    : {unique[-1][1]}, {unique[-1][0]}")


if __name__ == "__main__":
    main()
