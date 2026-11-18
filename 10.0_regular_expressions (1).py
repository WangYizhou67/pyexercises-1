"""Exercise 10.0 — Checking the shape of text (bonus, not graded)

WHAT THE PROGRAM MUST DO
    Validate three pieces of information typed by the user, and only save them when all
    three are acceptable.

ANSWER THESE FIRST, in comments
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. What are your three fields, and what makes a value acceptable for each? Write the
       rule in plain English before writing any pattern.

WHAT THE AI CANNOT KNOW
    Your three rules. "A valid email" is not a rule, it is a wish. Say what you accept
    and what you reject, and be ready to defend a borderline case.

WHAT TO WATCH
    An assistant will hand you a pattern that looks like line noise. Do not accept it
    until it has explained it to you piece by piece, and you have written that
    explanation in your own words above it.

CHECK IT YOURSELF
    For each field, prepare one value that must pass and two that must fail. Run all
    nine. Any surprise goes in a comment.

DELIVERABLE
    This file, with your comments and your code.
"""

# Your code below
"""
Exercise 10.0 — Checking the shape of text (bonus, not graded)

==============================================================================
ANSWERS FIRST
==============================================================================

1. What goes in?
   Three separate lines typed by the user, each read with input(). They are
   *supposed* to be a username, an email address, and a phone number, but the
   user can type anything — including nothing, spaces, emoji, brackets,
   letters where digits belong.

2. What happens to it?
   For each of the three strings we run a compiled regular expression with
   .fullmatch(), which means "the ENTIRE string must match". Each field has
   its own pattern and its own English message. If ANY of the three fails,
   nothing is saved. All three messages are printed together so the user can
   fix them in one pass.

3. What comes out?
   - If all three pass: a short "Saved:" block echoing the three values back.
   - If any fail: a "Not saved. Please fix the following:" block with ONE
     bullet per failing field, each naming the field, the offending text,
     and the rule it broke.
   - No traceback, ever — the program only uses fullmatch, which cannot raise.

4. My three fields and the rule for each.

   --- Field 1: Username ------------------------------------------------
   RULE (plain English):
     • 3 to 20 characters long, inclusive.
     • First character MUST be an English letter (A–Z or a–z).
     • Every remaining character may be a letter, a digit, or underscore.
     • Anything else — spaces, dots, hyphens, accented letters, leading digit
       or underscore, length outside 3–20 — is rejected.

   --- Field 2: Email (pragmatic check, NOT RFC-compliant) --------------
   RULE (plain English):
     • Split on exactly one '@'. If there is no '@' or more than one, reject.
     • The part before '@' must be at least one character, using only
       A–Z, a–z, 0–9, dot, underscore, percent, plus, hyphen.
     • The part after '@' must be at least one character, using only
       A–Z, a–z, 0–9, dot, hyphen, AND must contain a literal '.' followed
       by at least two letters (the TLD).
     • No spaces anywhere.
   I am NOT trying to accept every legal email address. I am trying to catch
   obvious typos on a web form. Deliberately rejected: `user@localhost`
   (no TLD), `user@[192.168.1.1]` (bracketed IP), quoted local parts,
   `user@example.c` (one-letter TLD). If you need those, use a real library.

   --- Field 3: Phone number (simple international) ---------------------
   RULE (plain English):
     • An optional leading '+'.
     • Then between 7 and 15 digits inclusive.
     • Between digits, at most ONE space or ONE hyphen is allowed. No two
       consecutive separators, no other characters.
     • Rejects: fewer than 7 digits, more than 15 digits, parentheses,
       letters, dots, tabs, double spaces, double hyphens.
   Defending a borderline case: `+44 (20) 7946 0958` FAILS. Brackets are
   common in the real world, but I decided a form for a simple app does not
   need to accept them; users can remove them. Simplicity beats coverage here.

==============================================================================
"WHAT THE AI CANNOT KNOW" — a note on why I hand-checked every pattern
==============================================================================
The assignment warns that an AI will produce a regex that looks like line
noise. Every pattern below has a plain-English paragraph above it, in my
words, describing exactly what each token does. If I could not write that
paragraph, I replaced the pattern with one I could defend.

==============================================================================
CHECK IT YOURSELF — nine cases I ran, three per field
==============================================================================

USERNAME
  pass   "alice_99"   -> matches: 'a' is a letter, 'lice_99' is 7 chars,
                         total 8, which is within 3-20.
  fail   "_alice"     -> first char '_' is not a letter. Rejected.
  fail   "ab"         -> 'a' + 'b' = 1 trailing char, but we require 2-19.
                         Rejected.

EMAIL
  pass   "alice@example.com" -> local 'alice', '@', 'example' as domain,
                         '.' + 'com' as TLD. Accepted.
  fail   "alice@example"     -> no '.' followed by a TLD in the domain part.
                         Rejected.
  fail   "alice.example.com" -> no '@'. Rejected.

PHONE
  pass   "+44 20 7946 0958"  -> optional '+', then 12 digits with single
                         spaces between them. Accepted.
  fail   "12345"             -> only 5 digits; below the 7-digit floor.
                         Rejected.
  fail   "+44 (20) 7946 0958"-> contains '(' and ')' which are not in the
                         separator set [- ]. Rejected.

SURPRISES I DID NOT ANTICIPATE (written down so I do not forget):
  a) Email "alice..bob@example.com" (consecutive dots in the local part)
     PASSES my pattern. It is technically invalid per RFC 5321, but the
     pattern only rejects characters, not dot placement. I am leaving it
     loose deliberately — spotting that would need a second pattern and it
     is not the kind of typo a user actually types.
  b) Email ".alice@example.com" (leading dot in the local part) PASSES for
     the same reason. Same call: leaving it.
  c) Phone "1 2 3 4 5 6 7" PASSES. I decided single-space separators between
     every digit is acceptable, even if it looks strange. It is unambiguous
     and easy for a human to read back.
  d) Phone "1--2--3--4--5--6--7" FAILS because [-]? allows AT MOST one
     separator per digit. Two consecutive hyphens break it. That matches my
     stated rule and I am comfortable with it.
  e) Username "abcdé" (final 'é' is a letter in Unicode) FAILS because I
     restricted to A-Z, a-z. If a real app needs Unicode usernames, that is a
     separate decision with separate pattern; I am not silently allowing it.

==============================================================================
CODE
==============================================================================
"""

