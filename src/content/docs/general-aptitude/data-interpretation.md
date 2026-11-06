---
title: 6. Data interpretation
description: Reading pie charts, bar charts, histograms, grids and tables quickly; percentage-of-total, weighted averages from frequency charts, and common traps.
sidebar:
  label: 6. Data interpretation
  order: 6
---

**Why it matters:** a data-interpretation question appeared every year:
- 2024 Q5: a pie chart with invalid votes;
- 2025 Q3: counting cells in a pixel grid;
- 2025 Q10: an average from a histogram.

The arithmetic is light. The marks are lost by **reading the wrong base** (the total) or skipping a step.

## Topic map

<div class="mindmap">

- **Data interpretation**
  - Pie chart
    - share × **correct** total (valid, not cast)
  - Bar chart / histogram
    - frequency-weighted mean $= \sum f_ix_i / \sum f_i$
    - linear transform: mean of $aX + b$ = $a\,\bar X + b$
  - Tables & grids
    - count systematically, row by row
  - Quick checks
    - estimate first, then compute
    - read the units and the base of every percentage

</div>

## 6.1 Pie charts: find the right total first

<!-- fig:ga-pie-q5 -->
<figure class="diagram"><svg class="dg" viewBox="0 0 600 240" role="img" aria-label="Pie chart of valid vote shares" xmlns="http://www.w3.org/2000/svg"><path d="M160,120 L160.0,25.0 A95,95 0 0 1 215.8,196.9 Z" style="fill:var(--gd-ink);fill-opacity:.35;stroke:var(--gd-surface);stroke-width:2"/><text class="title" x="216.0" y="106.8" text-anchor="middle">A 40%</text><path d="M160,120 L215.8,196.9 A95,95 0 0 1 83.1,175.8 Z" style="fill:var(--gd-hl-strong);fill-opacity:.9;stroke:var(--gd-surface);stroke-width:2"/><text class="title" x="150.8" y="183.2" text-anchor="middle">B 25%</text><path d="M160,120 L83.1,175.8 A95,95 0 0 1 83.1,64.2 Z" style="fill:var(--gd-trap);fill-opacity:.9;stroke:var(--gd-surface);stroke-width:2"/><text class="title" x="101.1" y="125.0" text-anchor="middle">C 20%</text><path d="M160,120 L83.1,64.2 A95,95 0 0 1 160.0,25.0 Z" style="fill:var(--sl-color-gray-4);fill-opacity:.35;stroke:var(--gd-surface);stroke-width:2"/><text class="title" x="133.3" y="72.5" text-anchor="middle">D 15%</text><text class="t-mut" x="300" y="60">votes cast</text><text class="" x="430" y="60">1,15,000</text><text class="t-mut" x="300" y="88">invalid</text><text class="" x="430" y="88">− 5,000</text><text class="t-mut" x="300" y="116">valid</text><text class="" x="430" y="116">1,10,000</text><text class="t-ink" x="300" y="144">B + C = 45%</text><text class="t-ink" x="430" y="144">0.45 × 1,10,000</text><text class="t-ink" x="300" y="172"></text><text class="t-ink" x="430" y="172">= 49,500</text></svg><figcaption>The 2024 Q5 data redrawn: shares of the 1,10,000 valid votes (1,15,000 cast minus 5,000 invalid). B and C together hold 25% + 20% = 45%, which is 49,500 votes.</figcaption></figure>
<!-- /fig:ga-pie-q5 -->

Percentages in a pie chart are shares of **whatever the chart represents**: valid votes here, not all votes cast. Subtract the excluded part **before** applying the percentages.

## 6.2 Histograms and frequency charts

