---
title: 8. Spatial aptitude & geometry
description: Dice and their nets, map colouring, cross-sections of solids, assembling pieces, polygon and circle geometry (inscribed angles, areas), and quick mensuration formulas.
sidebar:
  label: 8. Spatial & geometry
  order: 8
---

**Why it matters:** this is the second-largest GA block, with 6 PYQs, and **every year** has at least one:
- 2024 Q2: map colouring;
- 2024 Q9: a dice net;
- 2024 Q10: a double cone's cross-section;
- 2025 Q8: a dodecagon;
- 2026 Q3: assembling puzzle pieces;
- 2026 Q10: a kite in a circle.

These look visual, but most can be solved with **one rule**.

## Topic map

<div class="mindmap">

- **Spatial & geometry**
  - Dice
    - opposite faces never appear together
    - nets: faces two apart in a strip are opposite
  - Colouring
    - three mutually touching regions need 3 colours
    - a region touching all three needs a 4th; 4 always suffice
  - Solids
    - cross-sections through the axis
  - Assembling / folding / cutting
    - count notches and edges, match boundaries
  - Plane geometry
    - inscribed angle = ½ central angle
    - triangle area $\frac12 ab\sin C$, kite area $\frac12 d_1d_2$
    - regular n-gon split into n central triangles

</div>

## 8.1 Dice and nets

<div class="formula">

1. **Opposite faces never show together.** From several views, the face that appears with **all** the others' neighbours but never with face X is X's opposite.
2. **In a net**, two squares with **exactly one square between them in a straight line** are opposite. Flaps attached on **opposite sides** of a strip are opposite each other.
3. Eliminate any net whose opposite pairs contradict the views.

</div>

<!-- fig:ga-dice-net -->
<figure class="diagram"><svg class="dg" viewBox="0 0 560 200" role="img" aria-label="Dice net with opposite faces" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="60" y="20" width="40" height="40" style="stroke:var(--gd-ink)"/><text class="title" x="80.0" y="45.0" text-anchor="middle" style="font-size:15px">5</text><rect class="box" x="100" y="20" width="40" height="40" style="stroke:var(--gd-ink)"/><text class="title" x="120.0" y="45.0" text-anchor="middle" style="font-size:15px">1</text><rect class="box" x="100" y="60" width="40" height="40" style="stroke:var(--gd-ink)"/><text class="title" x="120.0" y="85.0" text-anchor="middle" style="font-size:15px">4</text><rect class="box" x="100" y="100" width="40" height="40" style="stroke:var(--gd-ink)"/><text class="title" x="120.0" y="125.0" text-anchor="middle" style="font-size:15px">6</text><rect class="box" x="100" y="140" width="40" height="40" style="stroke:var(--gd-ink)"/><text class="title" x="120.0" y="165.0" text-anchor="middle" style="font-size:15px">2</text><rect class="box" x="140" y="140" width="40" height="40" style="stroke:var(--gd-ink)"/><text class="title" x="160.0" y="165.0" text-anchor="middle" style="font-size:15px">3</text><text class="t-ink" x="230" y="50" style="font-weight:700">1 ↔ 6</text><text class="t-mut" x="300" y="50">two apart in the column</text><text class="t-ink" x="230" y="84" style="font-weight:700">4 ↔ 2</text><text class="t-mut" x="300" y="84">two apart in the column</text><text class="t-ink" x="230" y="118" style="font-weight:700">5 ↔ 3</text><text class="t-mut" x="300" y="118">flaps on opposite sides</text><text class="t-mut" x="230" y="160">views: (5,4,1), (4,6,3), (2,6,5) are</text><text class="t-mut" x="230" y="178">each three mutually adjacent faces ✓</text></svg><figcaption>Reading opposite faces from a net. In a straight column of four squares, faces two apart are opposite (1–6 and 4–2 here). Squares attached to the column on opposite sides become the left and right faces, which are also opposite each other (5–3). This is net (A) of 2024 Q9: its pairs 1–6, 4–2, 5–3 match the three dice views.</figcaption></figure>
<!-- /fig:ga-dice-net -->

## 8.2 Map colouring

- The **minimum** number of colours is set by the most demanding cluster of mutually adjacent regions.
- Three regions that all touch each other force 3 colours. A further region touching all three forces a 4th.
- By the **four-colour theorem**, 4 colours always suffice for a flat map. So the answer is at most 4.

Regions that meet only at a corner point don't count as adjacent.

## 8.3 Solids and cross-sections

