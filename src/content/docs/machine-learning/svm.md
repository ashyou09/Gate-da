---
title: 8. Support vector machines
description: Maximum-margin classifiers, functional vs geometric margin, the hard-margin optimisation problem, support vectors and the dual, solving small SVMs by hand, soft margin and C, hinge loss, and kernels.
sidebar:
  label: 8. SVM
  order: 8
---

**Why it matters:** 2024 Q17 and 2025 Q53 both gave a tiny 2-D dataset and asked about the hard-margin SVM: which points are support vectors, what $w$ and $b$ are, and how wide the margin is. You can **solve these by hand in a minute** once you know the geometry. Soft margins, C and kernels are the next likely questions.

## Topic map

<div class="mindmap">

- **SVM**
  - Idea
    - among all separating lines, choose the widest margin
  - Margin
    - functional $y(w^\top x + b)$, geometric $\div \|w\|$
    - canonical scaling: the closest points have $y f(x) = 1$
    - width $= 2/\|w\|$
  - Hard margin
    - $\min \frac12\|w\|^2$ s.t. $y_i(w^\top x_i + b) \ge 1$
  - Support vectors
    - points with $y_i f(x_i) = 1$
    - dual: $w = \sum \alpha_i y_i x_i$, $\alpha_i > 0$ only for SVs
  - Soft margin
    - slack $\xi_i$, penalty $C\sum\xi_i$
    - large C → narrow margin, small C → wide margin
    - hinge loss $\max(0, 1 - yf)$
  - Kernels
    - dot product → $K(x, z)$
    - polynomial, RBF

</div>

## 8.1 The idea: the widest street

If the data is linearly separable, there are infinitely many separating lines, and the perceptron (topic 4) stops at whichever one it reaches first. The SVM picks the one with the **largest margin**: the widest "street" between the classes with no points inside it.

**Why the widest?** A wide margin means small perturbations of the data don't flip predictions, so the classifier is more robust and generalises better. Only the points **on the edge of the street** affect the answer. Moving any other point (without crossing the street) changes nothing.

## 8.2 Margins and the canonical scaling

Labels are $y_i \in \{+1, -1\}$, and $f(x) = w^\top x + b$.

<div class="formula">

- **Functional margin** of a point: $y_i(w^\top x_i + b)$. It's positive if the point is classified correctly.
- **Geometric margin** (actual distance to the boundary): $\dfrac{y_i(w^\top x_i + b)}{\|w\|}$.
- Scaling $(w, b)$ changes the functional margin but not the boundary. So fix the scale with the **canonical** choice: the closest points satisfy $y_i(w^\top x_i + b) = 1$.
- Then the margin lines are $w^\top x + b = \pm 1$, the distance from the boundary to each margin line is $\dfrac{1}{\|w\|}$, and the **total width of the street is $\dfrac{2}{\|w\|}$**.

</div>

**Check how "margin" is defined.** Some books call $1/\|w\|$ the margin (boundary to the nearest point). GATE 2025 Q53 called the full width $2/\|w\| = \sqrt2$ the margin. If an option gives one of these values, check which definition makes it true.

## 8.3 The hard-margin problem

Maximising $2/\|w\|$ is the same as minimising $\|w\|^2$:

<div class="formula">

$$
\min_{w, b}\; \tfrac12\|w\|^2 \quad \text{subject to} \quad y_i(w^\top x_i + b) \ge 1 \;\; \text{for all } i.
$$

This is a **convex quadratic program**: a quadratic objective with linear constraints, so it has a **unique** optimal $w$. It's feasible only if the data is linearly separable.

</div>

## 8.4 Support vectors and the dual

At the optimum, the constraints split the points into two groups:

- **Support vectors (SVs):** $y_i(w^\top x_i + b) = 1$. They lie **on** a margin line.
- **All other points:** $y_i(w^\top x_i + b) > 1$. They're strictly outside the street.

Solving with Lagrange multipliers $\alpha_i \ge 0$ (one per constraint) gives:

<div class="formula">

$$
w = \sum_i \alpha_i y_i x_i, \qquad \sum_i \alpha_i y_i = 0, \qquad \alpha_i > 0 \text{ only for support vectors}.
$$

The **dual problem** is $\max_\alpha \sum_i\alpha_i - \frac12\sum_{i,j}\alpha_i\alpha_jy_iy_j\,x_i^\top x_j$ subject to $\alpha_i \ge 0$ and $\sum\alpha_iy_i = 0$.

The data appears **only through dot products** $x_i^\top x_j$. That's what makes kernels possible (§8.7).

</div>

Consequences GATE likes:

- **Deleting a non-support vector doesn't change the solution.** Deleting a support vector can.
- Prediction: $f(x) = \sum_{i \in SV}\alpha_iy_i\,x_i^\top x + b$, which only needs the SVs.
- There are at least 2 SVs (at least one from each class), and often only a few.

## 8.5 Solving a small SVM by hand