<!-- fig:ga-hist-q10 -->
<figure class="diagram"><svg class="dg" viewBox="0 0 640 262" role="img" aria-label="Histogram of patients per shift" xmlns="http://www.w3.org/2000/svg"><path class="ax" d="M60,20 V220 H440"/><text x="250.0" y="252" text-anchor="middle">patients per shift (X)</text><text x="22" y="120.0" text-anchor="middle" transform="rotate(-90 22 120.0)">number of shifts</text><line class="grid" x1="60.0" y1="180.0" x2="440.0" y2="180.0"/><text class="t-mut" x="54.0" y="184.0" text-anchor="end">10</text><line class="grid" x1="60.0" y1="140.0" x2="440.0" y2="140.0"/><text class="t-mut" x="54.0" y="144.0" text-anchor="end">20</text><line class="grid" x1="60.0" y1="100.0" x2="440.0" y2="100.0"/><text class="t-mut" x="54.0" y="104.0" text-anchor="end">30</text><line class="grid" x1="60.0" y1="60.0" x2="440.0" y2="60.0"/><text class="t-mut" x="54.0" y="64.0" text-anchor="end">40</text><line class="grid" x1="60.0" y1="20.0" x2="440.0" y2="20.0"/><text class="t-mut" x="54.0" y="24.0" text-anchor="end">50</text><rect class="box-ink" x="92.3" y="140.0" width="44" height="80.0" rx="3" style="opacity:.85"/><text class="t-ink" x="114.3" y="134.0" text-anchor="middle">20</text><text class="t-mut" x="114.3" y="235.0" text-anchor="middle">5</text><rect class="box-ink" x="182.8" y="60.0" width="44" height="160.0" rx="3" style="opacity:.85"/><text class="t-ink" x="204.8" y="54.0" text-anchor="middle">40</text><text class="t-mut" x="204.8" y="235.0" text-anchor="middle">6</text><rect class="box-ink" x="273.2" y="100.0" width="44" height="120.0" rx="3" style="opacity:.85"/><text class="t-ink" x="295.2" y="94.0" text-anchor="middle">30</text><text class="t-mut" x="295.2" y="235.0" text-anchor="middle">7</text><rect class="box-ink" x="363.7" y="180.0" width="44" height="40.0" rx="3" style="opacity:.85"/><text class="t-ink" x="385.7" y="174.0" text-anchor="middle">10</text><text class="t-mut" x="385.7" y="235.0" text-anchor="middle">8</text><text class="t-ink" x="470" y="80">mean X = 6.3</text><text class="t-mut" x="470" y="104">earning = 1000(X − 0.2)</text><text class="t-ink" x="470" y="128">average = ₹6,100</text></svg><figcaption>The 2025 Q10 histogram redrawn: 100 shifts with 5, 6, 7 or 8 patients. The mean is (5·20 + 6·40 + 7·30 + 8·10)/100 = 6.3 patients, so the average earning is 1000 × (6.3 − 0.2) = ₹6,100.</figcaption></figure>
<!-- /fig:ga-hist-q10 -->

<div class="formula">

$$
\bar X = \frac{\sum_i f_i\,x_i}{\sum_i f_i}
\qquad\qquad
\text{mean of } (aX + b) = a\bar X + b
$$

You don't need to compute every shift's earnings separately. Find the mean of $X$ once, then apply the linear formula.

</div>

## 6.3 Tables and grids

- Count **row by row** and write the running total. 2025 Q3's 4 × 4 grid has 4 + 3 + 2 + 2 = 11 cells with $U \le 4$.
- For "percentage increase from year 1 to year 2", the base is **year 1**.
- For "share of total", the base is the **column or row total**, so check which one the question means.

---

## Summary: important points

<div class="formula">

1. Identify the **base** of every percentage (valid vs cast, previous year vs this year).
2. Histogram mean $= \sum f x / \sum f$. Mean of $aX + b$ is $a\bar X + b$.
3. Count grids row by row with a running total.
4. Estimate before computing, so you can reject options that are clearly off.

</div>

---

## Test yourself (A): previous-year questions

### GATE 2024 Q5 (1 mark)

1,15,000 votes were cast, of which 5,000 were invalid. Valid shares: A 40%, B 25%, C 20%, D 15%. How many valid votes did B and C receive together?

<details>
<summary>Show solution</summary>

**Answer: 49,500**

Valid votes: $1{,}10{,}000$. B + C $= 45\% \times 1{,}10{,}000 = 49{,}500$. (Using 1,15,000 gives 51,750, option C, which is the trap.)

</details>

### GATE 2025 Q3 (1 mark)

A 4 × 4 image has rows (0, 1, 0, 2), (4, 7, 3, 3), (5, 5, 4, 4), (6, 7, 3, 2). How many pixels have $U \le 4$?

<details>
<summary>Show solution</summary>

**Answer: 11**

Row by row: 4, then 3 (4, 3, 3), then 2 (4, 4), then 2 (3, 2). Total $4 + 3 + 2 + 2 = 11$.

</details>

### GATE 2025 Q10 (2 marks)

Over 100 shifts, the number of patients was 5 (20 shifts), 6 (40), 7 (30) and 8 (10). Earnings per shift are ₹1000(X − 0.2). What are the average earnings per shift?

<details>
<summary>Show solution</summary>

**Answer: ₹6,100**

$\bar X = \frac{100 + 240 + 210 + 80}{100} = 6.3$, and $1000(6.3 - 0.2) = 6100$.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1.** The sample mean of 50 data points is 40. A new point, 142, is added. What is the new mean?

<details>
<summary>Show solution</summary>

**Answer: 42**

$\frac{50 \times 40 + 142}{51} = \frac{2142}{51} = 42$. (This was a 2024 core-section question in the same style.)

</details>

**F2.** Sales were 400 units in 2023 and 500 in 2024. What is the percentage increase, and by what percentage would sales have to fall in 2025 to return to 400?

<details>
<summary>Show solution</summary>

**Answer: 25% increase, then a 20% decrease**

The bases differ: $100/400 = 25\%$ but $100/500 = 20\%$.

</details>

**F3.** A pie chart shows a company's spending: salaries 45%, rent 15%, the rest other costs. Total spending is ₹8 lakh. How much more goes to salaries than to rent?

<details>
<summary>Show solution</summary>

**Answer: ₹2.4 lakh**

$30\% \times 8 = 2.4$.

</details>
