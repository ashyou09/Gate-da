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