<!-- fig:svm-margin -->
<figure class="diagram"><svg class="dg" viewBox="0 0 600 320" role="img" aria-label="Maximum-margin separator with support vectors" xmlns="http://www.w3.org/2000/svg"><clipPath id="svmclip"><rect x="50" y="20" width="300" height="260"/></clipPath><path class="ax" d="M50,20 V280 H350"/><text x="200.0" y="310" text-anchor="middle">x₁</text><text x="24" y="150.0" text-anchor="middle" transform="rotate(-90 24 150.0)">x₂</text><text class="t-mut" x="116.7" y="294.0" text-anchor="middle">0</text><text class="t-mut" x="44.0" y="226.2" text-anchor="end">0</text><text class="t-mut" x="200.0" y="294.0" text-anchor="middle">1</text><text class="t-mut" x="44.0" y="154.0" text-anchor="end">1</text><text class="t-mut" x="283.3" y="294.0" text-anchor="middle">2</text><text class="t-mut" x="44.0" y="81.8" text-anchor="end">2</text><g clip-path="url(#svmclip)"><polygon style="fill:var(--gd-hl-strong);fill-opacity:.12" points="50.0,164.4 183.3,280.0 350.0,280.0 50.0,20.0"/><line class="ink" x1="50.0" y1="92.2" x2="266.7" y2="280.0"/><line class="mut" x1="50.0" y1="164.4" x2="183.3" y2="280.0"/><line class="mut" x1="50.0" y1="20.0" x2="350.0" y2="280.0"/></g><line class="hl" x1="116.7" y1="222.2" x2="200.0" y2="150.0" style="stroke-width:1.8"/><text class="t-hl" x="168.3" y="191.9">√2</text><circle class="dot-ink" cx="283.3" cy="222.2" r="6"/><circle class="dot-ink" cx="116.7" cy="77.8" r="6"/><circle class="dot-ink" cx="283.3" cy="77.8" r="6"/><rect class="dot-warn" x="110.7" y="216.2" width="12" height="12"/><circle class="warn" style="fill:none;stroke-width:1.6" cx="283.3" cy="222.2" r="11"/><circle class="warn" style="fill:none;stroke-width:1.6" cx="116.7" cy="77.8" r="11"/><circle class="warn" style="fill:none;stroke-width:1.6" cx="116.7" cy="222.2" r="11"/><text class="t-ink" x="245.8" y="254.7">x₁+x₂ = 1</text><text class="t-ink" x="380" y="60" style="font-weight:600">boundary</text><text x="380" y="78">wᵀx + b = 0</text><text class="t-mut" x="380" y="104" style="font-weight:600">margin lines</text><text x="380" y="122">wᵀx + b = ±1</text><text class="t-warn" x="380" y="148" style="font-weight:600">support vectors</text><text x="380" y="166">ringed: y(wᵀx+b) = 1</text><text class="t-hl" x="380" y="192" style="font-weight:600">width</text><text x="380" y="210">2/‖w‖ = 2/√2 = √2</text><text class="t-mut" x="380" y="236" style="font-weight:600">(2,2)</text><text x="380" y="254">y f(x) = 3 > 1: not a SV</text></svg><figcaption>Hard-margin SVM on the 2025 Q53 data: class 1 at (2,0), (0,2), (2,2), class 2 at (0,0). The solution is w = (1, 1), b = −1, so the boundary is x₁ + x₂ = 1 and the margin lines are x₁ + x₂ = 0 and x₁ + x₂ = 2. The three ringed points touch the margin: they are the support vectors. Margin width = 2/‖w‖ = √2.</figcaption></figure>
<!-- /fig:svm-margin -->

**Recipe:**

1. **Guess the support vectors**: the closest points between the two classes. Symmetry helps a lot.
2. **Guess the direction of $w$**: perpendicular to the gap between them. For two points it's along their difference. For a point and a parallel pair, it's perpendicular to the pair's line.
3. **Fix the scale**: write $y_i(w^\top x_i + b) = 1$ for each support vector and solve for $w$ and $b$.
4. **Check** that every other point has $y_i f(x_i) \ge 1$.
5. **Margin width** $= 2/\|w\|$.

**Applied to 2025 Q53.** The closest class-1 points to (0, 0) are (2, 0) and (0, 2), on the line $x_1 + x_2 = 2$. So $w \propto (1, 1)$; write $w = (a, a)$.

- From (0, 0) with $y = -1$: $-(0 + b) = 1$, so $b = -1$.
- From (2, 0) with $y = +1$: $2a - 1 = 1$, so $a = 1$.

So $w = (1, 1)$ and $b = -1$. Check (2, 2): $1 \cdot (2 + 2 - 1) = 3 \ge 1$ ✓ (not a support vector). Width $= 2/\sqrt2 = \sqrt2$.

The dual agrees: $\alpha = (0.5, 0.5, 1)$ for (2,0), (0,2), (0,0) gives $w = 0.5(2,0) + 0.5(0,2) - 1(0,0) = (1, 1)$, and $\sum\alpha_iy_i = 0.5 + 0.5 - 1 = 0$ ✓.

