---
title: 7. Analytical reasoning & logic puzzles
description: Systematic case analysis for arrangement and tournament puzzles, Venn-region rules, reasoning about monotonic functions, syllogisms, and number relations.
sidebar:
  label: 7. Analytical reasoning
  order: 7
---

**Why it matters:**
- 2025 Q4: a rule for the regions of overlapping shapes;
- 2025 Q7: two people with the same weight on an increasing-then-decreasing function;
- 2026 Q8: a three-game chess elimination puzzle.

They look different, but each is solved by **turning the words into constraints and checking cases**. I brute-forced every possibility for each one to confirm the answers.

## Topic map

<div class="mindmap">

- **Analytical reasoning**
  - Translate
    - list the entities, attributes and every constraint
  - Case analysis
    - start with the most restrictive constraint
    - draw a table; eliminate
  - Patterns
    - region-sum rules in Venn figures
    - number relations, series rules
  - Functions & order
    - monotone pieces, a peak or a valley
  - Syllogisms
    - all / some / no with Venn diagrams

</div>

## 7.1 Method for logic puzzles

1. **List the entities and attributes.** Here: 4 students × {class, gender}.
2. **Write each constraint** as a short rule.
3. Start from the **most restrictive** rule. It usually fixes the first event.
4. **Branch** on the remaining choices and **kill branches** that break a rule.
5. Answer only after **one** branch survives, or after checking that all surviving branches agree.

**Elimination games:** "a loser plays no more games" means **each game removes one player**. With 4 players and 3 games, exactly **one** player never loses.

## 7.2 Region rules in overlapping figures

<!-- fig:ga-venn-q4 -->
<figure class="diagram"><svg class="dg" viewBox="0 0 700 240" role="img" aria-label="Overlapping shapes with region sums" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="40" y="60" width="250" height="150" style="fill:var(--gd-ink);fill-opacity:.06;stroke:var(--gd-ink)"/><polygon points="260,20 390,215 120,215" style="fill:var(--gd-hl-strong);fill-opacity:.08;stroke:var(--gd-hl-strong);stroke-width:1.6"/><ellipse cx="240" cy="160" rx="120" ry="70" style="fill:var(--gd-trap);fill-opacity:.06;stroke:var(--gd-trap);stroke-width:1.6"/><text class="title" x="70" y="100" text-anchor="middle" style="font-weight:700">1</text><text class="title" x="300" y="55" text-anchor="middle" style="font-weight:700">2</text><text class="title" x="240" y="222" text-anchor="middle" style="font-weight:700">3</text><text class="title" x="160" y="150" text-anchor="middle" style="font-weight:700">4</text><text class="t-ink" x="245" y="160" text-anchor="middle" style="font-weight:700">P = 6</text><text class="t-ink" x="320" y="160" text-anchor="middle" style="font-weight:700">Q = 5</text><text class="t-ink" x="255" y="85" text-anchor="middle" style="font-weight:700">R = 3</text><text class="t-mut" x="410" y="60">rectangle = 1, triangle = 2, ellipse = 3</text><text class="t-mut" x="410" y="88">rect ∩ ellipse = 1 + 3 = 4 ✓</text><text class="t-ink" x="410" y="116">P = rect ∩ tri ∩ ellipse = 6</text><text class="t-ink" x="410" y="144">Q = tri ∩ ellipse = 5</text><text class="t-ink" x="410" y="172">R = rect ∩ tri = 3</text></svg><figcaption>The rule in 2025 Q4: each region carries the sum of the numbers of the shapes that contain it (rectangle 1, triangle 2, ellipse 3). Rectangle ∩ ellipse = 1 + 3 = 4 (given), so all three = 6 (P), triangle ∩ ellipse = 5 (Q), rectangle ∩ triangle = 3 (R).</figcaption></figure>
<!-- /fig:ga-venn-q4 -->

Test a hypothesis (the sum, the product, a count) on the **given** labelled regions, and only then fill in the unknowns.

## 7.3 Reasoning with an increasing-then-decreasing function

If $w(a)$ **increases** up to 50 and **decreases** after it, then each weight value (except the peak) is reached at **exactly two** ages, one on each side of 50. So two different ages with the same weight must satisfy $a_1 < 50 < a_2$.

## 7.4 Syllogisms (all / some / no)

