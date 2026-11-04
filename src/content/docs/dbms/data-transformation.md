---
title: 6. Data types & data transformation
description: Attribute types (nominal, ordinal, interval, ratio), preprocessing steps, min-max, z-score and decimal-scaling normalization, discretization by equal-width and equal-frequency binning, smoothing, sampling, and data compression.
sidebar:
  label: 6. Data transformation
  order: 6
---

**Why it matters:** 2024 Q27 asked for a **z-score** value, a one-line 1-mark question. The syllabus explicitly lists *data types, normalization, discretization, sampling, compression*, so expect a definition or a small calculation from this list. It also feeds ML: k-NN, k-means, PCA and regularization all need scaled features.

## Topic map

<div class="mindmap">

- **Data preparation**
  - Attribute types
    - nominal, binary, ordinal, interval, ratio
    - which statistics are meaningful
  - Preprocessing
    - cleaning (missing values, noise, outliers), integration, reduction, transformation
  - Normalization (scaling)
    - min-max, z-score, decimal scaling
  - Discretization
    - equal-width, equal-frequency binning
    - smoothing by means / medians / boundaries
    - concept hierarchies
  - Sampling
    - SRSWOR, SRSWR, stratified, cluster
  - Compression / reduction
    - lossless vs lossy; dimensionality vs numerosity reduction

</div>

## 6.1 Attribute (data) types

<div class="formula">

| Type | Meaning | Example | Meaningful operations | Centre |
|---|---|---|---|---|
| **Nominal** | names or labels, no order | colour, PIN code | $=, \ne$ | mode |
| **Binary** | two states. **Symmetric** (equal weight: gender) or **asymmetric** (a positive is rarer and matters more: test result) | smoker yes/no | $=, \ne$ | mode |
| **Ordinal** | ordered, but gaps aren't meaningful | grade A > B > C, rank | $<, >$ | median, mode |
| **Interval** | numeric with equal units, **no true zero** | °C, calendar year | $+, -$ (differences) | mean |
| **Ratio** | numeric with a **true zero** | height, income, kelvin | $+, -, \times, \div$ (ratios) | mean (geometric mean too) |

</div>

**Ratio vs interval:** "20 °C is twice as hot as 10 °C" is **meaningless**, because 0 °C isn't "no heat". "200 K is twice 100 K" is meaningful, because kelvin has a true zero.

Numeric attributes can also be **discrete** (counts) or **continuous** (measurements).

## 6.2 Preprocessing steps

1. **Cleaning:** fill **missing values** (ignore the tuple, use a global constant, the mean or median, or the class-wise mean), smooth **noise** (binning, regression), and handle **outliers**.
2. **Integration:** combine sources, resolving naming conflicts and redundant attributes (detected with correlation or $\chi^2$).
3. **Reduction:** fewer attributes (PCA, feature selection) or fewer values or records (sampling, histograms, aggregation).
4. **Transformation:** normalization, discretization, building concept hierarchies.

## 6.3 Normalization (feature scaling)

<div class="formula">

**Min-max** to a new range $[a, b]$ (usually $[0, 1]$):

$$
v' = \frac{v - \min}{\max - \min}\,(b - a) + a
$$

**z-score** (standardization):

$$
v' = \frac{v - \mu}{\sigma}
$$

The result has mean 0 and standard deviation 1.

**Decimal scaling:**

$$
v' = \frac{v}{10^j}, \quad j = \text{the smallest integer with } \max|v'| < 1
$$

</div>

| Method | Needs | Good for | Watch out |
|---|---|---|---|
| Min-max | min, max | a fixed output range (e.g. neural-network inputs) | **one outlier squashes everything else**; new data outside $[\min, \max]$ falls outside $[a, b]$ |
| z-score | mean, std | unknown range, data with outliers, distance-based methods | the result isn't bounded |
| Decimal scaling | max abs value | quick, keeps digits readable | coarse |

**A question gives min, max, mean and SD?** Use only what the requested method needs. z-score ignores min and max, and min-max ignores mean and SD. Including the unused numbers is GATE's distractor.

## 6.4 Discretization (binning)

Discretization turns a continuous attribute into a small number of intervals (bins). It reduces noise and the number of distinct values, and it feeds algorithms that need categories, such as naive Bayes.

