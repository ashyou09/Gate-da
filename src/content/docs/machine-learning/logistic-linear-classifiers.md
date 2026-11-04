---
title: 4. Logistic regression & linear classifiers
description: The sigmoid and its derivative, logistic regression as a model of log-odds, cross-entropy and its gradient, softmax, the geometry of linear decision boundaries, linear separability, the perceptron, and nearest-mean classifiers.
sidebar:
  label: 4. Logistic & linear classifiers
  order: 4
---

**Why it matters:** four PYQs live here:
- 2024 Q33: the sigmoid derivative;
- 2024 Q53: which datasets are linearly separable;
- 2025 Q22: what the perceptron update does;
- 2025 Q55: the nearest-mean classifier is linear.

They all rest on one picture: a **linear score $f(x) = w^\top x + b$** and the line where it equals 0.

## Topic map

<div class="mindmap">

- **Linear classifiers**
  - Score
    - $f(x) = w^\top x + b$, predict by its sign
    - boundary $f(x) = 0$ is a hyperplane, $w$ is its normal
    - distance $= |f(x)|/\|w\|$
  - Logistic regression
    - $P(y = 1 \mid x) = \sigma(w^\top x + b)$
    - log-odds are linear in $x$
    - cross-entropy loss, gradient $(p - y)x$
    - softmax for $K$ classes
  - Sigmoid
    - $\sigma(-z) = 1 - \sigma(z)$, $\sigma' = \sigma(1 - \sigma) \le 0.25$
  - Linear separability
    - XOR isn't separable; feature maps fix it
  - Perceptron
    - update on a mistake: $w \leftarrow w + yx$, $b \leftarrow b + y$
    - converges iff the data is separable
  - Nearest-mean classifier
    - turns out to be linear

</div>

## 4.1 The linear score and its geometry

A **linear classifier** computes one number per input,

$$
f(x) = w^\top x + b = w_1x_1 + \dots + w_dx_d + b,
$$

and predicts **class +1 if $f(x) > 0$** and **class −1 otherwise**.

<!-- fig:linear-boundary -->
<figure class="diagram"><svg class="dg" viewBox="0 0 500 320" role="img" aria-label="Linear decision boundary with normal vector" xmlns="http://www.w3.org/2000/svg"><path class="ax" d="M40,20 V280 H460"/><text x="250.0" y="310" text-anchor="middle">x₁</text><text x="16" y="150.0" text-anchor="middle" transform="rotate(-90 16 150.0)">x₂</text><polygon style="fill:var(--gd-ink);fill-opacity:.08" points="40.0,85.0 383.6,280.0 460.0,280.0 460.0,20.0 40.0,20.0"/><line class="ink" x1="40.0" y1="85.0" x2="383.6" y2="280.0"/><line class="hl" x1="169.8" y1="158.7" x2="211.1" y2="117.1"/><circle class="dot-hl" cx="211.1" cy="117.1" r="4"/><text class="t-hl" x="219.1" y="117.1">w</text><line class="mut" style="stroke:var(--gd-trap)" x1="345.5" y1="106.7" x2="249.2" y2="203.7"/><circle class="dot" cx="345.5" cy="106.7" r="5"/><text class="t-warn" x="345.5" y="94.7" text-anchor="middle">x · distance |f(x)|/‖w‖</text><text class="t-ink" x="93.5" y="43.1">f(x) &gt; 0 → class +1</text><text class="t-mut" x="55.3" y="265.6">f(x) &lt; 0 → class −1</text><text class="t-ink" x="223.3" y="245.3" text-anchor="start">wᵀx + b = 0</text></svg><figcaption>A linear classifier f(x) = wᵀx + b. The boundary f(x) = 0 is a line (a hyperplane in higher dimensions); w is perpendicular to it and points towards the positive side. The distance of a point from the boundary is |f(x)| / ‖w‖.</figcaption></figure>
<!-- /fig:linear-boundary -->

<div class="formula">

- The **decision boundary** $\{x : w^\top x + b = 0\}$ is a line in 2-D, a plane in 3-D, and a **hyperplane** in general.
- $w$ is **perpendicular** to the boundary and points into the positive region.
- Signed distance of a point from the boundary: $\dfrac{w^\top x + b}{\|w\|}$.
- Scaling $(w, b)$ by any $c > 0$ gives the **same** boundary and the same predictions. Only the direction matters, which is why SVMs have to fix a scale.

</div>

Logistic regression, the perceptron, linear SVM, LDA and the nearest-mean classifier are **all** linear classifiers. They differ only in **how they choose $w$ and $b$**.

## 4.2 Why not just use linear regression for classes?

Code the classes as 0/1 and fit a line. You get "probabilities" below 0 and above 1, and a single far-away point drags the line and moves the boundary even though it was already correctly classified. We want a model that outputs a value in $(0, 1)$ and doesn't get punished for being *confidently right*.

## 4.3 The sigmoid

<div class="formula">