## 8.6 Soft margin, C and the hinge loss

Real data overlaps, so the hard constraints can't all be met. Let each point violate the margin by a **slack** $\xi_i \ge 0$:

<div class="formula">

$$
\min_{w, b, \xi}\; \tfrac12\|w\|^2 + C\sum_i\xi_i \quad \text{s.t.} \quad y_i(w^\top x_i + b) \ge 1 - \xi_i,\;\; \xi_i \ge 0.
$$

- $\xi_i = 0$: on or outside the margin. $0 < \xi_i \le 1$: inside the street but still correctly classified. $\xi_i > 1$: misclassified.
- The support vectors are now the points on the margin **plus** the margin violators.

| C | Penalty for violations | Margin | Bias / variance |
|---|---|---|---|
| **large** | heavy (close to hard margin) | narrow | low bias, **high variance** (may overfit) |
| **small** | light | wide | higher bias, **low variance** |

</div>

**Equivalent unconstrained form.** At the optimum $\xi_i = \max(0, 1 - y_if(x_i))$, so the soft-margin SVM is

$$
\min_{w, b}\;\sum_i \underbrace{\max\big(0,\; 1 - y_i(w^\top x_i + b)\big)}_{\text{hinge loss}} + \lambda\|w\|^2, \qquad \lambda = \frac{1}{2C}.
$$

That's **hinge loss plus L2 regularization**, the same "loss + penalty" pattern as ridge regression (topic 3).