<!-- fig:binning -->
<figure class="diagram"><svg class="dg" viewBox="0 0 620 275" role="img" aria-label="Equal-width versus equal-frequency binning" xmlns="http://www.w3.org/2000/svg"><text class="title" x="40" y="26">equal width (width 10)</text><line class="ax" x1="40.0" y1="102" x2="580.0" y2="102"/><rect x="93.8" y="66" width="148.1" height="22" rx="5" style="fill:var(--gd-ink);fill-opacity:.22;stroke:var(--gd-ink)"/><text class="t-ink" x="167.9" y="44" text-anchor="middle">n = 2</text><text class="t-mut" x="167.9" y="59" text-anchor="middle">mean 6</text><rect x="235.9" y="66" width="148.1" height="22" rx="5" style="fill:var(--gd-hl-strong);fill-opacity:.22;stroke:var(--gd-hl-strong)"/><text class="t-ink" x="310.0" y="44" text-anchor="middle">n = 3</text><text class="t-mut" x="310.0" y="59" text-anchor="middle">mean 19</text><rect x="378.1" y="66" width="148.1" height="22" rx="5" style="fill:var(--gd-ink);fill-opacity:.22;stroke:var(--gd-ink)"/><text class="t-ink" x="452.1" y="44" text-anchor="middle">n = 4</text><text class="t-mut" x="452.1" y="59" text-anchor="middle">mean 27.75</text><circle class="dot" cx="96.8" cy="102.0" r="4"/><circle class="dot" cx="153.7" cy="102.0" r="4"/><circle class="dot" cx="253.2" cy="102.0" r="4"/><circle class="dot" cx="338.4" cy="102.0" r="4"/><circle class="dot" cx="338.4" cy="95.0" r="4"/><circle class="dot" cx="381.1" cy="102.0" r="4"/><circle class="dot" cx="395.3" cy="102.0" r="4"/><circle class="dot" cx="437.9" cy="102.0" r="4"/><circle class="dot" cx="523.2" cy="102.0" r="4"/><text class="t-mut" x="40.0" y="118" text-anchor="middle">0</text><text class="t-mut" x="182.1" y="118" text-anchor="middle">10</text><text class="t-mut" x="324.2" y="118" text-anchor="middle">20</text><text class="t-mut" x="466.3" y="118" text-anchor="middle">30</text><text class="title" x="40" y="146">equal frequency (3 per bin)</text><line class="ax" x1="40.0" y1="222" x2="580.0" y2="222"/><rect x="93.8" y="186" width="162.3" height="22" rx="5" style="fill:var(--gd-ink);fill-opacity:.22;stroke:var(--gd-ink)"/><text class="t-ink" x="175.0" y="164" text-anchor="middle">n = 3</text><text class="t-mut" x="175.0" y="179" text-anchor="middle">mean 9</text><rect x="335.4" y="186" width="48.6" height="22" rx="5" style="fill:var(--gd-hl-strong);fill-opacity:.22;stroke:var(--gd-hl-strong)"/><text class="t-ink" x="359.7" y="164" text-anchor="middle">n = 3</text><text class="t-mut" x="359.7" y="179" text-anchor="middle">mean 22</text><rect x="392.3" y="186" width="133.9" height="22" rx="5" style="fill:var(--gd-ink);fill-opacity:.22;stroke:var(--gd-ink)"/><text class="t-ink" x="459.2" y="164" text-anchor="middle">n = 3</text><text class="t-mut" x="459.2" y="179" text-anchor="middle">mean 29</text><circle class="dot" cx="96.8" cy="222.0" r="4"/><circle class="dot" cx="153.7" cy="222.0" r="4"/><circle class="dot" cx="253.2" cy="222.0" r="4"/><circle class="dot" cx="338.4" cy="222.0" r="4"/><circle class="dot" cx="338.4" cy="215.0" r="4"/><circle class="dot" cx="381.1" cy="222.0" r="4"/><circle class="dot" cx="395.3" cy="222.0" r="4"/><circle class="dot" cx="437.9" cy="222.0" r="4"/><circle class="dot" cx="523.2" cy="222.0" r="4"/><text class="t-mut" x="40.0" y="238" text-anchor="middle">0</text><text class="t-mut" x="182.1" y="238" text-anchor="middle">10</text><text class="t-mut" x="324.2" y="238" text-anchor="middle">20</text><text class="t-mut" x="466.3" y="238" text-anchor="middle">30</text></svg><figcaption>The same nine sorted values 4, 8, 15, 21, 21, 24, 25, 28, 34 discretized into 3 bins two ways. Equal-width bins have the same range (width (34 − 4)/3 = 10) but unequal counts (2, 3, 4). Equal-frequency bins have the same count (3 each) but unequal ranges. Smoothing by bin means replaces each value by its bin's mean.</figcaption></figure>
<!-- /fig:binning -->

<div class="formula">

- **Equal-width** with $k$ bins: width $= (\max - \min)/k$. It's simple, but skewed data leaves some bins nearly empty.
- **Equal-frequency (equal-depth):** each bin holds about $n/k$ values. The bins adapt to the data.
- **Smoothing within a bin:**
  - by **means**: replace each value with its bin's mean;
  - by **medians**: replace with the bin's median;
  - by **boundaries**: replace with the **nearer** of the bin's min and max.
- **Supervised** discretization (entropy-based, $\chi^2$-merge) uses class labels to place the cuts.

</div>

With the equal-frequency bins [4, 8, 15], [21, 21, 24], [25, 28, 34]:

