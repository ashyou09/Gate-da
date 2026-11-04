---
title: 3. Ridge & lasso regularization
description: Why we penalise large weights, the ridge (L2) and lasso (L1) objectives, shrinkage vs sparsity, the geometry, the effect of λ, weight decay and regularized-loss numericals.
sidebar:
  label: 3. Ridge & lasso
  order: 3
---

**Why it matters:** 2026 had **two** ridge questions: Q37 (what the regularizer does) and Q55 (compute a regularized loss). Both come down to two facts: **ridge adds $\lambda\|w\|_2^2$**, and **that trades a little bias for less variance**. Lasso is the natural next question.

## Topic map

<div class="mindmap">

- **Regularization**
  - Why
    - overfitting, huge weights
    - collinear features, $p > n$
  - Ridge (L2)
    - $\text{loss} + \lambda\|w\|_2^2$
    - $\hat w = (X^\top X + \lambda I)^{-1}X^\top y$
    - shrinks, never exactly 0
  - Lasso (L1)
    - $\text{loss} + \lambda\|w\|_1$
    - soft-thresholding, exact zeros → feature selection
  - Geometry
    - L2 ball round, L1 ball has corners
  - Effect of λ
    - $\lambda = 0$: OLS; $\lambda \to \infty$: weights → 0
    - bias ↑, variance ↓, choose λ by CV
  - Extras
    - weight decay in gradient descent
    - elastic net, Bayesian priors

</div>

## 3.1 Why penalise weights?

An overfitting model typically has **huge weights**. A degree-11 polynomial that threads every noisy point needs enormous coefficients that cancel each other out. Large weights mean that a small change in the input causes a big swing in the output, which is exactly **high variance**.

Regularization adds a **penalty on the size of the weights** to the training loss:

$$
J(w) = \underbrace{\text{data loss}(w)}_{\text{fit the data}} \;+\; \lambda \cdot \underbrace{\text{penalty}(w)}_{\text{keep weights small}}
$$

$\lambda \ge 0$ is a **hyperparameter** that sets the balance. The model now accepts a slightly worse fit on the training data in return for smaller, more stable weights.

Regularization also rescues cases where OLS breaks: **collinear features** (where $X^\top X$ is nearly singular, so the OLS weights explode) and **more features than examples**.

## 3.2 Ridge regression (L2)

<div class="formula">

$$
J_{\text{ridge}}(w) = \sum_{i=1}^n (y_i - w^\top x_i)^2 + \lambda \|w\|_2^2,
\qquad \|w\|_2^2 = \sum_j w_j^2
$$

Setting the gradient to zero, $-2X^\top(y - Xw) + 2\lambda w = 0$, gives

$$
\hat w_{\text{ridge}} = (X^\top X + \lambda I)^{-1} X^\top y.
$$

- For $\lambda > 0$, $X^\top X + \lambda I$ is **always invertible**: its eigenvalues are those of $X^\top X$ (all $\ge 0$) plus $\lambda > 0$.
- **One feature, no intercept:** $\hat w = \dfrac{\sum x_i y_i}{\sum x_i^2 + \lambda}$. Compare with OLS, $\dfrac{\sum x_i y_i}{\sum x_i^2}$: the denominator grows, so the weight shrinks.
- **Orthonormal features** ($X^\top X = I$): $\hat w_{\text{ridge}} = \dfrac{\hat w_{\text{OLS}}}{1 + \lambda}$. Every weight is scaled down by the same factor, and **none becomes exactly 0**.

</div>

**Penalty is $\lambda$ times the *squared* L2 norm.** If a question says "ridge with weight 0.2", the penalty is $0.2 \sum w_j^2$, not $0.2\sqrt{\sum w_j^2}$. That's the whole trick in 2026 Q55.

**Practical conventions:**

- The **intercept is not penalised**. Penalising it would make the predictions depend on where the origin of $y$ is.
- **Standardise the features first.** The penalty treats all weights equally, so a feature measured in metres would be penalised differently from the same feature in centimetres.

## 3.3 Lasso (L1)

<div class="formula">

$$
J_{\text{lasso}}(w) = \sum_{i=1}^n (y_i - w^\top x_i)^2 + \lambda \|w\|_1,
\qquad \|w\|_1 = \sum_j |w_j|
$$

- $|w|$ has a kink at 0, so there's **no closed form** in general. It's solved by coordinate descent or by subgradient methods.
- **Orthonormal features:** each weight is **soft-thresholded**,

$$
\hat w_j^{\text{lasso}} = \operatorname{sign}(\hat w_j^{\text{OLS}})\,\max\!\Big(|\hat w_j^{\text{OLS}}| - \tfrac{\lambda}{2},\; 0\Big).
$$

Any weight whose OLS value is smaller than $\lambda/2$ in absolute value becomes **exactly 0**. Larger weights are pulled towards 0 by $\lambda/2$.

</div>

That threshold $\lambda/2$ comes from differentiating $(w - w_{\text{OLS}})^2 + \lambda|w|$. If the loss were written $\frac12\sum(\cdot)^2$, the threshold would be $\lambda$. **Always check how the question writes the loss.**

Because lasso sets weights to exactly zero, it performs **automatic feature selection** and produces **sparse** models.

## 3.4 The geometry: why lasso gives zeros and ridge doesn't

Minimising "loss + $\lambda\cdot$penalty" is equivalent to minimising the loss **subject to** penalty $\le t$ for some budget $t$. Picture the RSS contours (ellipses around the OLS solution) expanding until they first touch the allowed region:

