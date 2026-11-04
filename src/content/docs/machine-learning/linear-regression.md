---
title: 2. Linear regression & gradient descent
description: Least squares from scratch, the slope and intercept formulas, regression through the origin, the normal equation and its geometry, R², and gradient-descent updates.
sidebar:
  label: 2. Linear regression
  order: 2
---

**Why it matters:** 2025 Q34 (least squares for $y = wx$) and 2026 Q29 (one SGD step) are one-line numericals **if** you know the formula or the update rule exactly. Linear regression is also the base for ridge, lasso, logistic regression and neural networks, and every one of those reuses the ideas on this page.

## Topic map

<div class="mindmap">

- **Linear regression**
  - Model
    - $\hat y = \beta_0 + \beta_1 x$ (simple), $\hat y = X\beta$ (multiple)
  - Least squares
    - minimise RSS $= \sum (y_i - \hat y_i)^2$
    - $\beta_1 = S_{xy}/S_{xx}$, $\beta_0 = \bar y - \beta_1 \bar x$
    - through the origin: $w = \sum x_i y_i / \sum x_i^2$
  - Normal equation
    - $\hat\beta = (X^\top X)^{-1}X^\top y$
    - geometry: projection, residual ⟂ columns
  - Goodness of fit
    - RSS, TSS, $R^2 = 1 - \text{RSS}/\text{TSS}$
    - adjusted $R^2$
  - Gradient descent
    - $w \leftarrow w - \eta \nabla L$
    - batch, stochastic, mini-batch
    - learning rate too small / too large

</div>

## 2.1 The model

**Simple linear regression** predicts a number $y$ from one feature $x$ using a straight line:

$$
\hat y = \beta_0 + \beta_1 x.
$$

$\beta_0$ is the **intercept** (the prediction when $x = 0$) and $\beta_1$ is the **slope** (how much $\hat y$ changes when $x$ goes up by 1). We assume the real data is $y = \beta_0 + \beta_1 x + \varepsilon$, a line plus random noise $\varepsilon$ with mean 0.

**Multiple linear regression** uses $p$ features:

$$
\hat y = \beta_0 + \beta_1 x_1 + \dots + \beta_p x_p = x^\top \beta,
$$

where we add a constant feature $x_0 = 1$ so the intercept fits inside the vector. Stacking all $n$ examples as rows gives the **design matrix** $X$ ($n \times (p+1)$), and the predictions are $\hat y = X\beta$.

"Linear" means linear **in the parameters $\beta$**. A model like $\hat y = \beta_0 + \beta_1 x + \beta_2 x^2$ is still linear regression, with $x^2$ treated as one more feature. That's why polynomial fits (like the overfitting figure in topic 1) are solved with exactly the same equations.

## 2.2 Least squares: which line is "best"?

For each point, the **residual** $e_i = y_i - \hat y_i$ is the vertical miss. **Ordinary least squares (OLS)** picks the line that minimises the **residual sum of squares**:

$$
\text{RSS}(\beta_0, \beta_1) = \sum_{i=1}^n \big(y_i - \beta_0 - \beta_1 x_i\big)^2.
$$

