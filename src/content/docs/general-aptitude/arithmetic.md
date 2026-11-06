---
title: 4. Arithmetic — percentages, ratios, powers, logs & series
description: Percentage change and successive changes, rates of return, ratios and averages, exponent and logarithm laws, geometric series, digit puzzles and quick estimation.
sidebar:
  label: 4. Arithmetic
  order: 4
---

**Why it matters:** this is the **largest GA block**, with 7 PYQs:
- 2024 Q4: a split series;
- 2024 Q8: a rate of return;
- 2025 Q5: a percentage change in a rectangle;
- 2025 Q9: an exponent equation;
- 2026 Q2: digit product;
- 2026 Q4: comparing log powers;
- 2026 Q9: a digit puzzle.

Each takes one identity and careful arithmetic.

## Topic map

<div class="mindmap">

- **Arithmetic**
  - Percentages
    - change = (new − old)/old
    - successive changes multiply
    - area and volume scale with products
  - Ratios & averages
    - combining ratios, weighted average, average speed
  - Exponents
    - $a^m a^n = a^{m+n}$, $(a^m)^n = a^{mn}$; equate exponents on the same base
  - Logarithms
    - product, quotient, power, change of base
    - $a^{\log c} = c^{\log a}$
  - Series
    - arithmetic sum, geometric sum, infinite geometric $\frac{a}{1-r}$
  - Numbers
    - prime factorization, digit puzzles, divisibility

</div>

## 4.1 Percentages

<div class="formula">

- Percentage change $= \dfrac{\text{new} - \text{old}}{\text{old}} \times 100$.
- **Successive changes multiply:** $+a\%$ then $+b\%$ gives a factor of $(1 + a/100)(1 + b/100)$. For example, +20% then −20% gives $1.2 \times 0.8 = 0.96$, a **4% fall**, not zero.
- **Products scale by the product of factors:** a rectangle's area scales by (length factor) × (width factor). Widening by 10% raises the area by exactly 10%, but the perimeter and the diagonal by less.
- **Constant spending:** if the price rises by $r\%$, consumption must fall by $\dfrac{r}{100 + r} \times 100\%$ to keep spending the same (25% → 20%).
- **Return:** final amount = principal × (1 + rate). Compound interest: $P(1 + r)^n$. Simple interest: $Prn$.

</div>

<!-- fig:ga-rect-percent -->
<figure class="diagram"><svg class="dg" viewBox="0 0 720 195" role="img" aria-label="Effect of a 10 percent width increase on a rectangle" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="60" y="40" width="360" height="120" style="stroke:var(--gd-ink);stroke-width:1.6"/><rect x="60" y="28" width="360" height="12" style="fill:var(--gd-hl-strong);fill-opacity:.7"/><text class="title" x="240" y="105" text-anchor="middle">area L·W</text><text class="t-hl" x="430" y="38">+0.1W strip → +0.1·L·W</text><text class="t-mut" x="240" y="180" text-anchor="middle">L</text><text class="t-mut" x="44" y="104" text-anchor="middle">W</text><text class="t-ink" x="450" y="80" style="font-weight:600">area</text><text class="t-ink" x="530" y="80">+10%</text><text class="t-mut" x="450" y="106" style="font-weight:600">perimeter</text><text class="t-mut" x="530" y="106">+0.2W / (2L+2W) < 10%</text><text class="t-mut" x="450" y="132" style="font-weight:600">diagonal</text><text class="t-mut" x="530" y="132">< 10% (√(L² + 1.21W²))</text></svg><figcaption>Widening a rectangle by 10% (2025 Q5). The added strip has the same length L and width 0.1W, so the area grows by exactly 0.1·LW, i.e. 10%. The perimeter grows by only 0.2W/(2L + 2W) < 10%, and the diagonal by less than 10%.</figcaption></figure>
<!-- /fig:ga-rect-percent -->

## 4.2 Ratios and averages