$$
\sigma(z) = \frac{1}{1 + e^{-z}} \in (0, 1)
$$

| Property | Value |
|---|---|
| $\sigma(0)$ | $0.5$ |
| $z \to +\infty$ / $z \to -\infty$ | $\sigma \to 1$ / $\sigma \to 0$ |
| Symmetry | $\sigma(-z) = 1 - \sigma(z)$ |
| **Derivative** | $\sigma'(z) = \sigma(z)\,\big(1 - \sigma(z)\big)$, largest value $0.25$ at $z = 0$ |
| Inverse (the **logit**) | $z = \ln\dfrac{p}{1 - p}$, the log-odds |

</div>

<!-- fig:logit-sigmoid -->
<figure class="diagram"><svg class="dg" viewBox="0 0 580 285" role="img" aria-label="Sigmoid and its derivative" xmlns="http://www.w3.org/2000/svg"><path class="ax" d="M60,20 V240 H560"/><text x="310.0" y="270" text-anchor="middle">z = wᵀx + b</text><text class="t-mut" x="95.7" y="254.0" text-anchor="middle">-6</text><text class="t-mut" x="167.1" y="254.0" text-anchor="middle">-4</text><text class="t-mut" x="238.6" y="254.0" text-anchor="middle">-2</text><text class="t-mut" x="310.0" y="254.0" text-anchor="middle">0</text><text class="t-mut" x="381.4" y="254.0" text-anchor="middle">2</text><text class="t-mut" x="452.9" y="254.0" text-anchor="middle">4</text><text class="t-mut" x="524.3" y="254.0" text-anchor="middle">6</text><line class="grid" x1="60.0" y1="187.6" x2="560.0" y2="187.6"/><text class="t-mut" x="54.0" y="191.6" text-anchor="end">0.25</text><line class="grid" x1="60.0" y1="135.2" x2="560.0" y2="135.2"/><text class="t-mut" x="54.0" y="139.2" text-anchor="end">0.5</text><line class="grid" x1="60.0" y1="30.5" x2="560.0" y2="30.5"/><text class="t-mut" x="54.0" y="34.5" text-anchor="end">1</text><polyline class="ink" points="60.0,239.8 61.7,239.8 63.3,239.8 65.0,239.8 66.7,239.8 68.4,239.8 70.0,239.7 71.7,239.7 73.4,239.7 75.1,239.7 76.7,239.7 78.4,239.7 80.1,239.7 81.7,239.6 83.4,239.6 85.1,239.6 86.8,239.6 88.4,239.6 90.1,239.6 91.8,239.5 93.4,239.5 95.1,239.5 96.8,239.5 98.5,239.4 100.1,239.4 101.8,239.4 103.5,239.4 105.2,239.3 106.8,239.3 108.5,239.3 110.2,239.2 111.8,239.2 113.5,239.1 115.2,239.1 116.9,239.1 118.5,239.0 120.2,239.0 121.9,238.9 123.5,238.9 125.2,238.8 126.9,238.8 128.6,238.7 130.2,238.6 131.9,238.6 133.6,238.5 135.3,238.4 136.9,238.4 138.6,238.3 140.3,238.2 141.9,238.1 143.6,238.0 145.3,237.9 147.0,237.8 148.6,237.7 150.3,237.6 152.0,237.5 153.6,237.4 155.3,237.3 157.0,237.2 158.7,237.0 160.3,236.9 162.0,236.7 163.7,236.6 165.4,236.4 167.0,236.2 168.7,236.1 170.4,235.9 172.0,235.7 173.7,235.5 175.4,235.3 177.1,235.1 178.7,234.8 180.4,234.6 182.1,234.3 183.7,234.1 185.4,233.8 187.1,233.5 188.8,233.2 190.4,232.9 192.1,232.6 193.8,232.2 195.5,231.9 197.1,231.5 198.8,231.1 200.5,230.7 202.1,230.3 203.8,229.8 205.5,229.3 207.2,228.9 208.8,228.4 210.5,227.8 212.2,227.3 213.8,226.7 215.5,226.1 217.2,225.5 218.9,224.9 220.5,224.2 222.2,223.5 223.9,222.8 225.6,222.0 227.2,221.2 228.9,220.4 230.6,219.5 232.2,218.7 233.9,217.8 235.6,216.8 237.3,215.8 238.9,214.8 240.6,213.7 242.3,212.7 243.9,211.5 245.6,210.3 247.3,209.1 249.0,207.9 250.6,206.6 252.3,205.3 254.0,203.9 255.7,202.5 257.3,201.0 259.0,199.5 260.7,197.9 262.3,196.3 264.0,194.7 265.7,193.0 267.4,191.3 269.0,189.5 270.7,187.7 272.4,185.8 274.0,183.9 275.7,182.0 277.4,180.0 279.1,178.0 280.7,175.9 282.4,173.8 284.1,171.7 285.8,169.5 287.4,167.3 289.1,165.0 290.8,162.8 292.4,160.5 294.1,158.2 295.8,155.8 297.5,153.4 299.1,151.1 300.8,148.7 302.5,146.2 304.1,143.8 305.8,141.4 307.5,138.9 309.2,136.5 310.8,134.0 312.5,131.6 314.2,129.1 315.9,126.7 317.5,124.2 319.2,121.8 320.9,119.4 322.5,117.0 324.2,114.7 325.9,112.3 327.6,110.0 329.2,107.7 330.9,105.4 332.6,103.2 334.2,101.0 335.9,98.8 337.6,96.7 339.3,94.6 340.9,92.5 342.6,90.5 344.3,88.5 346.0,86.6 347.6,84.6 349.3,82.8 351.0,81.0 352.6,79.2 354.3,77.5 356.0,75.8 357.7,74.1 359.3,72.5 361.0,71.0 362.7,69.5 364.3,68.0 366.0,66.6 367.7,65.2 369.4,63.9 371.0,62.6 372.7,61.3 374.4,60.1 376.1,59.0 377.7,57.8 379.4,56.7 381.1,55.7 382.7,54.7 384.4,53.7 386.1,52.7 387.8,51.8 389.4,50.9 391.1,50.1 392.8,49.3 394.4,48.5 396.1,47.7 397.8,47.0 399.5,46.3 401.1,45.6 402.8,45.0 404.5,44.4 406.2,43.8 407.8,43.2 409.5,42.6 411.2,42.1 412.8,41.6 414.5,41.1 416.2,40.7 417.9,40.2 419.5,39.8 421.2,39.4 422.9,39.0 424.5,38.6 426.2,38.3 427.9,37.9 429.6,37.6 431.2,37.3 432.9,37.0 434.6,36.7 436.3,36.4 437.9,36.1 439.6,35.9 441.3,35.7 442.9,35.4 444.6,35.2 446.3,35.0 448.0,34.8 449.6,34.6 451.3,34.4 453.0,34.2 454.6,34.1 456.3,33.9 458.0,33.7 459.7,33.6 461.3,33.5 463.0,33.3 464.7,33.2 466.4,33.1 468.0,33.0 469.7,32.8 471.4,32.7 473.0,32.6 474.7,32.5 476.4,32.4 478.1,32.4 479.7,32.3 481.4,32.2 483.1,32.1 484.7,32.0 486.4,32.0 488.1,31.9 489.8,31.8 491.4,31.8 493.1,31.7 494.8,31.7 496.5,31.6 498.1,31.6 499.8,31.5 501.5,31.5 503.1,31.4 504.8,31.4 506.5,31.3 508.2,31.3 509.8,31.3 511.5,31.2 513.2,31.2 514.8,31.2 516.5,31.1 518.2,31.1 519.9,31.1 521.5,31.0 523.2,31.0 524.9,31.0 526.6,31.0 528.2,30.9 529.9,30.9 531.6,30.9 533.2,30.9 534.9,30.9 536.6,30.8 538.3,30.8 539.9,30.8 541.6,30.8 543.3,30.8 544.9,30.8 546.6,30.8 548.3,30.7 550.0,30.7 551.6,30.7 553.3,30.7 555.0,30.7 556.7,30.7 558.3,30.7 560.0,30.7"/><polyline class="hl" points="60.0,239.8 61.7,239.8 63.3,239.8 65.0,239.8 66.7,239.8 68.4,239.8 70.0,239.7 71.7,239.7 73.4,239.7 75.1,239.7 76.7,239.7 78.4,239.7 80.1,239.7 81.7,239.6 83.4,239.6 85.1,239.6 86.8,239.6 88.4,239.6 90.1,239.6 91.8,239.5 93.4,239.5 95.1,239.5 96.8,239.5 98.5,239.4 100.1,239.4 101.8,239.4 103.5,239.4 105.2,239.3 106.8,239.3 108.5,239.3 110.2,239.2 111.8,239.2 113.5,239.2 115.2,239.1 116.9,239.1 118.5,239.0 120.2,239.0 121.9,238.9 123.5,238.9 125.2,238.8 126.9,238.8 128.6,238.7 130.2,238.7 131.9,238.6 133.6,238.5 135.3,238.5 136.9,238.4 138.6,238.3 140.3,238.2 141.9,238.1 143.6,238.1 145.3,238.0 147.0,237.9 148.6,237.8 150.3,237.7 152.0,237.5 153.6,237.4 155.3,237.3 157.0,237.2 158.7,237.1 160.3,236.9 162.0,236.8 163.7,236.6 165.4,236.5 167.0,236.3 168.7,236.1 170.4,236.0 172.0,235.8 173.7,235.6 175.4,235.4 177.1,235.2 178.7,235.0 180.4,234.7 182.1,234.5 183.7,234.2 185.4,234.0 187.1,233.7 188.8,233.4 190.4,233.1 192.1,232.8 193.8,232.5 195.5,232.2 197.1,231.8 198.8,231.5 200.5,231.1 202.1,230.7 203.8,230.3 205.5,229.9 207.2,229.5 208.8,229.0 210.5,228.5 212.2,228.1 213.8,227.6 215.5,227.0 217.2,226.5 218.9,225.9 220.5,225.4 222.2,224.8 223.9,224.2 225.6,223.5 227.2,222.9 228.9,222.2 230.6,221.5 232.2,220.8 233.9,220.1 235.6,219.4 237.3,218.6 238.9,217.8 240.6,217.0 242.3,216.2 243.9,215.4 245.6,214.5 247.3,213.7 249.0,212.8 250.6,211.9 252.3,211.0 254.0,210.1 255.7,209.2 257.3,208.3 259.0,207.3 260.7,206.4 262.3,205.4 264.0,204.5 265.7,203.5 267.4,202.6 269.0,201.7 270.7,200.7 272.4,199.8 274.0,198.9 275.7,198.0 277.4,197.2 279.1,196.3 280.7,195.5 282.4,194.7 284.1,194.0 285.8,193.2 287.4,192.5 289.1,191.9 290.8,191.2 292.4,190.7 294.1,190.1 295.8,189.6 297.5,189.2 299.1,188.8 300.8,188.5 302.5,188.2 304.1,188.0 305.8,187.8 307.5,187.7 309.2,187.6 310.8,187.6 312.5,187.7 314.2,187.8 315.9,188.0 317.5,188.2 319.2,188.5 320.9,188.8 322.5,189.2 324.2,189.6 325.9,190.1 327.6,190.7 329.2,191.2 330.9,191.9 332.6,192.5 334.2,193.2 335.9,194.0 337.6,194.7 339.3,195.5 340.9,196.3 342.6,197.2 344.3,198.0 346.0,198.9 347.6,199.8 349.3,200.7 351.0,201.7 352.6,202.6 354.3,203.5 356.0,204.5 357.7,205.4 359.3,206.4 361.0,207.3 362.7,208.3 364.3,209.2 366.0,210.1 367.7,211.0 369.4,211.9 371.0,212.8 372.7,213.7 374.4,214.5 376.1,215.4 377.7,216.2 379.4,217.0 381.1,217.8 382.7,218.6 384.4,219.4 386.1,220.1 387.8,220.8 389.4,221.5 391.1,222.2 392.8,222.9 394.4,223.5 396.1,224.2 397.8,224.8 399.5,225.4 401.1,225.9 402.8,226.5 404.5,227.0 406.2,227.6 407.8,228.1 409.5,228.5 411.2,229.0 412.8,229.5 414.5,229.9 416.2,230.3 417.9,230.7 419.5,231.1 421.2,231.5 422.9,231.8 424.5,232.2 426.2,232.5 427.9,232.8 429.6,233.1 431.2,233.4 432.9,233.7 434.6,234.0 436.3,234.2 437.9,234.5 439.6,234.7 441.3,235.0 442.9,235.2 444.6,235.4 446.3,235.6 448.0,235.8 449.6,236.0 451.3,236.1 453.0,236.3 454.6,236.5 456.3,236.6 458.0,236.8 459.7,236.9 461.3,237.1 463.0,237.2 464.7,237.3 466.4,237.4 468.0,237.5 469.7,237.7 471.4,237.8 473.0,237.9 474.7,238.0 476.4,238.1 478.1,238.1 479.7,238.2 481.4,238.3 483.1,238.4 484.7,238.5 486.4,238.5 488.1,238.6 489.8,238.7 491.4,238.7 493.1,238.8 494.8,238.8 496.5,238.9 498.1,238.9 499.8,239.0 501.5,239.0 503.1,239.1 504.8,239.1 506.5,239.2 508.2,239.2 509.8,239.2 511.5,239.3 513.2,239.3 514.8,239.3 516.5,239.4 518.2,239.4 519.9,239.4 521.5,239.4 523.2,239.5 524.9,239.5 526.6,239.5 528.2,239.5 529.9,239.6 531.6,239.6 533.2,239.6 534.9,239.6 536.6,239.6 538.3,239.6 539.9,239.7 541.6,239.7 543.3,239.7 544.9,239.7 546.6,239.7 548.3,239.7 550.0,239.7 551.6,239.8 553.3,239.8 555.0,239.8 556.7,239.8 558.3,239.8 560.0,239.8"/><circle class="dot-warn" cx="295.5" cy="156.2" r="4"/><circle class="dot-warn" cx="295.5" cy="189.7" r="4"/><line class="mut" x1="295.5" y1="156.2" x2="295.5" y2="189.7"/><text class="t-warn" x="287.5" y="150.2" text-anchor="end">σ = 0.4</text><text class="t-warn" x="285.5" y="185.7" text-anchor="end">σ′ = 0.24</text><text class="t-ink" x="460.0" y="51.6">σ(z)</text><text class="t-hl" x="352.9" y="179.6">σ′(z), max 0.25</text></svg><figcaption>The sigmoid σ(z) = 1/(1 + e^(−z)) squashes any real score into (0, 1). σ(0) = 0.5 is the decision threshold. Its derivative σ'(z) = σ(z)(1 − σ(z)) peaks at 0.25 when z = 0; at σ = 0.4 it is 0.4 × 0.6 = 0.24 (2024 Q33).</figcaption></figure>
<!-- /fig:logit-sigmoid -->