<!-- fig:lr-residuals -->
<figure class="diagram"><svg class="dg" viewBox="0 0 540 310" role="img" aria-label="Least squares line with residuals" xmlns="http://www.w3.org/2000/svg"><path class="ax" d="M60,20 V270 H520"/><text x="290.0" y="302" text-anchor="middle">x</text><text x="30" y="145.0" text-anchor="middle" transform="rotate(-90 30 145.0)">y</text><text class="t-mut" x="136.7" y="284.0" text-anchor="middle">1</text><text class="t-mut" x="52.0" y="235.5" text-anchor="end">1</text><text class="t-mut" x="213.3" y="284.0" text-anchor="middle">2</text><text class="t-mut" x="52.0" y="197.1" text-anchor="end">2</text><text class="t-mut" x="290.0" y="284.0" text-anchor="middle">3</text><text class="t-mut" x="52.0" y="158.6" text-anchor="end">3</text><text class="t-mut" x="366.7" y="284.0" text-anchor="middle">4</text><text class="t-mut" x="52.0" y="120.2" text-anchor="end">4</text><text class="t-mut" x="443.3" y="284.0" text-anchor="middle">5</text><text class="t-mut" x="52.0" y="81.7" text-anchor="end">5</text><polyline class="ink" points="83.0,178.5 497.0,53.8"/><line class="warn" style="stroke-width:1.6;stroke-dasharray:4 3" x1="136.7" y1="193.1" x2="136.7" y2="162.3"/><text class="t-warn" x="142.7" y="181.7">-0.8</text><circle class="dot" cx="136.7" cy="193.1" r="4"/><line class="warn" style="stroke-width:1.6;stroke-dasharray:4 3" x1="213.3" y1="116.2" x2="213.3" y2="139.2"/><text class="t-warn" x="219.3" y="131.7">+0.6</text><circle class="dot" cx="213.3" cy="116.2" r="4"/><line class="warn" style="stroke-width:1.6;stroke-dasharray:4 3" x1="290.0" y1="77.7" x2="290.0" y2="116.2"/><text class="t-warn" x="296.0" y="100.9">+1.0</text><circle class="dot" cx="290.0" cy="77.7" r="4"/><line class="warn" style="stroke-width:1.6;stroke-dasharray:4 3" x1="366.7" y1="116.2" x2="366.7" y2="93.1"/><text class="t-warn" x="372.7" y="108.6">-0.6</text><circle class="dot" cx="366.7" cy="116.2" r="4"/><line class="warn" style="stroke-width:1.6;stroke-dasharray:4 3" x1="443.3" y1="77.7" x2="443.3" y2="70.0"/><text class="t-warn" x="449.3" y="77.8">-0.2</text><circle class="dot" cx="443.3" cy="77.7" r="4"/><circle class="dot-hl" cx="290.0" cy="116.2" r="5"/><text class="t-hl" x="282.0" y="106.2" text-anchor="end">(x̄, ȳ)</text><text class="t-ink" x="489.3" y="46.2" text-anchor="end">ŷ = 2.2 + 0.6x</text></svg><figcaption>Least squares on the worked example: points (1,2), (2,4), (3,5), (4,4), (5,5). The fitted line is ŷ = 2.2 + 0.6x. Each dashed segment is a residual eᵢ = yᵢ − ŷᵢ; OLS chooses the line that makes the sum of their squares (RSS = 2.4) as small as possible. The line passes through (x̄, ȳ) = (3, 4).</figcaption></figure>
<!-- /fig:lr-residuals -->

**Why squares?** Squaring makes every miss positive. It punishes big misses much more than small ones, and it makes RSS a smooth **convex bowl** in $\beta$, so there's exactly one minimum and calculus finds it. (It's also what maximum likelihood gives when the noise is Gaussian.)

### Deriving the formulas

Set both partial derivatives of RSS to zero.

$$
\frac{\partial\,\text{RSS}}{\partial \beta_0} = -2\sum (y_i - \beta_0 - \beta_1 x_i) = 0 \;\Rightarrow\; \bar y = \beta_0 + \beta_1 \bar x
$$

So **the fitted line always passes through $(\bar x, \bar y)$**. Substituting $\beta_0 = \bar y - \beta_1 \bar x$ into the second equation, $\partial\,\text{RSS}/\partial\beta_1 = 0$, and simplifying gives:

<div class="formula">

$$
\beta_1 = \frac{S_{xy}}{S_{xx}} = \frac{\sum (x_i - \bar x)(y_i - \bar y)}{\sum (x_i - \bar x)^2} = r\,\frac{s_y}{s_x}
\qquad\qquad
\beta_0 = \bar y - \beta_1 \bar x
$$

Here $r$ is the correlation between $x$ and $y$, and $s_x$, $s_y$ are their standard deviations. So the slope has the **same sign as the correlation**.

**Regression through the origin** (the model $\hat y = wx$, with no intercept):

$$
\frac{d}{dw}\sum (y_i - w x_i)^2 = -2\sum x_i (y_i - w x_i) = 0 \;\Rightarrow\; w = \frac{\sum x_i y_i}{\sum x_i^2}
$$

</div>

Don't mix up the two formulas. The through-origin version uses **raw** sums, $\sum xy$ and $\sum x^2$. The version with an intercept uses **centred** sums, $S_{xy}$ and $S_{xx}$.

### Worked example

Data: $(1,2), (2,4), (3,5), (4,4), (5,5)$.