<!-- fig:svm-losses -->
<figure class="diagram"><svg class="dg" viewBox="0 0 560 285" role="img" aria-label="Hinge, logistic and zero-one losses" xmlns="http://www.w3.org/2000/svg"><path class="ax" d="M60,20 V240 H540"/><text x="300.0" y="272" text-anchor="middle">margin  y · f(x)</text><text x="30" y="130.0" text-anchor="middle" transform="rotate(-90 30 130.0)">loss</text><text class="t-mut" x="103.6" y="255.0" text-anchor="middle">-2</text><text class="t-mut" x="190.9" y="255.0" text-anchor="middle">-1</text><text class="t-mut" x="278.2" y="255.0" text-anchor="middle">0</text><text class="t-mut" x="365.5" y="255.0" text-anchor="middle">1</text><text class="t-mut" x="452.7" y="255.0" text-anchor="middle">2</text><text class="t-mut" x="540.0" y="255.0" text-anchor="middle">3</text><line class="grid" x1="365.5" y1="240.0" x2="365.5" y2="20.0"/><polyline class="mut" points="60.0,178.9 61.6,178.9 63.2,178.9 64.8,178.9 66.4,178.9 68.0,178.9 69.6,178.9 71.2,178.9 72.8,178.9 74.4,178.9 76.1,178.9 77.7,178.9 79.3,178.9 80.9,178.9 82.5,178.9 84.1,178.9 85.7,178.9 87.3,178.9 88.9,178.9 90.5,178.9 92.1,178.9 93.7,178.9 95.3,178.9 96.9,178.9 98.5,178.9 100.1,178.9 101.7,178.9 103.3,178.9 104.9,178.9 106.6,178.9 108.2,178.9 109.8,178.9 111.4,178.9 113.0,178.9 114.6,178.9 116.2,178.9 117.8,178.9 119.4,178.9 121.0,178.9 122.6,178.9 124.2,178.9 125.8,178.9 127.4,178.9 129.0,178.9 130.6,178.9 132.2,178.9 133.8,178.9 135.5,178.9 137.1,178.9 138.7,178.9 140.3,178.9 141.9,178.9 143.5,178.9 145.1,178.9 146.7,178.9 148.3,178.9 149.9,178.9 151.5,178.9 153.1,178.9 154.7,178.9 156.3,178.9 157.9,178.9 159.5,178.9 161.1,178.9 162.7,178.9 164.3,178.9 166.0,178.9 167.6,178.9 169.2,178.9 170.8,178.9 172.4,178.9 174.0,178.9 175.6,178.9 177.2,178.9 178.8,178.9 180.4,178.9 182.0,178.9 183.6,178.9 185.2,178.9 186.8,178.9 188.4,178.9 190.0,178.9 191.6,178.9 193.2,178.9 194.8,178.9 196.5,178.9 198.1,178.9 199.7,178.9 201.3,178.9 202.9,178.9 204.5,178.9 206.1,178.9 207.7,178.9 209.3,178.9 210.9,178.9 212.5,178.9 214.1,178.9 215.7,178.9 217.3,178.9 218.9,178.9 220.5,178.9 222.1,178.9 223.7,178.9 225.4,178.9 227.0,178.9 228.6,178.9 230.2,178.9 231.8,178.9 233.4,178.9 235.0,178.9 236.6,178.9 238.2,178.9 239.8,178.9 241.4,178.9 243.0,178.9 244.6,178.9 246.2,178.9 247.8,178.9 249.4,178.9 251.0,178.9 252.6,178.9 254.2,178.9 255.9,178.9 257.5,178.9 259.1,178.9 260.7,178.9 262.3,178.9 263.9,178.9 265.5,178.9 267.1,178.9 268.7,178.9 270.3,178.9 271.9,178.9 273.5,178.9 275.1,178.9 276.7,178.9"/><polyline class="mut" points="278.3,240.0 279.9,240.0 281.5,240.0 283.1,240.0 284.7,240.0 286.4,240.0 288.0,240.0 289.6,240.0 291.2,240.0 292.8,240.0 294.4,240.0 296.0,240.0 297.6,240.0 299.2,240.0 300.8,240.0 302.4,240.0 304.0,240.0 305.6,240.0 307.2,240.0 308.8,240.0 310.4,240.0 312.0,240.0 313.6,240.0 315.3,240.0 316.9,240.0 318.5,240.0 320.1,240.0 321.7,240.0 323.3,240.0 324.9,240.0 326.5,240.0 328.1,240.0 329.7,240.0 331.3,240.0 332.9,240.0 334.5,240.0 336.1,240.0 337.7,240.0 339.3,240.0 340.9,240.0 342.5,240.0 344.1,240.0 345.8,240.0 347.4,240.0 349.0,240.0 350.6,240.0 352.2,240.0 353.8,240.0 355.4,240.0 357.0,240.0 358.6,240.0 360.2,240.0 361.8,240.0 363.4,240.0 365.0,240.0 366.6,240.0 368.2,240.0 369.8,240.0 371.4,240.0 373.0,240.0 374.6,240.0 376.3,240.0 377.9,240.0 379.5,240.0 381.1,240.0 382.7,240.0 384.3,240.0 385.9,240.0 387.5,240.0 389.1,240.0 390.7,240.0 392.3,240.0 393.9,240.0 395.5,240.0 397.1,240.0 398.7,240.0 400.3,240.0 401.9,240.0 403.5,240.0 405.2,240.0 406.8,240.0 408.4,240.0 410.0,240.0 411.6,240.0 413.2,240.0 414.8,240.0 416.4,240.0 418.0,240.0 419.6,240.0 421.2,240.0 422.8,240.0 424.4,240.0 426.0,240.0 427.6,240.0 429.2,240.0 430.8,240.0 432.4,240.0 434.0,240.0 435.7,240.0 437.3,240.0 438.9,240.0 440.5,240.0 442.1,240.0 443.7,240.0 445.3,240.0 446.9,240.0 448.5,240.0 450.1,240.0 451.7,240.0 453.3,240.0 454.9,240.0 456.5,240.0 458.1,240.0 459.7,240.0 461.3,240.0 462.9,240.0 464.5,240.0 466.2,240.0 467.8,240.0 469.4,240.0 471.0,240.0 472.6,240.0 474.2,240.0 475.8,240.0 477.4,240.0 479.0,240.0 480.6,240.0 482.2,240.0 483.8,240.0 485.4,240.0 487.0,240.0 488.6,240.0 490.2,240.0 491.8,240.0 493.4,240.0 495.1,240.0 496.7,240.0 498.3,240.0 499.9,240.0 501.5,240.0 503.1,240.0 504.7,240.0 506.3,240.0 507.9,240.0 509.5,240.0 511.1,240.0 512.7,240.0 514.3,240.0 515.9,240.0 517.5,240.0 519.1,240.0 520.7,240.0 522.3,240.0 523.9,240.0 525.6,240.0 527.2,240.0 528.8,240.0 530.4,240.0 532.0,240.0 533.6,240.0 535.2,240.0 536.8,240.0 538.4,240.0 540.0,240.0"/><polyline class="ink" points="60.0,26.1 61.6,27.2 63.2,28.4 64.8,29.5 66.4,30.6 68.0,31.7 69.6,32.9 71.2,34.0 72.8,35.1 74.4,36.2 76.1,37.4 77.7,38.5 79.3,39.6 80.9,40.7 82.5,41.8 84.1,43.0 85.7,44.1 87.3,45.2 88.9,46.3 90.5,47.5 92.1,48.6 93.7,49.7 95.3,50.8 96.9,52.0 98.5,53.1 100.1,54.2 101.7,55.3 103.3,56.5 104.9,57.6 106.6,58.7 108.2,59.8 109.8,61.0 111.4,62.1 113.0,63.2 114.6,64.3 116.2,65.5 117.8,66.6 119.4,67.7 121.0,68.8 122.6,70.0 124.2,71.1 125.8,72.2 127.4,73.3 129.0,74.4 130.6,75.6 132.2,76.7 133.8,77.8 135.5,78.9 137.1,80.1 138.7,81.2 140.3,82.3 141.9,83.4 143.5,84.6 145.1,85.7 146.7,86.8 148.3,87.9 149.9,89.1 151.5,90.2 153.1,91.3 154.7,92.4 156.3,93.6 157.9,94.7 159.5,95.8 161.1,96.9 162.7,98.1 164.3,99.2 166.0,100.3 167.6,101.4 169.2,102.6 170.8,103.7 172.4,104.8 174.0,105.9 175.6,107.0 177.2,108.2 178.8,109.3 180.4,110.4 182.0,111.5 183.6,112.7 185.2,113.8 186.8,114.9 188.4,116.0 190.0,117.2 191.6,118.3 193.2,119.4 194.8,120.5 196.5,121.7 198.1,122.8 199.7,123.9 201.3,125.0 202.9,126.2 204.5,127.3 206.1,128.4 207.7,129.5 209.3,130.7 210.9,131.8 212.5,132.9 214.1,134.0 215.7,135.2 217.3,136.3 218.9,137.4 220.5,138.5 222.1,139.6 223.7,140.8 225.4,141.9 227.0,143.0 228.6,144.1 230.2,145.3 231.8,146.4 233.4,147.5 235.0,148.6 236.6,149.8 238.2,150.9 239.8,152.0 241.4,153.1 243.0,154.3 244.6,155.4 246.2,156.5 247.8,157.6 249.4,158.8 251.0,159.9 252.6,161.0 254.2,162.1 255.9,163.3 257.5,164.4 259.1,165.5 260.7,166.6 262.3,167.7 263.9,168.9 265.5,170.0 267.1,171.1 268.7,172.2 270.3,173.4 271.9,174.5 273.5,175.6 275.1,176.7 276.7,177.9 278.3,179.0 279.9,180.1 281.5,181.2 283.1,182.4 284.7,183.5 286.4,184.6 288.0,185.7 289.6,186.9 291.2,188.0 292.8,189.1 294.4,190.2 296.0,191.4 297.6,192.5 299.2,193.6 300.8,194.7 302.4,195.9 304.0,197.0 305.6,198.1 307.2,199.2 308.8,200.3 310.4,201.5 312.0,202.6 313.6,203.7 315.3,204.8 316.9,206.0 318.5,207.1 320.1,208.2 321.7,209.3 323.3,210.5 324.9,211.6 326.5,212.7 328.1,213.8 329.7,215.0 331.3,216.1 332.9,217.2 334.5,218.3 336.1,219.5 337.7,220.6 339.3,221.7 340.9,222.8 342.5,224.0 344.1,225.1 345.8,226.2 347.4,227.3 349.0,228.5 350.6,229.6 352.2,230.7 353.8,231.8 355.4,232.9 357.0,234.1 358.6,235.2 360.2,236.3 361.8,237.4 363.4,238.6 365.0,239.7 366.6,240.0 368.2,240.0 369.8,240.0 371.4,240.0 373.0,240.0 374.6,240.0 376.3,240.0 377.9,240.0 379.5,240.0 381.1,240.0 382.7,240.0 384.3,240.0 385.9,240.0 387.5,240.0 389.1,240.0 390.7,240.0 392.3,240.0 393.9,240.0 395.5,240.0 397.1,240.0 398.7,240.0 400.3,240.0 401.9,240.0 403.5,240.0 405.2,240.0 406.8,240.0 408.4,240.0 410.0,240.0 411.6,240.0 413.2,240.0 414.8,240.0 416.4,240.0 418.0,240.0 419.6,240.0 421.2,240.0 422.8,240.0 424.4,240.0 426.0,240.0 427.6,240.0 429.2,240.0 430.8,240.0 432.4,240.0 434.0,240.0 435.7,240.0 437.3,240.0 438.9,240.0 440.5,240.0 442.1,240.0 443.7,240.0 445.3,240.0 446.9,240.0 448.5,240.0 450.1,240.0 451.7,240.0 453.3,240.0 454.9,240.0 456.5,240.0 458.1,240.0 459.7,240.0 461.3,240.0 462.9,240.0 464.5,240.0 466.2,240.0 467.8,240.0 469.4,240.0 471.0,240.0 472.6,240.0 474.2,240.0 475.8,240.0 477.4,240.0 479.0,240.0 480.6,240.0 482.2,240.0 483.8,240.0 485.4,240.0 487.0,240.0 488.6,240.0 490.2,240.0 491.8,240.0 493.4,240.0 495.1,240.0 496.7,240.0 498.3,240.0 499.9,240.0 501.5,240.0 503.1,240.0 504.7,240.0 506.3,240.0 507.9,240.0 509.5,240.0 511.1,240.0 512.7,240.0 514.3,240.0 515.9,240.0 517.5,240.0 519.1,240.0 520.7,240.0 522.3,240.0 523.9,240.0 525.6,240.0 527.2,240.0 528.8,240.0 530.4,240.0 532.0,240.0 533.6,240.0 535.2,240.0 536.8,240.0 538.4,240.0 540.0,240.0"/><polyline class="hl" points="60.0,12.6 61.6,14.1 63.2,15.6 64.8,17.1 66.4,18.6 68.0,20.1 69.6,21.6 71.2,23.1 72.8,24.6 74.4,26.0 76.1,27.5 77.7,29.0 79.3,30.5 80.9,31.9 82.5,33.4 84.1,34.9 85.7,36.3 87.3,37.8 88.9,39.2 90.5,40.7 92.1,42.1 93.7,43.6 95.3,45.0 96.9,46.5 98.5,47.9 100.1,49.4 101.7,50.8 103.3,52.2 104.9,53.6 106.6,55.1 108.2,56.5 109.8,57.9 111.4,59.3 113.0,60.7 114.6,62.1 116.2,63.5 117.8,64.9 119.4,66.3 121.0,67.7 122.6,69.1 124.2,70.5 125.8,71.9 127.4,73.3 129.0,74.7 130.6,76.0 132.2,77.4 133.8,78.8 135.5,80.1 137.1,81.5 138.7,82.8 140.3,84.2 141.9,85.5 143.5,86.8 145.1,88.2 146.7,89.5 148.3,90.8 149.9,92.2 151.5,93.5 153.1,94.8 154.7,96.1 156.3,97.4 157.9,98.7 159.5,100.0 161.1,101.3 162.7,102.6 164.3,103.8 166.0,105.1 167.6,106.4 169.2,107.6 170.8,108.9 172.4,110.2 174.0,111.4 175.6,112.6 177.2,113.9 178.8,115.1 180.4,116.3 182.0,117.6 183.6,118.8 185.2,120.0 186.8,121.2 188.4,122.4 190.0,123.6 191.6,124.8 193.2,125.9 194.8,127.1 196.5,128.3 198.1,129.4 199.7,130.6 201.3,131.7 202.9,132.9 204.5,134.0 206.1,135.2 207.7,136.3 209.3,137.4 210.9,138.5 212.5,139.6 214.1,140.7 215.7,141.8 217.3,142.9 218.9,144.0 220.5,145.0 222.1,146.1 223.7,147.2 225.4,148.2 227.0,149.3 228.6,150.3 230.2,151.3 231.8,152.4 233.4,153.4 235.0,154.4 236.6,155.4 238.2,156.4 239.8,157.4 241.4,158.4 243.0,159.3 244.6,160.3 246.2,161.3 247.8,162.2 249.4,163.2 251.0,164.1 252.6,165.0 254.2,166.0 255.9,166.9 257.5,167.8 259.1,168.7 260.7,169.6 262.3,170.5 263.9,171.4 265.5,172.2 267.1,173.1 268.7,174.0 270.3,174.8 271.9,175.7 273.5,176.5 275.1,177.3 276.7,178.1 278.3,179.0 279.9,179.8 281.5,180.6 283.1,181.4 284.7,182.1 286.4,182.9 288.0,183.7 289.6,184.5 291.2,185.2 292.8,186.0 294.4,186.7 296.0,187.4 297.6,188.1 299.2,188.9 300.8,189.6 302.4,190.3 304.0,191.0 305.6,191.7 307.2,192.3 308.8,193.0 310.4,193.7 312.0,194.3 313.6,195.0 315.3,195.6 316.9,196.3 318.5,196.9 320.1,197.5 321.7,198.1 323.3,198.8 324.9,199.4 326.5,200.0 328.1,200.5 329.7,201.1 331.3,201.7 332.9,202.3 334.5,202.8 336.1,203.4 337.7,203.9 339.3,204.5 340.9,205.0 342.5,205.5 344.1,206.1 345.8,206.6 347.4,207.1 349.0,207.6 350.6,208.1 352.2,208.6 353.8,209.1 355.4,209.5 357.0,210.0 358.6,210.5 360.2,210.9 361.8,211.4 363.4,211.8 365.0,212.3 366.6,212.7 368.2,213.1 369.8,213.5 371.4,214.0 373.0,214.4 374.6,214.8 376.3,215.2 377.9,215.6 379.5,216.0 381.1,216.4 382.7,216.7 384.3,217.1 385.9,217.5 387.5,217.8 389.1,218.2 390.7,218.5 392.3,218.9 393.9,219.2 395.5,219.6 397.1,219.9 398.7,220.2 400.3,220.6 401.9,220.9 403.5,221.2 405.2,221.5 406.8,221.8 408.4,222.1 410.0,222.4 411.6,222.7 413.2,223.0 414.8,223.3 416.4,223.5 418.0,223.8 419.6,224.1 421.2,224.4 422.8,224.6 424.4,224.9 426.0,225.1 427.6,225.4 429.2,225.6 430.8,225.9 432.4,226.1 434.0,226.3 435.7,226.6 437.3,226.8 438.9,227.0 440.5,227.2 442.1,227.5 443.7,227.7 445.3,227.9 446.9,228.1 448.5,228.3 450.1,228.5 451.7,228.7 453.3,228.9 454.9,229.1 456.5,229.3 458.1,229.4 459.7,229.6 461.3,229.8 462.9,230.0 464.5,230.2 466.2,230.3 467.8,230.5 469.4,230.7 471.0,230.8 472.6,231.0 474.2,231.1 475.8,231.3 477.4,231.4 479.0,231.6 480.6,231.7 482.2,231.9 483.8,232.0 485.4,232.2 487.0,232.3 488.6,232.4 490.2,232.6 491.8,232.7 493.4,232.8 495.1,232.9 496.7,233.1 498.3,233.2 499.9,233.3 501.5,233.4 503.1,233.5 504.7,233.7 506.3,233.8 507.9,233.9 509.5,234.0 511.1,234.1 512.7,234.2 514.3,234.3 515.9,234.4 517.5,234.5 519.1,234.6 520.7,234.7 522.3,234.8 523.9,234.9 525.6,235.0 527.2,235.1 528.8,235.1 530.4,235.2 532.0,235.3 533.6,235.4 535.2,235.5 536.8,235.6 538.4,235.6 540.0,235.7"/><text class="t-ink" x="184.9" y="135.8" text-anchor="end">hinge</text><text class="t-hl" x="417.8" y="213.8">logistic</text><text class="t-mut" x="173.5" y="172.9">0–1</text><text class="t-mut" x="369.5" y="38.3">yf = 1</text></svg><figcaption>Losses as a function of the margin y·f(x). The 0–1 loss counts mistakes. The hinge loss max(0, 1 − yf) (SVM) is zero once a point is beyond the margin (yf ≥ 1) and grows linearly otherwise. The logistic loss log₂(1 + e^(−yf)) never reaches exactly zero.</figcaption></figure>
<!-- /fig:svm-losses -->