**Deriving the derivative** (worth doing once): $\sigma = (1 + e^{-z})^{-1}$, so

$$
\sigma' = \frac{e^{-z}}{(1 + e^{-z})^2} = \frac{1}{1 + e^{-z}} \cdot \frac{e^{-z}}{1 + e^{-z}} = \sigma\,(1 - \sigma).
$$

This means **you never need $z$**. If you know the output $\sigma$, the slope is $\sigma(1 - \sigma)$. That's the whole of 2024 Q33.

## 4.4 Logistic regression

<div class="formula">

$$
P(y = 1 \mid x) = p = \sigma(w^\top x + b) \qquad\Longleftrightarrow\qquad \ln\frac{p}{1 - p} = w^\top x + b
$$

- The **log-odds** are a linear function of $x$, and that's the whole model.
- Predict 1 when $p > 0.5$, which is when $w^\top x + b > 0$. So the **decision boundary is linear**.
- Weight interpretation: increasing $x_j$ by 1 **multiplies the odds by $e^{w_j}$**. A weight of $\ln 2$ doubles the odds.

</div>

It's called regression because it regresses the log-odds, but it's a **classifier**. It's also **discriminative**: it models $P(y \mid x)$ directly.

### The loss: cross-entropy

Treat each label as a coin flip with probability $p_i$. Maximising the likelihood $\prod p_i^{y_i}(1 - p_i)^{1 - y_i}$ is the same as minimising the **binary cross-entropy (log loss)**, with $y_i \in \{0, 1\}$:

