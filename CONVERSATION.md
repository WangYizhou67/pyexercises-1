# Conversation with the AI

Written automatically by `tutor.py`. Add your own notes under any entry: what you tried, what broke, what you changed. Those notes are what is graded.

---
## 2026-11-18 14:28, in .

**Me:** I have a file called scenarios_B.csv. The separator is a semicolon.

**Tutor:**

Refused, off topic.

---
## 2026-11-18 14:33, in .

**Me:** My file scenarios_B.csv uses ; as separator. Header:

**Tutor:**

Refused, off topic.

---
## 2026-11-18 14:56, in .

**Me:** I want reputation never above 100 after adding rep_change.

**Tutor:**

Limiting a value to a maximum with a conditional expression.

```python
def cap_reputation(current: int, rep_change: int) -> int:
    new = current + rep_change
    # TODO: cap new so it never exceeds 100
    return new
```

What built-in operator keeps `new` from going above 100?