<!-- fig:reg-geometry -->
<figure class="diagram"><svg class="dg" viewBox="0 0 620 270" role="img" aria-label="Ridge and lasso constraint geometry" xmlns="http://www.w3.org/2000/svg"><rect class="grid" x="30.0" y="30.0" width="270.0" height="230.0" rx="6"/><text class="title" x="165" y="16" text-anchor="middle">Ridge · ‖w‖₂ ≤ 1</text><line class="ax" x1="30.0" y1="171.5" x2="300.0" y2="171.5"/><line class="ax" x1="118.0" y1="260.0" x2="118.0" y2="30.0"/><text class="t-mut" x="297.1" y="185.5" text-anchor="end">w₁</text><text class="t-mut" x="124.0" y="35.9">w₂</text><circle class="ink" style="fill:var(--gd-ink);fill-opacity:.14" cx="118.0" cy="171.5" r="58.7"/><clipPath id="rgclip0"><rect x="30.0" y="30.0" width="270.0" height="230.0"/></clipPath><g clip-path="url(#rgclip0)"><polyline class="hl" points="301.6,142.1 300.5,139.5 299.4,136.9 298.1,134.3 296.7,131.8 295.2,129.3 293.7,126.7 292.0,124.2 290.3,121.8 288.4,119.4 286.5,117.0 284.5,114.6 282.5,112.3 280.3,110.0 278.1,107.8 275.8,105.6 273.5,103.5 271.1,101.5 268.6,99.5 266.1,97.6 263.6,95.7 260.9,93.9 258.3,92.2 255.6,90.6 252.9,89.1 250.2,87.6 247.4,86.2 244.7,85.0 241.9,83.8 239.1,82.7 236.3,81.6 233.4,80.7 230.6,79.9 227.8,79.2 225.1,78.5 222.3,78.0 219.5,77.6 216.8,77.2 214.1,77.0 211.5,76.9 208.8,76.9 206.2,76.9 203.7,77.1 201.2,77.4 198.8,77.8 196.4,78.3 194.1,78.8 191.8,79.5 189.7,80.3 187.5,81.2 185.5,82.1 183.5,83.2 181.7,84.3 179.9,85.6 178.2,86.9 176.5,88.3 175.0,89.8 173.6,91.4 172.2,93.1 171.0,94.8 169.9,96.6 168.8,98.5 167.9,100.5 167.1,102.5 166.4,104.6 165.8,106.7 165.3,108.9 164.9,111.1 164.6,113.4 164.4,115.8 164.4,118.1 164.4,120.6 164.6,123.0 164.8,125.5 165.2,128.0 165.7,130.5 166.3,133.1 167.0,135.6 167.8,138.2 168.8,140.8 169.8,143.3 170.9,145.9 172.1,148.5 173.5,151.0 174.9,153.6 176.4,156.1 178.0,158.6 179.7,161.1 181.5,163.5 183.4,166.0 185.3,168.3 187.4,170.7 189.5,173.0 191.7,175.2 193.9,177.4 196.2,179.5 198.6,181.6 201.0,183.6 203.5,185.6 206.0,187.5 208.6,189.3 211.2,191.0 213.9,192.7 216.6,194.3 219.3,195.8 222.1,197.2 224.8,198.5 227.6,199.8 230.4,200.9 233.2,202.0 236.0,202.9 238.8,203.8 241.6,204.6 244.4,205.3 247.2,205.8 250.0,206.3 252.7,206.7 255.4,207.0 258.1,207.2 260.7,207.2 263.3,207.2 265.9,207.1 268.4,206.9 270.9,206.5 273.3,206.1 275.6,205.6 277.9,204.9 280.1,204.2 282.3,203.4 284.4,202.5 286.4,201.5 288.3,200.3 290.1,199.1 291.9,197.9 293.5,196.5 295.1,195.0 296.6,193.5 298.0,191.9 299.3,190.2 300.4,188.4 301.5,186.5 302.5,184.6 303.4,182.6 304.2,180.6 304.8,178.5 305.4,176.3 305.8,174.1 306.2,171.8 306.4,169.5 306.5,167.1 306.5,164.8 306.4,162.3 306.2,159.9 305.9,157.4 305.4,154.8 304.9,152.3 304.2,149.8 303.5,147.2 302.6,144.6 301.6,142.1"/><polyline class="mut" points="329.0,142.1 327.5,138.4 325.8,134.8 324.0,131.1 322.1,127.5 320.0,124.0 317.8,120.4 315.4,116.9 313.0,113.4 310.4,109.9 307.7,106.6 304.9,103.2 301.9,99.9 298.9,96.7 295.8,93.6 292.5,90.5 289.2,87.6 285.8,84.7 282.4,81.9 278.8,79.1 275.2,76.5 271.5,74.0 267.8,71.6 264.0,69.3 260.2,67.1 256.3,65.1 252.4,63.1 248.5,61.3 244.5,59.6 240.6,58.0 236.6,56.6 232.6,55.3 228.7,54.1 224.7,53.1 220.8,52.2 216.8,51.5 212.9,50.9 209.1,50.4 205.3,50.1 201.5,49.9 197.8,49.9 194.2,50.0 190.6,50.2 187.0,50.6 183.6,51.1 180.2,51.8 177.0,52.6 173.8,53.6 170.7,54.7 167.7,55.9 164.8,57.3 162.1,58.8 159.4,60.4 156.9,62.2 154.4,64.1 152.2,66.1 150.0,68.2 148.0,70.5 146.1,72.8 144.3,75.3 142.7,77.8 141.3,80.5 139.9,83.3 138.8,86.1 137.8,89.0 136.9,92.1 136.2,95.2 135.6,98.3 135.2,101.6 135.0,104.9 134.9,108.2 135.0,111.7 135.2,115.1 135.6,118.6 136.1,122.2 136.8,125.7 137.7,129.3 138.7,133.0 139.8,136.6 141.1,140.2 142.6,143.9 144.2,147.5 145.9,151.1 147.8,154.8 149.8,158.4 152.0,161.9 154.2,165.5 156.7,169.0 159.2,172.4 161.8,175.9 164.6,179.2 167.5,182.5 170.4,185.8 173.5,188.9 176.7,192.0 180.0,195.1 183.3,198.0 186.8,200.9 190.3,203.6 193.9,206.3 197.5,208.8 201.2,211.3 205.0,213.6 208.8,215.9 212.6,218.0 216.5,220.0 220.4,221.9 224.4,223.7 228.3,225.3 232.3,226.8 236.3,228.2 240.2,229.4 244.2,230.5 248.1,231.5 252.1,232.3 256.0,233.0 259.9,233.5 263.7,233.9 267.5,234.1 271.2,234.2 274.9,234.2 278.5,234.0 282.1,233.7 285.6,233.2 289.0,232.6 292.3,231.9 295.5,231.0 298.6,230.0 301.7,228.8 304.6,227.5 307.4,226.1 310.2,224.5 312.8,222.8 315.2,221.0 317.6,219.0 319.8,217.0 321.9,214.8 323.9,212.5 325.7,210.1 327.4,207.6 328.9,205.0 330.3,202.2 331.5,199.4 332.6,196.5 333.6,193.6 334.3,190.5 335.0,187.4 335.5,184.2 335.8,180.9 335.9,177.5 335.9,174.2 335.8,170.7 335.5,167.2 335.0,163.7 334.4,160.2 333.6,156.6 332.7,153.0 331.6,149.3 330.4,145.7 329.0,142.1"/></g><text class="t-hl" x="241.4" y="136.1">★ OLS</text><circle class="dot-hl" cx="235.4" cy="142.1" r="3.5"/><circle class="dot-warn" cx="171.2" cy="146.5" r="5"/><text class="t-warn" x="163.2" y="136.5" text-anchor="end">≈ (0.9, 0.4)</text><rect class="grid" x="335.0" y="30.0" width="270.0" height="230.0" rx="6"/><text class="title" x="470" y="16" text-anchor="middle">Lasso · ‖w‖₁ ≤ 1</text><line class="ax" x1="335.0" y1="171.5" x2="605.0" y2="171.5"/><line class="ax" x1="423.0" y1="260.0" x2="423.0" y2="30.0"/><text class="t-mut" x="602.1" y="185.5" text-anchor="end">w₁</text><text class="t-mut" x="429.0" y="35.9">w₂</text><polygon class="ink" style="fill:var(--gd-ink);fill-opacity:.14" points="481.7,171.5 423.0,112.6 364.3,171.5 423.0,230.5"/><clipPath id="rgclip1"><rect x="335.0" y="30.0" width="270.0" height="230.0"/></clipPath><g clip-path="url(#rgclip1)"><polyline class="hl" points="617.0,142.1 615.7,139.1 614.4,136.1 612.9,133.1 611.3,130.2 609.6,127.3 607.8,124.3 605.9,121.5 603.8,118.6 601.7,115.8 599.5,113.0 597.2,110.3 594.8,107.6 592.3,105.0 589.8,102.4 587.1,99.9 584.4,97.5 581.7,95.1 578.8,92.8 575.9,90.6 573.0,88.5 569.9,86.4 566.9,84.5 563.8,82.6 560.7,80.8 557.5,79.1 554.3,77.5 551.1,76.0 547.9,74.6 544.6,73.4 541.4,72.2 538.1,71.1 534.9,70.2 531.7,69.3 528.4,68.6 525.2,68.0 522.0,67.5 518.9,67.1 515.8,66.8 512.7,66.7 509.7,66.7 506.7,66.7 503.7,66.9 500.9,67.3 498.0,67.7 495.3,68.3 492.6,68.9 490.0,69.7 487.5,70.6 485.0,71.6 482.7,72.8 480.4,74.0 478.2,75.3 476.2,76.8 474.2,78.3 472.3,79.9 470.6,81.7 468.9,83.5 467.4,85.4 465.9,87.4 464.6,89.5 463.4,91.7 462.3,94.0 461.4,96.3 460.6,98.7 459.9,101.2 459.3,103.7 458.8,106.3 458.5,109.0 458.3,111.7 458.2,114.4 458.3,117.2 458.5,120.0 458.8,122.9 459.2,125.8 459.8,128.7 460.5,131.7 461.3,134.6 462.3,137.6 463.3,140.6 464.5,143.5 465.8,146.5 467.2,149.5 468.8,152.4 470.4,155.4 472.2,158.3 474.0,161.2 476.0,164.1 478.1,166.9 480.2,169.7 482.5,172.4 484.8,175.1 487.3,177.8 489.8,180.4 492.4,182.9 495.1,185.4 497.8,187.8 500.6,190.1 503.5,192.4 506.4,194.6 509.4,196.7 512.4,198.7 515.5,200.6 518.6,202.4 521.8,204.2 525.0,205.8 528.2,207.3 531.4,208.8 534.6,210.1 537.9,211.4 541.1,212.5 544.4,213.5 547.6,214.4 550.8,215.2 554.0,215.8 557.2,216.4 560.4,216.8 563.5,217.2 566.6,217.4 569.7,217.4 572.7,217.4 575.7,217.3 578.6,217.0 581.4,216.6 584.2,216.1 586.9,215.5 589.6,214.8 592.1,213.9 594.6,213.0 597.0,211.9 599.3,210.7 601.5,209.5 603.7,208.1 605.7,206.6 607.6,205.0 609.4,203.3 611.2,201.5 612.8,199.7 614.2,197.7 615.6,195.6 616.9,193.5 618.0,191.3 619.0,189.0 619.9,186.6 620.7,184.2 621.3,181.7 621.8,179.1 622.2,176.5 622.5,173.8 622.6,171.1 622.6,168.3 622.5,165.5 622.3,162.6 621.9,159.8 621.4,156.9 620.7,153.9 620.0,151.0 619.1,148.0 618.1,145.0 617.0,142.1"/><polyline class="mut" points="648.7,142.1 646.9,137.8 645.0,133.6 642.9,129.4 640.6,125.3 638.2,121.1 635.7,117.0 633.0,112.9 630.1,108.9 627.1,104.9 624.0,101.0 620.7,97.1 617.3,93.4 613.8,89.7 610.2,86.0 606.5,82.5 602.7,79.0 598.7,75.7 594.7,72.4 590.6,69.3 586.4,66.3 582.2,63.4 577.8,60.6 573.5,57.9 569.0,55.4 564.6,53.0 560.1,50.8 555.5,48.7 550.9,46.7 546.4,44.9 541.8,43.2 537.2,41.7 532.6,40.4 528.0,39.2 523.5,38.2 518.9,37.3 514.4,36.6 510.0,36.0 505.6,35.7 501.2,35.5 496.9,35.4 492.7,35.5 488.5,35.8 484.5,36.3 480.5,36.9 476.6,37.7 472.8,38.7 469.1,39.8 465.6,41.0 462.1,42.5 458.8,44.0 455.6,45.8 452.5,47.7 449.6,49.7 446.8,51.9 444.1,54.2 441.6,56.7 439.3,59.2 437.1,62.0 435.1,64.8 433.2,67.8 431.5,70.9 430.0,74.0 428.6,77.3 427.5,80.7 426.5,84.2 425.7,87.8 425.0,91.5 424.6,95.2 424.3,99.1 424.2,103.0 424.3,106.9 424.5,110.9 425.0,115.0 425.6,119.1 426.4,123.2 427.4,127.4 428.5,131.5 429.9,135.7 431.4,139.9 433.1,144.2 434.9,148.4 436.9,152.6 439.1,156.8 441.4,160.9 443.9,165.0 446.5,169.1 449.3,173.2 452.2,177.2 455.3,181.1 458.5,185.0 461.8,188.9 465.3,192.6 468.8,196.3 472.5,199.9 476.3,203.4 480.2,206.8 484.1,210.1 488.2,213.2 492.3,216.3 496.6,219.3 500.9,222.1 505.2,224.9 509.6,227.4 514.1,229.9 518.6,232.2 523.1,234.4 527.6,236.4 532.2,238.3 536.8,240.1 541.4,241.6 546.0,243.1 550.6,244.3 555.1,245.4 559.7,246.4 564.2,247.2 568.7,247.8 573.1,248.3 577.5,248.6 581.8,248.7 586.1,248.6 590.3,248.4 594.4,248.1 598.4,247.5 602.3,246.8 606.2,245.9 609.9,244.9 613.5,243.7 617.1,242.4 620.4,240.9 623.7,239.2 626.9,237.4 629.9,235.4 632.7,233.3 635.4,231.1 638.0,228.7 640.4,226.2 642.7,223.5 644.8,220.7 646.8,217.8 648.5,214.8 650.1,211.7 651.6,208.4 652.8,205.1 653.9,201.6 654.8,198.1 655.6,194.5 656.1,190.7 656.5,187.0 656.7,183.1 656.7,179.2 656.5,175.2 656.1,171.2 655.6,167.1 654.9,163.0 654.0,158.8 652.9,154.7 651.7,150.5 650.3,146.3 648.7,142.1"/></g><text class="t-hl" x="546.4" y="136.1">★ OLS</text><circle class="dot-hl" cx="540.4" cy="142.1" r="3.5"/><circle class="dot-warn" cx="481.7" cy="171.5" r="5"/><text class="t-warn" x="485.7" y="191.5" text-anchor="start">(1, 0)</text></svg><figcaption>Why lasso gives exact zeros. Contours of the RSS (ellipses) grow outward from the OLS solution ★ until they first touch the constraint region. The L2 ball (ridge) is round, so it is touched at a generic point with both weights non-zero, about (0.9, 0.4). The L1 ball (lasso) has corners on the axes, and the ellipse touches a corner: (1, 0), so w₂ is exactly 0.</figcaption></figure>
<!-- /fig:reg-geometry -->