$$
L(w) = -\sum_{i=1}^n \Big[\,y_i \ln p_i + (1 - y_i)\ln(1 - p_i)\Big].
$$

- For $y = 1$ the loss is $-\ln p$: zero when $p = 1$, and growing without bound as $p \to 0$. Confident mistakes are punished heavily.
- **Why not squared error?** MSE composed with the sigmoid is **non-convex** in $w$, while cross-entropy is **convex**, so gradient descent finds the global minimum.

### The gradient (remarkably simple)

<div class="formula">

$$
\frac{\partial L_i}{\partial w} = (p_i - y_i)\,x_i \qquad\qquad \frac{\partial L_i}{\partial b} = p_i - y_i
$$

Gradient-descent update for one example: $w \leftarrow w - \eta\,(p - y)\,x$.

</div>

This has the **same form as linear regression's** gradient, (prediction − target) × input. The $\sigma'$ factor from the chain rule cancels exactly against the derivative of the log.

There's no closed-form solution, so we use gradient descent or Newton's method. If the data is **perfectly separable**, the unregularized weights grow without limit (pushing every $p$ towards 0 or 1), so in practice we add an L2 penalty, exactly as in topic 3.

### More than two classes: softmax

$$
P(y = k \mid x) = \frac{e^{w_k^\top x}}{\sum_{j=1}^K e^{w_j^\top x}}, \qquad \text{loss} = -\ln P(y = \text{true class} \mid x).
$$