<!-- fig:ga-cone-kite -->
<figure class="diagram"><svg class="dg" viewBox="0 0 620 250" role="img" aria-label="Double cone cross-section and kite in a circle" xmlns="http://www.w3.org/2000/svg"><ellipse class="grid" cx="140" cy="120" rx="80" ry="18"/><path class="ax" d="M60,120 L140,30 L220,120 L140,210 Z"/><polygon points="140,30 220,120 140,210 60,120" style="fill:var(--gd-ink);fill-opacity:.15;stroke:var(--gd-ink);stroke-width:2.2"/><text class="t-ink" x="140" y="235" text-anchor="middle">cross-section: rhombus</text><circle class="grid" cx="450" cy="120" r="85" style="stroke:var(--sl-color-gray-3)"/><polygon points="450,120 389.9,180.1 450,35 510.1,180.1" style="fill:var(--gd-hl-strong);fill-opacity:.25;stroke:var(--gd-hl-strong);stroke-width:2"/><line class="mut" x1="450" y1="120" x2="450" y2="35"/><line class="mut" x1="389.9" y1="180.1" x2="510.1" y2="180.1"/><circle class="dot-ink" cx="450.0" cy="120.0" r="3.5"/><text class="title" x="460.0" y="136.0" text-anchor="middle">O</text><circle class="dot-ink" cx="389.9" cy="180.1" r="3.5"/><text class="title" x="375.9" y="184.1" text-anchor="middle">P</text><circle class="dot-ink" cx="450.0" cy="35.0" r="3.5"/><text class="title" x="450.0" y="27.0" text-anchor="middle">Q</text><circle class="dot-ink" cx="510.1" cy="180.1" r="3.5"/><text class="title" x="524.1" y="184.1" text-anchor="middle">R</text><text class="t-ink" x="450" y="235" text-anchor="middle">kite OPQR: area 50√2 cm²</text></svg><figcaption>Left: two identical cones sharing a base (2024 Q10). A plane through both vertices also passes through the axis, so it cuts the shape in two generators on each cone: four equal slant edges, which form a rhombus. Right: 2026 Q10. The inscribed angle PQR = 45° makes the central angle POR = 90°, so PR = 10√2; Q lies on the perpendicular bisector, so OPQR is a kite with diagonals OQ = 10 and PR = 10√2, giving area ½ · 10 · 10√2 = 50√2.</figcaption></figure>
<!-- /fig:ga-cone-kite -->

| Cut | Shape |
|---|---|
| a cone through its vertex and axis | triangle |
| a cone parallel to its base | circle |
| a cone at a slant, not through the base | ellipse |
| a double cone through both vertices | **rhombus** |
| a cylinder through its axis | rectangle |
| a cube through two opposite edges | rectangle; three suitable midpoints give a hexagon |

## 8.4 Plane geometry essentials

<div class="formula">

- **Inscribed angle theorem:** an inscribed angle is **half** the central angle on the same arc. ∠PQR = 45° gives ∠POR = 90°.
- Chord: $2r\sin(\theta/2)$ for a central angle $\theta$. For $\theta = 90°$, that's $r\sqrt2$.
- Triangle area $= \frac12 ab\sin C$. For a central triangle of a regular $n$-gon: $\frac12 r^2\sin(360°/n)$.
- **Kite** (or dart) with perpendicular diagonals $d_1, d_2$: area $= \frac12 d_1 d_2$.
- Regular $n$-gon in a circle of radius $r$: area $= \frac n2 r^2 \sin\frac{360°}{n}$. A dodecagon gives $3r^2$.
- Sector area $= \frac{\theta}{360°}\pi r^2$.

</div>

## 8.5 Assembling pieces (2026 Q3 style)

Compare **boundary features**: the number of notches, curved edges, straight cuts and angles. A candidate figure is possible only if every notch and curve in it can be matched to a piece. Eliminate a figure as soon as one feature can't be produced.

---

## Summary: important points

<div class="formula">

1. Dice: faces seen together are adjacent. In a net, squares two apart in a strip are opposite.
2. Colouring: find mutually adjacent triples, and a region touching all three. 4 colours always suffice.
3. A double cone cut through both vertices gives a rhombus.
4. An inscribed angle is half the central angle. A kite's area is $\frac12 d_1d_2$.
5. A regular 12-gon is 12 central triangles of area $\frac{r^2}{4}$ each, so its total area is $3r^2$.

</div>

---

## Test yourself (A): previous-year questions

### GATE 2024 Q2 (1 mark)