| | Value |
|---|---|
| $\bar x$, $\bar y$ | 3, 4 |
| $x_i - \bar x$ | −2, −1, 0, 1, 2 |
| $y_i - \bar y$ | −2, 0, 1, 0, 1 |
| $S_{xy} = \sum (x_i - \bar x)(y_i - \bar y)$ | $4 + 0 + 0 + 0 + 2 = 6$ |
| $S_{xx}$ | $4 + 1 + 0 + 1 + 4 = 10$ |
| $\beta_1 = 6/10$ | **0.6** |
| $\beta_0 = 4 - 0.6 \times 3$ | **2.2** |

So $\hat y = 2.2 + 0.6x$. The predictions are 2.8, 3.4, 4.0, 4.6, 5.2, and the residuals are −0.8, +0.6, +1.0, −0.6, −0.2. Those residuals **sum to 0**, which always happens when the model has an intercept.

## 2.3 Multiple regression: the normal equation

In matrix form, $\text{RSS}(\beta) = \|y - X\beta\|^2$. Setting its gradient to zero:

$$
\nabla_\beta \text{RSS} = -2X^\top (y - X\beta) = 0 \quad\Longrightarrow\quad X^\top X\,\beta = X^\top y.
$$

<div class="formula">

$$
\hat\beta = (X^\top X)^{-1} X^\top y \qquad \text{(when } X^\top X \text{ is invertible)}
$$

- $X^\top X$ is invertible exactly when the columns of $X$ are **linearly independent** (full column rank).
- It is **singular** when one feature is a linear combination of others (perfect multicollinearity), or when there are more features than examples ($p + 1 > n$). Then there are infinitely many least-squares solutions, which is one reason to use ridge regression.
- Solving it costs $O(np^2 + p^3)$. That's fine for small $p$, but for large problems we use gradient descent instead.

</div>

### The geometry (this is what makes it click)

$X\beta$ can only reach vectors in the **column space** of $X$. Least squares picks the point $\hat y$ in that space **closest** to $y$, which is the **orthogonal projection** of $y$ onto it.

- The residual $e = y - \hat y$ is **perpendicular** to every column of $X$: $X^\top e = 0$. That's exactly the normal equation.
- If there's an intercept column of 1s, this gives $\sum e_i = 0$ (residuals sum to zero), and since $x$ is also a column, $\sum x_i e_i = 0$.
- $\hat y = Hy$ with the **hat matrix** $H = X(X^\top X)^{-1}X^\top$, a projection matrix: symmetric, $H^2 = H$ (idempotent), with eigenvalues 0 or 1. This links straight to Linear Algebra.

## 2.4 How good is the fit?

<div class="formula">

$$
\text{TSS} = \sum (y_i - \bar y)^2 \qquad \text{RSS} = \sum (y_i - \hat y_i)^2 \qquad R^2 = 1 - \frac{\text{RSS}}{\text{TSS}}
$$

- TSS is the variation in $y$ before using $x$. RSS is what's left over after the fit.
- $R^2$ is the **fraction of the variance in $y$ that the model explains**. With an intercept, on the training data, $0 \le R^2 \le 1$.
- For simple linear regression, $R^2 = r^2$, the square of the correlation.
- **Adding a feature never decreases training $R^2$.** **Adjusted** $R^2 = 1 - (1 - R^2)\frac{n-1}{n-p-1}$ penalises useless features.
- **MSE** $= \text{RSS}/n$. **RMSE** $= \sqrt{\text{MSE}}$, in the units of $y$. **MAE** $= \frac1n\sum |y_i - \hat y_i|$, which is less sensitive to outliers.

</div>

In the worked example, TSS $= 4 + 0 + 1 + 0 + 1 = 6$ and RSS $= 0.64 + 0.36 + 1 + 0.36 + 0.04 = 2.4$, so $R^2 = 1 - 2.4/6 = 0.6$. You can check that $r^2 = 0.6$ too.

## 2.5 Gradient descent

When a closed form is too expensive, or doesn't exist (logistic regression, neural networks), we **walk downhill**. The gradient $\nabla L(w)$ points in the direction of steepest **increase**, so we step the opposite way:

<div class="formula">

$$
w \;\leftarrow\; w - \eta\,\nabla_w L(w)
$$

$\eta > 0$ is the **learning rate** (step size).

For MSE with a linear model, $L(w) = \frac1n\|Xw - y\|^2$:

$$
\nabla_w L = \frac{2}{n}X^\top (Xw - y).
$$