The L1 ball is a diamond with **corners on the axes**. An expanding ellipse is far more likely to hit a corner first, and at a corner some coordinates are exactly 0. The L2 ball is round, with no corners, so the touching point generally has every coordinate non-zero.

## 3.5 The effect of λ

<!-- fig:reg-paths -->
<figure class="diagram"><svg class="dg" viewBox="0 0 620 262" role="img" aria-label="Ridge and lasso coefficient paths" xmlns="http://www.w3.org/2000/svg"><text class="title" x="170" y="16" text-anchor="middle">Ridge (L2)</text><path class="ax" d="M44,30 V220 H299"/><text x="171.5" y="250" text-anchor="middle">log₁₀ λ →</text><text x="18" y="125.0" text-anchor="middle" transform="rotate(-90 18 125.0)">weight</text><line class="grid" x1="44.0" y1="144.0" x2="299.0" y2="144.0"/><text class="t-mut" x="44.0" y="234.0" text-anchor="middle">-1</text><text class="t-mut" x="107.8" y="234.0" text-anchor="middle">0</text><text class="t-mut" x="171.5" y="234.0" text-anchor="middle">1</text><text class="t-mut" x="235.2" y="234.0" text-anchor="middle">2</text><text class="t-mut" x="299.0" y="234.0" text-anchor="middle">3</text><polyline class="ink" points="44.0,39.1 47.7,39.2 51.4,39.2 55.1,39.2 58.8,39.2 62.5,39.3 66.2,39.3 69.9,39.4 73.6,39.4 77.3,39.5 81.0,39.6 84.7,39.7 88.3,39.8 92.0,39.9 95.7,40.0 99.4,40.2 103.1,40.3 106.8,40.5 110.5,40.7 114.2,41.0 117.9,41.3 121.6,41.6 125.3,42.0 129.0,42.4 132.7,42.8 136.4,43.4 140.1,44.0 143.8,44.6 147.5,45.4 151.2,46.3 154.9,47.2 158.6,48.3 162.3,49.5 166.0,50.8 169.7,52.3 173.3,53.9 177.0,55.6 180.7,57.6 184.4,59.7 188.1,62.0 191.8,64.5 195.5,67.1 199.2,69.9 202.9,72.9 206.6,76.0 210.3,79.2 214.0,82.5 217.7,85.9 221.4,89.4 225.1,92.8 228.8,96.3 232.5,99.7 236.2,103.1 239.9,106.3 243.6,109.4 247.3,112.4 251.0,115.3 254.7,118.0 258.3,120.5 262.0,122.8 265.7,125.0 269.4,126.9 273.1,128.8 276.8,130.4 280.5,131.9 284.2,133.3 287.9,134.5 291.6,135.6 295.3,136.5 299.0,137.4"/><polyline class="warn" points="44.0,206.8 47.7,206.8 51.4,206.8 55.1,206.7 58.8,206.7 62.5,206.7 66.2,206.7 69.9,206.7 73.6,206.6 77.3,206.6 81.0,206.5 84.7,206.5 88.3,206.5 92.0,206.4 95.7,206.3 99.4,206.2 103.1,206.2 106.8,206.1 110.5,205.9 114.2,205.8 117.9,205.7 121.6,205.5 125.3,205.3 129.0,205.1 132.7,204.8 136.4,204.5 140.1,204.2 143.8,203.9 147.5,203.4 151.2,203.0 154.9,202.5 158.6,201.9 162.3,201.2 166.0,200.5 169.7,199.7 173.3,198.8 177.0,197.8 180.7,196.7 184.4,195.5 188.1,194.2 191.8,192.8 195.5,191.3 199.2,189.7 202.9,187.9 206.6,186.1 210.3,184.2 214.0,182.2 217.7,180.2 221.4,178.1 225.1,176.0 228.8,173.9 232.5,171.8 236.2,169.8 239.9,167.7 243.6,165.8 247.3,163.9 251.0,162.1 254.7,160.5 258.3,158.9 262.0,157.4 265.7,156.1 269.4,154.8 273.1,153.7 276.8,152.6 280.5,151.7 284.2,150.8 287.9,150.1 291.6,149.4 295.3,148.7 299.0,148.2"/><polyline class="hl" points="44.0,118.0 47.7,118.0 51.4,118.0 55.1,118.0 58.8,118.0 62.5,118.0 66.2,118.0 69.9,118.0 73.6,118.0 77.3,118.0 81.0,118.0 84.7,118.1 88.3,118.1 92.0,118.1 95.7,118.1 99.4,118.1 103.1,118.1 106.8,118.1 110.5,118.1 114.2,118.2 117.9,118.2 121.6,118.2 125.3,118.2 129.0,118.3 132.7,118.3 136.4,118.4 140.1,118.4 143.8,118.5 147.5,118.6 151.2,118.7 154.9,118.8 158.6,118.9 162.3,119.0 166.0,119.2 169.7,119.3 173.3,119.5 177.0,119.8 180.7,120.1 184.4,120.4 188.1,120.7 191.8,121.1 195.5,121.6 199.2,122.1 202.9,122.7 206.6,123.3 210.3,124.0 214.0,124.8 217.7,125.5 221.4,126.4 225.1,127.3 228.8,128.2 232.5,129.1 236.2,130.1 239.9,131.0 243.6,132.0 247.3,132.9 251.0,133.8 254.7,134.7 258.3,135.5 262.0,136.3 265.7,137.0 269.4,137.7 273.1,138.4 276.8,138.9 280.5,139.5 284.2,140.0 287.9,140.4 291.6,140.8 295.3,141.2 299.0,141.5"/><polyline class="mut" points="44.0,140.4 47.7,140.4 51.4,140.5 55.1,140.5 58.8,140.5 62.5,140.5 66.2,140.5 69.9,140.5 73.6,140.5 77.3,140.5 81.0,140.5 84.7,140.5 88.3,140.5 92.0,140.5 95.7,140.5 99.4,140.6 103.1,140.6 106.8,140.6 110.5,140.6 114.2,140.6 117.9,140.7 121.6,140.7 125.3,140.7 129.0,140.8 132.7,140.8 136.4,140.9 140.1,140.9 143.8,141.0 147.5,141.1 151.2,141.2 154.9,141.3 158.6,141.4 162.3,141.5 166.0,141.6 169.7,141.7 173.3,141.9 177.0,142.0 180.7,142.2 184.4,142.3 188.1,142.5 191.8,142.7 195.5,142.8 199.2,143.0 202.9,143.2 206.6,143.4 210.3,143.5 214.0,143.7 217.7,143.8 221.4,143.9 225.1,144.0 228.8,144.1 232.5,144.2 236.2,144.3 239.9,144.3 243.6,144.3 247.3,144.4 251.0,144.4 254.7,144.4 258.3,144.4 262.0,144.4 265.7,144.3 269.4,144.3 273.1,144.3 276.8,144.3 280.5,144.3 284.2,144.2 287.9,144.2 291.6,144.2 295.3,144.2 299.0,144.2"/><text class="t-mut" x="48.0" y="34.1">w₁</text><text class="t-mut" x="48.0" y="201.8">w₂</text><text class="t-mut" x="48.0" y="113.0">w₃</text><text class="t-mut" x="48.0" y="135.4">w₄</text><text class="title" x="475" y="16" text-anchor="middle">Lasso (L1)</text><path class="ax" d="M349,30 V220 H604"/><text x="476.5" y="250" text-anchor="middle">log₁₀ λ →</text><text x="323" y="125.0" text-anchor="middle" transform="rotate(-90 323 125.0)">weight</text><line class="grid" x1="349.0" y1="144.0" x2="604.0" y2="144.0"/><text class="t-mut" x="349.0" y="234.0" text-anchor="middle">-1</text><text class="t-mut" x="412.8" y="234.0" text-anchor="middle">0</text><text class="t-mut" x="476.5" y="234.0" text-anchor="middle">1</text><text class="t-mut" x="540.2" y="234.0" text-anchor="middle">2</text><text class="t-mut" x="604.0" y="234.0" text-anchor="middle">3</text><polyline class="ink" points="349.0,39.0 352.7,39.0 356.4,39.0 360.1,39.0 363.8,39.0 367.5,39.0 371.2,39.0 374.9,39.0 378.6,39.0 382.3,39.0 386.0,39.1 389.7,39.1 393.3,39.1 397.0,39.1 400.7,39.1 404.4,39.1 408.1,39.2 411.8,39.2 415.5,39.2 419.2,39.3 422.9,39.3 426.6,39.3 430.3,39.4 434.0,39.5 437.7,39.5 441.4,39.6 445.1,39.7 448.8,39.8 452.5,39.9 456.2,40.1 459.9,40.2 463.6,40.4 467.3,40.6 471.0,40.9 474.7,41.1 478.3,41.4 482.0,41.8 485.7,42.1 489.4,42.5 493.1,43.0 496.8,43.6 500.5,44.2 504.2,44.9 507.9,45.7 511.6,46.6 515.3,47.7 519.0,48.9 522.7,50.2 526.4,51.8 530.1,53.6 533.8,55.6 537.5,58.0 541.2,60.7 544.9,64.4 548.6,68.8 552.3,73.8 556.0,79.4 559.7,85.9 563.3,93.3 567.0,102.5 570.7,113.3 574.4,125.7 578.1,139.8 581.8,144.0 585.5,144.0 589.2,144.0 592.9,144.0 596.6,144.0 600.3,144.0 604.0,144.0"/><polyline class="warn" points="349.0,206.8 352.7,206.8 356.4,206.8 360.1,206.8 363.8,206.8 367.5,206.8 371.2,206.8 374.9,206.8 378.6,206.8 382.3,206.8 386.0,206.8 389.7,206.8 393.3,206.7 397.0,206.7 400.7,206.7 404.4,206.7 408.1,206.6 411.8,206.6 415.5,206.6 419.2,206.5 422.9,206.5 426.6,206.4 430.3,206.4 434.0,206.3 437.7,206.2 441.4,206.1 445.1,206.0 448.8,205.9 452.5,205.7 456.2,205.6 459.9,205.4 463.6,205.2 467.3,204.9 471.0,204.6 474.7,204.3 478.3,204.0 482.0,203.6 485.7,203.1 489.4,202.5 493.1,201.9 496.8,201.2 500.5,200.4 504.2,199.5 507.9,198.5 511.6,197.3 515.3,195.9 519.0,194.4 522.7,192.6 526.4,190.6 530.1,188.2 533.8,185.6 537.5,182.6 541.2,179.1 544.9,175.3 548.6,170.9 552.3,166.0 556.0,160.3 559.7,153.8 563.3,146.4 567.0,144.0 570.7,144.0 574.4,144.0 578.1,144.0 581.8,144.0 585.5,144.0 589.2,144.0 592.9,144.0 596.6,144.0 600.3,144.0 604.0,144.0"/><polyline class="hl" points="349.0,118.0 352.7,118.0 356.4,118.0 360.1,118.0 363.8,118.0 367.5,118.0 371.2,118.1 374.9,118.1 378.6,118.1 382.3,118.1 386.0,118.1 389.7,118.1 393.3,118.1 397.0,118.1 400.7,118.1 404.4,118.2 408.1,118.2 411.8,118.2 415.5,118.3 419.2,118.3 422.9,118.3 426.6,118.4 430.3,118.4 434.0,118.5 437.7,118.6 441.4,118.7 445.1,118.7 448.8,118.9 452.5,119.0 456.2,119.1 459.9,119.3 463.6,119.5 467.3,119.7 471.0,119.9 474.7,120.2 478.3,120.5 482.0,120.8 485.7,121.3 489.4,121.8 493.1,122.4 496.8,123.0 500.5,123.8 504.2,124.6 507.9,125.6 511.6,126.7 515.3,128.0 519.0,129.5 522.7,131.2 526.4,133.1 530.1,135.3 533.8,137.8 537.5,140.6 541.2,143.9 544.9,144.0 548.6,144.0 552.3,144.0 556.0,144.0 559.7,144.0 563.3,144.0 567.0,144.0 570.7,144.0 574.4,144.0 578.1,144.0 581.8,144.0 585.5,144.0 589.2,144.0 592.9,144.0 596.6,144.0 600.3,144.0 604.0,144.0"/><polyline class="mut" points="349.0,140.5 352.7,140.5 356.4,140.5 360.1,140.5 363.8,140.5 367.5,140.5 371.2,140.5 374.9,140.5 378.6,140.5 382.3,140.5 386.0,140.5 389.7,140.6 393.3,140.6 397.0,140.6 400.7,140.6 404.4,140.6 408.1,140.7 411.8,140.7 415.5,140.8 419.2,140.8 422.9,140.9 426.6,140.9 430.3,141.0 434.0,141.1 437.7,141.2 441.4,141.3 445.1,141.4 448.8,141.5 452.5,141.7 456.2,141.8 459.9,142.1 463.6,142.3 467.3,142.5 471.0,142.8 474.7,143.2 478.3,143.6 482.0,144.0 485.7,144.0 489.4,144.0 493.1,144.0 496.8,144.0 500.5,144.0 504.2,144.0 507.9,144.0 511.6,144.0 515.3,144.0 519.0,144.0 522.7,144.0 526.4,144.0 530.1,144.0 533.8,144.0 537.5,144.0 541.2,144.0 544.9,144.0 548.6,144.0 552.3,144.0 556.0,144.0 559.7,144.0 563.3,144.0 567.0,144.0 570.7,144.0 574.4,144.0 578.1,144.0 581.8,144.0 585.5,144.0 589.2,144.0 592.9,144.0 596.6,144.0 600.3,144.0 604.0,144.0"/><text class="t-mut" x="353.0" y="34.0">w₁</text><text class="t-mut" x="353.0" y="201.8">w₂</text><text class="t-mut" x="353.0" y="113.0">w₃</text><text class="t-mut" x="353.0" y="135.5">w₄</text></svg><figcaption>Coefficient paths on the same standardised data (true weights 3, −2, 0.8, 0) as λ grows. Ridge shrinks every weight smoothly towards 0 but none reaches it. Lasso drives weights to exactly 0 one by one; by λ = 400 only one feature is left.</figcaption></figure>
<!-- /fig:reg-paths -->