A figure has 15 parts:
- a circle split into 3 sectors;
- inside a square, 4 regions around the circle;
- outside the square, inside an ellipse, 4 side regions and 4 corner regions.

Adjacent parts (sharing an edge, not just a corner) must differ in colour. What is the minimum number of colours?

<details>
<summary>Show solution</summary>

**Answer: 4**

- The 3 sectors all touch each other, so they need colours a, b, c.
- The top ring region touches the two upper sectors, so it must be c.
- The left ring region touches one upper sector and the bottom sector, which forces its colour. Likewise for the right ring region.
- The **bottom ring region** then touches the bottom sector **and** the left and right ring regions, which use all three of a, b, c. It needs a **4th** colour.

Four colours suffice for the rest. I checked this with an exhaustive colouring search: 3 colours fail and 4 succeed.

</details>

### GATE 2024 Q9 (2 marks)

Three views of a die show (5, 4, 1), (4, 6, 3) and (2, 6, 5). Which net folds into this die?

<details>
<summary>Show solution</summary>

**Answer: (A)**

- 4 appears with 5, 1, 6 and 3, so its opposite is **2**.
- 6 appears with 4, 3, 2 and 5, so its opposite is **1**.
- That leaves **5–3** as the third pair.

Net (A), drawn in §8.1, has exactly these opposite pairs.

</details>

### GATE 2024 Q10 (2 marks)

Two identical cones share a base, one inverted over the other. A plane passes through both vertices. What shape is the cross-section?

<details>
<summary>Show solution</summary>

**Answer: (A) a rhombus**

A plane through both vertices contains the common axis, so it cuts each cone along two slant generators. That gives four equal sides.

</details>

### GATE 2025 Q8 (2 marks)

A regular dodecagon is inscribed in a circle of radius $r$, and its 12 central triangles are used to make squares of side $r$, each triangle used once. How many squares can be formed, and with how many triangles each?

<details>
<summary>Show solution</summary>

**Answer: (A)** 3 squares, 4 triangles each

Each triangle has area $\frac12 r^2\sin 30° = \frac{r^2}{4}$. A square of side $r$ has area $r^2$, so it needs **4** triangles, and $12/4 = $ **3** squares can be made.

</details>

### GATE 2026 Q10 (2 marks)

P, Q and R lie on a circle of radius 10 with centre O. PQ = RQ and ∠PQR = 45°. What is the area of PQRO?

<details>
<summary>Show solution</summary>

**Answer: $50\sqrt2$ cm²**

- ∠POR $= 2 \times 45° = 90°$, so PR $= 10\sqrt2$.
- PQ = RQ puts Q on the perpendicular bisector of PR, so OQ ⟂ PR, and OQ $= 10$.
- OPQR is a kite with perpendicular diagonals. (O lies inside triangle PQR, so it's a concave kite, but $\frac12 d_1d_2$ still applies: it equals area(PQR) − area(POR).)
- Area $= \frac12 \times 10 \times 10\sqrt2 = 50\sqrt2$.

</details>

### GATE 2026 Q3 (1 mark)

Four black pieces must assemble one of four square figures P, Q, R, S without overlap. **Answer: (A) P.** Match the curved notch, the two triangular bumps and the slanted cuts of each piece against each figure's white cut-outs. Only P has every cut-out produced by exactly the four pieces.

---

## Test yourself (B): predicted 2027-style questions

**F1.** A regular hexagon is inscribed in a circle of radius 4 cm. What is its area? (Leave √3 in the answer.)

<details>
<summary>Show solution</summary>

**Answer: $24\sqrt3$ cm²**

$\frac62 \times 16 \times \sin 60° = 48 \times \frac{\sqrt3}{2} = 24\sqrt3$.

</details>

**F2.** An inscribed angle subtends an arc whose central angle is 140°. What is the inscribed angle?

<details>
<summary>Show solution</summary>

**Answer: 70°**

</details>

**F3.** A cube is painted on all faces and cut into 27 equal small cubes. How many small cubes have exactly two painted faces?

<details>
<summary>Show solution</summary>

**Answer: 12**

These are the edge-middle cubes: one per edge, and a cube has 12 edges.

</details>

**F4.** A strip net reads 1-2-3-4 in a column, with 5 to the left of 2 and 6 to the right of 3. What is opposite 5?

<details>
<summary>Show solution</summary>

**Answer: 6**

Flaps on opposite sides of the strip are opposite faces. (Also: 1–3 and 2–4 are opposite.)

</details>