For **one** example with loss $(wx - y)^2$, the gradient is $2(wx - y)\,x$.

</div>

**Reading a GATE question:** find the loss $L$, differentiate it **with respect to the parameter** (not the input), substitute the current values, then apply the update. Nothing else is involved.

| Variant | Gradient computed on | Behaviour |
|---|---|---|
| **Batch GD** | all $n$ examples | smooth, accurate steps, but each step is expensive |
| **Stochastic GD (SGD)** | **one** random example | cheap and noisy; the noise can help escape flat regions |
| **Mini-batch GD** | a batch of $b$ examples | the usual choice in practice |

**Choosing $\eta$:**

<!-- fig:lr-gd-steps -->
<figure class="diagram"><svg class="dg" viewBox="0 0 610 260" role="img" aria-label="Gradient descent with small and large learning rate" xmlns="http://www.w3.org/2000/svg"><text class="title" x="165" y="18" text-anchor="middle">η = 0.25 (good)</text><path class="ax" d="M40,34 V224 H290"/><text x="286.7" y="238.0" text-anchor="end">w</text><polyline class="mut" points="45.4,53.7 47.4,59.4 49.5,65.0 51.5,70.4 53.5,75.8 55.5,81.1 57.5,86.3 59.5,91.4 61.5,96.4 63.5,101.3 65.5,106.1 67.5,110.8 69.5,115.5 71.6,120.0 73.6,124.4 75.6,128.7 77.6,133.0 79.6,137.1 81.6,141.2 83.6,145.1 85.6,148.9 87.6,152.7 89.6,156.4 91.7,159.9 93.7,163.4 95.7,166.7 97.7,170.0 99.7,173.2 101.7,176.3 103.7,179.3 105.7,182.1 107.7,184.9 109.7,187.6 111.7,190.2 113.8,192.7 115.8,195.1 117.8,197.4 119.8,199.6 121.8,201.8 123.8,203.8 125.8,205.7 127.8,207.5 129.8,209.3 131.8,210.9 133.9,212.4 135.9,213.9 137.9,215.2 139.9,216.5 141.9,217.6 143.9,218.7 145.9,219.7 147.9,220.5 149.9,221.3 151.9,222.0 153.9,222.5 156.0,223.0 158.0,223.4 160.0,223.7 162.0,223.9 164.0,224.0 166.0,224.0 168.0,223.9 170.0,223.7 172.0,223.4 174.0,223.0 176.1,222.5 178.1,222.0 180.1,221.3 182.1,220.5 184.1,219.7 186.1,218.7 188.1,217.6 190.1,216.5 192.1,215.2 194.1,213.9 196.1,212.4 198.2,210.9 200.2,209.3 202.2,207.5 204.2,205.7 206.2,203.8 208.2,201.8 210.2,199.6 212.2,197.4 214.2,195.1 216.2,192.7 218.3,190.2 220.3,187.6 222.3,184.9 224.3,182.1 226.3,179.3 228.3,176.3 230.3,173.2 232.3,170.0 234.3,166.7 236.3,163.4 238.3,159.9 240.4,156.4 242.4,152.7 244.4,148.9 246.4,145.1 248.4,141.2 250.4,137.1 252.4,133.0 254.4,128.7 256.4,124.4 258.4,120.0 260.5,115.5 262.5,110.8 264.5,106.1 266.5,101.3 268.5,96.4 270.5,91.4 272.5,86.3 274.5,81.1 276.5,75.8 278.5,70.4 280.5,65.0 282.6,59.4 284.6,53.7"/><line class="ink" style="stroke-width:1.6" x1="273.7" y1="83.3" x2="219.3" y2="188.8"/><line class="ink" style="stroke-width:1.6" x1="219.3" y1="188.8" x2="192.2" y2="215.2"/><line class="ink" style="stroke-width:1.6" x1="192.2" y1="215.2" x2="178.6" y2="221.8"/><line class="ink" style="stroke-width:1.6" x1="178.6" y1="221.8" x2="171.8" y2="223.5"/><line class="ink" style="stroke-width:1.6" x1="171.8" y1="223.5" x2="168.4" y2="223.9"/><line class="ink" style="stroke-width:1.6" x1="168.4" y1="223.9" x2="166.7" y2="224.0"/><circle class="dot-ink" cx="273.7" cy="83.3" r="4.2"/><circle class="dot-ink" cx="219.3" cy="188.8" r="3.2"/><circle class="dot-ink" cx="192.2" cy="215.2" r="3.2"/><circle class="dot-ink" cx="178.6" cy="221.8" r="3.2"/><circle class="dot-ink" cx="171.8" cy="223.5" r="3.2"/><circle class="dot-ink" cx="168.4" cy="223.9" r="3.2"/><circle class="dot-ink" cx="166.7" cy="224.0" r="3.2"/><text class="t-mut" x="273.7" y="75.3" text-anchor="middle">start</text><text class="t-mut" x="165.0" y="238.0" text-anchor="middle">0</text><text class="title" x="465" y="18" text-anchor="middle">η = 0.95 (too large)</text><path class="ax" d="M340,34 V224 H590"/><text x="586.7" y="238.0" text-anchor="end">w</text><polyline class="mut" points="345.4,53.7 347.4,59.4 349.5,65.0 351.5,70.4 353.5,75.8 355.5,81.1 357.5,86.3 359.5,91.4 361.5,96.4 363.5,101.3 365.5,106.1 367.5,110.8 369.5,115.5 371.6,120.0 373.6,124.4 375.6,128.7 377.6,133.0 379.6,137.1 381.6,141.2 383.6,145.1 385.6,148.9 387.6,152.7 389.6,156.4 391.7,159.9 393.7,163.4 395.7,166.7 397.7,170.0 399.7,173.2 401.7,176.3 403.7,179.3 405.7,182.1 407.7,184.9 409.7,187.6 411.7,190.2 413.8,192.7 415.8,195.1 417.8,197.4 419.8,199.6 421.8,201.8 423.8,203.8 425.8,205.7 427.8,207.5 429.8,209.3 431.8,210.9 433.9,212.4 435.9,213.9 437.9,215.2 439.9,216.5 441.9,217.6 443.9,218.7 445.9,219.7 447.9,220.5 449.9,221.3 451.9,222.0 453.9,222.5 456.0,223.0 458.0,223.4 460.0,223.7 462.0,223.9 464.0,224.0 466.0,224.0 468.0,223.9 470.0,223.7 472.0,223.4 474.0,223.0 476.1,222.5 478.1,222.0 480.1,221.3 482.1,220.5 484.1,219.7 486.1,218.7 488.1,217.6 490.1,216.5 492.1,215.2 494.1,213.9 496.1,212.4 498.2,210.9 500.2,209.3 502.2,207.5 504.2,205.7 506.2,203.8 508.2,201.8 510.2,199.6 512.2,197.4 514.2,195.1 516.2,192.7 518.3,190.2 520.3,187.6 522.3,184.9 524.3,182.1 526.3,179.3 528.3,176.3 530.3,173.2 532.3,170.0 534.3,166.7 536.3,163.4 538.3,159.9 540.4,156.4 542.4,152.7 544.4,148.9 546.4,145.1 548.4,141.2 550.4,137.1 552.4,133.0 554.4,128.7 556.4,124.4 558.4,120.0 560.5,115.5 562.5,110.8 564.5,106.1 566.5,101.3 568.5,96.4 570.5,91.4 572.5,86.3 574.5,81.1 576.5,75.8 578.5,70.4 580.5,65.0 582.6,59.4 584.6,53.7"/><line class="warn" style="stroke-width:1.6" x1="573.7" y1="83.3" x2="367.2" y2="110.0"/><line class="warn" style="stroke-width:1.6" x1="367.2" y1="110.0" x2="553.0" y2="131.7"/><line class="warn" style="stroke-width:1.6" x1="553.0" y1="131.7" x2="385.8" y2="149.2"/><line class="warn" style="stroke-width:1.6" x1="385.8" y1="149.2" x2="536.3" y2="163.4"/><line class="warn" style="stroke-width:1.6" x1="536.3" y1="163.4" x2="400.8" y2="174.9"/><line class="warn" style="stroke-width:1.6" x1="400.8" y1="174.9" x2="522.8" y2="184.3"/><circle class="dot-warn" cx="573.7" cy="83.3" r="4.2"/><circle class="dot-warn" cx="367.2" cy="110.0" r="3.2"/><circle class="dot-warn" cx="553.0" cy="131.7" r="3.2"/><circle class="dot-warn" cx="385.8" cy="149.2" r="3.2"/><circle class="dot-warn" cx="536.3" cy="163.4" r="3.2"/><circle class="dot-warn" cx="400.8" cy="174.9" r="3.2"/><circle class="dot-warn" cx="522.8" cy="184.3" r="3.2"/><text class="t-mut" x="573.7" y="75.3" text-anchor="middle">start</text><text class="t-mut" x="465.0" y="238.0" text-anchor="middle">0</text></svg><figcaption>Gradient descent on L(w) = w², starting at w = 1. With η = 0.25 each step multiplies w by (1 − 2η) = 0.5 and slides smoothly to the minimum. With η = 0.95 the factor is −0.9: w flips sign every step and barely shrinks; any η > 1 would make it diverge.</figcaption></figure>
<!-- /fig:lr-gd-steps -->