| $\lambda$ | Weights | Bias | Variance | Behaviour |
|---|---|---|---|---|
| $0$ | the OLS solution | lowest | highest | may overfit |
| moderate | shrunk | ↑ | ↓ | often the best test error |
| $\to \infty$ | $\to 0$ (all of them) | very high | → 0 | predicts a constant ($\bar y$ when the intercept is unpenalised): underfits |

**Choose $\lambda$ by cross-validation** (topic 1), never on the test set.

## 3.6 Ridge in gradient descent: weight decay

The gradient of $\lambda\|w\|_2^2$ is $2\lambda w$, so a ridge GD step is

$$
w \;\leftarrow\; w - \eta\big(\nabla L_{\text{data}}(w) + 2\lambda w\big) \;=\; (1 - 2\eta\lambda)\,w - \eta\,\nabla L_{\text{data}}(w).
$$

Before the usual update, the weights are multiplied by a factor slightly below 1. That's why L2 regularization is called **weight decay** in neural networks.

For lasso, the (sub)gradient of $\lambda|w_j|$ is $\lambda\,\operatorname{sign}(w_j)$: a **constant-size** push towards 0, no matter how small $w_j$ already is. That's why it can reach 0 exactly.

## 3.7 Two more facts you may be asked

- **Elastic net** $= \text{loss} + \lambda_1\|w\|_1 + \lambda_2\|w\|_2^2$. It gives sparsity like lasso but handles groups of correlated features better.
- **Bayesian view:** ridge is the MAP estimate under a **Gaussian** prior on the weights. Lasso is MAP under a **Laplace** prior, which has a sharp peak at 0 and so favours exact zeros.

