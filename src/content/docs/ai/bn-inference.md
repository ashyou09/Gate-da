---
title: 7. Inference — variable elimination & sampling
description: Inference queries in Bayesian networks, exact inference by enumeration and variable elimination, its complexity, and approximate inference by prior sampling, rejection sampling, likelihood weighting and Gibbs sampling.
sidebar:
  label: "7. Inference: VE & sampling"
  order: 7
---

**Why it matters:** 2025 Q26 asked which algorithms are **exact** and which are **approximate**: variable elimination, Gibbs sampling, rejection sampling. The syllabus names exactly these two families. Expect one classification MSQ, or a small computation on a 3-node network.

## Topic map

<div class="mindmap">

- **Inference in Bayesian networks**
  - Query
    - $P(X \mid e)$: posterior of query variables given evidence
  - Exact
    - enumeration: sum the joint over hidden variables
    - variable elimination: multiply factors, sum out one variable at a time
    - cost set by the largest intermediate factor (elimination order matters)
    - linear on polytrees, NP-hard in general
  - Approximate (sampling)
    - prior (direct) sampling
    - rejection sampling: discard samples inconsistent with the evidence
    - likelihood weighting: fix the evidence, weight each sample
    - Gibbs sampling (MCMC): resample one variable from its Markov blanket
    - consistent as $N \to \infty$

</div>

## 7.1 The inference problem

Given **evidence** $e$ (observed variables), compute the **posterior** of a **query** variable $X$, summing out the **hidden** variables $Y$:

$$
P(X \mid e) = \alpha\, P(X, e) = \alpha \sum_{y} P(X, e, y),
$$

where $\alpha$ normalises the result so it sums to 1.

**Running example** (binary chain A → B → C): $P(A{=}1) = 0.3$; $P(B{=}1 \mid A) = 0.8$ (A = 1) or $0.1$ (A = 0); $P(C{=}1 \mid B) = 0.9$ (B = 1) or $0.2$ (B = 0).

## 7.2 Exact inference: enumeration and variable elimination

**Enumeration** writes out the full sum. With $n$ binary variables, that's up to $2^n$ terms, and the same sub-products get recomputed many times.

**Variable elimination (VE)** pushes each sum inward and caches the intermediate results as **factors**:

$$
P(C) = \sum_b P(C \mid b) \underbrace{\sum_a P(a)\,P(b \mid a)}_{g(b)}.
$$

<!-- fig:ve-chain -->
<figure class="diagram"><svg class="dg" viewBox="0 0 640 170" role="img" aria-label="Variable elimination on a chain" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="20" y="30" width="170" height="40" rx="8"/><text class="title" x="105" y="55" text-anchor="middle">P(A) · P(B|A)</text><path class="ax" d="M195,50 h60 m-6,-5 l6,5 l-6,5"/><text class="t-mut" x="225" y="42" text-anchor="middle">Σ over A</text><rect class="box-ink" x="262" y="30" width="150" height="40" rx="8"/><text class="on-ink" x="337" y="55" text-anchor="middle">g(B) = P(B)</text><text class="t-ink" x="425" y="55">= (0.69, 0.31)</text><rect class="box" x="20" y="110" width="170" height="40" rx="8"/><text class="title" x="105" y="135" text-anchor="middle">g(B) · P(C|B)</text><path class="ax" d="M195,130 h60 m-6,-5 l6,5 l-6,5"/><text class="t-mut" x="225" y="122" text-anchor="middle">Σ over B</text><rect class="box-ink" x="262" y="110" width="150" height="40" rx="8"/><text class="on-ink" x="337" y="135" text-anchor="middle">h(C) = P(C)</text><text class="t-ink" x="425" y="135">= (0.583, 0.417)</text><path class="mut" d="M337,72 v28 H105 v8"/></svg><figcaption>Variable elimination on the chain A → B → C to get P(C). Multiply the factors that mention A and sum A out, giving a new factor over B; then multiply in P(C | B) and sum B out. Each step only touches small tables, instead of the whole joint over (A, B, C). Values are listed for the variable = 0, 1.</figcaption></figure>
<!-- /fig:ve-chain -->

<div class="formula">

**VE algorithm:**

1. Make a factor from each CPT, with the evidence values plugged in.
2. For each hidden variable, in some order: **multiply** all factors that mention it, then **sum it out**. This produces a new, smaller factor.
3. Multiply the remaining factors and **normalise**.

**Cost:** exponential only in the size of the **largest factor** created, which depends on the **elimination order**.