- **Combining ratios:** if A : B = 2 : 3 and B : C = 4 : 5, scale B to a common value (12): A : B : C = 8 : 12 : 15.
- **Weighted average** $= \dfrac{\sum w_ix_i}{\sum w_i}$. Adding one value $v$ to $n$ values with mean $\bar x$ gives a new mean of $\dfrac{n\bar x + v}{n + 1}$.
- **Average speed** over equal distances is the **harmonic** mean $\dfrac{2uv}{u + v}$, not $\dfrac{u + v}{2}$. For 60 and 40 km/h, it's 48 km/h.

## 4.3 Exponents and logarithms

<div class="formula">

| Law | Exponents | Logarithms |
|---|---|---|
| Product | $a^ma^n = a^{m+n}$ | $\log(xy) = \log x + \log y$ |
| Quotient | $a^m/a^n = a^{m-n}$ | $\log(x/y) = \log x - \log y$ |
| Power | $(a^m)^n = a^{mn}$ | $\log x^k = k\log x$ |
| Change of base | | $\log_b x = \dfrac{\log_k x}{\log_k b}$, and $\log_b c \cdot \log_c d = \log_b d$ |
| **Swap identity** | | $a^{\log_b c} = c^{\log_b a}$ (take $\log_b$ of both sides) |

</div>

**Solving exponent equations:** write both sides with the **same base**, then equate the exponents. For $3^{x^2} = 27 \cdot 9^x = 3^{3 + 2x}$, that gives $x^2 - 2x - 3 = 0$.

## 4.4 Series

<div class="formula">

$$
\text{AP: } S_n = \frac n2\,(2a + (n - 1)d) \qquad
\text{GP: } S_n = a\,\frac{1 - r^n}{1 - r} \qquad
\text{infinite GP } (|r| < 1): S_\infty = \frac{a}{1 - r}
$$

</div>

**Mixed series:** split them into separate geometric series. In 2024 Q4, the terms $\frac12, \frac14, \frac18, \dots$ and $\frac13, \frac19, \frac1{27}, \dots$ are interleaved.

## 4.5 Number puzzles