- Too small: convergence takes forever.
- Too large: the steps overshoot and oscillate or diverge.
- For $L(w) = aw^2$ the update is $w \leftarrow (1 - 2a\eta)\,w$, which converges exactly when $|1 - 2a\eta| < 1$, that is, $0 < \eta < 1/a$.
- MSE for linear regression is **convex**, so with a suitable $\eta$, gradient descent reaches the **global** minimum, which is the same answer as the normal equation.
- Features on very different scales make the loss bowl long and narrow, and GD zig-zags. **Standardising** the features fixes this.

---

## Summary: important points

<div class="formula">

1. OLS minimises RSS $= \sum (y_i - \hat y_i)^2$.
2. $\beta_1 = S_{xy}/S_{xx}$ and $\beta_0 = \bar y - \beta_1\bar x$. The line passes through $(\bar x, \bar y)$.
3. Through the origin: $w = \sum x_i y_i / \sum x_i^2$ (raw sums, not centred ones).
4. Normal equation: $\hat\beta = (X^\top X)^{-1}X^\top y$. The residuals are orthogonal to every column of $X$.
5. With an intercept, the residuals sum to 0 and training $R^2 \in [0, 1]$.
6. $R^2 = 1 - \text{RSS}/\text{TSS}$, which equals $r^2$ in simple regression. Adding features never lowers training $R^2$.
7. GD: $w \leftarrow w - \eta\nabla L$. For one example with squared loss, the gradient is $2(wx - y)x$.
8. A too-large $\eta$ overshoots or diverges. A too-small one is slow. MSE is convex, so GD finds the global minimum.