With $K = 2$, softmax reduces to the sigmoid. The alternative is **one-vs-rest**: train $K$ binary classifiers and pick the most confident.

## 4.5 Linear separability

A labelled dataset is **linearly separable** if some hyperplane puts every positive point strictly on one side and every negative point on the other.

<!-- fig:linsep-q53 -->
<figure class="diagram"><svg class="dg" viewBox="0 0 610 380" role="img" aria-label="Linear separability of four datasets" xmlns="http://www.w3.org/2000/svg"><text class="title" x="155" y="22" text-anchor="middle">(i) separable</text><path class="ax" d="M40,36 V166 H270"/><line class="grid" x1="100.5" y1="166.0" x2="100.5" y2="36.0"/><line class="grid" x1="40.0" y1="122.7" x2="270.0" y2="122.7"/><line class="grid" x1="161.1" y1="166.0" x2="161.1" y2="36.0"/><line class="grid" x1="40.0" y1="89.3" x2="270.0" y2="89.3"/><line class="grid" x1="221.6" y1="166.0" x2="221.6" y2="36.0"/><line class="grid" x1="40.0" y1="56.0" x2="270.0" y2="56.0"/><line class="mut" style="stroke:var(--gd-ink)" x1="58.2" y1="136.0" x2="257.9" y2="69.3"/><circle class="dot" cx="100.5" cy="56.0" r="6"/><circle class="dot" cx="161.1" cy="56.0" r="6"/><circle class="dot" cx="100.5" cy="89.3" r="6"/><rect class="dot-warn" x="155.1" y="116.7" width="12" height="12"/><rect class="dot-warn" x="215.6" y="116.7" width="12" height="12"/><rect class="dot-warn" x="155.1" y="150.0" width="12" height="12"/><text class="title" x="455" y="22" text-anchor="middle">(ii) not separable</text><path class="ax" d="M340,36 V166 H570"/><line class="grid" x1="400.5" y1="166.0" x2="400.5" y2="36.0"/><line class="grid" x1="340.0" y1="122.7" x2="570.0" y2="122.7"/><line class="grid" x1="461.1" y1="166.0" x2="461.1" y2="36.0"/><line class="grid" x1="340.0" y1="89.3" x2="570.0" y2="89.3"/><line class="grid" x1="521.6" y1="166.0" x2="521.6" y2="36.0"/><line class="grid" x1="340.0" y1="56.0" x2="570.0" y2="56.0"/><circle class="dot" cx="461.1" cy="89.3" r="6"/><rect class="dot-warn" x="455.1" y="50.0" width="12" height="12"/><rect class="dot-warn" x="394.5" y="83.3" width="12" height="12"/><rect class="dot-warn" x="515.6" y="83.3" width="12" height="12"/><rect class="dot-warn" x="455.1" y="116.7" width="12" height="12"/><text class="title" x="155" y="207" text-anchor="middle">(iii) not separable (XOR)</text><path class="ax" d="M40,221 V351 H270"/><line class="grid" x1="100.5" y1="351.0" x2="100.5" y2="221.0"/><line class="grid" x1="40.0" y1="307.7" x2="270.0" y2="307.7"/><line class="grid" x1="161.1" y1="351.0" x2="161.1" y2="221.0"/><line class="grid" x1="40.0" y1="274.3" x2="270.0" y2="274.3"/><line class="grid" x1="221.6" y1="351.0" x2="221.6" y2="221.0"/><line class="grid" x1="40.0" y1="241.0" x2="270.0" y2="241.0"/><circle class="dot" cx="221.6" cy="241.0" r="6"/><circle class="dot" cx="100.5" cy="307.7" r="6"/><rect class="dot-warn" x="94.5" y="235.0" width="12" height="12"/><rect class="dot-warn" x="215.6" y="301.7" width="12" height="12"/><text class="title" x="455" y="207" text-anchor="middle">(iv) separable</text><path class="ax" d="M340,221 V351 H570"/><line class="grid" x1="400.5" y1="351.0" x2="400.5" y2="221.0"/><line class="grid" x1="340.0" y1="307.7" x2="570.0" y2="307.7"/><line class="grid" x1="461.1" y1="351.0" x2="461.1" y2="221.0"/><line class="grid" x1="340.0" y1="274.3" x2="570.0" y2="274.3"/><line class="grid" x1="521.6" y1="351.0" x2="521.6" y2="221.0"/><line class="grid" x1="340.0" y1="241.0" x2="570.0" y2="241.0"/><line class="mut" style="stroke:var(--gd-ink)" x1="376.3" y1="341.0" x2="557.9" y2="244.3"/><circle class="dot" cx="461.1" cy="337.7" r="6"/><circle class="dot" cx="521.6" cy="291.0" r="6"/><circle class="dot" cx="521.6" cy="334.3" r="6"/><rect class="dot-warn" x="394.5" y="258.3" width="12" height="12"/><rect class="dot-warn" x="455.1" y="248.3" width="12" height="12"/><rect class="dot-warn" x="394.5" y="295.0" width="12" height="12"/></svg><figcaption>The four datasets of GATE DA 2024 Q53, redrawn (● circles, ■ squares). A dashed line separates the classes in (i) and (iv). In (ii) a circle is surrounded by squares, and (iii) is the XOR pattern: no single straight line works.</figcaption></figure>
<!-- /fig:linsep-q53 -->