---

## Summary: important points

<div class="formula">

1. Ridge: $\text{RSS} + \lambda\sum w_j^2$, giving $(X^\top X + \lambda I)^{-1}X^\top y$, always invertible for $\lambda > 0$.
2. Lasso: $\text{RSS} + \lambda\sum |w_j|$. No closed form. Soft-thresholding produces **exact zeros** (feature selection).
3. Ridge **shrinks** weights but never zeroes them. With orthonormal features, $w_{\text{OLS}}/(1 + \lambda)$.
4. Geometry: the L1 diamond has corners on the axes, so solutions land on axes and give sparsity.
5. Larger $\lambda$: bias ↑, variance ↓. $\lambda = 0$ is OLS. $\lambda \to \infty$ sends the weights to 0.
6. In GD, ridge is weight decay: $w \leftarrow (1 - 2\eta\lambda)w - \eta\nabla L$.
7. Standardise the features. Don't penalise the intercept. Choose $\lambda$ by CV.

</div>

<div class="trap">

- Ridge uses the **squared** L2 norm, $\sum w_j^2$, not $\|w\|_2$.
- Ridge doesn't "remove negative weights" or "reduce the number of parameters". It shrinks their **magnitude**.
- "Overfitting" means good on train and poor on test (2026 Q37 option A reverses this).
- The soft-threshold is $\lambda/2$ or $\lambda$ depending on whether the loss has a factor of $\frac12$.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2026 Q55 (2 marks, NAT)