import re


# Username -----------------------------------------------------------------
# Piece by piece:
#   [A-Za-z]                 one English letter (first char)
#   [A-Za-z0-9_]{2,19}       then 2 to 19 more chars, each a letter,
#                            digit, or underscore
# fullmatch means the whole string must match, so total length is 3..20.
USERNAME_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]{2,19}")


# Email (pragmatic) --------------------------------------------------------
# Piece by piece:
#   [A-Za-z0-9._%+-]+       one or more local-part characters
#   @                       exactly one at-sign
#   [A-Za-z0-9.-]+          one or more domain characters (dots and
#                           hyphens allowed as characters here)
#   \.                      a literal dot separating domain from TLD
#   [A-Za-z]{2,}            TLD of two or more letters
# Because we use fullmatch, a stray newline or trailing space fails too.
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


# Phone (simple international) --------------------------------------------
# Piece by piece:
#   \+?                     optional literal '+'
#   \d                      the first digit
#   (?:[- ]?\d){6,14}       six to fourteen repetitions of: one optional
#                           hyphen-or-space, then one digit
# Total digits: 1 + [6..14] = 7..15. At most one separator per digit, so
# "--" or "  " cannot slip through.
PHONE_RE = re.compile(r"\+?\d(?:[- ]?\d){6,14}")


def main() -> None:
    print("Please enter three pieces of information.")

    username = input("Username : ").strip()
    email    = input("Email    : ").strip()
    phone    = input("Phone    : ").strip()

    errors: list[str] = []

    # --- Field 1 ---------------------------------------------------------
    # Used fullmatch, not search/match: a substring match would happily
    # accept "alice!!" by matching just "alice".
    if not USERNAME_RE.fullmatch(username):
        errors.append(
            f"  Username {username!r}: must be 3-20 characters, start with "
            f"a letter, and use only letters, digits, and underscore."
        )

    # --- Field 2 ---------------------------------------------------------
    if not EMAIL_RE.fullmatch(email):
        errors.append(
            f"  Email {email!r}: must look like name@domain.tld, with a TLD "
            f"of at least two letters and no spaces."
        )

    # --- Field 3 ---------------------------------------------------------
    if not PHONE_RE.fullmatch(phone):
        errors.append(
            f"  Phone {phone!r}: must contain 7-15 digits, may start with "
            f"'+', and may use single spaces or hyphens between digits."
        )

    if errors:
        print()
        print("Not saved. Please fix the following:")
        for line in errors:
            print(line)
        return

    # All three passed: only now do we "save".
    print()
    print("Saved:")
    print(f"  username = {username!r}")
    print(f"  email    = {email!r}")
    print(f"  phone    = {phone!r}")


if __name__ == "__main__":
    main()