**How to decide quickly:**

1. Look for a **class point inside the region enclosed by points of the other class** (as in (ii)). If you find one, the data isn't separable.
2. Look for the **XOR pattern**: the two diagonals of a rectangle carry different labels (as in (iii)). Not separable.
3. Otherwise, try to draw a line. It's often obvious, as in (i) and (iv).

The precise test: the data is separable **if and only if** the **convex hulls** of the two classes don't intersect.

**Fixing non-separable data:** map the features into a richer space. XOR becomes separable with the extra feature $x_1x_2$, and (ii) becomes separable with $(x_1 - 2)^2 + (x_2 - 2)^2$. That's the idea behind **kernels** (SVM, topic 8) and **hidden layers** (neural networks, topic 10).

## 4.6 The perceptron

The oldest learning algorithm for a linear classifier. With labels $y \in \{+1, -1\}$, visit the points one at a time:

<div class="formula">

If point $(x_n, y_n)$ is **misclassified**, meaning $\operatorname{sign}(w^\top x_n + b) \ne y_n$:

$$
w \leftarrow w + y_n x_n, \qquad b \leftarrow b + y_n.
$$

Correctly classified points cause no change.

</div>

**Why the update helps.** The new score on that same point is

$$
f_{\text{new}}(x_n) = (w + y_nx_n)^\top x_n + (b + y_n) = f_{\text{old}}(x_n) + y_n\big(\|x_n\|^2 + 1\big).
$$

