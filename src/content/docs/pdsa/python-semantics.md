---
title: 1. Python semantics & code tracing
description: Names, objects, mutability, aliasing, scope, closures, operators — the traps behind every GATE DA "what does this print?" question.
sidebar:
  label: 1. Python semantics
  order: 1
---

<span class="tag high">★ HIGH</span> <span class="tag yr">2024 ×2</span> <span class="tag yr">2025 ×3</span> <span class="tag yr">2026 ×3</span>

**Why it matters:** 8 of about 30 PDSA questions in three years were "trace this Python code". Most were 2-mark questions. Every one tested one of the six ideas below, never obscure library trivia.

If you already know Python, read this page for the **GATE angle**: it covers only the corners of the language that examiners turn into trick questions. Skim §1.1–1.2 and slow down from §1.3.

## Topic map

<div class="mindmap">

- **Python semantics**
  - Names & objects
    - variable = name tag on an object
    - `is` vs `==`
  - Mutability
    - mutable: list, dict, set
    - immutable: int, float, str, tuple
  - Mutate vs rebind
    - `L.append`, `L += …` → mutate
    - `L = L + …` → rebind
  - Functions
    - pass by object reference
    - mutable default argument
  - Scope
    - LEGB rule
    - `global`, `nonlocal`, closures
  - Operators & built-ins
    - `/` vs `//` vs `%`
    - tuple (simultaneous) assignment
    - list / dict / set methods

</div>

---

## 1.1 Names point to objects

In Python, a variable isn't a box that holds a value. It's a **name tag stuck on an object**.

```python
a = [1, 2, 3]   # create a list object, stick tag "a" on it
b = a           # stick a SECOND tag "b" on the SAME object
b.append(4)
print(a)        # [1, 2, 3, 4]  ← a sees the change
```

Picture it like this:

```
a ──┐
    ├──►  [1, 2, 3, 4]      (one object)
b ──┘
```

- `a == b` asks: **same value?**
- `a is b` asks: **same object?**

```python
x = [1, 2, 3]
y = x[:]        # slice → NEW list with the same values
print(x == y, x is y)   # True False
```

## 1.2 Mutable vs immutable

| Mutable (can change in place) | Immutable (can never change) |
|---|---|
| `list`, `dict`, `set` | `int`, `float`, `bool`, `str`, `tuple`, `frozenset` |

When you "change" an immutable object, Python builds a **new** object and moves the tag:

```python
s = "gate"
t = s
s = s + "!"     # new string; t still points to the old one
print(t)        # gate
```

Only **hashable** (immutable) objects can be dict keys or set members. `{[1,2]: 5}` raises a `TypeError`, but `{(1,2): 5}` is fine.

## 1.3 Mutate vs rebind: the most important distinction

Ask this about every line that touches a list: **does it change the object, or move the name?**