- **Polytrees** (no undirected cycles): linear in the network size.
- General networks: exact inference is **NP-hard**, which is why approximate methods exist.

</div>

**Worked numbers.**

- $P(B{=}1) = 0.3 \times 0.8 + 0.7 \times 0.1 = 0.31$.
- $P(C{=}1) = 0.31 \times 0.9 + 0.69 \times 0.2 = 0.417$.
- With evidence $C = 1$: $P(A{=}1, C{=}1) = 0.3\,(0.8 \times 0.9 + 0.2 \times 0.2) = 0.228$, so $P(A{=}1 \mid C{=}1) = 0.228/0.417 = 0.547$.

**VE gives exact answers.** It's an exact algorithm, not an approximation.

## 7.3 Approximate inference: sampling

Draw many random samples from the network and estimate probabilities by **counting**. The estimates are **consistent**: they converge to the true values as the number of samples $N \to \infty$. But they're never exact for finite $N$.

<div class="formula">

| Method | How | Problem |
|---|---|---|
| **Prior (direct) sampling** | sample every variable in topological order from its CPT | can't condition on evidence by itself |
| **Rejection sampling** | prior-sample, **discard** samples that disagree with the evidence, count the rest | wastes samples: only a fraction $P(e)$ are kept, hopeless for rare evidence |
| **Likelihood weighting** | **fix** the evidence variables; sample the others; weight each sample by $\prod P(e_i \mid \text{parents})$ | weights degrade when the evidence is "downstream" and unlikely |
| **Gibbs sampling** (MCMC) | start from any state consistent with the evidence; repeatedly resample one non-evidence variable from $P(X \mid \text{Markov blanket})$ | correlated samples; needs a burn-in period |

</div>