For $y_n = +1$ the score goes **up**, and for $y_n = -1$ it goes **down**. Either way, $y_n f(x_n)$ increases by $\|x_n\|^2 + 1 > 0$. The update always moves the score in the right direction, though it may not fix the mistake in a single step.

**Perceptron convergence theorem:** if the data is **linearly separable** with margin $\gamma$ and $\|x\| \le R$, the perceptron makes **at most $(R/\gamma)^2$ mistakes** and stops at a separating hyperplane. If the data **isn't** separable, it never stops. It cycles forever. The perceptron also doesn't find the *best* separator, only *some* separator. Finding the best one is SVM's job.

## 4.7 The nearest-mean classifier is linear

Assign $x$ to the class whose mean $\mu$ is closer:

$$
f(x) = \|\mu_r - x\|^2 - \|\mu_g - x\|^2 \quad (\text{red if } f < 0).
$$

Expand both squares. The $\|x\|^2$ terms **cancel**:

$$
f(x) = \|\mu_r\|^2 - 2\mu_r^\top x - \|\mu_g\|^2 + 2\mu_g^\top x = \underbrace{2(\mu_g - \mu_r)^\top}_{w^\top} x + \underbrace{\|\mu_r\|^2 - \|\mu_g\|^2}_{b}.
$$

So the boundary is the **perpendicular bisector** of the segment joining the two means, which is a hyperplane. LDA with an identity covariance reduces to exactly this rule (topic 7).

---

## Summary: important points

<div class="formula">

1. A linear classifier predicts with $\operatorname{sign}(w^\top x + b)$. The boundary is a hyperplane with normal $w$. Distance $= |f(x)|/\|w\|$.
2. $\sigma(z) = 1/(1 + e^{-z})$, $\sigma(0) = 0.5$, $\sigma(-z) = 1 - \sigma(z)$, $\sigma' = \sigma(1 - \sigma) \le 0.25$.
3. Logistic regression: log-odds $= w^\top x + b$. Increasing $x_j$ by 1 multiplies the odds by $e^{w_j}$. The boundary is linear.
4. Loss = cross-entropy (convex). Gradient $= (p - y)x$. No closed form.
5. Separable data: the unregularized logistic weights grow without bound. The perceptron converges.
6. XOR and "a point surrounded by the other class" aren't linearly separable. Feature maps or kernels fix this.
7. Perceptron update on a mistake: $w \leftarrow w + yx$, $b \leftarrow b + y$. It always increases $y f(x)$ on that point.
8. The nearest-mean classifier is linear: its boundary is the perpendicular bisector of the two means.

</div>

<div class="trap">

- Logistic **regression** is a classification method.
- $\sigma'(z) = \sigma(1 - \sigma)$ uses the **output** $\sigma$, not $z$.
- The perceptron finds *a* separating line, not the maximum-margin one. On non-separable data it never converges.
- Labels: logistic regression uses $\{0, 1\}$, while the perceptron and SVM use $\{-1, +1\}$. Check which one the formula expects.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q33 (1 mark, NAT)

$f(x) = \dfrac{1}{1 + e^{-x}}$. What is $f'(x)$ at the point where $f(x) = 0.4$? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.24**

$f' = f(1 - f) = 0.4 \times 0.6 = $ **0.24**. You never need to find $x$ itself (which would be $\ln(0.4/0.6) \approx -0.405$).

</details>

### GATE DA 2024 Q53 (2 marks, MSQ)

The four 2-D datasets shown in §4.5. Which are linearly separable?

<details>
<summary>Show solution</summary>

**Answer: A; D**, so (i) and (iv)

- **(i)** The circles occupy the upper-left and the squares the lower-right. A diagonal line separates them.
- **(ii)** The circle at (2, 2) lies inside the diamond of squares (1, 2), (3, 2), (2, 1), (2, 3), so it's inside their convex hull. Not separable.
- **(iii)** The circles at (1, 1) and (3, 3) and the squares at (1, 3) and (3, 1) form XOR. Not separable.
- **(iv)** The squares are upper-left and the circles lower-right. Separable.

</details>

### GATE DA 2025 Q22 (1 mark, MCQ)

A linear classifier $y = \operatorname{sign}(w^\top x + b)$ is trained with the update $w_{\text{new}} = w_{\text{old}} + y_nx_n$, $b_{\text{new}} = b_{\text{old}} + y_n$, applied whenever $(x_n, y_n)$ is misclassified. For a point $(x_n, +1)$ with $f(x_n; w_{\text{old}}, b_{\text{old}}) < 0$:
(A) $f_{\text{new}}(x_n) > f_{\text{old}}(x_n)$ (B) $f_{\text{new}} < f_{\text{old}}$ (C) $f_{\text{new}} = f_{\text{old}}$ (D) $y_n f_{\text{old}}(x_n) > 1$