</div>

<div class="trap">

- Differentiate with respect to the **parameter** $w$, not the input $x$.
- "Linear" regression is linear in the **parameters**. Polynomial features still count.
- $X^\top X$ is singular when features are collinear or $p + 1 > n$.
- The update **subtracts** the gradient. A sign slip turns descent into ascent.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2025 Q34 (1 mark, NAT)

Data $\{(-1, 1), (2, -5), (3, 5)\}$. Fit $y = wx$ by least squares. What is the optimal $w$? (3 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.286**

There's no intercept, so use $w = \dfrac{\sum x_i y_i}{\sum x_i^2}$.

- $\sum x_i y_i = (-1)(1) + (2)(-5) + (3)(5) = -1 - 10 + 15 = 4$
- $\sum x_i^2 = 1 + 4 + 9 = 14$
- $w = 4/14 = 0.2857 \approx$ **0.286**

A common mistake is to use the centred formula $S_{xy}/S_{xx}$, which is for the model **with** an intercept.

</details>

### GATE DA 2026 Q29 (1 mark, NAT)

The objective being minimised is $f_w(x) = wx$. SGD uses learning rate 0.10. After iteration $i$, $w = 10.00$. The input for iteration $i + 1$ is $x = 10.00$. What is $w$ after iteration $i + 1$?

<details>
<summary>Show solution</summary>

**Answer: 9.00**

1. Gradient with respect to the **parameter**: $\dfrac{\partial}{\partial w}(wx) = x = 10$.
2. Update: $w \leftarrow w - \eta \cdot 10 = 10 - 0.1 \times 10 = $ **9.00**.

The trap is differentiating with respect to $x$ (which gives $w = 10$) or adding the gradient instead of subtracting it.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (2 marks, NAT).** Fit $\hat y = \beta_0 + \beta_1 x$ by least squares to $(1, 3), (2, 5), (3, 7), (4, 10)$. What is the prediction at $x = 5$?

<details>
<summary>Show solution</summary>

**Answer: 12**

- $\bar x = 2.5$, $\bar y = 6.25$.
- $x - \bar x = -1.5, -0.5, 0.5, 1.5$ and $y - \bar y = -3.25, -1.25, 0.75, 3.75$.
- $S_{xy} = 4.875 + 0.625 + 0.375 + 5.625 = 11.5$ and $S_{xx} = 2.25 + 0.25 + 0.25 + 2.25 = 5$.
- $\beta_1 = 11.5/5 = 2.3$ and $\beta_0 = 6.25 - 2.3 \times 2.5 = 0.5$.
- $\hat y(5) = 0.5 + 2.3 \times 5 = $ **12**.

</details>

**F2 (1 mark, NAT).** For the fit in F1, what is $R^2$? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.99**

- Predictions: 2.8, 5.1, 7.4, 9.7. Residuals: 0.2, −0.1, −0.4, 0.3. RSS $= 0.04 + 0.01 + 0.16 + 0.09 = 0.30$.
- TSS $= 3.25^2 + 1.25^2 + 0.75^2 + 3.75^2 = 26.75$.
- $R^2 = 1 - 0.30/26.75 = 0.9888 \approx$ **0.99**.

</details>

**F3 (2 marks, MSQ).** OLS **with an intercept** is fitted to $n$ points. Which statements are always true?
(A) The residuals sum to zero (B) The fitted line passes through $(\bar x, \bar y)$ (C) $\sum x_i e_i = 0$ (D) Training $R^2$ can be negative

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

(A) and (C) are $X^\top e = 0$ for the columns $1$ and $x$. (B) comes from $\partial\,\text{RSS}/\partial\beta_0 = 0$. (D) is false: with an intercept, OLS can always do at least as well as predicting $\bar y$, so RSS $\le$ TSS. ($R^2$ *can* be negative on **test** data, or for a model with no intercept.)

</details>

**F4 (1 mark, NAT).** Squared loss on one example: $L = (wx - y)^2$ with $x = 2$ and $y = 3$. Starting from $w = 0$ with $\eta = 0.1$, what is $w$ after one gradient step?

<details>
<summary>Show solution</summary>

**Answer: 1.2**

$\nabla = 2(wx - y)x = 2(0 - 3)(2) = -12$. Then $w \leftarrow 0 - 0.1 \times (-12) = $ **1.2**.

</details>

**F5 (2 marks, NAT).** Gradient descent on $L(w) = w^2$, starting at $w = 1$ with $\eta = 0.25$. What is $w$ after 3 steps?

<details>
<summary>Show solution</summary>

**Answer: 0.125**

$\nabla = 2w$, so each step does $w \leftarrow w - 0.25 \times 2w = 0.5w$. After 3 steps, $w = 0.5^3 = $ **0.125**.

</details>

**F6 (2 marks, MCQ).** Solve the normal equations for $\hat y = \beta_1 x_1 + \beta_2 x_2$ (no intercept) with rows $(x_1, x_2, y) = (1, 0, 1), (0, 1, 2), (1, 1, 4)$.
(A) $(1, 2)$ (B) $(4/3, 7/3)$ (C) $(1.5, 2.5)$ (D) $(2, 1)$

<details>
<summary>Show solution</summary>

**Answer: (B)**

$X^\top X = \begin{pmatrix}2 & 1\\ 1 & 2\end{pmatrix}$ and $X^\top y = \begin{pmatrix}5\\ 6\end{pmatrix}$.

Solve $2\beta_1 + \beta_2 = 5$ and $\beta_1 + 2\beta_2 = 6$: $\beta_1 = 4/3$, $\beta_2 = 7/3$.

Check: the residuals are $(-1/3, -1/3, 1/3)$, which are orthogonal to both columns. ✓

</details>

**F7 (1 mark, MSQ).** Which statements about the learning rate $\eta$ in gradient descent are true?
(A) Too large an $\eta$ can make the loss diverge (B) Too small an $\eta$ makes convergence slow (C) For $L = w^2$, any $\eta \in (0, 1)$ converges (D) SGD computes the exact gradient of the full training loss at every step

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

For $L = w^2$, the factor $|1 - 2\eta| < 1 \iff 0 < \eta < 1$, so (C) is true. (D) is false: SGD uses a single example, which gives a **noisy estimate** of the full gradient.

</details>