<!-- fig:sampling-convergence -->
<figure class="diagram"><svg class="dg" viewBox="0 0 560 270" role="img" aria-label="Convergence of rejection sampling" xmlns="http://www.w3.org/2000/svg"><path class="ax" d="M60,20 V220 H540"/><text x="300.0" y="252" text-anchor="middle">number of samples N (log scale)</text><text x="20" y="120.0" text-anchor="middle" transform="rotate(-90 20 120.0)">estimate</text><text class="t-mut" x="60.0" y="235.0" text-anchor="middle">10^1</text><text class="t-mut" x="180.0" y="235.0" text-anchor="middle">10^2</text><text class="t-mut" x="300.0" y="235.0" text-anchor="middle">10^3</text><text class="t-mut" x="420.0" y="235.0" text-anchor="middle">10^4</text><text class="t-mut" x="540.0" y="235.0" text-anchor="middle">10^5</text><text class="t-mut" x="54.0" y="195.4" text-anchor="end">0.3</text><text class="t-mut" x="54.0" y="138.3" text-anchor="end">0.5</text><text class="t-mut" x="54.0" y="81.1" text-anchor="end">0.7</text><text class="t-mut" x="54.0" y="24.0" text-anchor="end">0.9</text><line class="mut" x1="60.0" y1="120.9" x2="540.0" y2="120.9"/><polyline class="ink" points="60.0,105.7 69.5,105.7 77.5,134.3 84.5,134.3 93.5,134.3 101.1,154.7 109.8,147.3 117.3,145.3 125.3,154.7 133.5,176.3 141.7,156.8 149.8,141.1 157.5,122.4 165.7,99.8 173.9,102.5 182.0,86.7 190.4,100.0 198.3,103.7 206.4,104.0 214.5,114.4 222.7,119.7 230.8,122.0 239.0,119.6 247.2,122.3 255.3,115.7 263.4,112.6 271.5,115.2 279.7,115.0 287.8,113.9 295.9,115.4 304.1,112.2 312.2,111.3 320.3,113.5 328.5,115.9 336.6,117.7 344.7,119.0 352.9,122.0 361.0,122.8 369.1,123.0 377.3,125.1 385.4,124.5 393.6,124.0 401.7,124.4 409.8,121.9 418.0,122.7 426.1,123.3 434.2,123.1 442.4,123.0 450.5,122.7 458.6,122.5 466.8,123.2 474.9,123.3 483.1,122.5 491.2,122.0 499.3,122.5 507.5,121.8 515.6,122.7 523.7,122.7 531.9,122.7 540.0,122.0"/><circle class="dot-ink" cx="60.0" cy="105.7" r="2.4"/><circle class="dot-ink" cx="69.5" cy="105.7" r="2.4"/><circle class="dot-ink" cx="77.5" cy="134.3" r="2.4"/><circle class="dot-ink" cx="84.5" cy="134.3" r="2.4"/><circle class="dot-ink" cx="93.5" cy="134.3" r="2.4"/><circle class="dot-ink" cx="101.1" cy="154.7" r="2.4"/><circle class="dot-ink" cx="109.8" cy="147.3" r="2.4"/><circle class="dot-ink" cx="117.3" cy="145.3" r="2.4"/><circle class="dot-ink" cx="125.3" cy="154.7" r="2.4"/><circle class="dot-ink" cx="133.5" cy="176.3" r="2.4"/><circle class="dot-ink" cx="141.7" cy="156.8" r="2.4"/><circle class="dot-ink" cx="149.8" cy="141.1" r="2.4"/><circle class="dot-ink" cx="157.5" cy="122.4" r="2.4"/><circle class="dot-ink" cx="165.7" cy="99.8" r="2.4"/><circle class="dot-ink" cx="173.9" cy="102.5" r="2.4"/><circle class="dot-ink" cx="182.0" cy="86.7" r="2.4"/><circle class="dot-ink" cx="190.4" cy="100.0" r="2.4"/><circle class="dot-ink" cx="198.3" cy="103.7" r="2.4"/><circle class="dot-ink" cx="206.4" cy="104.0" r="2.4"/><circle class="dot-ink" cx="214.5" cy="114.4" r="2.4"/><circle class="dot-ink" cx="222.7" cy="119.7" r="2.4"/><circle class="dot-ink" cx="230.8" cy="122.0" r="2.4"/><circle class="dot-ink" cx="239.0" cy="119.6" r="2.4"/><circle class="dot-ink" cx="247.2" cy="122.3" r="2.4"/><circle class="dot-ink" cx="255.3" cy="115.7" r="2.4"/><circle class="dot-ink" cx="263.4" cy="112.6" r="2.4"/><circle class="dot-ink" cx="271.5" cy="115.2" r="2.4"/><circle class="dot-ink" cx="279.7" cy="115.0" r="2.4"/><circle class="dot-ink" cx="287.8" cy="113.9" r="2.4"/><circle class="dot-ink" cx="295.9" cy="115.4" r="2.4"/><circle class="dot-ink" cx="304.1" cy="112.2" r="2.4"/><circle class="dot-ink" cx="312.2" cy="111.3" r="2.4"/><circle class="dot-ink" cx="320.3" cy="113.5" r="2.4"/><circle class="dot-ink" cx="328.5" cy="115.9" r="2.4"/><circle class="dot-ink" cx="336.6" cy="117.7" r="2.4"/><circle class="dot-ink" cx="344.7" cy="119.0" r="2.4"/><circle class="dot-ink" cx="352.9" cy="122.0" r="2.4"/><circle class="dot-ink" cx="361.0" cy="122.8" r="2.4"/><circle class="dot-ink" cx="369.1" cy="123.0" r="2.4"/><circle class="dot-ink" cx="377.3" cy="125.1" r="2.4"/><circle class="dot-ink" cx="385.4" cy="124.5" r="2.4"/><circle class="dot-ink" cx="393.6" cy="124.0" r="2.4"/><circle class="dot-ink" cx="401.7" cy="124.4" r="2.4"/><circle class="dot-ink" cx="409.8" cy="121.9" r="2.4"/><circle class="dot-ink" cx="418.0" cy="122.7" r="2.4"/><circle class="dot-ink" cx="426.1" cy="123.3" r="2.4"/><circle class="dot-ink" cx="434.2" cy="123.1" r="2.4"/><circle class="dot-ink" cx="442.4" cy="123.0" r="2.4"/><circle class="dot-ink" cx="450.5" cy="122.7" r="2.4"/><circle class="dot-ink" cx="458.6" cy="122.5" r="2.4"/><circle class="dot-ink" cx="466.8" cy="123.2" r="2.4"/><circle class="dot-ink" cx="474.9" cy="123.3" r="2.4"/><circle class="dot-ink" cx="483.1" cy="122.5" r="2.4"/><circle class="dot-ink" cx="491.2" cy="122.0" r="2.4"/><circle class="dot-ink" cx="499.3" cy="122.5" r="2.4"/><circle class="dot-ink" cx="507.5" cy="121.8" r="2.4"/><circle class="dot-ink" cx="515.6" cy="122.7" r="2.4"/><circle class="dot-ink" cx="523.7" cy="122.7" r="2.4"/><circle class="dot-ink" cx="531.9" cy="122.7" r="2.4"/><circle class="dot-ink" cx="540.0" cy="122.0" r="2.4"/><text class="t-mut" x="534.0" y="112.9" text-anchor="end">exact 0.547</text></svg><figcaption>Rejection sampling for P(A=1 | C=1) on the chain example, from one run of the sampler. Each point is the estimate after N prior samples (only the ~41.7% with C = 1 are kept). The estimate wanders for small N and settles near the exact value 0.547 (dashed) as N grows: approximate, but consistent.</figcaption></figure>
<!-- /fig:sampling-convergence -->