- **Digit products:** factor into primes and assign them to digits 1–9. $70 = 2 \times 5 \times 7$, so the digits are 2, 5, 7 (since 1, 7, 10 isn't allowed).
- **Two-digit numbers:** $\overline{PQ} = 10P + Q$. Bound the range first (the result must have 3 digits), then test the few remaining cases.
- **Divisibility:** by 3 or 9, the digit sum; by 4, the last two digits; by 8, the last three; by 11, the alternating sum.

---

## Summary: important points

<div class="formula">

1. Successive percentage changes **multiply**: +20% then −20% gives −4%.
2. Area scales by the product of the side factors.
3. A price rise of $r\%$ needs a consumption fall of $\frac{r}{100 + r}$ to keep spending constant.
4. Average speed over equal distances is the harmonic mean $\frac{2uv}{u + v}$.
5. Equate exponents on the same base. $a^{\log c} = c^{\log a}$.
6. Infinite GP: $\frac{a}{1 - r}$. Split mixed series into separate GPs.
7. Digit puzzles: prime-factorize, bound the range, then check the few remaining candidates.

</div>

---

## Test yourself (A): previous-year questions

### GATE 2024 Q4 (1 mark)

What is the sum of $2 + \frac12 + \frac13 + \frac14 + \frac18 + \frac19 + \frac1{16} + \frac1{27} + \cdots$?

<details>
<summary>Show solution</summary>

**Answer: 7/2**

Split it: $2 + (\frac12 + \frac14 + \frac18 + \dots) + (\frac13 + \frac19 + \frac1{27} + \dots) = 2 + 1 + \frac12 = \frac72$.

</details>

### GATE 2024 Q8 (2 marks)

Person 1 invests ₹10,000 / 20,000 / 20,000 in funds A / B / C. Person 2 invests ₹20,000 / 15,000 / 15,000. B and C each return 15%, and Person 1 ends with ₹500 more than Person 2. What is A's return?

<details>
<summary>Show solution</summary>

**Answer: 10%**

- Person 1: $10000(1 + r) + 40000 \times 1.15 = 56000 + 10000r$.
- Person 2: $20000(1 + r) + 30000 \times 1.15 = 54500 + 20000r$.
- Difference: $1500 - 10000r = 500$, so $r = 0.10$.

</details>

### GATE 2025 Q5 (1 mark)

The width W of an L × W rectangle (L > W) increases by 10%. Which is always true?

<details>
<summary>Show solution</summary>

**Answer: (C)** the area increases by 10%

$L \times 1.1W = 1.1LW$. The perimeter rises by $\frac{0.2W}{2L + 2W} < 10\%$, and the diagonal by less than 10%. The figure in §4.1 shows this.

</details>

### GATE 2025 Q9 (2 marks)

$3^{x^2} = 27 \times 9^x$. What is $\dfrac{2^{x^2}}{(2^x)^2}$?

<details>
<summary>Show solution</summary>

**Answer: $2^3$**

$x^2 = 3 + 2x$, so $x^2 - 2x = 3$. The expression is $2^{x^2 - 2x} = 2^3$. (Both roots, $x = 3$ and $x = -1$, give 8.)

</details>

### GATE 2026 Q2 (1 mark)

The product of the digits of a three-digit number is 70. What is the sum of its digits?

<details>
<summary>Show solution</summary>

**Answer: 14**

$70 = 2 \cdot 5 \cdot 7$ is the only way to write it with three digits from 1 to 9, and $2 + 5 + 7 = 14$. I checked every case by enumeration.

</details>

### GATE 2026 Q4 (1 mark)

For $m > n > 0$, $x = n^{\log_{10} m}$ and $y = m^{\log_{10} n}$. How are $x$ and $y$ related?

<details>
<summary>Show solution</summary>

**Answer: $x = y$**

$\log x = \log m \cdot \log n = \log y$. This is the swap identity.

</details>

### GATE 2026 Q9 (2 marks)

$\overline{PQ}$ and $\overline{RS}$ are consecutive two-digit numbers, all six digits P, Q, R, S, X, Y are distinct, and $\overline{PQ}^2 + \overline{RS}^2 = \overline{XYP}$. What is Y?

<details>
<summary>Show solution</summary>

**Answer: 6**

The sum must be at most 999, so $2n^2 + 2n + 1 \le 999$, giving $n \le 21$. Testing $n = 10..21$, only $19^2 + 20^2 = 361 + 400 = 761$ works: its last digit 1 equals P = 1, and the digits 1, 9, 2, 0, 7, 6 are distinct. So **Y = 6**. I confirmed by brute force over every two-digit number.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1.** A price rises 25%. By what percentage must consumption fall to keep spending unchanged?

<details>
<summary>Show solution</summary>

**Answer: 20%**

$\frac{25}{125} = 20\%$.

</details>

**F2.** A salary is raised by 20% and then cut by 20%. What's the net change?

<details>
<summary>Show solution</summary>

**Answer: −4%**

$1.2 \times 0.8 = 0.96$.

</details>

**F3.** What is $\log_2 8 \times \log_8 64$?

<details>
<summary>Show solution</summary>

**Answer: 6**

By the chain rule for change of base, this is $\log_2 64 = 6$.

</details>

**F4.** If $A : B = 2 : 3$ and $B : C = 4 : 5$, what is $A : C$?

<details>
<summary>Show solution</summary>

**Answer: 8 : 15**

</details>

**F5.** A car covers equal distances at 60 km/h and 40 km/h. What is its average speed?

<details>
<summary>Show solution</summary>

**Answer: 48 km/h**

$\frac{2 \times 60 \times 40}{100} = 48$.

</details>

**F6.** What is $\sum_{k=1}^{\infty} \frac{2}{5^k}$?

<details>
<summary>Show solution</summary>

**Answer: 0.5**

$\frac{2/5}{1 - 1/5} = 0.5$.

</details>