| Statement | Effect on the object | Other names pointing to it see the change? |
|---|---|---|
| `L.append(x)`, `L.extend(M)`, `L.insert(i,x)`, `L.pop()`, `L.remove(x)`, `L.sort()`, `L[i] = x` | mutates | **yes** |
| `L += M` (for lists) | mutates (same as `extend`) | **yes** |
| `L = L + M` | builds a new list, rebinds `L` | no |
| `L = [..]` | rebinds `L` | no |
| `t += (3,)` (tuple) | new tuple, rebinds (tuples can't mutate) | no |

```python
a = [1, 2, 3]; b = a; b = b + [4]
print(a)        # [1, 2, 3]      ← rebind: a untouched

a = [1, 2, 3]; b = a; b += [4]
print(a)        # [1, 2, 3, 4]   ← += on a list mutates!
```

<div class="trap">

**Trap: `+=` isn't always `= +`.** For lists, `+=` mutates in place. For tuples, strings and ints, it rebinds. Many students lose marks by treating both the same way.

</div>

### Copies: shallow vs deep

| Way | Result |
|---|---|
| `b = a` | no copy, same object |
| `b = a[:]`, `list(a)`, `a.copy()`, `copy.copy(a)` | **shallow** copy: new outer list, *same inner objects* |
| `copy.deepcopy(a)` | fully independent copy |

The classic grid trap:

```python
g = [[0]*3]*3          # ONE inner list, referenced 3 times
g[0][0] = 1
print(g)               # [[1,0,0], [1,0,0], [1,0,0]]

g = [[0]*3 for _ in range(3)]   # 3 separate inner lists
g[0][0] = 1
print(g)               # [[1,0,0], [0,0,0], [0,0,0]]
```

## 1.4 Functions: pass by object reference

Python passes the **reference** (the tag) into the function. So:

- **Mutating** the parameter changes the caller's object.
- **Rebinding** the parameter only moves the local tag. The caller sees nothing.

```python
def mutate(L): L[0] = 9
def rebind(L): L = [9]

X = [1]
rebind(X); print(X)   # [1]
mutate(X); print(X)   # [9]
```

### Mutable default arguments

Default values are evaluated **once, when `def` runs**, not each time the function is called. A mutable default is therefore **shared across calls**.

```python
def f(v, L=[]):     # this [] is created ONE time
    L.append(v)
    return L
```

The standard fix is `def f(v, L=None): if L is None: L = []`.

## 1.5 Scope: LEGB, `global`, `nonlocal`, closures

When Python looks up a name, it searches four places in order:

<div class="formula">

**L**ocal → **E**nclosing function → **G**lobal (module) → **B**uilt-in

</div>

- **Assigning** to a name inside a function makes it *local* to that function, unless it's declared `global` or `nonlocal`.
- Reading a name works without any declaration.
- `x += 1` inside a function without `nonlocal`/`global` raises `UnboundLocalError`, because it's an assignment.

**Closure:** an inner function that remembers the variables of the enclosing call that created it. Each call to the outer function creates a **fresh** set of enclosing variables.

```python
def outer():
    x = []              # new list on EVERY call to outer()
    def inner(v):
        x.append(v)     # mutation, so no nonlocal needed
        return x
    return inner
```

**Late binding:** a closure looks up the variable's *value when it's called*, not when it was defined.

```python
fs = [lambda: i for i in range(3)]
print([f() for f in fs])           # [2, 2, 2]
fs = [lambda i=i: i for i in range(3)]
print([f() for f in fs])           # [0, 1, 2]  (default binds now)
```

## 1.6 Operators & built-ins you must know cold

<div class="formula">

| Expression | Value | Rule |
|---|---|---|
| `7 / 2`, `6 / 2` | `3.5`, `3.0` | `/` **always** gives a float |
| `7 // 2`, `-7 // 2` | `3`, `-4` | `//` floors (rounds toward $-\infty$) |
| `-7 % 2`, `7 % -2` | `1`, `-1` | result takes the sign of the divisor: $a = (a//b)\cdot b + a\%b$ |
| `2 ** 3 ** 2` | `512` | `**` is right-associative: $2^{9}$ |
| `-2 ** 2` | `-4` | `**` binds tighter than unary minus |
| `True + True` | `2` | `bool` is a subclass of `int` |
| `5 == 5.0` | `True` | value comparison across int and float |
| `0.1 + 0.2 == 0.3` | `False` | floating-point error |

</div>

**Tuple (simultaneous) assignment:** `a, b = b, a + b` evaluates the **whole right side first** using the old values, then assigns.

### List / dict / set cheat sheet

| Code | Result |
|---|---|
| `[1,2,3].append([4,5])` | `[1, 2, 3, [4, 5]]` (length 4) |
| `[1,2,3].extend([4,5])` | `[1, 2, 3, 4, 5]` |
| `[1,2,3].extend("ab")` | `[1, 2, 3, 'a', 'b']` (iterates the string) |
| `L.sort()` | sorts in place, **returns `None`** |
| `sorted(L)` | returns a new sorted list |
| `"GATE2027"[::-1]` | `'7202ETAG'` |
| `"GATE2027"[1:6:2]` | `'AE0'` (indices 1, 3, 5) |
| `d.get(k, 0)` | value, or `0` if key missing (no error) |
| `{1,2,3} - {2}` | `{1, 3}` |
| `{1,2} \| {3}`, `{1,2} & {2,3}`, `{1,2} ^ {2,3}` | `{1,2,3}`, `{2}`, `{1,3}` |
| `list(range(10, 0, -3))` | `[10, 7, 4, 1]` |
| `m = map(f, L)` | lazy iterator, usable **once**: a second `list(m)` gives `[]` |

**`for … else`:** the `else` runs only if the loop finished **without** `break`.

**Changing a list while looping over it** skips elements:

```python
L = [1, 2, 2, 3]
for v in L:
    if v == 2: L.remove(v)
print(L)     # [1, 2, 3]  ← the second 2 got skipped
```

### Built-in operation costs

| Operation | list | dict / set |
|---|---|---|
| index / lookup `x[i]`, `d[k]` | $O(1)$ | $O(1)$ average |
| `x in …` | $O(n)$ | $O(1)$ average |
| `append` / add | $O(1)$ amortised | $O(1)$ average |
| `insert(0, x)`, `pop(0)` | $O(n)$ | — |
| `pop()` from the end | $O(1)$ | — |
| slicing `L[a:b]` | $O(b-a)$ (it copies) | — |
| `len` | $O(1)$ | $O(1)$ |
| `sum`, `min`, `max` | $O(n)$ | $O(n)$ |

---

## Summary: important points

<div class="formula">

1. Variables are tags on objects. `is` checks the object, `==` checks the value.
2. `append`, `extend`, `+=` on a list, and `L[i]=…` **mutate**. `L = …` and `L = L + …` **rebind**.
3. A default argument is created **once**, when `def` runs.
4. Each call to an outer function creates a **new** closure environment.
5. `a, b, c = …`: evaluate the whole right side first.
6. `/` gives a float, `//` floors, and `%` takes the sign of the divisor.
7. `[[0]*n]*m` repeats one inner list m times. Use a comprehension instead.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2026 Q16 (1 mark, MCQ)

```python
def append_to_lst(val, lst=[]):
    lst.append(val)
    return lst

print(append_to_lst(1))
print(append_to_lst(2))
print(append_to_lst(3, []))
```

<details>
<summary>Solution: answer (B) [1] / [1, 2] / [3]</summary>

1. The default `[]` is created once, when `def` runs. Call it $D$.
2. `append_to_lst(1)`: `lst` is $D$, so $D$ becomes `[1]`. Prints `[1]`.
3. `append_to_lst(2)`: `lst` is still $D$, so $D$ becomes `[1, 2]`. Prints `[1, 2]`.
4. `append_to_lst(3, [])`: a fresh list is passed, so `[3]`. $D$ is untouched.

**Idea tested:** mutable default argument (§1.4).

</details>

### GATE DA 2026 Q50 (2 marks, MSQ)

```python
def outer():
    x = []
    def inner(val):
        x.append(val)
        return x
    return inner

f1 = outer()
f2 = outer()
print(f1(10))  # Line P
print(f1(20))  # Line Q
print(f2(30))  # Line R
print(f1(40))  # Line S
```

(A) `f1` and `f2` share the same list `x` (B) Line Q prints `[10, 20]` (C) Line R prints `[10, 20, 30]` (D) Line S prints `[10, 20, 40]`

<details>
<summary>Solution: answer B; D</summary>

Each call to `outer()` runs `x = []` again, so `f1` and `f2` each have their **own** list. Call them $x_1$ and $x_2$.

| Line | Call | $x_1$ | $x_2$ | Printed |
|---|---|---|---|---|
| P | `f1(10)` | `[10]` | `[]` | `[10]` |
| Q | `f1(20)` | `[10, 20]` | `[]` | `[10, 20]` |
| R | `f2(30)` | `[10, 20]` | `[30]` | `[30]` |
| S | `f1(40)` | `[10, 20, 40]` | `[30]` | `[10, 20, 40]` |

(A) is false because the lists are separate. (C) is false because it prints `[30]`. **B and D are true.**

**Idea tested:** closures (§1.5). Compare with Q16: a default argument is created once per `def`, while a local in `outer` is created once per *call* to `outer`.

</details>

### GATE DA 2025 Q23 (1 mark, MCQ)

`A = [1,2,3]`, `B = [4,5,6]`. Which gives `A = [1,2,3,4,5,6]`?
(A) `A.extend(B)` (B) `A.append(B)` (C) `A.update(B)` (D) `A.insert(B)`

<details>
<summary>Solution: answer (A)</summary>

- `extend` adds each element of `B`, giving `[1,2,3,4,5,6]`. Correct.
- `append(B)` adds `B` as **one** element, giving `[1,2,3,[4,5,6]]`.
- Lists have no `update` method (that's for dict/set), so it's an `AttributeError`.
- `insert` needs two arguments, `insert(i, x)`, so it's a `TypeError`.

</details>

### GATE DA 2025 Q47 (2 marks, MCQ)

```python
A = {"this", "that"}
B = {"that", "other"}
C = {"other", "this"}
while "other" in C:
    if "this" in A:
        A, B, C = A - B, B - C, C - A
    if "that" in B:
        A, B, C = C | A, A | B, B | C
```

At the end, which sets contain `"this"`? (A) only A (B) only B (C) only C (D) A and C

<details>
<summary>Solution: answer (B) only B</summary>

Key rule: in `A, B, C = …`, **all three right sides use the old values** (§1.6).

**Iteration 1.** `"other"` is in C, so the loop body runs.

- `"this"` in A: yes.
  - A − B = {this, that} − {that, other} = **{this}**
  - B − C = {that, other} − {other, this} = **{that}**
  - C − A = {other, this} − {this, that} = **{other}**
- `"that"` in B = {that}: yes.
  - C ∪ A = {other} ∪ {this} = **{this, other}**
  - A ∪ B = {this} ∪ {that} = **{this, that}**
  - B ∪ C = {that} ∪ {other} = **{that, other}**

**Iteration 2.** C = {that, other} contains `"other"`, so the body runs again.

- `"this"` in A = {this, other}: yes.
  - A − B = {this, other} − {this, that} = **{other}**
  - B − C = {this, that} − {that, other} = **{this}**
  - C − A = {that, other} − {this, other} = **{that}**
- `"that"` in B = {this}: no.

**Check.** C = {that} has no `"other"`, so the loop stops.

Final: A = {other}, B = {this}, C = {that}. Only **B** contains `"this"`.

</details>

### GATE DA 2025 Q63 (2 marks, NAT)

```python
def f(a, b):
    if (a == 0):
        return b
    if (a % 2 == 1):
        return 2 * f((a - 1) / 2, b)
    return b + f(a - 1, b)

print(f(15, 10))
```

<details>
<summary>Solution: answer 160</summary>

`/` produces floats, but `7.0 % 2 == 1` is still `True` and `0.0 == 0` is `True`, so the float type doesn't change the path taken.

| Call | `a` odd? | Returns |
|---|---|---|
| `f(15, 10)` | yes | `2 * f(7.0, 10)` |
| `f(7.0, 10)` | yes | `2 * f(3.0, 10)` |
| `f(3.0, 10)` | yes | `2 * f(1.0, 10)` |
| `f(1.0, 10)` | yes | `2 * f(0.0, 10)` |
| `f(0.0, 10)` | base case | `10` |

Unwind: $10 \to 20 \to 40 \to 80 \to 160$.

**Shortcut:** $15 = 1111_2$. Every step takes the odd branch, so the answer is $2^4 \times 10 = 160$.

</details>

---

## Test yourself (B): predicted 2027-style questions

These follow the PYQ patterns above. Try each one on paper before opening the solution.

**P1 (1 mark, NAT).** What's printed?

```python
a = [1, 2, 3]
b = a
b += [4]
b = b + [5]
print(len(a))
```

<details>
<summary>Answer: 4</summary>

`b += [4]` mutates the shared list, so `a` becomes `[1,2,3,4]`. `b = b + [5]` builds a new list and moves only `b`. So `len(a)` is **4**.

</details>

**P2 (1 mark, MCQ).** `print(-17 // 5, -17 % 5)`
(A) `-3 -2` (B) `-4 3` (C) `-3 2` (D) `-4 -3`

<details>
<summary>Answer: (B)</summary>

$-17/5 = -3.4$, and the floor of that is $-4$. Then $-17 - (-4)(5) = -17 + 20 = 3$. Check: $(-4)(5) + 3 = -17$. ✓

</details>

**P3 (2 marks, MSQ).** Which statements are true after this code runs?

```python
g = [[0] * 2] * 3
g[1][0] = 5
h = [row[:] for row in g]
h[0][1] = 7
```

(A) `g == [[5,0],[5,0],[5,0]]` (B) `h[2] == [5, 0]` (C) `g[0][1] == 7` (D) `h[1] == [5, 7]`

<details>
<summary>Answer: A; B</summary>

- `g` holds the **same** inner list three times, so `g[1][0] = 5` shows up in every row. (A) is true.
- `h` copies each row separately, so `h` has three independent `[5, 0]` lists. (B) is true.
- `h[0][1] = 7` changes only `h[0]`. `g` is untouched, so (C) is false, and `h[1]` is still `[5, 0]`, so (D) is false.

</details>

**P4 (2 marks, NAT).** What's printed?

```python
def f(x, acc=[]):
    acc.append(x)
    return sum(acc)

f(1); f(2)
print(f(3) + f(4, []))
```

<details>
<summary>Answer: 10</summary>

The shared default grows to `[1]`, then `[1, 2]`, then `[1, 2, 3]`, so `f(3)` returns $6$. `f(4, [])` uses a fresh list and returns $4$. Total: $6 + 4 = 10$.

</details>

**P5 (2 marks, NAT).** What's printed?

```python
def make():
    count = 0
    def step():
        nonlocal count
        count += 2
        return count
    return step

s1 = make(); s2 = make()
s1(); s1(); s2()
print(s1() * 10 + s2())
```

<details>
<summary>Answer: 64</summary>

`s1` and `s2` each have their own `count`.

- `s1` is called 3 times in total, so its last return is $6$.
- `s2` is called 2 times, so its last return is $4$.

$6 \times 10 + 4 = 64$.

</details>

**P6 (1 mark, MCQ).** What's printed?

```python
x = 5
def f():
    print(x)
    x = 10
f()
```

(A) `5` (B) `10` (C) `UnboundLocalError` (D) `None`

<details>
<summary>Answer: (C)</summary>

Because `x` is assigned somewhere inside `f`, Python treats `x` as local for the **whole** function body. The `print(x)` line reads that local before it has a value, which raises `UnboundLocalError`.

</details>