On the running example, rejection sampling kept 42, 420, 4143 and 41,852 of 100, 1,000, 10,000 and 100,000 samples (about $P(C{=}1) = 0.417$ of them). The estimates of $P(A{=}1 \mid C{=}1)$ were 0.595, 0.533, 0.548 and 0.543. Likelihood weighting with 100,000 samples gave 0.5466. The exact value is 0.547.

## 7.4 Exact vs approximate: the classification table

| Algorithm | Type |
|---|---|
| Enumeration | exact |
| **Variable elimination** | **exact** |
| Junction tree / clique tree | exact |
| Prior sampling | approximate |
| **Rejection sampling** | **approximate** |
| Likelihood weighting | approximate |
| **Gibbs sampling / MCMC** | **approximate** |

---

## Summary: important points

<div class="formula">

1. $P(X \mid e) = \alpha\sum_y P(X, e, y)$. Sum out the hidden variables, then normalise.
2. Variable elimination is **exact**: multiply the factors containing a variable, then sum it out.
3. VE's cost is set by the largest factor (it depends on the elimination order). It's linear on polytrees and NP-hard in general.
4. Sampling methods are **approximate** but consistent as $N \to \infty$.
5. Rejection sampling keeps only about $P(e)$ of its samples.
6. Likelihood weighting fixes the evidence and weights each sample by $\prod P(e_i \mid \text{parents})$.
7. Gibbs sampling resamples one variable at a time from $P(X \mid \text{Markov blanket})$.

</div>

<div class="trap">

- "Variable elimination is approximate" and "Gibbs sampling is exact" are both **false**. That's 2025 Q26's trap.
- Rejection sampling is still correct with rare evidence. It's just extremely inefficient.
- Don't forget to **normalise** at the end of VE when evidence is present.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2025 Q26 (1 mark, MSQ)

In a Bayesian network, which statements are correct?
(A) Variable elimination is an approximate inference algorithm (B) Gibbs sampling is an exact inference algorithm (C) Variable elimination is used to determine conditional probabilities (D) Rejection sampling is an approximate inference algorithm

<details>
<summary>Show solution</summary>

**Answer: C; D**

VE is **exact** and computes posteriors such as $P(X \mid e)$. Gibbs and rejection sampling are both **approximate** (Monte Carlo) methods.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** In the running example, what is $P(C = 1)$? (3 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.417**

$P(B{=}1) = 0.31$, then $0.31 \times 0.9 + 0.69 \times 0.2 = 0.417$.

</details>

**F2 (2 marks, NAT).** What is $P(A = 1 \mid C = 1)$? (3 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.547**

$0.3\,(0.8 \times 0.9 + 0.2 \times 0.2) = 0.228$, and $0.228/0.417 = 0.547$.

</details>

**F3 (1 mark, NAT).** Rejection sampling for evidence $C = 1$ draws 1000 prior samples. About how many are kept?

<details>
<summary>Show solution</summary>

**Answer: about 417**

The expected number kept is $1000 \times P(C{=}1) = 417$. (One actual run kept 420.)

</details>

**F4 (1 mark, NAT).** Likelihood weighting with evidence $C = 1$ generates the sample $A = 1, B = 0$. What is its weight?

<details>
<summary>Show solution</summary>

**Answer: 0.2**

The weight is $P(C{=}1 \mid B{=}0) = 0.2$. Only the evidence variable contributes to the weight.

</details>

**F5 (2 marks, MSQ).** Which statements are true?
(A) Exact inference in general Bayesian networks is NP-hard (B) Variable elimination is linear-time on polytrees (C) Gibbs sampling resamples a variable conditioned on its Markov blanket (D) Rejection sampling is efficient when the evidence is very unlikely

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

(D) is the opposite of the truth: rare evidence means almost every sample is rejected.

</details>