Linear ridge regression with $y_{\text{pred}} = w^\top x$, where $w, x \in \mathbb{R}^2$. The error measure is MAE and the regularizer has weight 0.20. Currently $w = [-3, 4]^\top$. The input is $x = [1, 2]^\top$ and $y_{\text{true}} = x_1 + x_2$. What is the overall regularized loss for this instance? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 7.00**

1. Prediction: $w^\top x = -3(1) + 4(2) = 5$.
2. Truth: $y_{\text{true}} = 1 + 2 = 3$.
3. MAE for one example: $|5 - 3| = 2$.
4. Ridge penalty: $0.2\,\|w\|_2^2 = 0.2\,(9 + 16) = 5$.
5. Total: $2 + 5 = $ **7.00**.

If you used $\|w\|_2 = 5$ instead of $\|w\|_2^2 = 25$, you'd get $2 + 1 = 3$, which is wrong.

</details>

### GATE DA 2026 Q37 (2 marks, MCQ)

Which statement is true for ridge regression?
(A) The regularizer guards against the model working well on test data but poorly on training data (B) The regularizer uses the $L_1$ norm (C) It aims to reduce the number of parameters with negative values (D) The regularizer may increase the bias of the model but helps reduce the variance of predictions

<details>
<summary>Show solution</summary>