Unlike logistic loss, the hinge loss is **exactly zero** for points with $yf \ge 1$. That's why points far from the boundary have no influence and the solution is **sparse** (only the SVs matter).

## 8.7 Kernels: non-linear boundaries for free

Map the inputs to a richer feature space $\phi(x)$ where the classes become linearly separable. XOR becomes separable once you add $x_1x_2$ (topic 4). Because the dual only uses dot products, we never need $\phi$ itself, only the **kernel** $K(x, z) = \phi(x)^\top\phi(z)$:

<div class="formula">

| Kernel | $K(x, z)$ | Notes |
|---|---|---|
| Linear | $x^\top z$ | the ordinary SVM |
| Polynomial | $(x^\top z + c)^d$ | all monomials up to degree $d$ |
| RBF (Gaussian) | $\exp(-\gamma\|x - z\|^2)$ | infinite-dimensional $\phi$; large $\gamma$ → wiggly boundary (overfits), small $\gamma$ → smooth |

A valid kernel must give a symmetric, positive semi-definite Gram matrix (Mercer's condition).

</div>

For example, with $x, z \in \mathbb{R}^2$, $(x^\top z)^2$ equals $\phi(x)^\top\phi(z)$ with $\phi(x) = (x_1^2, \sqrt2x_1x_2, x_2^2)$. This is the **kernel trick**: a dot product in 3-D, computed with 2-D arithmetic.

---

## Summary: important points

<div class="formula">

1. The SVM chooses the maximum-margin separator. Canonical scaling puts the nearest points at $y f(x) = 1$.
2. Margin lines are $w^\top x + b = \pm1$. Width $= 2/\|w\|$, and the distance from the boundary to the nearest point is $1/\|w\|$.
3. Hard margin: $\min\frac12\|w\|^2$ s.t. $y_i(w^\top x_i + b) \ge 1$. It's convex with a unique $w$.
4. Support vectors satisfy $y_if(x_i) = 1$. $w = \sum\alpha_iy_ix_i$ with $\alpha_i > 0$ only for SVs, and $\sum\alpha_iy_i = 0$.
5. Removing non-SVs leaves the solution unchanged.
6. Soft margin $= \frac12\|w\|^2 + C\sum\xi_i$ = hinge loss + L2. Large C: narrow margin, overfitting risk. Small C: wide margin.
7. Kernels replace $x_i^\top x_j$ with $K(x_i, x_j)$: polynomial $(x^\top z + c)^d$, RBF $e^{-\gamma\|x - z\|^2}$.
8. A hard-margin SVM on separable data has 100% training accuracy.

</div>

<div class="trap">

- "Margin" can mean $1/\|w\|$ or $2/\|w\|$. Read the options.
- Support vectors are the points **on** the margin, not every point near the boundary, and not the farthest points.
- Large C means a *smaller* margin, the opposite of what many people guess.
- An SVM outputs a class (or a score), not a probability.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2025 Q53 (2 marks, MSQ)

Class 1: (2, 0), (0, 2), (2, 2). Class 2: (0, 0). A hard-margin SVM gives $w$ and $b$. Which are correct?
(A) $w = (4, 4)$ and $b = 1$ (B) There are 3 support vectors (C) The margin is $\sqrt2$ (D) The training accuracy is 98%

<details>
<summary>Show solution</summary>

**Answer: B; C**

From §8.5: $w = (1, 1)$, $b = -1$. The support vectors are (2, 0), (0, 2) and (0, 0), so (B) is true. (2, 2) has $yf = 3$ and isn't a support vector. The width is $2/\|w\| = \sqrt2$, so (C) is true.

- (A): with $w = (4, 4)$, $b = 1$, the point (0, 0) gives $f = 1 > 0$, so it would be classified as class 1, which is wrong.
- (D): a hard-margin SVM separates its training data perfectly, so the accuracy is 100%. And with 4 points, 98% isn't even possible.

</details>

### GATE DA 2024 Q17 (1 mark, MCQ)

Points $x_1 = (1, 0)$, $x_2 = (0, 1)$, $x_5 = (2, 2)$ have label $+1$; $x_3 = (0, -1)$, $x_4 = (-1, 0)$, $x_6 = (-2, -2)$ have label $-1$. Which set is a possible set of support vectors for the hard-margin linear SVM?
(A) $\{x_1, x_2, x_5\}$ (B) $\{x_3, x_4, x_5\}$ (C) $\{x_4, x_5\}$ (D) $\{x_1, x_2, x_3, x_4\}$

<details>
<summary>Show solution</summary>

**Answer: (D)**

The data is symmetric under $x \to -x$ with the labels flipped, so the boundary passes through the origin. The closest pairs across classes are $x_1, x_2$ (on the line $x_1 + x_2 = 1$) and $x_3, x_4$ (on $x_1 + x_2 = -1$). These two lines are parallel, so $w \propto (1, 1)$ and $b = 0$.

Canonical scaling: $w^\top x_1 = 1$ gives $w = (1, 1)$. Then:

- $x_1, x_2$: $yf = 1$ → support vectors.
- $x_3, x_4$: $yf = (-1)(-1) = 1$ → support vectors.
- $x_5$: $yf = 4$ and $x_6$: $yf = 4$ → not support vectors.

The support vectors are $\{x_1, x_2, x_3, x_4\}$, and the margin width is $2/\sqrt2 = \sqrt2$. I confirmed this with an exact search over all directions $w$.

- (A), (B) and (C) all include $x_5$, which is far from the boundary.
- (A) and (C) also lack support vectors from both classes.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** A hard-margin SVM has $w = (3, 4)$. What is the total width of the margin?

<details>
<summary>Show solution</summary>

**Answer: 0.4**

$2/\|w\| = 2/5 = $ **0.4**.

</details>

**F2 (2 marks, MSQ).** A linear SVM has $w = (1, 1)$ and $b = -3$. Which training points lie exactly on a margin line?
(A) $(1, 1)$ with $y = -1$ (B) $(2, 2)$ with $y = +1$ (C) $(3, 1)$ with $y = +1$ (D) $(0, 0)$ with $y = -1$

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

Compute $y\,(x_1 + x_2 - 3)$ for each:

- (A) $-1 \times (-1) = 1$
- (B) $1 \times 1 = 1$
- (C) $1 \times 1 = 1$
- (D) $-1 \times (-3) = 3$, which is outside the margin.

</details>

**F3 (1 mark, NAT).** Four points have $(y, f(x))$ = $(+1, 2.0)$, $(+1, 0.5)$, $(-1, 0.2)$, $(-1, -3)$. What is their total hinge loss?

<details>
<summary>Show solution</summary>

**Answer: 1.7**

$\max(0, 1 - yf)$ for each:

- $1 - 2 = -1 \to 0$
- $1 - 0.5 = 0.5$
- $1 + 0.2 = 1.2$ (this one is misclassified)
- $1 - 3 = -2 \to 0$

Total: $0.5 + 1.2 = $ **1.7**.

</details>

**F4 (1 mark, NAT).** What is the polynomial kernel $K(x, z) = (x^\top z + 1)^2$ for $x = (1, 2)$ and $z = (3, 1)$?

<details>
<summary>Show solution</summary>

**Answer: 36**

$x^\top z = 3 + 2 = 5$, so $K = (5 + 1)^2 = $ **36**.

</details>

**F5 (2 marks, MSQ).** Which statements about soft-margin SVMs are true?
(A) Increasing C tends to reduce the margin width (B) As $C \to \infty$, the solution on separable data approaches the hard-margin solution (C) A point with slack $\xi_i = 1.5$ is misclassified (D) Removing a point that lies strictly outside the margin changes the solution

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

(C): $\xi > 1$ means $yf < 0$, so the point is on the wrong side. (D) is false, because such a point has $\alpha_i = 0$ and doesn't affect the solution.

</details>

**F6 (2 marks, NAT).** The dual variables of a trained SVM are $\alpha = (0.5, 0.5, 1)$ for the points $(2, 0)$ with $y = +1$, $(0, 2)$ with $y = +1$, and $(0, 0)$ with $y = -1$. What is $w_1$?

<details>
<summary>Show solution</summary>

**Answer: 1**

$w = \sum\alpha_iy_ix_i = 0.5(2, 0) + 0.5(0, 2) - 1(0, 0) = (1, 1)$, so $w_1 = $ **1**.

</details>