| Premises | Valid conclusion |
|---|---|
| All A are B. All B are C. | All A are C. |
| All A are B. Some C are A. | Some C are B. |
| No A is B. All C are A. | No C is B. |
| Some A are B. Some B are C. | **Nothing** definite about A and C. |

Draw the Venn diagram in the **least favourable** way. A conclusion is valid only if it holds in **every** diagram consistent with the premises.

---

## Summary: important points

<div class="formula">

1. Convert the words into rules. Start from the most restrictive one, branch, and eliminate.
2. Elimination tournaments: each game removes one player, so with $n$ players and $n - 1$ games, exactly one player never loses.
3. Region puzzles: infer the rule from the known regions, then apply it.
4. Increasing-then-decreasing (unimodal) function: equal values occur on opposite sides of the peak.
5. Syllogisms: a conclusion is valid only if every possible diagram supports it.

</div>

---

## Test yourself (A): previous-year questions

### GATE 2026 Q8 (2 marks)

Rishi and Swathi are in Class 5, Pavan and Tanvi in Class 4. Rishi and Pavan are boys. Three games were played one after another, and a loser played no more games. (i) Only the first game was between students of the same class. (ii) Class-5 students won more games than Class-4 students. (iii) Boys won two games and girls won one. Who never lost?

<details>
<summary>Show solution</summary>

**Answer: (D) Tanvi**

1. **Game 1 can't be Pavan vs Tanvi.** If it were, Class 4 would win game 1, so Class 5 must win games 2 and 3. Game 2 is then the surviving Class-4 player vs a Class-5 player, and the Class-4 player loses. That leaves only the two Class-5 students for game 3, a same-class game, which breaks rule (i). So **game 1 is Rishi vs Swathi**.
2. **The winner of game 1 (call it W) must also win game 2.** Game 2 is W vs a Class-4 student. If W lost, game 3 would be between the two Class-4 students, which breaks (i). So Class 5 has 2 wins, satisfying (ii), and game 3 is W vs the last Class-4 student.
3. **Who is W?** If W = Swathi, girls would already have 2 wins, breaking (iii). So **W = Rishi**: boys have 2 wins, and game 3 must be won by a girl. That means Rishi's opponent in game 3 is **Tanvi**, and Tanvi wins.

The only schedule is: Rishi beats Swathi, Rishi beats Pavan, Tanvi beats Rishi. **Tanvi** never lost. A brute-force search over all game orders and winners finds exactly this one schedule.

</details>

### GATE 2025 Q4 (1 mark)

In the figure, the rectangle is 1, the triangle 2, the ellipse 3, and one region is labelled 4. Find P, Q and R.

<details>
<summary>Show solution</summary>

**Answer: (A) P = 6, Q = 5, R = 3**

The region labelled 4 lies in the rectangle and the ellipse: $1 + 3 = 4$. So the rule is "sum of the containing shapes". That gives P (all three) = 6, Q (triangle ∩ ellipse) = 5, and R (rectangle ∩ triangle) = 3.

</details>

### GATE 2025 Q7 (2 marks)

Two brothers share a weight-vs-age function that increases until age 50 and then decreases. At ages $a_1 < a_2$ they have the same weight. Which is correct?

<details>
<summary>Show solution</summary>

**Answer: (B) $a_1 < 50 < a_2$**

On each monotone piece, weight is one-to-one with age. So two **different** ages with equal weight can't both be on the same side of 50.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1.** Five players play a knockout chain where the loser of each game leaves. How many games are needed to leave one unbeaten player?

<details>
<summary>Show solution</summary>

**Answer: 4**

Each game removes exactly one player.

</details>

**F2.** "All engineers are graduates. Some graduates are artists." Which conclusion follows?
(A) Some engineers are artists (B) All artists are graduates (C) No engineer is an artist (D) None of these

<details>
<summary>Show solution</summary>

**Answer: (D)**

The artists may overlap graduates who aren't engineers. Nothing about engineers and artists is forced.

</details>

**F3.** In the 2025 Q4 figure, if the numbers were multiplied instead of added (rectangle 1, triangle 2, ellipse 3), what would P be?

<details>
<summary>Show solution</summary>

**Answer: 6**

$1 \times 2 \times 3 = 6$. This is why one data point (P alone) can't tell the two rules apart: you must check the region labelled 4, which gives $1 \times 3 = 3 \ne 4$, so the rule is addition.

</details>