**Answer: (D)**

- (A) states overfitting backwards.
- (B) Ridge is L2. L1 is lasso.
- (C) Ridge shrinks magnitudes regardless of sign.
- (D) is exactly §3.5.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** Data $x = (1, 2, 3)$, $y = (2, 4, 5)$, model $\hat y = wx$ with no intercept. What is the ridge estimate of $w$ with $\lambda = 1$? (3 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 1.667**

$\sum x_i y_i = 2 + 8 + 15 = 25$ and $\sum x_i^2 = 14$.

- Ridge: $25/(14 + 1) = 1.667$.
- For comparison, OLS gives $25/14 = 1.786$. The ridge weight is smaller.

</details>

**F2 (2 marks, NAT).** With orthonormal features, the OLS weights are $(3, -0.5, 1.2)$. Lasso with objective $\text{RSS} + \lambda\|w\|_1$ and $\lambda = 2$ is applied. How many weights are non-zero?

<details>
<summary>Show solution</summary>

**Answer: 2**

The threshold is $\lambda/2 = 1$.

- $3 \to 3 - 1 = 2$
- $|-0.5| < 1 \to 0$
- $1.2 \to 0.2$

The result is $(2, 0, 0.2)$, which has **2** non-zero weights. Ridge with the same $\lambda$ would give $(1, -0.167, 0.4)$: all three non-zero.

</details>

**F3 (2 marks, MSQ).** Which statements are true?
(A) Lasso can set some weights exactly to zero (B) Ridge can set some weights exactly to zero (C) As $\lambda \to \infty$ in ridge, all penalised weights tend to 0 (D) For $\lambda > 0$, $X^\top X + \lambda I$ is invertible even if $X$ has collinear columns

<details>
<summary>Show solution</summary>

**Answer: A; C; D**

(B) is false. Ridge shrinks the weights, but in general none becomes exactly zero.

</details>

**F4 (1 mark, NAT).** One gradient-descent step on $J = L(w) + \lambda w^2$, with $w = 2$, $L'(w) = 1$, $\lambda = 0.5$ and $\eta = 0.1$. What is the new $w$?

<details>
<summary>Show solution</summary>

**Answer: 1.7**

$\nabla J = L'(w) + 2\lambda w = 1 + 2(0.5)(2) = 3$. So $w \leftarrow 2 - 0.1 \times 3 = $ **1.7**.

</details>

**F5 (2 marks, NAT).** Lasso with squared error. $w = [2, -1]^\top$, $x = [1, 3]^\top$, $y_{\text{true}} = 0$ and $\lambda = 0.5$. What is the regularized loss for this instance?

<details>
<summary>Show solution</summary>

**Answer: 2.5**

- Prediction: $2 - 3 = -1$. Squared error: $(-1 - 0)^2 = 1$.
- L1 penalty: $0.5(|2| + |-1|) = 1.5$.
- Total: $1 + 1.5 = $ **2.5**.

</details>

**F6 (1 mark, MCQ).** Ridge regression with an unpenalised intercept is fitted with $\lambda \to \infty$. What does the model predict for every input?
(A) 0 (B) the mean of the training targets $\bar y$ (C) the OLS prediction (D) the median of $y$

<details>
<summary>Show solution</summary>

**Answer: (B)**

All penalised weights go to 0, which leaves $\hat y = \beta_0$. The best constant under squared error is $\bar y$.

</details>
