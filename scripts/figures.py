"""Theme-aware SVG figures for the notes.

Run:  python3 scripts/figures.py

Each figure is a function that returns an SVG string. Markdown pages hold markers

    <!-- fig:NAME -->
    <!-- /fig:NAME -->

and this script replaces whatever is between them with
<figure class="diagram"><svg …>…</svg><figcaption>…</figcaption></figure>.
Colours come from CSS classes in src/styles/custom.css (.dg .ink, .hl, …), so the
figures follow the light/dark theme. No blank lines are emitted (Markdown HTML blocks
end at a blank line).
"""
import math
import pathlib
import random
import re

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "src/content/docs"
FIGS = {}


def fig(name, caption):
    def deco(fn):
        FIGS[name] = (fn, caption)
        return fn
    return deco


class Plot:
    """Maps data coordinates to an SVG box."""

    def __init__(self, x0, y0, w, h, xr, yr):
        self.x0, self.y0, self.w, self.h, self.xr, self.yr = x0, y0, w, h, xr, yr

    def X(self, x):
        return self.x0 + (x - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w

    def Y(self, y):
        return self.y0 + self.h - (y - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h

    def path(self, xs, ys, cls):
        pts = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in zip(xs, ys))
        return f'<polyline class="{cls}" points="{pts}"/>'

    def axes(self, xlabel="", ylabel="", xoff=22, yoff=12):
        x0, y0, w, h = self.x0, self.y0, self.w, self.h
        out = [f'<path class="ax" d="M{x0},{y0} V{y0 + h} H{x0 + w}"/>']
        if xlabel:
            out.append(f'<text x="{x0 + w / 2}" y="{y0 + h + xoff}" text-anchor="middle">{xlabel}</text>')
        if ylabel:
            out.append(
                f'<text x="{x0 - yoff}" y="{y0 + h / 2}" text-anchor="middle" '
                f'transform="rotate(-90 {x0 - yoff} {y0 + h / 2})">{ylabel}</text>'
            )
        return "".join(out)


def svg(w, h, body, label):
    return (
        f'<svg class="dg" viewBox="0 0 {w} {h}" role="img" aria-label="{label}" '
        f'xmlns="http://www.w3.org/2000/svg">{body}</svg>'
    )


# ---------------------------------------------------------------- ML foundations


@fig("ml-fit-regimes", "The same 12 noisy points from y = sin(2πx), fitted by polynomials of degree 1, 3 and 11. "
     "Degree 1 misses the pattern (high bias). Degree 11 passes through every point but swings wildly between them (high variance).")
def fit_regimes():
    rng = np.random.default_rng(7)
    xs = np.linspace(0.04, 0.96, 12)
    ys = np.sin(2 * np.pi * xs) + rng.normal(0, 0.22, xs.size)
    grid = np.linspace(0, 1, 200)
    panels = [(1, "Underfit · degree 1", "warn"), (3, "Good fit · degree 3", "ink"), (11, "Overfit · degree 11", "warn")]
    body = []
    W, H, pad = 210, 170, 18
    for i, (deg, title, cls) in enumerate(panels):
        ox = 10 + i * (W + pad)
        p = Plot(ox + 8, 34, W - 16, H - 40, (0, 1), (-1.9, 1.9))
        body.append(f'<text class="title" x="{ox + W / 2}" y="18" text-anchor="middle">{title}</text>')
        body.append(f'<rect class="grid" x="{ox}" y="28" width="{W}" height="{H - 28}" rx="6"/>')
        body.append(p.path(grid, np.sin(2 * np.pi * grid), "mut"))
        coef = np.polyfit(xs, ys, deg)
        fy = np.clip(np.polyval(coef, grid), -1.85, 1.85)
        body.append(p.path(grid, fy, cls))
        for x, y in zip(xs, ys):
            body.append(f'<circle class="dot" cx="{p.X(x):.1f}" cy="{p.Y(y):.1f}" r="3.3"/>')
    body.append(f'<text class="t-mut" x="{3 * W + 2 * pad + 10}" y="{H + 18}" text-anchor="end">dashed = true function sin(2πx)</text>')
    return svg(3 * W + 2 * pad + 20, H + 26, "".join(body), "Underfitting, good fit and overfitting")


@fig("ml-bias-variance", "Expected test error = bias² + variance + irreducible noise. As the model gets more flexible, bias falls "
     "and variance rises; the best model sits at the bottom of the total-error curve.")
def bias_variance():
    c = np.linspace(0.9, 10, 200)
    bias2 = 2.6 / c
    var = 0.022 * c ** 1.9
    noise = np.full_like(c, 0.35)
    total = bias2 + var + noise
    p = Plot(60, 20, 520, 240, (0.9, 10), (0, 3.4))
    best = c[np.argmin(total)]
    body = [
        p.axes("model complexity (flexibility) →", "expected error"),
        p.path(c, bias2, "ink"),
        p.path(c, var, "hl"),
        p.path(c, noise, "mut"),
        p.path(c, total, "warn"),
        f'<line class="mut" x1="{p.X(best):.1f}" y1="{p.Y(0)}" x2="{p.X(best):.1f}" y2="{p.Y(total.min()) - 6:.1f}"/>',
        f'<circle class="dot-warn" cx="{p.X(best):.1f}" cy="{p.Y(total.min()):.1f}" r="4.5"/>',
        f'<text class="t-warn" x="{p.X(best):.1f}" y="{p.Y(total.min()) - 12:.1f}" text-anchor="middle">best trade-off</text>',
        f'<text class="t-ink" x="{p.X(1.6):.1f}" y="{p.Y(2.6 / 1.6) - 10:.1f}">bias²</text>',
        f'<text class="t-hl" x="{p.X(8.6):.1f}" y="{p.Y(0.022 * 8.6 ** 1.9) - 8:.1f}" text-anchor="end">variance</text>',
        f'<text class="t-mut" x="{p.X(9.9):.1f}" y="{p.Y(0.35) - 6:.1f}" text-anchor="end">noise σ² (irreducible)</text>',
        f'<text class="t-warn" x="{p.X(9.9):.1f}" y="{p.Y(total[-1]) + 16:.1f}" text-anchor="end">total test error</text>',
        f'<text class="t-mut" x="{p.X(0.7):.1f}" y="{p.Y(0) + 38:.1f}">← underfitting</text>',
        f'<text class="t-mut" x="{p.X(9.9):.1f}" y="{p.Y(0) + 38:.1f}" text-anchor="end">overfitting →</text>',
    ]
    return svg(600, 305, "".join(body), "Bias-variance trade-off curves")


@fig("ml-train-test-curve", "Training error keeps falling as complexity grows. Validation error falls, then rises again. "
     "The gap between the two curves is the signature of overfitting.")
def train_test():
    c = np.linspace(0.9, 10, 200)
    train = 2.4 / c + 0.05
    val = 2.6 / c + 0.022 * c ** 1.9 + 0.35
    p = Plot(60, 20, 520, 220, (0.9, 10), (0, 3.4))
    i = np.argmin(val)
    body = [
        p.axes("model complexity →", "error"),
        p.path(c, train, "ink"),
        p.path(c, val, "warn"),
        f'<line class="mut" x1="{p.X(c[i]):.1f}" y1="{p.Y(0)}" x2="{p.X(c[i]):.1f}" y2="{p.Y(3.3)}"/>',
        f'<text class="t-mut" x="{p.X(c[i]) + 6:.1f}" y="{p.Y(3.2):.1f}">stop here</text>',
        f'<text class="t-ink" x="{p.X(9.9):.1f}" y="{p.Y(train[-1]) - 8:.1f}" text-anchor="end">training error</text>',
        f'<text class="t-warn" x="{p.X(9.9):.1f}" y="{p.Y(val[-1]) + 16:.1f}" text-anchor="end">validation error</text>',
        f'<text class="t-mut" x="{p.X(1.0):.1f}" y="{p.Y(0) + 38:.1f}">both high: underfit</text>',
        f'<text class="t-mut" x="{p.X(9.9):.1f}" y="{p.Y(0) + 38:.1f}" text-anchor="end">train low, val high: overfit</text>',
    ]
    return svg(600, 285, "".join(body), "Training and validation error versus model complexity")


@fig("ml-kfold", "5-fold cross-validation. The data is split into 5 equal folds; each round trains on 4 and validates on the "
     "remaining one. The CV score is the average of the 5 validation scores. Leave-one-out is the extreme case k = n.")
def kfold():
    k = 5
    bw, bh, gap = 86, 30, 6
    x0, y0 = 92, 50
    body = [f'<text class="title" x="{x0}" y="16">data split into k = 5 folds</text>']
    for f in range(k):
        body.append(f'<text x="{x0 + f * (bw + gap) + bw / 2}" y="{y0 - 8}" text-anchor="middle" class="t-mut">fold {f + 1}</text>')
    for r in range(k):
        y = y0 + r * (bh + gap)
        body.append(f'<text x="{x0 - 10}" y="{y + bh / 2 + 4}" text-anchor="end">round {r + 1}</text>')
        for f in range(k):
            x = x0 + f * (bw + gap)
            val = f == r
            body.append(f'<rect class="{"box-ink" if val else "box"}" x="{x}" y="{y}" width="{bw}" height="{bh}" rx="5"/>')
            body.append(
                f'<text x="{x + bw / 2}" y="{y + bh / 2 + 4}" text-anchor="middle" class="{"on-ink" if val else "t-mut"}">'
                f'{"validate" if val else "train"}</text>'
            )
        body.append(f'<text x="{x0 + k * (bw + gap) + 4}" y="{y + bh / 2 + 4}" class="t-ink">→ score {r + 1}</text>')
    y = y0 + k * (bh + gap) + 18
    body.append(f'<text x="{x0}" y="{y}" class="title">CV score = (score 1 + … + score 5) / 5</text>')
    return svg(640, y + 10, "".join(body), "Five-fold cross-validation diagram")


# ---------------------------------------------------------------- linear regression


@fig("lr-residuals", "Least squares on the worked example: points (1,2), (2,4), (3,5), (4,4), (5,5). "
     "The fitted line is ŷ = 2.2 + 0.6x. Each dashed segment is a residual eᵢ = yᵢ − ŷᵢ; OLS chooses the line that "
     "makes the sum of their squares (RSS = 2.4) as small as possible. The line passes through (x̄, ȳ) = (3, 4).")
def lr_residuals():
    xs = np.array([1, 2, 3, 4, 5.0]); ys = np.array([2, 4, 5, 4, 5.0])
    b0, b1 = 2.2, 0.6
    p = Plot(60, 20, 460, 250, (0, 6), (0, 6.5))
    body = [p.axes("x", "y", xoff=32, yoff=30)]
    for t in range(1, 6):
        body.append(f'<text class="t-mut" x="{p.X(t):.1f}" y="{p.Y(0) + 14:.1f}" text-anchor="middle">{t}</text>')
        body.append(f'<text class="t-mut" x="{p.X(0) - 8:.1f}" y="{p.Y(t) + 4:.1f}" text-anchor="end">{t}</text>')
    gx = np.array([0.3, 5.7])
    body.append(p.path(gx, b0 + b1 * gx, "ink"))
    for x, y in zip(xs, ys):
        yh = b0 + b1 * x
        body.append(f'<line class="warn" style="stroke-width:1.6;stroke-dasharray:4 3" x1="{p.X(x):.1f}" y1="{p.Y(y):.1f}" x2="{p.X(x):.1f}" y2="{p.Y(yh):.1f}"/>')
        body.append(f'<text class="t-warn" x="{p.X(x) + 6:.1f}" y="{p.Y((y + yh) / 2) + 4:.1f}">{y - yh:+.1f}</text>')
        body.append(f'<circle class="dot" cx="{p.X(x):.1f}" cy="{p.Y(y):.1f}" r="4"/>')
    body.append(f'<circle class="dot-hl" cx="{p.X(3):.1f}" cy="{p.Y(4):.1f}" r="5"/>')
    body.append(f'<text class="t-hl" x="{p.X(3) - 8:.1f}" y="{p.Y(4) - 10:.1f}" text-anchor="end">(x̄, ȳ)</text>')
    body.append(f'<text class="t-ink" x="{p.X(5.6):.1f}" y="{p.Y(b0 + b1 * 5.6) - 10:.1f}" text-anchor="end">ŷ = 2.2 + 0.6x</text>')
    return svg(540, 310, "".join(body), "Least squares line with residuals")


@fig("lr-gd-steps", "Gradient descent on L(w) = w², starting at w = 1. With η = 0.25 each step multiplies w by (1 − 2η) = 0.5 and "
     "slides smoothly to the minimum. With η = 0.95 the factor is −0.9: w flips sign every step and barely shrinks; "
     "any η > 1 would make it diverge.")
def gd_steps():
    body = []
    for k, (eta, title, cls) in enumerate([(0.25, "η = 0.25 (good)", "ink"), (0.95, "η = 0.95 (too large)", "warn")]):
        ox = 10 + k * 300
        p = Plot(ox + 30, 34, 250, 190, (-1.15, 1.15), (0, 1.35))
        g = np.linspace(-1.1, 1.1, 120)
        body.append(f'<text class="title" x="{ox + 155}" y="18" text-anchor="middle">{title}</text>')
        body.append(p.axes("", ""))
        body.append(f'<text x="{p.X(1.12):.1f}" y="{p.Y(0) + 14:.1f}" text-anchor="end">w</text>')
        body.append(p.path(g, g ** 2, "mut"))
        w = 1.0
        pts = [w]
        for _ in range(6):
            w = w - eta * 2 * w
            pts.append(w)
        for a, b in zip(pts, pts[1:]):
            body.append(f'<line class="{cls}" style="stroke-width:1.6" x1="{p.X(a):.1f}" y1="{p.Y(a * a):.1f}" x2="{p.X(b):.1f}" y2="{p.Y(b * b):.1f}"/>')
        for i, a in enumerate(pts):
            body.append(f'<circle class="{"dot-ink" if cls == "ink" else "dot-warn"}" cx="{p.X(a):.1f}" cy="{p.Y(a * a):.1f}" r="{4.2 if i == 0 else 3.2}"/>')
        body.append(f'<text class="t-mut" x="{p.X(1):.1f}" y="{p.Y(1) - 8:.1f}" text-anchor="middle">start</text>')
        body.append(f'<text class="t-mut" x="{p.X(0):.1f}" y="{p.Y(0) + 14:.1f}" text-anchor="middle">0</text>')
    return svg(610, 260, "".join(body), "Gradient descent with small and large learning rate")


# ---------------------------------------------------------------- ridge & lasso


def _ellipse(c, A, level, n=160):
    L = np.linalg.cholesky(A)
    t = np.linspace(0, 2 * np.pi, n)
    z = np.sqrt(level) * np.stack([np.cos(t), np.sin(t)])
    w = np.linalg.solve(L.T, z)
    return c[0] + w[0], c[1] + w[1]


@fig("reg-geometry", "Why lasso gives exact zeros. Contours of the RSS (ellipses) grow outward from the OLS solution ★ until they "
     "first touch the constraint region. The L2 ball (ridge) is round, so it is touched at a generic point with both "
     "weights non-zero, about (0.9, 0.4). The L1 ball (lasso) has corners on the axes, and the ellipse touches a corner: (1, 0), "
     "so w₂ is exactly 0.")
def reg_geometry():
    c = np.array([2.0, 0.5]); A = np.array([[1, 0.4], [0.4, 1.2]])
    body = []
    panels = [("Ridge · ‖w‖₂ ≤ 1", "circle", 1.271, (0.905, 0.425), "≈ (0.9, 0.4)"), ("Lasso · ‖w‖₁ ≤ 1", "diamond", 1.7, (1.0, 0.0), "(1, 0)")]
    for k, (title, shape, lvl, sol, lab) in enumerate(panels):
        ox = 10 + k * 305
        p = Plot(ox + 20, 30, 270, 230, (-1.5, 3.1), (-1.5, 2.4))
        body.append(f'<rect class="grid" x="{p.X(-1.5):.1f}" y="{p.Y(2.4):.1f}" width="{p.w:.1f}" height="{p.h:.1f}" rx="6"/>')
        body.append(f'<text class="title" x="{ox + 155}" y="16" text-anchor="middle">{title}</text>')
        body.append(f'<line class="ax" x1="{p.X(-1.5):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(3.1):.1f}" y2="{p.Y(0):.1f}"/>')
        body.append(f'<line class="ax" x1="{p.X(0):.1f}" y1="{p.Y(-1.5):.1f}" x2="{p.X(0):.1f}" y2="{p.Y(2.4):.1f}"/>')
        body.append(f'<text class="t-mut" x="{p.X(3.05):.1f}" y="{p.Y(0) + 14:.1f}" text-anchor="end">w₁</text>')
        body.append(f'<text class="t-mut" x="{p.X(0) + 6:.1f}" y="{p.Y(2.3):.1f}">w₂</text>')
        if shape == "circle":
            body.append(f'<circle class="ink" style="fill:var(--gd-ink);fill-opacity:.14" cx="{p.X(0):.1f}" cy="{p.Y(0):.1f}" r="{p.X(1) - p.X(0):.1f}"/>')
        else:
            pts = " ".join(f"{p.X(a):.1f},{p.Y(b):.1f}" for a, b in [(1, 0), (0, 1), (-1, 0), (0, -1)])
            body.append(f'<polygon class="ink" style="fill:var(--gd-ink);fill-opacity:.14" points="{pts}"/>')
        cid = f"rgclip{k}"
        body.append(f'<clipPath id="{cid}"><rect x="{p.X(-1.5):.1f}" y="{p.Y(2.4):.1f}" width="{p.w:.1f}" height="{p.h:.1f}"/></clipPath>')
        body.append(f'<g clip-path="url(#{cid})">')
        for f in (lvl, lvl * 2.0):
            ex, ey = _ellipse(c, A, f)
            body.append(p.path(ex, ey, "hl" if f == lvl else "mut"))
        body.append('</g>')
        body.append(f'<text class="t-hl" x="{p.X(c[0]) + 6:.1f}" y="{p.Y(c[1]) - 6:.1f}">★ OLS</text>')
        body.append(f'<circle class="dot-hl" cx="{p.X(c[0]):.1f}" cy="{p.Y(c[1]):.1f}" r="3.5"/>')
        body.append(f'<circle class="dot-warn" cx="{p.X(sol[0]):.1f}" cy="{p.Y(sol[1]):.1f}" r="5"/>')
        if sol[1] == 0:
            body.append(f'<text class="t-warn" x="{p.X(sol[0]) + 4:.1f}" y="{p.Y(sol[1]) + 20:.1f}" text-anchor="start">{lab}</text>')
        else:
            body.append(f'<text class="t-warn" x="{p.X(sol[0]) - 8:.1f}" y="{p.Y(sol[1]) - 10:.1f}" text-anchor="end">{lab}</text>')
    return svg(620, 270, "".join(body), "Ridge and lasso constraint geometry")


@fig("reg-paths", "Coefficient paths on the same standardised data (true weights 3, −2, 0.8, 0) as λ grows. "
     "Ridge shrinks every weight smoothly towards 0 but none reaches it. Lasso drives weights to exactly 0 one by one; "
     "by λ = 400 only one feature is left.")
def reg_paths():
    rng = np.random.default_rng(3); n, pdim = 60, 4
    X = rng.normal(size=(n, pdim)); X = (X - X.mean(0)) / X.std(0)
    y = X @ np.array([3, -2, 0.8, 0]) + rng.normal(0, 1, n); y = y - y.mean()

    def ridge(l):
        return np.linalg.solve(X.T @ X + l * np.eye(pdim), X.T @ y)

    def lasso(l):
        w = np.zeros(pdim)
        for _ in range(300):
            for j in range(pdim):
                r = y - X @ w + X[:, j] * w[j]; rho = X[:, j] @ r
                w[j] = np.sign(rho) * max(abs(rho) - l / 2, 0) / (X[:, j] @ X[:, j])
        return w

    lams = np.logspace(-1, 3, 70)
    body = []
    cls = ["ink", "warn", "hl", "mut"]
    for k, (title, fn) in enumerate([("Ridge (L2)", ridge), ("Lasso (L1)", lasso)]):
        ox = 10 + k * 305
        p = Plot(ox + 34, 30, 255, 190, (-1, 3), (-2.2, 3.3))
        W = np.array([fn(l) for l in lams])
        body.append(f'<text class="title" x="{ox + 160}" y="16" text-anchor="middle">{title}</text>')
        body.append(p.axes("log₁₀ λ →", "weight", xoff=30, yoff=26))
        body.append(f'<line class="grid" x1="{p.X(-1):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(3):.1f}" y2="{p.Y(0):.1f}"/>')
        for t in (-1, 0, 1, 2, 3):
            body.append(f'<text class="t-mut" x="{p.X(t):.1f}" y="{p.Y(-2.2) + 14:.1f}" text-anchor="middle">{t}</text>')
        for j in range(pdim):
            body.append(p.path(np.log10(lams), W[:, j], cls[j]))
        for j, lab in enumerate(["w₁", "w₂", "w₃", "w₄"]):
            body.append(f'<text class="t-mut" x="{p.X(-1) + 4:.1f}" y="{p.Y(W[0, j]) - 5:.1f}">{lab}</text>')
    return svg(620, 262, "".join(body), "Ridge and lasso coefficient paths")


# ---------------------------------------------------------------- logistic & linear classifiers


@fig("logit-sigmoid", "The sigmoid σ(z) = 1/(1 + e^(−z)) squashes any real score into (0, 1). σ(0) = 0.5 is the decision threshold. "
     "Its derivative σ'(z) = σ(z)(1 − σ(z)) peaks at 0.25 when z = 0; at σ = 0.4 it is 0.4 × 0.6 = 0.24 (2024 Q33).")
def logit_sigmoid():
    z = np.linspace(-7, 7, 300)
    sg = 1 / (1 + np.exp(-z))
    p = Plot(60, 20, 500, 220, (-7, 7), (0, 1.05))
    body = [p.axes("z = wᵀx + b", "", xoff=30)]
    for t in (-6, -4, -2, 0, 2, 4, 6):
        body.append(f'<text class="t-mut" x="{p.X(t):.1f}" y="{p.Y(0) + 14:.1f}" text-anchor="middle">{t}</text>')
    for v in (0.25, 0.5, 1.0):
        body.append(f'<line class="grid" x1="{p.X(-7):.1f}" y1="{p.Y(v):.1f}" x2="{p.X(7):.1f}" y2="{p.Y(v):.1f}"/>')
        body.append(f'<text class="t-mut" x="{p.X(-7) - 6:.1f}" y="{p.Y(v) + 4:.1f}" text-anchor="end">{v:g}</text>')
    body.append(p.path(z, sg, "ink"))
    body.append(p.path(z, sg * (1 - sg), "hl"))
    zz = np.log(0.4 / 0.6)
    body.append(f'<circle class="dot-warn" cx="{p.X(zz):.1f}" cy="{p.Y(0.4):.1f}" r="4"/>')
    body.append(f'<circle class="dot-warn" cx="{p.X(zz):.1f}" cy="{p.Y(0.24):.1f}" r="4"/>')
    body.append(f'<line class="mut" x1="{p.X(zz):.1f}" y1="{p.Y(0.4):.1f}" x2="{p.X(zz):.1f}" y2="{p.Y(0.24):.1f}"/>')
    body.append(f'<text class="t-warn" x="{p.X(zz) - 8:.1f}" y="{p.Y(0.4) - 6:.1f}" text-anchor="end">σ = 0.4</text>')
    body.append(f'<text class="t-warn" x="{p.X(zz) - 10:.1f}" y="{p.Y(0.24) - 4:.1f}" text-anchor="end">σ′ = 0.24</text>')
    body.append(f'<text class="t-ink" x="{p.X(4.2):.1f}" y="{p.Y(1 / (1 + np.exp(-4.2))) + 18:.1f}">σ(z)</text>')
    body.append(f'<text class="t-hl" x="{p.X(1.2):.1f}" y="{p.Y(0.25) - 8:.1f}">σ′(z), max 0.25</text>')
    return svg(580, 285, "".join(body), "Sigmoid and its derivative")


@fig("linsep-q53", "The four datasets of GATE DA 2024 Q53, redrawn (● circles, ■ squares). A dashed line separates the classes in "
     "(i) and (iv). In (ii) a circle is surrounded by squares, and (iii) is the XOR pattern: no single straight line works.")
def linsep():
    sets = {
        "(i) separable": ([(1, 3), (2, 3), (1, 2)], [(2, 1), (3, 1), (2, 0)], ((0.3, 0.6), (3.6, 2.6))),
        "(ii) not separable": ([(2, 2)], [(2, 3), (1, 2), (3, 2), (2, 1)], None),
        "(iii) not separable (XOR)": ([(3, 3), (1, 1)], [(1, 3), (3, 1)], None),
        "(iv) separable": ([(2, 0.1), (3, 1.5), (3, 0.2)], [(1, 2.3), (2, 2.6), (1, 1.2)], ((0.6, 0.0), (3.6, 2.9))),
    }
    body = []
    for k, (title, (circ, sq, line)) in enumerate(sets.items()):
        ox = 10 + (k % 2) * 300; oy = 10 + (k // 2) * 185
        p = Plot(ox + 30, oy + 26, 230, 130, (0, 3.8), (-0.3, 3.6))
        body.append(f'<text class="title" x="{ox + 145}" y="{oy + 12}" text-anchor="middle">{title}</text>')
        body.append(p.axes())
        for t in (1, 2, 3):
            body.append(f'<line class="grid" x1="{p.X(t):.1f}" y1="{p.Y(-0.3):.1f}" x2="{p.X(t):.1f}" y2="{p.Y(3.6):.1f}"/>')
            body.append(f'<line class="grid" x1="{p.X(0):.1f}" y1="{p.Y(t):.1f}" x2="{p.X(3.8):.1f}" y2="{p.Y(t):.1f}"/>')
        if line:
            (a, b), (c, d) = line
            body.append(f'<line class="mut" style="stroke:var(--gd-ink)" x1="{p.X(a):.1f}" y1="{p.Y(b):.1f}" x2="{p.X(c):.1f}" y2="{p.Y(d):.1f}"/>')
        for x, y in circ:
            body.append(f'<circle class="dot" cx="{p.X(x):.1f}" cy="{p.Y(y):.1f}" r="6"/>')
        for x, y in sq:
            body.append(f'<rect class="dot-warn" x="{p.X(x) - 6:.1f}" y="{p.Y(y) - 6:.1f}" width="12" height="12"/>')
    return svg(610, 380, "".join(body), "Linear separability of four datasets")


@fig("linear-boundary", "A linear classifier f(x) = wᵀx + b. The boundary f(x) = 0 is a line (a hyperplane in higher dimensions); "
     "w is perpendicular to it and points towards the positive side. The distance of a point from the boundary is |f(x)| / ‖w‖.")
def linear_boundary():
    p = Plot(40, 20, 420, 260, (-0.5, 5), (-0.5, 4))
    w = np.array([3, 4.0]); b = -10
    body = [p.axes("x₁", "x₂", xoff=30, yoff=24)]
    A, B = (-0.5, 2.875), (4.0, -0.5)
    poly = [A, B, (5, -0.5), (5, 4), (-0.5, 4)]
    body.append('<polygon style="fill:var(--gd-ink);fill-opacity:.08" points="' + " ".join(f"{p.X(a):.1f},{p.Y(c):.1f}" for a, c in poly) + '"/>')
    body.append(f'<line class="ink" x1="{p.X(A[0]):.1f}" y1="{p.Y(A[1]):.1f}" x2="{p.X(B[0]):.1f}" y2="{p.Y(B[1]):.1f}"/>')
    foot = np.array([1.2, (-b - 3 * 1.2) / 4])
    tip = foot + 0.9 * w / np.linalg.norm(w)
    body.append(f'<line class="hl" x1="{p.X(foot[0]):.1f}" y1="{p.Y(foot[1]):.1f}" x2="{p.X(tip[0]):.1f}" y2="{p.Y(tip[1]):.1f}"/>')
    body.append(f'<circle class="dot-hl" cx="{p.X(tip[0]):.1f}" cy="{p.Y(tip[1]):.1f}" r="4"/>')
    body.append(f'<text class="t-hl" x="{p.X(tip[0]) + 8:.1f}" y="{p.Y(tip[1]):.1f}">w</text>')
    pt = np.array([3.5, 2.5]); fval = w @ pt + b; proj = pt - fval / (w @ w) * w
    body.append(f'<line class="mut" style="stroke:var(--gd-trap)" x1="{p.X(pt[0]):.1f}" y1="{p.Y(pt[1]):.1f}" x2="{p.X(proj[0]):.1f}" y2="{p.Y(proj[1]):.1f}"/>')
    body.append(f'<circle class="dot" cx="{p.X(pt[0]):.1f}" cy="{p.Y(pt[1]):.1f}" r="5"/>')
    body.append(f'<text class="t-warn" x="{p.X(pt[0]):.1f}" y="{p.Y(pt[1]) - 12:.1f}" text-anchor="middle">x · distance |f(x)|/‖w‖</text>')
    body.append(f'<text class="t-ink" x="{p.X(0.2):.1f}" y="{p.Y(3.6):.1f}">f(x) &gt; 0 → class +1</text>')
    body.append(f'<text class="t-mut" x="{p.X(-0.3):.1f}" y="{p.Y(-0.25):.1f}">f(x) &lt; 0 → class −1</text>')
    body.append(f'<text class="t-ink" x="{p.X(1.9):.1f}" y="{p.Y(0.1):.1f}" text-anchor="start">wᵀx + b = 0</text>')
    return svg(500, 320, "".join(body), "Linear decision boundary with normal vector")


# ---------------------------------------------------------------- evaluation metrics


@fig("cm-layout", "The confusion matrix for a binary problem. Rows are the truth, columns the prediction. Precision reads down "
     "the 'predicted positive' column; recall reads across the 'actually positive' row.")
def cm_layout():
    x0, y0, cw, ch = 150, 60, 180, 70
    cells = [("TP", "true positive", "box-ink", "on-ink"), ("FN", "false negative (missed)", "box", ""),
             ("FP", "false positive (false alarm)", "box", ""), ("TN", "true negative", "box", "")]
    body = [f'<text class="title" x="{x0 + cw}" y="22" text-anchor="middle">predicted</text>',
            f'<text class="t-mut" x="{x0 + cw / 2}" y="{y0 - 10}" text-anchor="middle">positive</text>',
            f'<text class="t-mut" x="{x0 + 1.5 * cw}" y="{y0 - 10}" text-anchor="middle">negative</text>',
            f'<text class="title" x="40" y="{y0 + ch}" text-anchor="middle" transform="rotate(-90 40 {y0 + ch})">actual</text>',
            f'<text class="t-mut" x="{x0 - 10}" y="{y0 + ch / 2 + 4}" text-anchor="end">positive</text>',
            f'<text class="t-mut" x="{x0 - 10}" y="{y0 + 1.5 * ch + 4}" text-anchor="end">negative</text>']
    for i, (abbr, desc, cls, tcls) in enumerate(cells):
        r, c = divmod(i, 2)
        x = x0 + c * cw; y = y0 + r * ch
        body.append(f'<rect class="{cls}" x="{x + 3}" y="{y + 3}" width="{cw - 6}" height="{ch - 6}" rx="6"/>')
        body.append(f'<text class="{tcls or "title"}" x="{x + cw / 2}" y="{y + 30}" text-anchor="middle" style="font-size:16px;font-weight:700">{abbr}</text>')
        body.append(f'<text class="{tcls or "t-mut"}" x="{x + cw / 2}" y="{y + 50}" text-anchor="middle">{desc}</text>')
    body.append(f'<rect x="{x0 - 2}" y="{y0 - 2}" width="{cw + 4}" height="{2 * ch + 4}" rx="8" class="hl" style="fill:none;stroke-width:2"/>')
    body.append(f'<text class="t-hl" x="{x0 + cw / 2}" y="{y0 + 2 * ch + 22}" text-anchor="middle">precision = TP/(TP+FP)</text>')
    body.append(f'<rect x="{x0 - 2}" y="{y0 - 2}" width="{2 * cw + 4}" height="{ch + 4}" rx="8" class="warn" style="fill:none;stroke-width:2;stroke-dasharray:6 4"/>')
    body.append(f'<text class="t-warn" x="{x0 + 2 * cw + 12}" y="{y0 + ch / 2 + 4}">recall = TP/(TP+FN)</text>')
    return svg(700, y0 + 2 * ch + 34, "".join(body), "Confusion matrix layout")


@fig("roc-example", "ROC curve for 3 positives scored 0.9, 0.7, 0.4 and 4 negatives scored 0.8, 0.3, 0.2, 0.1. Lowering the threshold "
     "past each score moves up (a positive) or right (a negative). The shaded area is AUC = 10/12 ≈ 0.833; "
     "the dashed diagonal is a random classifier (AUC = 0.5).")
def roc_example():
    pts = [(0, 0), (0, 1 / 3), (0.25, 1 / 3), (0.25, 2 / 3), (0.25, 1), (0.5, 1), (0.75, 1), (1, 1)]
    p = Plot(70, 20, 300, 260, (0, 1), (0, 1))
    body = [p.axes("false positive rate (1 − specificity)", "true positive rate (recall)", xoff=34, yoff=40)]
    for t in (0, 0.25, 0.5, 0.75, 1):
        body.append(f'<text class="t-mut" x="{p.X(t):.1f}" y="{p.Y(0) + 15:.1f}" text-anchor="middle">{t:g}</text>')
    for t in (0, 1 / 3, 2 / 3, 1):
        body.append(f'<text class="t-mut" x="{p.X(0) - 6:.1f}" y="{p.Y(t) + 4:.1f}" text-anchor="end">{t:.2f}</text>')
    poly = pts + [(1, 0)]
    body.append('<polygon style="fill:var(--gd-ink);fill-opacity:.14" points="' + " ".join(f"{p.X(a):.1f},{p.Y(b):.1f}" for a, b in poly) + '"/>')
    body.append(f'<line class="mut" x1="{p.X(0):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(1):.1f}" y2="{p.Y(1):.1f}"/>')
    body.append(p.path([a for a, _ in pts], [b for _, b in pts], "ink"))
    labels = ["0.9 (+)", "0.8 (−)", "0.7 (+)", "0.4 (+)", "0.3 (−)", "0.2 (−)", "0.1 (−)"]
    for (a, b), lab in zip(pts[1:], labels):
        body.append(f'<circle class="dot-ink" cx="{p.X(a):.1f}" cy="{p.Y(b):.1f}" r="3.5"/>')
    body.append(f'<text class="t-ink" x="{p.X(0.55):.1f}" y="{p.Y(0.45):.1f}">AUC = 0.833</text>')
    body.append(f'<text class="t-mut" x="{p.X(0.62):.1f}" y="{p.Y(0.66):.1f}">random (0.5)</text>')
    body.append(f'<text class="t-mut" x="{p.X(1) + 18:.1f}" y="{p.Y(1) + 4:.1f}">threshold steps:</text>')
    for i, lab in enumerate(labels):
        body.append(f'<text class="{"t-ink" if "+" in lab else "t-mut"}" x="{p.X(1) + 18:.1f}" y="{p.Y(1) + 22 + i * 17:.1f}">{lab} → {"up" if "+" in lab else "right"}</text>')
    return svg(560, 320, "".join(body), "ROC curve of a worked example")


# ---------------------------------------------------------------- k-NN


@fig("knn-q63", "GATE DA 2024 Q63 redrawn. Query ◇ at (2, 1); circles at (1, 1), (1, 2); squares at (2, 3), (3, 3), (3, 2). "
     "Rings show the k = 1, 3, 5 neighbourhoods. Votes: k = 1 → 1 circle; k = 3 → 2 circles, 1 square; k = 5 → 2 circles, "
     "3 squares. The smallest odd k that gives 'square' is 5.")
def knn_q63():
    p = Plot(50, 20, 300, 260, (0, 4), (0, 4))
    q = (2, 1)
    body = [p.axes("", "")]
    for t in (1, 2, 3):
        body.append(f'<line class="grid" x1="{p.X(t):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(t):.1f}" y2="{p.Y(4):.1f}"/>')
        body.append(f'<line class="grid" x1="{p.X(0):.1f}" y1="{p.Y(t):.1f}" x2="{p.X(4):.1f}" y2="{p.Y(t):.1f}"/>')
        body.append(f'<text class="t-mut" x="{p.X(t):.1f}" y="{p.Y(0) + 14:.1f}" text-anchor="middle">{t}</text>')
        body.append(f'<text class="t-mut" x="{p.X(0) - 8:.1f}" y="{p.Y(t) + 4:.1f}" text-anchor="end">{t}</text>')
    unit = p.X(1) - p.X(0)
    body.append(f'<clipPath id="knnclip"><rect x="{p.x0}" y="{p.y0}" width="{p.w}" height="{p.h}"/></clipPath><g clip-path="url(#knnclip)">')
    for r, k, cls in [(1.0, 1, "ink"), (2 ** 0.5, 3, "hl"), (5 ** 0.5, 5, "warn")]:
        body.append(f'<circle class="{cls}" style="fill:none;stroke-dasharray:5 4;stroke-width:1.6" cx="{p.X(q[0]):.1f}" cy="{p.Y(q[1]):.1f}" r="{r * unit + 4:.1f}"/>')
    body.append('</g>')
    for x, y in [(1, 1), (1, 2)]:
        body.append(f'<circle class="dot" cx="{p.X(x):.1f}" cy="{p.Y(y):.1f}" r="8"/>')
    for x, y in [(2, 3), (3, 3), (3, 2)]:
        body.append(f'<rect class="dot-warn" x="{p.X(x) - 8:.1f}" y="{p.Y(y) - 8:.1f}" width="16" height="16"/>')
    cx, cy = p.X(q[0]), p.Y(q[1])
    body.append(f'<polygon class="dot-hl" points="{cx},{cy - 9} {cx + 9},{cy} {cx},{cy + 9} {cx - 9},{cy}"/>')
    rows = [("k = 1", "radius 1", "1 ● : 0 ■ → ●", "t-ink"), ("k = 3", "radius √2", "2 ● : 1 ■ → ●", "t-hl"), ("k = 5", "radius √5", "2 ● : 3 ■ → ■", "t-warn")]
    for i, (k, r, v, c) in enumerate(rows):
        y = 70 + i * 52
        body.append(f'<text class="{c}" x="380" y="{y}" style="font-weight:600">{k}</text>')
        body.append(f'<text class="t-mut" x="380" y="{y + 16}">{r}</text>')
        body.append(f'<text x="380" y="{y + 32}">{v}</text>')
    return svg(560, 310, "".join(body), "k-nearest neighbours on the 2024 Q63 dataset")


@fig("knn-k-effect", "The same 60 noisy training points classified by 1-NN and 15-NN. With k = 1 every point gets its own island, "
     "so the boundary is jagged (low bias, high variance; training error is 0). With k = 15 the boundary is smooth "
     "(higher bias, lower variance).")
def knn_k_effect():
    rng = np.random.default_rng(11)
    n = 60
    X = rng.uniform(0, 1, (n, 2))
    y = (X[:, 1] > 0.5 + 0.25 * np.sin(2 * np.pi * X[:, 0])).astype(int)
    flip = rng.random(n) < 0.12
    y[flip] = 1 - y[flip]
    body = []
    G = 34
    for k_i, k in enumerate((1, 15)):
        ox = 10 + k_i * 300
        p = Plot(ox + 10, 30, 270, 220, (0, 1), (0, 1))
        body.append(f'<text class="title" x="{ox + 145}" y="18" text-anchor="middle">{k}-NN</text>')
        cw = p.w / G; chh = p.h / G
        for i in range(G):
            for j in range(G):
                cx = (i + 0.5) / G; cy = (j + 0.5) / G
                d = np.hypot(X[:, 0] - cx, X[:, 1] - cy)
                lab = int(y[np.argsort(d)[:k]].mean() > 0.5)
                col = "var(--gd-ink)" if lab else "var(--gd-trap)"
                body.append(f'<rect x="{p.X(i / G):.1f}" y="{p.Y((j + 1) / G):.1f}" width="{cw + 0.3:.1f}" height="{chh + 0.3:.1f}" style="fill:{col};fill-opacity:.16"/>')
        for (a, b), lab in zip(X, y):
            if lab:
                body.append(f'<circle class="dot-ink" cx="{p.X(a):.1f}" cy="{p.Y(b):.1f}" r="3.6"/>')
            else:
                body.append(f'<rect class="dot-warn" x="{p.X(a) - 3.4:.1f}" y="{p.Y(b) - 3.4:.1f}" width="6.8" height="6.8"/>')
        body.append(f'<rect class="grid" x="{p.x0}" y="{p.y0}" width="{p.w}" height="{p.h}"/>')
    return svg(610, 262, "".join(body), "Decision regions of 1-NN and 15-NN")


# ---------------------------------------------------------------- LDA


@fig("lda-projection", "Two elongated classes. Projecting onto the line joining the means (yellow) mixes the classes because "
     "it ignores their shape; the Fisher direction u ∝ S_W⁻¹(μ₁ − μ₂) (blue) tilts away from the long axis of the clouds, "
     "so the projected classes barely overlap. Right: the 1-D projections on each direction.")
def lda_projection():
    rng = np.random.default_rng(5)
    C = np.array([[2.2, 1.9], [1.9, 2.0]])
    L = np.linalg.cholesky(C)
    A = rng.normal(size=(40, 2)) @ L.T + np.array([0, 0.0])
    B = rng.normal(size=(40, 2)) @ L.T + np.array([1.6, -0.6])
    mA, mB = A.mean(0), B.mean(0)
    SW = (A - mA).T @ (A - mA) + (B - mB).T @ (B - mB)
    d = mB - mA
    u = np.linalg.solve(SW, d); u /= np.linalg.norm(u)
    m = d / np.linalg.norm(d)
    p = Plot(30, 20, 300, 250, (-4.5, 5.5), (-4.5, 4.5))
    body = [f'<rect class="grid" x="{p.x0}" y="{p.y0}" width="{p.w}" height="{p.h}" rx="6"/>']
    c = (mA + mB) / 2
    for vec, cls in ((m, "hl"), (u, "ink")):
        a, b = c - 4 * vec, c + 4 * vec
        body.append(f'<line class="{cls}" x1="{p.X(a[0]):.1f}" y1="{p.Y(a[1]):.1f}" x2="{p.X(b[0]):.1f}" y2="{p.Y(b[1]):.1f}"/>')
    for x, y in A:
        body.append(f'<circle class="dot" cx="{p.X(x):.1f}" cy="{p.Y(y):.1f}" r="3.2"/>')
    for x, y in B:
        body.append(f'<rect class="dot-warn" x="{p.X(x) - 3:.1f}" y="{p.Y(y) - 3:.1f}" width="6" height="6"/>')
    body.append(f'<text class="t-hl" x="{p.X(c[0] - 4 * m[0]):.1f}" y="{p.Y(c[1] - 4 * m[1]) - 8:.1f}" text-anchor="start">μ₂ − μ₁</text>')
    body.append(f'<text class="t-ink" x="{p.X(c[0] + 3.6 * u[0]) + 4:.1f}" y="{p.Y(c[1] + 3.6 * u[1]):.1f}">Fisher u</text>')
    # 1-D projections
    for k, (vec, cls, title) in enumerate(((m, "hl", "projected on μ₂ − μ₁: overlap"), (u, "ink", "projected on Fisher u: separated"))):
        y0 = 70 + k * 110
        pa, pb = A @ vec, B @ vec
        lo, hi = min(pa.min(), pb.min()), max(pa.max(), pb.max())
        X = lambda v: 360 + (v - lo) / (hi - lo) * 240
        body.append(f'<text class="title" x="360" y="{y0 - 20}">{title}</text>')
        body.append(f'<line class="{cls}" x1="360" y1="{y0}" x2="600" y2="{y0}"/>')
        for v in pa:
            body.append(f'<circle class="dot" cx="{X(v):.1f}" cy="{y0 - 8:.1f}" r="2.8" style="opacity:.8"/>')
        for v in pb:
            body.append(f'<rect class="dot-warn" x="{X(v) - 2.6:.1f}" y="{y0 + 5:.1f}" width="5.2" height="5.2" style="opacity:.85"/>')
    return svg(620, 290, "".join(body), "LDA projection direction compared with the mean-difference direction")


# ---------------------------------------------------------------- SVM


@fig("svm-margin", "Hard-margin SVM on the 2025 Q53 data: class 1 at (2,0), (0,2), (2,2), class 2 at (0,0). The solution is "
     "w = (1, 1), b = −1, so the boundary is x₁ + x₂ = 1 and the margin lines are x₁ + x₂ = 0 and x₁ + x₂ = 2. "
     "The three ringed points touch the margin: they are the support vectors. Margin width = 2/‖w‖ = √2.")
def svm_margin():
    p = Plot(50, 20, 300, 260, (-0.8, 2.8), (-0.8, 2.8))
    body = [f'<clipPath id="svmclip"><rect x="{p.x0}" y="{p.y0}" width="{p.w}" height="{p.h}"/></clipPath>']
    body.append(p.axes("x₁", "x₂", xoff=30, yoff=26))
    for t in (0, 1, 2):
        body.append(f'<text class="t-mut" x="{p.X(t):.1f}" y="{p.Y(-0.8) + 14:.1f}" text-anchor="middle">{t}</text>')
        body.append(f'<text class="t-mut" x="{p.X(-0.8) - 6:.1f}" y="{p.Y(t) + 4:.1f}" text-anchor="end">{t}</text>')
    body.append('<g clip-path="url(#svmclip)">')
    band = [(-0.8, 0.8), (0.8, -0.8), (2.8, -0.8), (-0.8, 2.8)]
    body.append('<polygon style="fill:var(--gd-hl-strong);fill-opacity:.12" points="' + " ".join(f"{p.X(a):.1f},{p.Y(b):.1f}" for a, b in [(-0.8, 0.8), (0.8, -0.8), (2.8, -0.8), (2.8, -0.8), (-0.8, 2.8)][:2] + [(2.8, -0.8), (-0.8, 2.8)]) + '"/>')
    for c, cls in ((1, "ink"), (0, "mut"), (2, "mut")):
        a, b = (-0.8, c + 0.8), (c + 0.8, -0.8)
        body.append(f'<line class="{cls}" x1="{p.X(a[0]):.1f}" y1="{p.Y(a[1]):.1f}" x2="{p.X(b[0]):.1f}" y2="{p.Y(b[1]):.1f}"/>')
    body.append('</g>')
    body.append(f'<line class="hl" x1="{p.X(0):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(1):.1f}" y2="{p.Y(1):.1f}" style="stroke-width:1.8"/>')
    body.append(f'<text class="t-hl" x="{p.X(0.62):.1f}" y="{p.Y(0.42):.1f}">√2</text>')
    for x, y in [(2, 0), (0, 2), (2, 2)]:
        body.append(f'<circle class="dot-ink" cx="{p.X(x):.1f}" cy="{p.Y(y):.1f}" r="6"/>')
    body.append(f'<rect class="dot-warn" x="{p.X(0) - 6:.1f}" y="{p.Y(0) - 6:.1f}" width="12" height="12"/>')
    for x, y in [(2, 0), (0, 2), (0, 0)]:
        body.append(f'<circle class="warn" style="fill:none;stroke-width:1.6" cx="{p.X(x):.1f}" cy="{p.Y(y):.1f}" r="11"/>')
    body.append(f'<text class="t-ink" x="{p.X(1.55):.1f}" y="{p.Y(-0.45):.1f}">x₁+x₂ = 1</text>')
    lines = [("boundary", "wᵀx + b = 0", "t-ink"), ("margin lines", "wᵀx + b = ±1", "t-mut"),
             ("support vectors", "ringed: y(wᵀx+b) = 1", "t-warn"), ("width", "2/‖w‖ = 2/√2 = √2", "t-hl"),
             ("(2,2)", "y f(x) = 3 > 1: not a SV", "t-mut")]
    for i, (a, b, c) in enumerate(lines):
        body.append(f'<text class="{c}" x="380" y="{60 + i * 44}" style="font-weight:600">{a}</text>')
        body.append(f'<text x="380" y="{78 + i * 44}">{b}</text>')
    return svg(600, 320, "".join(body), "Maximum-margin separator with support vectors")


@fig("svm-losses", "Losses as a function of the margin y·f(x). The 0–1 loss counts mistakes. The hinge loss max(0, 1 − yf) "
     "(SVM) is zero once a point is beyond the margin (yf ≥ 1) and grows linearly otherwise. The logistic loss "
     "log₂(1 + e^(−yf)) never reaches exactly zero.")
def svm_losses():
    m = np.linspace(-2.5, 3, 300)
    p = Plot(60, 20, 480, 220, (-2.5, 3), (0, 3.6))
    body = [p.axes("margin  y · f(x)", "loss", xoff=32, yoff=30)]
    for t in (-2, -1, 0, 1, 2, 3):
        body.append(f'<text class="t-mut" x="{p.X(t):.1f}" y="{p.Y(0) + 15:.1f}" text-anchor="middle">{t}</text>')
    body.append(f'<line class="grid" x1="{p.X(1):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(1):.1f}" y2="{p.Y(3.6):.1f}"/>')
    zo = np.where(m < 0, 1.0, 0.0)
    body.append(p.path(m[m < 0], zo[m < 0], "mut"))
    body.append(p.path(m[m >= 0], zo[m >= 0], "mut"))
    body.append(p.path(m, np.maximum(0, 1 - m), "ink"))
    body.append(p.path(m, np.log2(1 + np.exp(-m)), "hl"))
    body.append(f'<text class="t-ink" x="{p.X(-1.0) - 6:.1f}" y="{p.Y(2.0) + 18:.1f}" text-anchor="end">hinge</text>')
    body.append(f'<text class="t-hl" x="{p.X(1.6):.1f}" y="{p.Y(np.log2(1 + np.exp(-1.6))) - 10:.1f}">logistic</text>')
    body.append(f'<text class="t-mut" x="{p.X(-1.2):.1f}" y="{p.Y(1) - 6:.1f}">0–1</text>')
    body.append(f'<text class="t-mut" x="{p.X(1) + 4:.1f}" y="{p.Y(3.3):.1f}">yf = 1</text>')
    return svg(560, 285, "".join(body), "Hinge, logistic and zero-one losses")


# ---------------------------------------------------------------- decision trees


@fig("dt-impurity", "Impurity of a two-class node as a function of p = fraction of class 1. All three measures are 0 for a pure "
     "node and largest at p = 0.5: entropy reaches 1 bit, Gini and misclassification error reach 0.5. Entropy and Gini are "
     "smooth and strictly concave, which is why they are preferred for choosing splits.")
def dt_impurity():
    q = np.linspace(0.001, 0.999, 300)
    ent = -(q * np.log2(q) + (1 - q) * np.log2(1 - q))
    gini = 1 - q ** 2 - (1 - q) ** 2
    mis = 1 - np.maximum(q, 1 - q)
    p = Plot(60, 20, 460, 220, (0, 1), (0, 1.08))
    body = [p.axes("p = P(class 1) in the node", "impurity", xoff=32, yoff=34)]
    for t in (0, 0.25, 0.5, 0.75, 1):
        body.append(f'<text class="t-mut" x="{p.X(t):.1f}" y="{p.Y(0) + 15:.1f}" text-anchor="middle">{t:g}</text>')
    for v in (0.5, 1.0):
        body.append(f'<line class="grid" x1="{p.X(0):.1f}" y1="{p.Y(v):.1f}" x2="{p.X(1):.1f}" y2="{p.Y(v):.1f}"/>')
        body.append(f'<text class="t-mut" x="{p.X(0) - 6:.1f}" y="{p.Y(v) + 4:.1f}" text-anchor="end">{v:g}</text>')
    body.append(p.path(q, ent, "ink"))
    body.append(p.path(q, gini, "hl"))
    body.append(p.path(q, mis, "mut"))
    body.append(f'<text class="t-ink" x="{p.X(0.5):.1f}" y="{p.Y(1.0) - 6:.1f}" text-anchor="middle">entropy (max 1)</text>')
    body.append(f'<text class="t-hl" x="{p.X(0.5):.1f}" y="{p.Y(0.5) - 8:.1f}" text-anchor="middle">Gini (max 0.5)</text>')
    body.append(f'<text class="t-mut" x="{p.X(0.27):.1f}" y="{p.Y(0.12):.1f}" text-anchor="start">misclassification</text>')
    return svg(560, 285, "".join(body), "Entropy, Gini and misclassification impurity")


@fig("dt-cricket", "The first split for the 2024 Q62 cricket data (Green G / Blue B). The root has 4 G, 6 B (entropy 0.971). "
     "Splitting on Pitch gives S: 3 G, 2 B (0.971) and F: 1 G, 4 B (0.722). Weighted child entropy = 0.846, so "
     "IG(Pitch) = 0.971 − 0.846 = 0.125. Splitting on Format would gain only 0.020.")
def dt_cricket():
    def node(x, y, title, counts, h, cls="box"):
        w, hh = 170, 62
        out = [f'<rect class="{cls}" x="{x - w / 2}" y="{y}" width="{w}" height="{hh}" rx="8"/>',
               f'<text class="title" x="{x}" y="{y + 20}" text-anchor="middle">{title}</text>',
               f'<text x="{x}" y="{y + 38}" text-anchor="middle">{counts}</text>',
               f'<text class="t-ink" x="{x}" y="{y + 54}" text-anchor="middle">H = {h}</text>']
        return out
    body = []
    body += node(300, 10, "all 10 matches", "4 G · 6 B", "0.971")
    body += node(150, 150, "Pitch = S", "3 G · 2 B", "0.971")
    body += node(450, 150, "Pitch = F", "1 G · 4 B", "0.722")
    for x2 in (150, 450):
        body.append(f'<line class="ax" x1="300" y1="72" x2="{x2}" y2="150"/>')
    body.append('<text class="t-mut" x="205" y="112" text-anchor="end">5/10</text>')
    body.append('<text class="t-mut" x="395" y="112">5/10</text>')
    body.append('<text class="t-hl" x="300" y="245" text-anchor="middle">IG = 0.971 − (0.5·0.971 + 0.5·0.722) = 0.125</text>')
    return svg(600, 260, "".join(body), "Information gain of the first split")


# ---------------------------------------------------------------- neural networks


@fig("nn-activations", "Common activation functions (solid) and their derivatives (dashed). Sigmoid's slope is at most 0.25 and "
     "tanh's at most 1, and both flatten for large |z| (vanishing gradients). ReLU's slope is exactly 1 for z > 0 and 0 for "
     "z < 0; it is continuous everywhere but has a kink (no derivative) at z = 0.")
def nn_activations():
    z = np.linspace(-4, 4, 300)
    sg = 1 / (1 + np.exp(-z))
    funcs = [("sigmoid", sg, sg * (1 - sg), (-0.1, 1.1)), ("tanh", np.tanh(z), 1 - np.tanh(z) ** 2, (-1.1, 1.1)),
             ("ReLU", np.maximum(z, 0), (z > 0).astype(float), (-0.4, 4.1))]
    body = []
    for k, (name, f, df, yr) in enumerate(funcs):
        ox = 10 + k * 205
        p = Plot(ox + 10, 30, 180, 150, (-4, 4), yr)
        body.append(f'<text class="title" x="{ox + 100}" y="18" text-anchor="middle">{name}</text>')
        body.append(f'<line class="grid" x1="{p.X(-4):.1f}" y1="{p.Y(0):.1f}" x2="{p.X(4):.1f}" y2="{p.Y(0):.1f}"/>')
        body.append(f'<line class="grid" x1="{p.X(0):.1f}" y1="{p.Y(yr[0]):.1f}" x2="{p.X(0):.1f}" y2="{p.Y(yr[1]):.1f}"/>')
        body.append(p.path(z, f, "ink"))
        if name == "ReLU":
            body.append(p.path(z[z < 0], df[z < 0], "mut"))
            body.append(p.path(z[z > 0], df[z > 0], "mut"))
            body.append(f'<circle class="dot-warn" cx="{p.X(0):.1f}" cy="{p.Y(0):.1f}" r="3.5"/>')
            body.append(f'<text class="t-warn" x="{p.X(0.3):.1f}" y="{p.Y(-0.25):.1f}">kink at 0</text>')
        else:
            body.append(p.path(z, df, "mut"))
        mx = {"sigmoid": "max slope 0.25", "tanh": "max slope 1", "ReLU": "slope 0 or 1"}[name]
        body.append(f'<text class="t-mut" x="{ox + 100}" y="198" text-anchor="middle">{mx}</text>')
    return svg(625, 208, "".join(body), "Activation functions and derivatives")


@fig("nn-mlp-count", "The MLP of 2026 Q56: 30 inputs → 4 → 3 → 1, fully connected, no biases. Each layer contributes "
     "(neurons in) × (neurons out) weights: 30·4 + 4·3 + 3·1 = 120 + 12 + 3 = 135. With biases you would add 4 + 3 + 1 = 8.")
def nn_mlp_count():
    layers = [(30, 6, "input · 30"), (4, 4, "hidden · 4"), (3, 3, "hidden · 3"), (1, 1, "output · 1")]
    xs = [70, 230, 390, 540]
    pos = []
    for (n, shown, _), x in zip(layers, xs):
        ys = np.linspace(40, 230, shown + 2)[1:-1] if shown > 1 else [135]
        pos.append([(x, y) for y in ys])
    body = []
    for a, b in zip(pos, pos[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                body.append(f'<line class="grid" x1="{x1}" y1="{y1:.1f}" x2="{x2}" y2="{y2:.1f}"/>')
    for k, nodes in enumerate(pos):
        for i, (x, y) in enumerate(nodes):
            body.append(f'<circle class="box" cx="{x}" cy="{y:.1f}" r="11"/>')
        if k == 0:
            body.append(f'<text class="t-mut" x="{xs[0]}" y="{(nodes[2][1] + nodes[3][1]) / 2 + 4:.1f}" text-anchor="middle">⋮</text>')
        body.append(f'<text class="title" x="{xs[k]}" y="258" text-anchor="middle">{layers[k][2]}</text>')
    for (a, b, w), x in zip([(30, 4, 120), (4, 3, 12), (3, 1, 3)], [150, 310, 465]):
        body.append(f'<text class="t-ink" x="{x}" y="20" text-anchor="middle">{a}×{b} = {w}</text>')
    body.append('<text class="t-hl" x="305" y="285" text-anchor="middle">total weights = 120 + 12 + 3 = 135</text>')
    return svg(610, 295, "".join(body), "Multi-layer perceptron parameter count")


@fig("nn-q42-backprop", "2025 Q42 with the numbers filled in. Under each unit is its forward pass: h₁ = R(1·2 + 1·3) = 5, h₂ = R(1·2 − 1·3) = R(−1) = 0, "
     "y = R(4·5 − 1·0) = 20. The gradients are on the right: ∂y/∂a = R′(20)·e·R′(5)·u = 1·4·1·2 = 8; ∂y/∂f = R′(20)·h₂ = 0. "
     "The bottom unit is inactive (dashed edges), so no gradient flows through it.")
def nn_q42():
    N = {"u": (60, 70), "v": (60, 210), "h1": (260, 70), "h2": (260, 210), "y": (450, 140)}
    E = [("u", "h1", "a=1"), ("v", "h1", "b=1"), ("u", "h2", "c=1"), ("v", "h2", "d=−1"), ("h1", "y", "e=4"), ("h2", "y", "f=−1")]
    body = []
    for a, b, lab in E:
        (x1, y1), (x2, y2) = N[a], N[b]
        dead = "h2" in (a, b)
        body.append(f'<line class="{"mut" if dead else "ax"}" x1="{x1 + 20}" y1="{y1}" x2="{x2 - 20}" y2="{y2}"/>')
        frac = {("u", "h2"): 0.25, ("v", "h1"): 0.25}.get((a, b), 0.5)
        mx, my = x1 + (x2 - x1) * frac, y1 + (y2 - y1) * frac
        dy = 16 if (a, b) == ("v", "h2") else -8
        body.append(f'<text class="t-mut" x="{mx + 14:.0f}" y="{my + dy:.0f}" text-anchor="middle">{lab}</text>')
    vals = {"u": ("u", "2"), "v": ("v", "3"), "h1": ("R", "z=5 → 5"), "h2": ("R", "z=−1 → 0"), "y": ("R", "z=20 → 20")}
    for k, (x, y) in N.items():
        cls = "box-ink" if k in ("h1", "y") else "box"
        body.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="20"/>')
        body.append(f'<text class="{"on-ink" if cls == "box-ink" else "title"}" x="{x}" y="{y + 4}" text-anchor="middle">{vals[k][0]}</text>')
        body.append(f'<text x="{x}" y="{y + 38}" text-anchor="middle">{vals[k][1]}</text>')
    body.append('<text class="t-ink" x="510" y="80">∂y/∂a = 1·4·1·2 = 8</text>')
    body.append('<text class="t-ink" x="510" y="104">∂y/∂f = 1·h₂ = 0</text>')
    body.append('<text class="t-warn" x="510" y="128">R′(−1) = 0: bottom</text>')
    body.append('<text class="t-warn" x="510" y="146">path carries no gradient</text>')
    return svg(700, 270, "".join(body), "Forward and backward pass of a small ReLU network")


# ---------------------------------------------------------------- clustering


@fig("km-iterations", "k-means (k = 3) on 45 points from a deliberately bad start: all three centroids begin in the bottom-left. "
     "Each round assigns every point to its nearest centroid (colours), then moves each centroid ✕ to the mean of its points. "
     "The within-cluster sum of squares (WCSS) never increases, and here the centroids settle on the three groups by round 4.")
def km_iterations():
    rng = np.random.default_rng(4)
    centers = np.array([[1.0, 1.0], [4.5, 1.5], [2.6, 4.2]])
    X = np.vstack([c + rng.normal(0, 0.45, (15, 2)) for c in centers])
    C = np.array([[0.6, 0.6], [1.2, 0.5], [0.8, 1.3]])
    snaps = []
    for it in range(8):
        lab = np.argmin(((X[:, None] - C[None]) ** 2).sum(-1), 1)
        wcss = sum(((X[lab == k] - C[k]) ** 2).sum() for k in range(3))
        snaps.append((C.copy(), lab.copy(), wcss))
        C = np.array([X[lab == k].mean(0) if (lab == k).any() else C[k] for k in range(3)])
    show = [(0, "round 1: assign"), (1, "round 2"), (3, "round 4: converged")]
    cls_pt = ["dot-ink", "dot-warn", "dot-hl"]
    body = []
    for k, (i, title) in enumerate(show):
        Cc, lab, wcss = snaps[i]
        ox = 10 + k * 205
        p = Plot(ox + 6, 30, 185, 165, (-0.2, 5.8), (-0.2, 5.6))
        body.append(f'<text class="title" x="{ox + 98}" y="18" text-anchor="middle">{title}</text>')
        body.append(f'<rect class="grid" x="{p.x0}" y="{p.y0}" width="{p.w}" height="{p.h}" rx="6"/>')
        for (a, b), l in zip(X, lab):
            body.append(f'<circle class="{cls_pt[l]}" cx="{p.X(a):.1f}" cy="{p.Y(b):.1f}" r="3.2" style="opacity:.85"/>')
        for (a, b) in Cc:
            x, y = p.X(a), p.Y(b)
            body.append(f'<path class="ax" style="stroke:var(--sl-color-white);stroke-width:3" d="M{x - 6:.1f},{y - 6:.1f} L{x + 6:.1f},{y + 6:.1f} M{x - 6:.1f},{y + 6:.1f} L{x + 6:.1f},{y - 6:.1f}"/>')
        body.append(f'<text class="t-mut" x="{ox + 98}" y="212" text-anchor="middle">WCSS = {wcss:.1f}</text>')
    return svg(625, 222, "".join(body), "k-means iterations")


def _dendrogram(merges, labels, x0, y0, w, h, hmax, title):
    """merges: list of (clusterA, clusterB, height) with clusters as lists of leaf labels."""
    order = []
    # leaf order: follow the final merge structure
    def leaves(c):
        return c
    final = merges[-1][0] + merges[-1][1]
    order = final
    xs = {lab: x0 + (i + 0.5) * w / len(order) for i, lab in enumerate(order)}
    Y = lambda v: y0 + h - v / hmax * h
    pos = {(lab,): (xs[lab], Y(0)) for lab in order}
    body = [f'<text class="title" x="{x0 + w / 2}" y="{y0 - 14}" text-anchor="middle">{title}</text>']
    for t in range(0, int(hmax) + 1):
        body.append(f'<line class="grid" x1="{x0 - 4}" y1="{Y(t):.1f}" x2="{x0 + w}" y2="{Y(t):.1f}"/>')
        body.append(f'<text class="t-mut" x="{x0 - 8}" y="{Y(t) + 4:.1f}" text-anchor="end">{t}</text>')
    for a, b, d in merges:
        ka, kb = tuple(a), tuple(b)
        (xa, ya), (xb, yb) = pos[ka], pos[kb]
        yd = Y(d)
        body.append(f'<path class="ink" style="stroke-width:2" d="M{xa:.1f},{ya:.1f} V{yd:.1f} H{xb:.1f} V{yb:.1f}"/>')
        pos[tuple(a + b)] = ((xa + xb) / 2, yd)
    for lab in order:
        body.append(f'<text x="{xs[lab]:.1f}" y="{Y(0) + 16:.1f}" text-anchor="middle">x{lab}</text>')
    return body


@fig("hc-dendrograms", "The 2024 Q42 distance table clustered two ways. Single linkage (left) merges x1–x2 and x4–x5 at 1, "
     "then x3 joins {x4, x5} at 2 (its nearest member is x4), then everything joins at 3. Complete linkage (right) uses the "
     "farthest pair, so x3 joins {x1, x2} at 4 and the final merge is at 6. Same data, different trees.")
def hc_dendrograms():
    single = [([1], [2], 1), ([4], [5], 1), ([3], [4, 5], 2), ([1, 2], [3, 4, 5], 3)]
    complete = [([1], [2], 1), ([4], [5], 1), ([1, 2], [3], 4), ([1, 2, 3], [4, 5], 6)]
    body = _dendrogram(single, None, 50, 40, 230, 190, 6, "single linkage (min)")
    body += _dendrogram(complete, None, 360, 40, 230, 190, 6, "complete linkage (max)")
    body.append('<text class="t-mut" x="20" y="135" text-anchor="middle" transform="rotate(-90 20 135)">merge distance</text>')
    return svg(620, 265, "".join(body), "Single and complete linkage dendrograms")


@fig("hc-linkage", "Distance between two clusters. Single linkage uses the closest pair (min), complete linkage the farthest "
     "pair (max), average linkage the mean over all pairs. Single linkage can 'chain' long thin clusters together; "
     "complete linkage prefers compact, round clusters.")
def hc_linkage():
    A = [(60, 90), (95, 140), (70, 175)]
    B = [(250, 110), (300, 70), (320, 160)]
    body = []
    body.append('<ellipse class="grid" cx="75" cy="135" rx="45" ry="70"/>')
    body.append('<ellipse class="grid" cx="290" cy="115" rx="55" ry="70"/>')
    for x, y in A:
        body.append(f'<circle class="dot-ink" cx="{x}" cy="{y}" r="6"/>')
    for x, y in B:
        body.append(f'<rect class="dot-warn" x="{x - 6}" y="{y - 6}" width="12" height="12"/>')
    body.append('<line class="hl" x1="95" y1="140" x2="250" y2="110"/>')
    body.append('<text class="t-hl" x="172" y="112" text-anchor="middle">single = min</text>')
    body.append('<line class="ink" style="stroke-dasharray:6 4" x1="60" y1="90" x2="320" y2="160"/>')
    body.append('<text class="t-ink" x="215" y="158" text-anchor="middle">complete = max</text>')
    body.append('<text class="title" x="75" y="225" text-anchor="middle">cluster C₁</text>')
    body.append('<text class="title" x="290" y="205" text-anchor="middle">cluster C₂</text>')
    rows = [("single", "min over pairs", "t-hl"), ("complete", "max over pairs", "t-ink"), ("average", "mean over all pairs", "t-mut"),
            ("centroid", "distance between means", "t-mut"), ("Ward", "increase in WCSS", "t-mut")]
    for i, (a, b, c) in enumerate(rows):
        body.append(f'<text class="{c}" x="400" y="{50 + i * 34}" style="font-weight:600">{a}</text>')
        body.append(f'<text x="480" y="{50 + i * 34}">{b}</text>')
    return svg(640, 240, "".join(body), "Single versus complete linkage")


# ---------------------------------------------------------------- PCA


@fig("pca-axes", "200 correlated points with their principal components. PC1 (blue) points along the direction of greatest "
     "spread; PC2 (yellow) is perpendicular to it. Each axis extends 2√λ on either side of the mean. Projecting onto PC1 alone keeps most of the "
     "variance; the short perpendicular segments are what that projection throws away (the reconstruction error).")
def pca_axes():
    rng = np.random.default_rng(2)
    C = np.array([[2.5, 1.5], [1.5, 1.6]])
    X = rng.multivariate_normal([0, 0], C, 200)
    X -= X.mean(0)
    S = X.T @ X / len(X)
    lam, V = np.linalg.eigh(S)
    lam, V = lam[::-1], V[:, ::-1]
    p = Plot(30, 20, 340, 280, (-5, 5), (-4, 4))
    body = [f'<rect class="grid" x="{p.x0}" y="{p.y0}" width="{p.w}" height="{p.h}" rx="6"/>']
    u = V[:, 0]
    for x in X[::8]:
        proj = (x @ u) * u
        body.append(f'<line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="{p.X(x[0]):.1f}" y1="{p.Y(x[1]):.1f}" x2="{p.X(proj[0]):.1f}" y2="{p.Y(proj[1]):.1f}"/>')
    for a, b in X:
        body.append(f'<circle class="dot" cx="{p.X(a):.1f}" cy="{p.Y(b):.1f}" r="2.4" style="opacity:.55"/>')
    for k, cls in ((0, "ink"), (1, "hl")):
        v = V[:, k] * 2 * np.sqrt(lam[k])
        body.append(f'<line class="{cls}" style="stroke-width:3.2" x1="{p.X(-v[0]):.1f}" y1="{p.Y(-v[1]):.1f}" x2="{p.X(v[0]):.1f}" y2="{p.Y(v[1]):.1f}"/>')
        body.append(f'<text class="{"t-ink" if k == 0 else "t-hl"}" x="{p.X(v[0]) + 6:.1f}" y="{p.Y(v[1]) - 4:.1f}">PC{k + 1}</text>')
    tot = lam.sum()
    info = [("covariance eigenvalues", "t-mut"), (f"λ₁ = {lam[0]:.2f}", "t-ink"), (f"λ₂ = {lam[1]:.2f}", "t-hl"),
            (f"PC1 explains {lam[0] / tot:.0%}", "t-ink"), ("PC1 ⟂ PC2 (angle 90°)", "t-mut")]
    for i, (t, c) in enumerate(info):
        body.append(f'<text class="{c}" x="395" y="{60 + i * 30}">{t}</text>')
    return svg(600, 320, "".join(body), "Principal component axes on correlated data")


@fig("pca-scree", "A scree plot for eigenvalues 4, 2, 1, 0.5, 0.5 (total 8). Bars show each component's share of the variance "
     "(50%, 25%, 12.5%, 6.25%, 6.25%); the line is the cumulative share. Keeping 90% of the variance needs 4 components.")
def pca_scree():
    lam = np.array([4, 2, 1, 0.5, 0.5])
    share = lam / lam.sum()
    cum = np.cumsum(share)
    p = Plot(60, 20, 420, 220, (0.4, 5.6), (0, 1.05))
    body = [p.axes("principal component", "fraction of variance", xoff=32, yoff=40)]
    for v in (0.25, 0.5, 0.75, 0.9, 1.0):
        body.append(f'<line class="grid" x1="{p.X(0.4):.1f}" y1="{p.Y(v):.1f}" x2="{p.X(5.6):.1f}" y2="{p.Y(v):.1f}"/>')
        body.append(f'<text class="t-mut" x="{p.X(0.4) - 6:.1f}" y="{p.Y(v) + 4:.1f}" text-anchor="end">{v:g}</text>')
    for i, (sh, c) in enumerate(zip(share, cum), 1):
        body.append(f'<rect class="box-ink" x="{p.X(i) - 22:.1f}" y="{p.Y(sh):.1f}" width="44" height="{p.Y(0) - p.Y(sh):.1f}" rx="3" style="opacity:.85"/>')
        body.append(f'<text class="t-mut" x="{p.X(i):.1f}" y="{p.Y(0) + 15:.1f}" text-anchor="middle">{i}</text>')
    body.append(p.path(np.arange(1, 6), cum, "hl"))
    for i, c in enumerate(cum, 1):
        body.append(f'<circle class="dot-hl" cx="{p.X(i):.1f}" cy="{p.Y(c):.1f}" r="4"/>')
        body.append(f'<text class="t-hl" x="{p.X(i):.1f}" y="{p.Y(c) - 9:.1f}" text-anchor="middle">{c:.3g}</text>')
    body.append(f'<text class="t-warn" x="{p.X(5.55):.1f}" y="{p.Y(0.9) + 14:.1f}" text-anchor="end">90% line</text>')
    return svg(520, 285, "".join(body), "Scree plot and cumulative explained variance")


# ---------------------------------------------------------------- DBMS: ER


@fig("er-q61", "The ER diagram of 2026 Q61 in Chen notation. Rectangles are entities, the diamond is the relationship, "
     "ellipses are attributes (key attributes underlined, the multivalued attribute A22 in a double ellipse). Double "
     "lines mean total participation; M and N mark a many-to-many relationship. It needs four 3NF tables.")
def er_q61():
    body = []

    def ent(x, y, name):
        return [f'<rect class="box" x="{x - 45}" y="{y - 20}" width="90" height="40" rx="2" style="stroke:var(--gd-ink);stroke-width:1.6"/>',
                f'<text class="title" x="{x}" y="{y + 5}" text-anchor="middle">{name}</text>']

    def attr(x, y, name, ex, ey, key=False, multi=False):
        out = [f'<line class="ax" x1="{x}" y1="{y}" x2="{ex}" y2="{ey}"/>',
               f'<ellipse class="box" cx="{x}" cy="{y}" rx="30" ry="15"/>']
        if multi:
            out.append(f'<ellipse class="box" style="fill:none" cx="{x}" cy="{y}" rx="25" ry="11"/>')
        deco = ' style="text-decoration:underline"' if key else ""
        out.append(f'<text x="{x}" y="{y + 4}" text-anchor="middle"{deco}>{name}</text>')
        return out

    E1, E2, R = (110, 130), (470, 130), (290, 130)
    for (x, y), nm, k in ((E1, "A1", "1"), (E2, "A2", "2")):
        ex, ey = x, y - 20
        for i, dx in enumerate((-70, 0, 70)):
            body += attr(x + dx, y - 85, f"A{k}{i + 1}", x + dx * 0.4, ey, key=(i == 0), multi=(k == "2" and i == 1))
    for (x, y), lab in ((E1, "M"), (E2, "N")):
        sx = x + 45 if x < R[0] else x - 45
        rx = R[0] - 45 if x < R[0] else R[0] + 45
        for off in (-3, 3):
            body.append(f'<line class="ax" x1="{sx}" y1="{y + off}" x2="{rx}" y2="{R[1] + off}"/>')
        body.append(f'<text class="t-ink" x="{(sx + rx) / 2}" y="{y - 10}" text-anchor="middle">{lab}</text>')
    body.append(f'<polygon class="box" style="stroke:var(--gd-ink);stroke-width:1.6" points="{R[0] - 45},{R[1]} {R[0]},{R[1] - 28} {R[0] + 45},{R[1]} {R[0]},{R[1] + 28}"/>')
    body.append(f'<text class="title" x="{R[0]}" y="{R[1] + 5}" text-anchor="middle">R12</text>')
    body += ent(*E1, "E1") + ent(*E2, "E2")
    tables = [("E1", "(A11, A12, A13)"), ("E2", "(A21, A23)"), ("E2_A22", "(A21, A22)"), ("R12", "(A11, A21)")]
    body.append('<text class="title" x="30" y="205">tables (3NF):</text>')
    for i, (t, cols) in enumerate(tables):
        x = 30 + i * 145
        body.append(f'<rect class="box" x="{x}" y="215" width="135" height="44" rx="6"/>')
        body.append(f'<text class="t-ink" x="{x + 67}" y="233" text-anchor="middle" style="font-weight:600">{t}</text>')
        body.append(f'<text x="{x + 67}" y="250" text-anchor="middle">{cols}</text>')
    return svg(610, 270, "".join(body), "ER diagram with many-to-many relationship and multivalued attribute")


# ---------------------------------------------------------------- DBMS: relational algebra


@fig("ra-division", "Division in 2025 Q62. Each tick is a (branch, customer) pair from π(branch, customer)(Loan ⋈ Borrower). "
     "Dividing by π(branch)(Loan) keeps a customer only if their row is ticked in every branch column. Only Karteek's "
     "row is complete, so the result has 1 tuple.")
def ra_division():
    branches = ["Banjara Hills", "Kondapur", "SR Nagar", "Balanagar"]
    pairs = {("Balanagar", "Karteek"), ("Balanagar", "Sunil"), ("Banjara Hills", "Anand"), ("Banjara Hills", "Karteek"),
             ("Kondapur", "Karteek"), ("Kondapur", "Sunil"), ("SR Nagar", "Ankita"), ("SR Nagar", "Gopal"), ("SR Nagar", "Karteek")}
    custs = ["Anand", "Ankita", "Gopal", "Karteek", "Sunil"]
    x0, y0, cw, rh = 120, 50, 110, 34
    body = []
    for j, b in enumerate(branches):
        body.append(f'<text class="title" x="{x0 + j * cw + cw / 2}" y="{y0 - 12}" text-anchor="middle">{b}</text>')
    for i, c in enumerate(custs):
        y = y0 + i * rh
        full = all((b, c) in pairs for b in branches)
        if full:
            body.append(f'<rect class="box-ink" x="{x0 - 100}" y="{y + 2}" width="{100 + 4 * cw + 90}" height="{rh - 4}" rx="6" style="opacity:.22"/>')
        body.append(f'<text class="{"t-ink" if full else ""}" x="{x0 - 12}" y="{y + rh / 2 + 4}" text-anchor="end" style="font-weight:{600 if full else 400}">{c}</text>')
        for j, b in enumerate(branches):
            cx = x0 + j * cw + cw / 2
            body.append(f'<rect class="box" x="{cx - 14}" y="{y + 5}" width="28" height="{rh - 10}" rx="4"/>')
            if (b, c) in pairs:
                body.append(f'<text class="t-ink" x="{cx}" y="{y + rh / 2 + 5}" text-anchor="middle" style="font-size:14px;font-weight:700">✓</text>')
        n = sum((b, c) in pairs for b in branches)
        body.append(f'<text class="{"t-ink" if full else "t-mut"}" x="{x0 + 4 * cw + 10}" y="{y + rh / 2 + 4}">{n}/4{"  → kept" if full else ""}</text>')
    return svg(640, y0 + len(custs) * rh + 12, "".join(body), "Relational division as a grid")


# ---------------------------------------------------------------- DBMS: SQL


@fig("sql-order", "The logical order in which SQL evaluates a query, which is not the order you write it in. WHERE filters "
     "rows before grouping (so it cannot use aggregates); HAVING filters groups after aggregation; SELECT aliases exist "
     "only from the SELECT step onward, so ORDER BY can use them but WHERE cannot.")
def sql_order():
    steps = [("1", "FROM / JOIN", "combine rows"), ("2", "WHERE", "filter rows"),
             ("3", "GROUP BY", "make groups"), ("4", "HAVING", "filter groups"),
             ("5", "SELECT", "pick columns"), ("6", "DISTINCT", "drop duplicates"),
             ("7", "ORDER BY", "sort rows"), ("8", "LIMIT", "keep n rows")]
    body = []
    w, h, gap = 140, 62, 14
    for i, (n, kw, desc) in enumerate(steps):
        r, c = divmod(i, 4)
        x = 20 + c * (w + gap); y = 20 + r * (h + 40)
        hot = kw in ("WHERE", "HAVING")
        body.append(f'<rect class="{"box-ink" if hot else "box"}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>')
        body.append(f'<text class="{"on-ink" if hot else "t-ink"}" x="{x + 12}" y="{y + 22}" style="font-weight:700">{n}. {kw}</text>')
        body.append(f'<text class="{"on-ink" if hot else "t-mut"}" x="{x + 12}" y="{y + 44}">{desc}</text>')
        if c < 3:
            body.append(f'<path class="ax" d="M{x + w + 2},{y + h / 2} h{gap - 4} m-5,-4 l5,4 l-5,4"/>')
    body.append(f'<path class="ax" d="M{20 + 3 * (w + gap) + w / 2},{20 + h + 2} v14 H{20 + w / 2} v14 m-4,-5 l4,5 l4,-5"/>')
    body.append('<text class="t-mut" x="20" y="232">written order: SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT</text>')
    return svg(640, 244, "".join(body), "Logical evaluation order of an SQL query")


# ---------------------------------------------------------------- DBMS: normalization


@fig("nf-ladder", "Each normal form is stricter than the one outside it: every BCNF relation is in 3NF, every 3NF relation "
     "is in 2NF, and so on. For each non-trivial FD X → A, the rule at each level says what is allowed.")
def nf_ladder():
    levels = [("1NF", "every attribute value is atomic (no lists or repeating groups)"),
              ("2NF", "no non-prime A depends on a proper part of a candidate key"),
              ("3NF", "X is a superkey, or A is prime (part of some candidate key)"),
              ("BCNF", "X is a superkey, for every non-trivial X → A")]
    body = []
    W, H = 600, 250
    for i, (name, rule) in enumerate(levels):
        pad = i * 32
        x, y, w, h = 10 + pad, 10 + pad * 0.85, W - 2 * pad, H - 2 * pad * 0.85
        cls = "box-ink" if name == "BCNF" else "box"
        body.append(f'<rect class="{cls}" x="{x}" y="{y:.1f}" width="{w}" height="{h:.1f}" rx="10" style="{"opacity:.9" if cls == "box-ink" else ""}"/>')
        tc = "on-ink" if cls == "box-ink" else "t-ink"
        body.append(f'<text class="{tc}" x="{x + 14}" y="{y + 22:.1f}" style="font-weight:700">{name}</text>')
        body.append(f'<text class="{"on-ink" if cls == "box-ink" else "t-mut"}" x="{x + 70}" y="{y + 22:.1f}">{rule}</text>')
    return svg(620, 270, "".join(body), "Nested normal forms")


# ---------------------------------------------------------------- DBMS: B+ trees


def _bnode(x, y, keys, leaf=False, hot=False):
    w = 30 * max(len(keys), 1) + 10
    cls = "box-ink" if hot else "box"
    out = [f'<rect class="{cls}" x="{x - w / 2:.1f}" y="{y}" width="{w}" height="26" rx="4" style="{"" if leaf else "stroke:var(--gd-ink);stroke-width:1.4"}"/>']
    for i, k in enumerate(keys):
        kx = x - w / 2 + 5 + 30 * i + 15
        out.append(f'<text class="{"on-ink" if hot else "title"}" x="{kx:.1f}" y="{y + 18}" text-anchor="middle">{k}</text>')
        if i:
            out.append(f'<line class="grid" x1="{kx - 15:.1f}" y1="{y + 3}" x2="{kx - 15:.1f}" y2="{y + 23}"/>')
    return out, w


@fig("bpt-q41", "2026 Q41. Leaves hold at most 2 keys and internal nodes at most 3 pointers; a key equal to a separator goes "
     "left (the convention of the figure in the paper). Inserting 3 overflows leaf [1, 5] → split into [1, 3] and [5], "
     "separator 3 goes up. The root [3, 5, 8] now has 4 pointers → split: the middle key 5 moves up and becomes the new root.")
def bpt_q41():
    body = ['<text class="title" x="150" y="16" text-anchor="middle">before</text>',
            '<text class="title" x="470" y="16" text-anchor="middle">after inserting 3</text>']
    def tree(nodes, edges):
        out = []
        pos = {}
        for name, (x, y, keys, leaf, hot) in nodes.items():
            o, w = _bnode(x, y, keys, leaf, hot); out += o; pos[name] = (x, y)
        for a, b in edges:
            (x1, y1), (x2, y2) = pos[a], pos[b]
            out.insert(0, f'<line class="ax" x1="{x1}" y1="{y1 + 26}" x2="{x2}" y2="{y2}"/>')
        return out
    body += tree({"r": (150, 40, [5, 8], False, False), "a": (55, 130, [1, 5], True, False), "b": (150, 130, [7, 8], True, False),
                  "c": (245, 130, [9, 12], True, False)}, [("r", "a"), ("r", "b"), ("r", "c")])
    body += tree({"r": (470, 40, [5], False, True), "L": (400, 100, [3], False, False), "R": (545, 100, [8], False, False),
                  "a": (350, 170, [1, 3], True, False), "a2": (425, 170, [5], True, False), "b": (505, 170, [7, 8], True, False),
                  "c": (590, 170, [9, 12], True, False)},
                 [("r", "L"), ("r", "R"), ("L", "a"), ("L", "a2"), ("R", "b"), ("R", "c")])
    body.append('<text class="t-mut" x="150" y="190" text-anchor="middle">leaf [1, 5] receives 3 → overflow</text>')
    body.append('<line class="mut" x1="300" y1="100" x2="330" y2="100"/>')
    return svg(640, 210, "".join(body), "B+ tree before and after an insertion with splits")


# ---------------------------------------------------------------- DBMS: data transformation


@fig("binning", "The same nine sorted values 4, 8, 15, 21, 21, 24, 25, 28, 34 discretized into 3 bins two ways. Equal-width bins "
     "have the same range (width (34 − 4)/3 = 10) but unequal counts (2, 3, 4). Equal-frequency bins have the same count "
     "(3 each) but unequal ranges. Smoothing by bin means replaces each value by its bin's mean.")
def binning():
    d = [4, 8, 15, 21, 21, 24, 25, 28, 34]
    X = lambda v: 40 + (v - 0) / 38 * 540
    body = []
    rows = [("equal width (width 10)", [(4, 14), (14, 24), (24, 34)], [[4, 8], [15, 21, 21], [24, 25, 28, 34]]),
            ("equal frequency (3 per bin)", [(4, 15), (21, 24), (25, 34)], [[4, 8, 15], [21, 21, 24], [25, 28, 34]])]
    fills = ["var(--gd-ink)", "var(--gd-hl-strong)", "var(--gd-ink)"]
    for r, (title, ranges, bins) in enumerate(rows):
        y = 40 + r * 120
        body.append(f'<text class="title" x="40" y="{y - 14}">{title}</text>')
        base = y + 62
        body.append(f'<line class="ax" x1="{X(0)}" y1="{base}" x2="{X(38)}" y2="{base}"/>')
        for i, ((a, b), items) in enumerate(zip(ranges, bins)):
            x1, x2 = X(a) - 3, X(b) + 3
            body.append(f'<rect x="{x1:.1f}" y="{y + 26}" width="{x2 - x1:.1f}" height="22" rx="5" style="fill:{fills[i]};fill-opacity:.22;stroke:{fills[i]}"/>')
            m = sum(items) / len(items)
            cx = (x1 + x2) / 2
            body.append(f'<text class="t-ink" x="{cx:.1f}" y="{y + 4}" text-anchor="middle">n = {len(items)}</text>')
            body.append(f'<text class="t-mut" x="{cx:.1f}" y="{y + 19}" text-anchor="middle">mean {m:g}</text>')
        seen = {}
        for v in d:
            k = seen.get(v, 0); seen[v] = k + 1
            body.append(f'<circle class="dot" cx="{X(v):.1f}" cy="{base - 7 * k:.1f}" r="4"/>')
        for t in (0, 10, 20, 30):
            body.append(f'<text class="t-mut" x="{X(t):.1f}" y="{base + 16}" text-anchor="middle">{t}</text>')
    return svg(620, 275, "".join(body), "Equal-width versus equal-frequency binning")


# ---------------------------------------------------------------- DBMS: warehousing


@fig("dw-star", "A star schema for sales. The central fact table holds the measures (units sold, revenue) and one foreign key "
     "per dimension. Each dimension table is denormalized: it holds a whole hierarchy (day → month → quarter → year) in one "
     "table. A snowflake schema would split those hierarchies into further normalized tables.")
def dw_star():
    body = []
    fact = (300, 130)
    dims = [("Time", ["time_key", "day, month", "quarter, year"], (110, 45)), ("Item", ["item_key", "name, brand", "type"], (490, 45)),
            ("Location", ["location_key", "city, state", "country"], (110, 215)), ("Branch", ["branch_key", "name", "type"], (490, 215))]
    for name, cols, (x, y) in dims:
        body.append(f'<line class="ax" x1="{fact[0]}" y1="{fact[1]}" x2="{x}" y2="{y}"/>')
    for name, cols, (x, y) in dims:
        body.append(f'<rect class="box" x="{x - 70}" y="{y - 32}" width="140" height="70" rx="6"/>')
        body.append(f'<text class="t-ink" x="{x}" y="{y - 14}" text-anchor="middle" style="font-weight:700">{name}</text>')
        for i, c in enumerate(cols):
            body.append(f'<text class="t-mut" x="{x}" y="{y + 4 + i * 14}" text-anchor="middle">{c}</text>')
    body.append(f'<rect class="box-ink" x="{fact[0] - 85}" y="{fact[1] - 52}" width="170" height="104" rx="8"/>')
    lines = ["Sales (fact)", "time_key", "item_key", "location_key", "branch_key", "units_sold, revenue"]
    for i, t in enumerate(lines):
        body.append(f'<text class="on-ink" x="{fact[0]}" y="{fact[1] - 32 + i * 15}" text-anchor="middle" style="font-weight:{700 if i == 0 else 400}">{t}</text>')
    return svg(600, 265, "".join(body), "Star schema with one fact table and four dimensions")


@fig("dw-lattice", "The lattice of cuboids for three dimensions (time, item, location) with no hierarchies: 2³ = 8 group-bys. "
     "The base cuboid at the bottom groups by all three; the apex at the top is the grand total. Moving up is roll-up "
     "(aggregate away a dimension); moving down is drill-down.")
def dw_lattice():
    levels = [["all (apex)"], ["time", "item", "location"], ["time, item", "time, location", "item, location"], ["time, item, location (base)"]]
    pos = {}
    body = []
    for li, row in enumerate(levels):
        y = 30 + li * 62
        for j, lab in enumerate(row):
            x = 310 + (j - (len(row) - 1) / 2) * 190
            pos[lab] = (x, y)
    def key(l):
        return set(t.strip() for t in l.replace("(base)", "").replace("(apex)", "").split(",")) - {"all", ""}
    labs = [l for row in levels for l in row]
    for a in labs:
        for b in labs:
            ka, kb = key(a), key(b)
            if ka < kb and len(kb) == len(ka) + 1:
                (x1, y1), (x2, y2) = pos[a], pos[b]
                body.append(f'<line class="grid" x1="{x1}" y1="{y1 + 12}" x2="{x2}" y2="{y2 - 12}"/>')
    for li, row in enumerate(levels):
        for lab in row:
            x, y = pos[lab]
            w = 9 * len(lab) + 20
            hot = li in (0, 3)
            body.append(f'<rect class="{"box-ink" if hot else "box"}" x="{x - w / 2:.1f}" y="{y - 13}" width="{w}" height="26" rx="13"/>')
            body.append(f'<text class="{"on-ink" if hot else ""}" x="{x}" y="{y + 4}" text-anchor="middle">{lab}</text>')
        body.append(f'<text class="t-mut" x="20" y="{30 + li * 62 + 4}">{li}-D</text>' if li < 3 else f'<text class="t-mut" x="20" y="{30 + li * 62 + 4}">3-D</text>')
    return svg(620, 240, "".join(body), "Lattice of cuboids for three dimensions")


# ---------------------------------------------------------------- AI: search


def _graph(nodes, edges, hl_path=(), hvals=None, r=15):
    """nodes: {name: (x, y)}; edges: [(a, b, label)] directed; hl_path: sequence of nodes to highlight."""
    body = []
    hp = set(zip(hl_path, hl_path[1:]))
    for a, b, lab in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / L, dy / L
        sx, sy, ex, ey = x1 + ux * r, y1 + uy * r, x2 - ux * (r + 2), y2 - uy * (r + 2)
        cls = "hl" if (a, b) in hp else "ax"
        body.append(f'<line class="{cls}" x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" style="{"" if cls == "hl" else "stroke-width:1.4"}"/>')
        ax, ay = ex, ey
        px, py = -uy, ux
        body.append(f'<path class="{cls}" style="fill:none" d="M{ax - ux * 8 + px * 4:.1f},{ay - uy * 8 + py * 4:.1f} L{ax:.1f},{ay:.1f} L{ax - ux * 8 - px * 4:.1f},{ay - uy * 8 - py * 4:.1f}"/>')
        mx, my = (x1 + x2) / 2 - uy * 11, (y1 + y2) / 2 + ux * 11
        if lab != "":
            body.append(f'<text class="t-mut" x="{mx:.1f}" y="{my + 4:.1f}" text-anchor="middle">{lab}</text>')
    for n, (x, y) in nodes.items():
        on = n in hl_path
        body.append(f'<circle class="{"box-ink" if on else "box"}" cx="{x}" cy="{y}" r="{r}"/>')
        body.append(f'<text class="{"on-ink" if on else "title"}" x="{x}" y="{y + 4}" text-anchor="middle">{n}</text>')
        if hvals and n in hvals:
            body.append(f'<text class="t-hl" x="{x}" y="{y - r - 6}" text-anchor="middle">h={hvals[n]}</text>')
    return body


@fig("search-bfs-dfs", "The order in which BFS and DFS expand the same binary tree (children visited left to right). BFS goes "
     "level by level using a FIFO queue; DFS goes as deep as possible first using a LIFO stack. BFS needs memory for a whole "
     "level (b^d nodes); DFS only for one path and its siblings (b·m).")
def search_bfs_dfs():
    pos = {}
    def place(i, depth, x, span):
        pos[i] = (x, 40 + depth * 62)
        if depth < 3:
            place(2 * i, depth + 1, x - span / 2, span / 2)
            place(2 * i + 1, depth + 1, x + span / 2, span / 2)
    body = []
    for k, (title, order) in enumerate([("BFS (queue)", None), ("DFS (stack)", None)]):
        pos.clear(); place(1, 0, 155 + k * 310, 150)
        body.append(f'<text class="title" x="{155 + k * 310}" y="16" text-anchor="middle">{title}</text>')
        bfs = sorted(pos)
        dfs = []
        def pre(i):
            if i in pos:
                dfs.append(i); pre(2 * i); pre(2 * i + 1)
        pre(1)
        seq = bfs if k == 0 else dfs
        rank = {n: j + 1 for j, n in enumerate(seq)}
        for i in pos:
            for c in (2 * i, 2 * i + 1):
                if c in pos:
                    (x1, y1), (x2, y2) = pos[i], pos[c]
                    body.append(f'<line class="grid" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke-width:1.4"/>')
        for i, (x, y) in pos.items():
            body.append(f'<circle class="{"box-ink" if rank[i] <= 5 else "box"}" cx="{x}" cy="{y}" r="12"/>')
            body.append(f'<text class="{"on-ink" if rank[i] <= 5 else ""}" x="{x}" y="{y + 4}" text-anchor="middle">{rank[i]}</text>')
    body.append('<text class="t-mut" x="310" y="262" text-anchor="middle">numbers = expansion order; the first 5 expansions are filled</text>')
    return svg(620, 270, "".join(body), "BFS versus DFS expansion order")


@fig("search-ucs", "A weighted graph from S to the goal G. BFS finds the path with the fewest edges, S → B → G (cost 7). "
     "Uniform-cost search always expands the cheapest frontier node, so it finds the cheapest path S → A → C → G (cost 5, highlighted).")
def search_ucs():
    nodes = {"S": (50, 120), "A": (190, 50), "B": (220, 200), "C": (350, 50), "D": (330, 128), "G": (490, 110)}
    edges = [("S", "A", 1), ("S", "B", 5), ("A", "C", 3), ("A", "D", 1), ("B", "G", 2), ("C", "G", 1), ("D", "G", 6)]
    body = _graph(nodes, edges, hl_path=("S", "A", "C", "G"))
    body.append('<text class="t-mut" x="540" y="60">BFS: S-B-G, cost 7</text>')
    body.append('<text class="t-ink" x="540" y="84">UCS: S-A-C-G, cost 5</text>')
    return svg(700, 220, "".join(body), "Weighted graph comparing BFS and uniform-cost search")


@fig("astar-q44", "The 2025 Q44 graph redrawn with step costs on the edges and h above each node. A* pops nodes in order of "
     "f = g + h: S(0), A(6), E(7), B(8), C(9), D(8), G(9). The optimal path S → E → C → D → G (cost 9) is highlighted. "
     "Note h(C) = 6 > c(C,D) + h(D) = 5, so this h is admissible but not consistent: f drops from 9 at C to 8 at D.")
def astar_q44():
    nodes = {"S": (40, 150), "A": (150, 70), "B": (260, 70), "C": (370, 70), "E": (150, 170), "D": (470, 150), "G": (570, 150)}
    edges = [("S", "A", 4), ("S", "E", 1), ("A", "B", 2), ("B", "C", 2), ("E", "C", 2), ("C", "D", 3), ("D", "G", 3)]
    h = {"S": "–", "A": 2, "B": 2, "C": 6, "E": 6, "D": 2, "G": 0}
    body = _graph(nodes, edges, hl_path=("S", "E", "C", "D", "G"), hvals=h)
    rows = [("S", 0, 0, 0), ("A", 4, 2, 6), ("E", 1, 6, 7), ("B", 6, 2, 8), ("C", 3, 6, 9), ("D", 6, 2, 8), ("G", 9, 0, 9)]
    body.append('<text class="title" x="40" y="225">pop order</text>')
    for i, (n, g, hh, f) in enumerate(rows):
        x = 130 + i * 68
        body.append(f'<rect class="box" x="{x - 28}" y="210" width="60" height="36" rx="6"/>')
        body.append(f'<text class="t-ink" x="{x + 2}" y="225" text-anchor="middle" style="font-weight:700">{i + 1}. {n}</text>')
        body.append(f'<text class="t-mut" x="{x + 2}" y="240" text-anchor="middle">f={f}</text>')
    return svg(620, 258, "".join(body), "A* search on the 2025 Q44 graph")


# ---------------------------------------------------------------- AI: games


@fig("ab-tree", "Alpha–beta on the classic tree [[3, 12, 8], [2, 4, 6], [14, 5, 2]], children searched left to right. The first MIN node "
     "returns 3, so MAX's α becomes 3. At the second MIN node the first leaf is 2 ≤ α: MIN will return at most 2, which MAX "
     "will never choose, so the leaves 4 and 6 are pruned (dashed). The root's minimax value is 3, the same as without pruning.")
def ab_tree():
    tree = [[3, 12, 8], [2, 4, 6], [14, 5, 2]]
    pruned = {(1, 1), (1, 2)}
    body = []
    root = (300, 34)
    mins = [(120, 110), (300, 110), (480, 110)]
    mvals = [3, "≤2", 2]
    def tri(x, y, up, label, hot=False):
        pts = f"{x},{y - 15} {x - 16},{y + 12} {x + 16},{y + 12}" if up else f"{x},{y + 15} {x - 16},{y - 12} {x + 16},{y - 12}"
        return [f'<polygon class="{"box-ink" if hot else "box"}" points="{pts}" style="stroke:var(--gd-ink)"/>',
                f'<text class="{"on-ink" if hot else "title"}" x="{x}" y="{y + (5 if up else 1)}" text-anchor="middle">{label}</text>']
    for i, (mx, my) in enumerate(mins):
        body.append(f'<line class="ax" x1="{root[0]}" y1="{root[1] + 12}" x2="{mx}" y2="{my - 12}"/>')
        for j, v in enumerate(tree[i]):
            lx, ly = mx + (j - 1) * 52, 200
            pr = (i, j) in pruned
            body.append(f'<line class="{"mut" if pr else "ax"}" x1="{mx}" y1="{my + 15}" x2="{lx}" y2="{ly - 12}"/>')
            body.append(f'<rect class="{"grid" if pr else "box"}" x="{lx - 13}" y="{ly - 12}" width="26" height="24" rx="3" style="{"stroke-dasharray:4 3" if pr else ""}"/>')
            body.append(f'<text class="{"t-mut" if pr else "title"}" x="{lx}" y="{ly + 4}" text-anchor="middle">{v}</text>')
            if pr:
                body.append(f'<text class="t-warn" x="{lx}" y="{ly + 28}" text-anchor="middle">pruned</text>')
        body += tri(mx, my, False, mvals[i])
    body += tri(root[0], root[1], True, 3, hot=True)
    body.append('<text class="t-mut" x="20" y="38">MAX</text><text class="t-mut" x="20" y="114">MIN</text>')
    body.append('<text class="t-ink" x="345" y="30">α = 3 after the first child</text>')
    body.append('<text class="t-warn" x="326" y="114" text-anchor="start">2 ≤ α = 3 → stop</text>')
    return svg(620, 245, "".join(body), "Alpha-beta pruning on a two-ply game tree")


# ---------------------------------------------------------------- injection


def main():
    pattern = re.compile(r"<!-- fig:([\w-]+) -->.*?<!-- /fig:\1 -->", re.S)
    used = set()
    for md in DOCS.rglob("*.md"):
        text = md.read_text()

        def repl(m):
            name = m.group(1)
            if name not in FIGS:
                raise SystemExit(f"{md}: unknown figure {name}")
            fn, cap = FIGS[name]
            used.add(name)
            return (
                f"<!-- fig:{name} -->\n<figure class=\"diagram\">{fn()}<figcaption>{cap}</figcaption></figure>\n"
                f"<!-- /fig:{name} -->"
            )

        new = pattern.sub(repl, text)
        if new != text:
            md.write_text(new)
            print("updated", md.relative_to(ROOT))
    unused = set(FIGS) - used
    if unused:
        print("figures defined but not placed:", ", ".join(sorted(unused)))


if __name__ == "__main__":
    random.seed(0)
    main()