- smoothing by **means** gives 9, 9, 9 | 22, 22, 22 | 29, 29, 29;
- smoothing by **boundaries** gives 4, 4, 15 | 21, 21, 24 | 25, 25, 34. (8 is closer to 4 than to 15; 28 is closer to 25 than to 34.)

**Concept hierarchies** replace low-level values with higher-level concepts (city → state → country, age → young / middle / senior). They're the foundation of OLAP roll-up (topic 7).

## 6.5 Sampling

| Method | How |
|---|---|
| **SRSWOR** | simple random sample **without** replacement: each tuple can be picked at most once |
| **SRSWR** | **with** replacement: a tuple can be picked again |
| **Stratified** | split into groups (strata), then sample each in proportion. Keeps rare classes represented |
| **Cluster** | split into clusters (e.g. disk pages), then pick whole clusters at random |

Proportional stratified sample: stratum $i$ gets $n \cdot \frac{N_i}{N}$ samples.

## 6.6 Compression and reduction

- **Lossless** compression reconstructs the data exactly (run-length or Huffman encoding of strings). **Lossy** compression keeps an approximation (wavelets, PCA keeping the top components).
- **Dimensionality reduction:** fewer attributes (PCA, attribute subset selection).
- **Numerosity reduction:** fewer values or records. **Parametric:** store model parameters, e.g. regression. **Non-parametric:** histograms, clustering, sampling, data-cube aggregation.

---

## Summary: important points

<div class="formula">

1. Nominal ($=$), ordinal (order), interval (differences, no true zero), ratio (true zero, so ratios make sense).
2. Min-max: $\frac{v - \min}{\max - \min}(b - a) + a$. It's sensitive to outliers.
3. z-score: $(v - \mu)/\sigma$, giving mean 0 and SD 1. It doesn't use min or max.
4. Decimal scaling: $v/10^j$, with the smallest $j$ that makes every $|v'| < 1$.
5. Equal-width: same range per bin. Equal-frequency: same count per bin.
6. Smoothing: replace with the bin mean, median or nearest boundary.
7. Stratified sampling: $n \cdot N_i/N$ per stratum. SRSWOR vs SRSWR differ in replacement.
8. Reduction can be dimensionality (attributes) or numerosity (values). Compression can be lossless or lossy.

</div>

<div class="trap">

- Don't mix the formulas up: z-score uses the **mean and SD**, min-max uses the **min and max**.
- Celsius is interval, not ratio.
- Equal-width bins on skewed data can be nearly empty.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q27 (1 mark, MCQ)

Income has min ₹46,000, max ₹1,70,000, mean ₹96,000 and SD ₹21,000. What is the z-score of ₹1,06,000?
(A) 0.217 (B) 0.476 (C) 0.623 (D) 2.304

<details>
<summary>Show solution</summary>

**Answer: (B) 0.476**

$\dfrac{106000 - 96000}{21000} = \dfrac{10000}{21000} = 0.476$.

The min and max are distractors. Using min-max scaling instead gives $(106000 - 46000)/124000 = 0.484$, which is close to (B) but comes from the wrong formula.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** Income ranges from ₹12,000 to ₹98,000. What is the min-max normalized value of ₹73,600 on $[0, 1]$? (3 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.716**

$(73600 - 12000)/(98000 - 12000) = 61600/86000 = 0.716$.

</details>

**F2 (1 mark, NAT).** The same value is min-max normalized to $[-1, 1]$. What is the result? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.43**

$0.716 \times 2 - 1 = 0.43$.

</details>

**F3 (1 mark, NAT).** Values range from −986 to 917. With decimal scaling, what does 917 become?

<details>
<summary>Show solution</summary>

**Answer: 0.917**

The largest absolute value is 986. With $j = 3$, $986/1000 < 1$, so 917 becomes $917/1000 = $ **0.917**.

</details>

**F4 (2 marks, NAT).** The data 4, 8, 15, 21, 21, 24, 25, 28, 34 is put into 3 equal-width bins. How many values fall in the last bin $[24, 34]$?

<details>
<summary>Show solution</summary>

**Answer: 4**

The width is 10, giving bins [4, 14), [14, 24) and [24, 34]. The last bin holds 24, 25, 28 and 34: **4** values.

</details>

**F5 (2 marks, MSQ).** Which pairings of attribute and type are correct?
(A) temperature in °C: interval (B) temperature in kelvin: ratio (C) class rank (1st, 2nd, …): ordinal (D) PIN code: ratio

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

A PIN code is **nominal**. Its digits are labels; arithmetic on them means nothing.

</details>

**F6 (1 mark, NAT).** A population has 600 records of class A and 400 of class B. A proportional stratified sample of 50 is drawn. How many class-A records does it contain?

<details>
<summary>Show solution</summary>

**Answer: 30**

$50 \times 600/1000 = 30$, and class B gets 20.

</details>