<details>
<summary>Show solution</summary>

**Answer: (A)**

From §4.6: $f_{\text{new}}(x_n) = f_{\text{old}}(x_n) + y_n(\|x_n\|^2 + 1) = f_{\text{old}}(x_n) + \|x_n\|^2 + 1 > f_{\text{old}}(x_n)$.

(D) is false: $y_n f_{\text{old}} = f_{\text{old}} < 0$.

</details>

### GATE DA 2025 Q55 (2 marks, MSQ)

Two classes, red and green, with means $\mu_{\text{red}}$ and $\mu_{\text{green}}$. The classifier computes $f(x) = \|\mu_{\text{red}} - x\|^2 - \|\mu_{\text{green}} - x\|^2$ and predicts red if $f(x) < 0$, green otherwise. Which are correct?
(A) $x = 0$ is labelled green if $\|\mu_{\text{red}}\| < \|\mu_{\text{green}}\|$ (B) $f$ is a linear function of $x$ (C) $f(x) = w^\top x + b$ with $w$, $b$ depending on the means (D) $f$ is a quadratic polynomial in $x$

<details>
<summary>Show solution</summary>

**Answer: B; C**

From §4.7, $f(x) = 2(\mu_g - \mu_r)^\top x + \|\mu_r\|^2 - \|\mu_g\|^2$. The $\|x\|^2$ terms cancel, so $f$ is linear (B, C), not quadratic (D).

For (A): $f(0) = \|\mu_r\|^2 - \|\mu_g\|^2 < 0$ when $\|\mu_r\| < \|\mu_g\|$, so $x = 0$ is labelled **red**, not green.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** Logistic regression has $w = (2, -1)$ and $b = 0.5$. What is $P(y = 1 \mid x)$ for $x = (1, 2)$? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.62**

$z = 2(1) - 1(2) + 0.5 = 0.5$, and $\sigma(0.5) = 1/(1 + e^{-0.5}) = 0.6225 \approx$ **0.62**.

</details>

**F2 (1 mark, NAT).** A positive example ($y = 1$) gets predicted probability 0.8. What is its cross-entropy loss (natural log, 3 decimal places)?

<details>
<summary>Show solution</summary>

**Answer: 0.223**

$-\ln 0.8 = 0.223$.

</details>

**F3 (2 marks, NAT).** One gradient step of logistic regression from $w = (0, 0)$, $b = 0$ on the example $x = (1, 2)$, $y = 1$, with $\eta = 0.5$. What is $w_2$ afterwards?

<details>
<summary>Show solution</summary>

**Answer: 0.5**

$p = \sigma(0) = 0.5$. The gradient is $(p - y)x = -0.5\,(1, 2)$. So $w \leftarrow (0, 0) + 0.5 \times 0.5\,(1, 2) = (0.25, 0.5)$ and $b = 0.25$. $w_2 = $ **0.5**.

</details>

**F4 (2 marks, NAT).** A linear classifier has $w = (3, 4)$ and $b = -5$. What is the distance of the point $(2, 1)$ from the decision boundary?

<details>
<summary>Show solution</summary>

**Answer: 1**

$f = 3(2) + 4(1) - 5 = 5$ and $\|w\| = 5$, so the distance is $5/5 = $ **1**.

</details>

**F5 (2 marks, MSQ).** Which statements about the sigmoid $\sigma$ are true?
(A) $\sigma(-z) = 1 - \sigma(z)$ (B) $\sigma'(z) \le 0.25$ for all $z$ (C) $\sigma'(z) = \sigma(z)^2$ (D) $\ln\frac{\sigma(z)}{1 - \sigma(z)} = z$

<details>
<summary>Show solution</summary>

**Answer: A; B; D**

(C) is wrong: the derivative is $\sigma(1 - \sigma)$. (D) says the logit is the inverse of the sigmoid, which is true.

</details>

**F6 (2 marks, MSQ).** Which statements are true?
(A) The perceptron converges in finitely many updates on linearly separable data (B) On non-separable data the perceptron stops at the minimum-error line (C) Logistic regression has a linear decision boundary (D) The XOR dataset becomes linearly separable after adding the feature $x_1x_2$

<details>
<summary>Show solution</summary>

**Answer: A; C; D**

(B) is false: on non-separable data the perceptron **never stops**. It keeps cycling through updates.

</details>

**F7 (1 mark, NAT).** In logistic regression, $w_j = \ln 3$. By what factor do the odds of class 1 change when $x_j$ increases by 1?

<details>
<summary>Show solution</summary>

**Answer: 3**

The odds are multiplied by $e^{w_j} = e^{\ln 3} = $ **3**.

</details>
