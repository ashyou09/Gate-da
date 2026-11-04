---
title: 11. Clustering — k-means, k-medoid, hierarchical
description: The k-means objective and Lloyd's algorithm, convergence and initialisation, convex cells, choosing k, k-medoids, agglomerative and divisive hierarchical clustering, single/complete/average linkage, dendrograms, and silhouette.
sidebar:
  label: 11. Clustering
  order: 11
---

**Why it matters:** clustering is the **most-asked ML topic** (5 questions in 3 years):
- 2024 Q19: which point must share a k-means cluster;
- 2024 Q42: a single-linkage dendrogram;
- 2025 Q30: single = min, complete = max;
- 2026 Q36: the first merge under Manhattan distance;
- 2026 Q23: k-medoid is a clustering algorithm.

Every one is solved by knowing the exact definition and tracing carefully.

## Topic map

<div class="mindmap">

- **Clustering**
  - Goal
    - group unlabelled points so similar points share a group
  - k-means
    - objective: WCSS $= \sum\|x - \mu_{c(x)}\|^2$
    - Lloyd: assign to the nearest centroid → recompute the means → repeat
    - WCSS never increases; converges to a **local** minimum
    - cells are convex (Voronoi); sensitive to initialisation, scale, outliers
    - choosing k: elbow, silhouette
  - k-medoid
    - centres are actual data points; any distance; robust to outliers
  - Hierarchical
    - agglomerative (bottom-up) / divisive (top-down)
    - linkage: single (min), complete (max), average, centroid, Ward
    - dendrogram; cut at a height to get clusters

</div>

## 11.1 What clustering is

Clustering is **unsupervised**: there are no labels. We look for groups where points **within** a group are close and points in **different** groups are far apart. "Close" depends entirely on the **distance measure** (Euclidean, Manhattan, cosine…), and changing it changes the answer.

- **Hard** clustering puts each point in exactly one cluster (k-means, hierarchical).
- **Soft** clustering gives membership probabilities (Gaussian mixture models).

## 11.2 k-means

<div class="formula">

**Objective:** choose $k$ centroids $\mu_1, \dots, \mu_k$ and an assignment $c(i)$ to minimise the **within-cluster sum of squares** (inertia)

$$
\text{WCSS} = \sum_{i=1}^{n}\big\|x_i - \mu_{c(i)}\big\|^2.
$$

**Lloyd's algorithm:**

1. **Initialise** $k$ centroids (for example, $k$ random data points).
2. **Assign:** put each point in the cluster of its nearest centroid.
3. **Update:** move each centroid to the **mean** of its assigned points.
4. Repeat steps 2–3 until the assignments stop changing.

Cost per iteration: $O(nkd)$.

</div>

<!-- fig:km-iterations -->
<figure class="diagram"><svg class="dg" viewBox="0 0 625 222" role="img" aria-label="k-means iterations" xmlns="http://www.w3.org/2000/svg"><text class="title" x="108" y="18" text-anchor="middle">round 1: assign</text><rect class="grid" x="16" y="30" width="185" height="165" rx="6"/><circle class="dot-ink" cx="44.0" cy="163.1" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="76.1" cy="152.4" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="30.2" cy="160.9" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="44.3" cy="159.0" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="30.7" cy="157.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="56.3" cy="140.7" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="57.4" cy="154.3" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="32.3" cy="132.0" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="26.4" cy="146.8" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="48.4" cy="172.1" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="43.9" cy="169.5" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="58.3" cy="162.3" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="73.6" cy="184.3" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="53.0" cy="172.3" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="63.8" cy="188.0" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="156.1" cy="143.9" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="140.3" cy="134.0" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="163.4" cy="133.7" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="174.2" cy="159.2" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="149.8" cy="149.2" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="171.3" cy="135.7" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="151.1" cy="154.4" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="149.8" cy="154.1" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="157.6" cy="148.3" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="189.5" cy="153.1" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="156.9" cy="140.8" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="147.7" cy="151.4" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="161.1" cy="136.7" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="142.7" cy="129.1" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="156.0" cy="144.5" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="114.1" cy="61.4" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="117.0" cy="67.6" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="102.1" cy="65.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="88.5" cy="54.3" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="91.6" cy="86.0" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="130.9" cy="71.6" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="86.0" cy="46.1" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="97.8" cy="56.2" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="90.8" cy="73.0" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="78.9" cy="94.3" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="88.8" cy="70.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="113.4" cy="38.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="88.0" cy="56.9" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="93.9" cy="71.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="81.8" cy="88.8" r="3.2" style="opacity:.85"/><path class="ax" style="stroke:var(--sl-color-white);stroke-width:3" d="M34.7,166.2 L46.7,178.2 M34.7,178.2 L46.7,166.2"/><path class="ax" style="stroke:var(--sl-color-white);stroke-width:3" d="M53.2,169.1 L65.2,181.1 M53.2,181.1 L65.2,169.1"/><path class="ax" style="stroke:var(--sl-color-white);stroke-width:3" d="M40.8,146.3 L52.8,158.3 M40.8,158.3 L52.8,146.3"/><text class="t-mut" x="108" y="212" text-anchor="middle">WCSS = 362.2</text><text class="title" x="313" y="18" text-anchor="middle">round 2</text><rect class="grid" x="221" y="30" width="185" height="165" rx="6"/><circle class="dot-ink" cx="249.0" cy="163.1" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="281.1" cy="152.4" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="235.2" cy="160.9" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="249.3" cy="159.0" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="235.7" cy="157.8" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="261.3" cy="140.7" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="262.4" cy="154.3" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="237.3" cy="132.0" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="231.4" cy="146.8" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="253.4" cy="172.1" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="248.9" cy="169.5" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="263.3" cy="162.3" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="278.6" cy="184.3" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="258.0" cy="172.3" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="268.8" cy="188.0" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="361.1" cy="143.9" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="345.3" cy="134.0" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="368.4" cy="133.7" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="379.2" cy="159.2" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="354.8" cy="149.2" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="376.3" cy="135.7" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="356.1" cy="154.4" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="354.8" cy="154.1" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="362.6" cy="148.3" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="394.5" cy="153.1" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="361.9" cy="140.8" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="352.7" cy="151.4" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="366.1" cy="136.7" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="347.7" cy="129.1" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="361.0" cy="144.5" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="319.1" cy="61.4" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="322.0" cy="67.6" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="307.1" cy="65.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="293.5" cy="54.3" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="296.6" cy="86.0" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="335.9" cy="71.6" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="291.0" cy="46.1" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="302.8" cy="56.2" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="295.8" cy="73.0" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="283.9" cy="94.3" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="293.8" cy="70.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="318.4" cy="38.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="293.0" cy="56.9" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="298.9" cy="71.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="286.8" cy="88.8" r="3.2" style="opacity:.85"/><path class="ax" style="stroke:var(--sl-color-white);stroke-width:3" d="M240.6,160.4 L252.6,172.4 M240.6,172.4 L252.6,160.4"/><path class="ax" style="stroke:var(--sl-color-white);stroke-width:3" d="M336.7,145.3 L348.7,157.3 M336.7,157.3 L348.7,145.3"/><path class="ax" style="stroke:var(--sl-color-white);stroke-width:3" d="M280.2,87.0 L292.2,99.0 M280.2,99.0 L292.2,87.0"/><text class="t-mut" x="313" y="212" text-anchor="middle">WCSS = 44.3</text><text class="title" x="518" y="18" text-anchor="middle">round 4: converged</text><rect class="grid" x="426" y="30" width="185" height="165" rx="6"/><circle class="dot-ink" cx="454.0" cy="163.1" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="486.1" cy="152.4" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="440.2" cy="160.9" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="454.3" cy="159.0" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="440.7" cy="157.8" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="466.3" cy="140.7" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="467.4" cy="154.3" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="442.3" cy="132.0" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="436.4" cy="146.8" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="458.4" cy="172.1" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="453.9" cy="169.5" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="468.3" cy="162.3" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="483.6" cy="184.3" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="463.0" cy="172.3" r="3.2" style="opacity:.85"/><circle class="dot-ink" cx="473.8" cy="188.0" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="566.1" cy="143.9" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="550.3" cy="134.0" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="573.4" cy="133.7" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="584.2" cy="159.2" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="559.8" cy="149.2" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="581.3" cy="135.7" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="561.1" cy="154.4" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="559.8" cy="154.1" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="567.6" cy="148.3" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="599.5" cy="153.1" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="566.9" cy="140.8" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="557.7" cy="151.4" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="571.1" cy="136.7" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="552.7" cy="129.1" r="3.2" style="opacity:.85"/><circle class="dot-warn" cx="566.0" cy="144.5" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="524.1" cy="61.4" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="527.0" cy="67.6" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="512.1" cy="65.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="498.5" cy="54.3" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="501.6" cy="86.0" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="540.9" cy="71.6" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="496.0" cy="46.1" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="507.8" cy="56.2" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="500.8" cy="73.0" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="488.9" cy="94.3" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="498.8" cy="70.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="523.4" cy="38.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="498.0" cy="56.9" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="503.9" cy="71.8" r="3.2" style="opacity:.85"/><circle class="dot-hl" cx="491.8" cy="88.8" r="3.2" style="opacity:.85"/><path class="ax" style="stroke:var(--sl-color-white);stroke-width:3" d="M453.2,155.0 L465.2,167.0 M453.2,167.0 L465.2,155.0"/><path class="ax" style="stroke:var(--sl-color-white);stroke-width:3" d="M561.8,138.6 L573.8,150.6 M561.8,150.6 L573.8,138.6"/><path class="ax" style="stroke:var(--sl-color-white);stroke-width:3" d="M501.6,60.9 L513.6,72.9 M501.6,72.9 L513.6,60.9"/><text class="t-mut" x="518" y="212" text-anchor="middle">WCSS = 18.7</text></svg><figcaption>k-means (k = 3) on 45 points from a deliberately bad start: all three centroids begin in the bottom-left. Each round assigns every point to its nearest centroid (colours), then moves each centroid ✕ to the mean of its points. The within-cluster sum of squares (WCSS) never increases, and here the centroids settle on the three groups by round 4.</figcaption></figure>
<!-- /fig:km-iterations -->

### Why it converges, and why only to a local minimum

- The **assign** step can't increase WCSS: each point moves to a centroid at least as close.
- The **update** step can't increase WCSS: the mean minimises the sum of squared distances to a set of points.
- WCSS never goes up, and there are only finitely many possible assignments, so the algorithm **must stop**.
- But it stops at a **local** minimum that depends on the initialisation. Standard practice is to run several random starts, or to use **k-means++** (spread the initial centroids out).

### The geometry: clusters are convex

Each point goes to its nearest centroid, so cluster $j$ is the region $\{x : \|x - \mu_j\| \le \|x - \mu_l\| \text{ for all } l\}$. That's an intersection of half-planes, so a **convex** polygon (a **Voronoi cell**).

**Consequence (2024 Q19):** if two points are in the same cluster, every point on the **segment between them** is in that cluster too.

### Limitations

- You must choose $k$. The **elbow method** plots WCSS against $k$ and picks where it stops dropping sharply. The **silhouette score** is another option (§11.5).
- k-means assumes roughly **spherical, similar-sized** clusters, because its cells are convex. It fails on rings or crescents.
- The **mean** is pulled by **outliers**.
- It's **scale-sensitive**, so standardise the features first.
- WCSS always decreases as $k$ grows (it's 0 at $k = n$), so you can't choose $k$ by minimising WCSS.

### A 1-D trace

Points 1, 2, 4, 7, 8, 10 with $k = 2$ and initial centroids 1 and 10.

- **Assign:** {1, 2, 4} → 1 and {7, 8, 10} → 10. (4 is closer to 1 than to 10.)
- **Update:** $\mu_1 = 7/3 \approx 2.33$ and $\mu_2 = 25/3 \approx 8.33$.
- **Assign again:** nothing changes, so it has **converged**.
- WCSS $= (1.78 + 0.11 + 2.78) + (1.78 + 0.11 + 2.78) = 9.33$.

## 11.3 k-medoids

Same idea, but each cluster centre must be an **actual data point**, the **medoid**: the member with the smallest total distance to the other members.

| | k-means | k-medoids (PAM) |
|---|---|---|
| Centre | mean (may not be a data point) | a real data point |
| Distance | squared Euclidean | **any** dissimilarity (Manhattan, edit distance…) |
| Outliers | pull the mean | **robust** |
| Cost | $O(nkd)$ per iteration | higher: $O(k(n - k)^2)$ per iteration for PAM |

Example: for {1, 2, 3, 4, 20}, the mean is **6** (dragged towards 20), but the medoid is **3**, with total distance $2 + 1 + 0 + 1 + 17 = 21$, the smallest of any member.

## 11.4 Hierarchical clustering

Instead of fixing $k$, build a whole **tree of merges** (a **dendrogram**), then cut it wherever you like.

- **Agglomerative (bottom-up):** start with every point as its own cluster, and repeatedly **merge the two closest clusters** until one remains. This is the usual method.
- **Divisive (top-down):** start with one cluster and repeatedly split it.

### Distance between two clusters: the linkage

<!-- fig:hc-linkage -->
<figure class="diagram"><svg class="dg" viewBox="0 0 640 240" role="img" aria-label="Single versus complete linkage" xmlns="http://www.w3.org/2000/svg"><ellipse class="grid" cx="75" cy="135" rx="45" ry="70"/><ellipse class="grid" cx="290" cy="115" rx="55" ry="70"/><circle class="dot-ink" cx="60" cy="90" r="6"/><circle class="dot-ink" cx="95" cy="140" r="6"/><circle class="dot-ink" cx="70" cy="175" r="6"/><rect class="dot-warn" x="244" y="104" width="12" height="12"/><rect class="dot-warn" x="294" y="64" width="12" height="12"/><rect class="dot-warn" x="314" y="154" width="12" height="12"/><line class="hl" x1="95" y1="140" x2="250" y2="110"/><text class="t-hl" x="172" y="112" text-anchor="middle">single = min</text><line class="ink" style="stroke-dasharray:6 4" x1="60" y1="90" x2="320" y2="160"/><text class="t-ink" x="215" y="158" text-anchor="middle">complete = max</text><text class="title" x="75" y="225" text-anchor="middle">cluster C₁</text><text class="title" x="290" y="205" text-anchor="middle">cluster C₂</text><text class="t-hl" x="400" y="50" style="font-weight:600">single</text><text x="480" y="50">min over pairs</text><text class="t-ink" x="400" y="84" style="font-weight:600">complete</text><text x="480" y="84">max over pairs</text><text class="t-mut" x="400" y="118" style="font-weight:600">average</text><text x="480" y="118">mean over all pairs</text><text class="t-mut" x="400" y="152" style="font-weight:600">centroid</text><text x="480" y="152">distance between means</text><text class="t-mut" x="400" y="186" style="font-weight:600">Ward</text><text x="480" y="186">increase in WCSS</text></svg><figcaption>Distance between two clusters. Single linkage uses the closest pair (min), complete linkage the farthest pair (max), average linkage the mean over all pairs. Single linkage can 'chain' long thin clusters together; complete linkage prefers compact, round clusters.</figcaption></figure>
<!-- /fig:hc-linkage -->

<div class="formula">

$$
d_{\text{single}}(C_1, C_2) = \min_{x \in C_1,\, y \in C_2} d(x, y) \qquad
d_{\text{complete}}(C_1, C_2) = \max_{x \in C_1,\, y \in C_2} d(x, y)
$$

$$
d_{\text{average}}(C_1, C_2) = \frac{1}{|C_1||C_2|}\sum_{x \in C_1}\sum_{y \in C_2} d(x, y)
$$

**Single** linkage gives long, "chained" clusters and is sensitive to noise bridges. **Complete** linkage gives compact clusters and is sensitive to outliers. **Ward** merges the pair that increases WCSS the least, which is close in spirit to k-means.

</div>

### Doing it by hand from a distance table

1. Find the **smallest** entry, and merge that pair.
2. Recompute the distance from the new cluster to every other cluster **using the linkage rule**. For single linkage that's the min of the two old rows; for complete linkage, the max.
3. Repeat. Record the distance at each merge: that's the **height** in the dendrogram.

<!-- fig:hc-dendrograms -->
<figure class="diagram"><svg class="dg" viewBox="0 0 620 265" role="img" aria-label="Single and complete linkage dendrograms" xmlns="http://www.w3.org/2000/svg"><text class="title" x="165.0" y="26" text-anchor="middle">single linkage (min)</text><line class="grid" x1="46" y1="230.0" x2="280" y2="230.0"/><text class="t-mut" x="42" y="234.0" text-anchor="end">0</text><line class="grid" x1="46" y1="198.3" x2="280" y2="198.3"/><text class="t-mut" x="42" y="202.3" text-anchor="end">1</text><line class="grid" x1="46" y1="166.7" x2="280" y2="166.7"/><text class="t-mut" x="42" y="170.7" text-anchor="end">2</text><line class="grid" x1="46" y1="135.0" x2="280" y2="135.0"/><text class="t-mut" x="42" y="139.0" text-anchor="end">3</text><line class="grid" x1="46" y1="103.3" x2="280" y2="103.3"/><text class="t-mut" x="42" y="107.3" text-anchor="end">4</text><line class="grid" x1="46" y1="71.7" x2="280" y2="71.7"/><text class="t-mut" x="42" y="75.7" text-anchor="end">5</text><line class="grid" x1="46" y1="40.0" x2="280" y2="40.0"/><text class="t-mut" x="42" y="44.0" text-anchor="end">6</text><path class="ink" style="stroke-width:2" d="M73.0,230.0 V198.3 H119.0 V230.0"/><path class="ink" style="stroke-width:2" d="M211.0,230.0 V198.3 H257.0 V230.0"/><path class="ink" style="stroke-width:2" d="M165.0,230.0 V166.7 H234.0 V198.3"/><path class="ink" style="stroke-width:2" d="M96.0,198.3 V135.0 H199.5 V166.7"/><text x="73.0" y="246.0" text-anchor="middle">x1</text><text x="119.0" y="246.0" text-anchor="middle">x2</text><text x="165.0" y="246.0" text-anchor="middle">x3</text><text x="211.0" y="246.0" text-anchor="middle">x4</text><text x="257.0" y="246.0" text-anchor="middle">x5</text><text class="title" x="475.0" y="26" text-anchor="middle">complete linkage (max)</text><line class="grid" x1="356" y1="230.0" x2="590" y2="230.0"/><text class="t-mut" x="352" y="234.0" text-anchor="end">0</text><line class="grid" x1="356" y1="198.3" x2="590" y2="198.3"/><text class="t-mut" x="352" y="202.3" text-anchor="end">1</text><line class="grid" x1="356" y1="166.7" x2="590" y2="166.7"/><text class="t-mut" x="352" y="170.7" text-anchor="end">2</text><line class="grid" x1="356" y1="135.0" x2="590" y2="135.0"/><text class="t-mut" x="352" y="139.0" text-anchor="end">3</text><line class="grid" x1="356" y1="103.3" x2="590" y2="103.3"/><text class="t-mut" x="352" y="107.3" text-anchor="end">4</text><line class="grid" x1="356" y1="71.7" x2="590" y2="71.7"/><text class="t-mut" x="352" y="75.7" text-anchor="end">5</text><line class="grid" x1="356" y1="40.0" x2="590" y2="40.0"/><text class="t-mut" x="352" y="44.0" text-anchor="end">6</text><path class="ink" style="stroke-width:2" d="M383.0,230.0 V198.3 H429.0 V230.0"/><path class="ink" style="stroke-width:2" d="M521.0,230.0 V198.3 H567.0 V230.0"/><path class="ink" style="stroke-width:2" d="M406.0,198.3 V103.3 H475.0 V230.0"/><path class="ink" style="stroke-width:2" d="M440.5,103.3 V40.0 H544.0 V198.3"/><text x="383.0" y="246.0" text-anchor="middle">x1</text><text x="429.0" y="246.0" text-anchor="middle">x2</text><text x="475.0" y="246.0" text-anchor="middle">x3</text><text x="521.0" y="246.0" text-anchor="middle">x4</text><text x="567.0" y="246.0" text-anchor="middle">x5</text><text class="t-mut" x="20" y="135" text-anchor="middle" transform="rotate(-90 20 135)">merge distance</text></svg><figcaption>The 2024 Q42 distance table clustered two ways. Single linkage (left) merges x1–x2 and x4–x5 at 1, then x3 joins {x4, x5} at 2 (its nearest member is x4), then everything joins at 3. Complete linkage (right) uses the farthest pair, so x3 joins {x1, x2} at 4 and the final merge is at 6. Same data, different trees.</figcaption></figure>
<!-- /fig:hc-dendrograms -->

**Cutting a dendrogram:** a horizontal cut at height $h$ gives one cluster per vertical line it crosses. In the single-linkage tree above, a cut at 1.5 gives {x1, x2}, {x3}, {x4, x5}: 3 clusters.

Cost: naive agglomerative clustering is $O(n^3)$ time and $O(n^2)$ memory for the distance matrix.

## 11.5 Judging a clustering

- **WCSS / inertia**: lower is tighter, but it always falls as $k$ grows.
- **Silhouette** of a point: $s = \dfrac{b - a}{\max(a, b)} \in [-1, 1]$, where $a$ is its mean distance to its own cluster and $b$ is its mean distance to the nearest *other* cluster. Close to 1 means well placed; close to 0 means on a border; negative means probably in the wrong cluster.

---

## Summary: important points

<div class="formula">

1. k-means minimises WCSS $= \sum\|x - \mu_{c(x)}\|^2$ by alternating **assign to the nearest** and **move to the mean**.
2. WCSS never increases, so k-means converges, but only to a **local** minimum that depends on the initialisation.
3. k-means cells are convex (Voronoi), so the segment between two members of a cluster stays in that cluster.
4. Choose $k$ by the elbow or silhouette. Scale the features. The mean is sensitive to outliers.
5. k-medoids uses actual data points and any distance, and it's robust to outliers.
6. Agglomerative clustering merges the closest clusters. Single = **min**, complete = **max**, average = mean over all pairs.
7. The dendrogram's height is the merge distance. A cut at height $h$ gives the clusters.
8. Silhouette $= (b - a)/\max(a, b)$.

</div>

<div class="trap">

- Single linkage uses the **closest** pair. Many students swap it with complete.
- In hierarchical questions, check **which distance** is used. 2026 Q36 used **Manhattan**, not Euclidean.
- k-means doesn't find the global optimum, and different starts can give different answers.
- Each k-means step updates **all** centroids from the assignments made at that step.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2025 Q30 (1 mark, MSQ)

DIS-1$(C_1, C_2) = \max D(x, y)$ and DIS-2$(C_1, C_2) = \min D(x, y)$, over $x \in C_1$, $y \in C_2$. Which are correct?
(A) Single linkage uses DIS-1 (B) Single linkage uses DIS-2 (C) Complete linkage uses DIS-2 (D) Complete linkage uses DIS-1

<details>
<summary>Show solution</summary>

**Answer: B; D**

Single = **min** (DIS-2). Complete = **max** (DIS-1).

</details>

### GATE DA 2026 Q36 (2 marks, MCQ)

P1 = (2, 3, −1), P2 = (3, 1, 1), P3 = (5, −2, 3), P4 = (3, 3, 3). Agglomerative clustering with **Manhattan** distance. Which two points are merged first?
(A) P1, P2 (B) P2, P3 (C) P3, P4 (D) P2, P4

<details>
<summary>Show solution</summary>

**Answer: (D) P2, P4**

Manhattan distances: P1–P2 $= 1 + 2 + 2 = 5$; P1–P3 $= 12$; P1–P4 $= 1 + 0 + 4 = 5$; P2–P3 $= 2 + 3 + 2 = 7$; **P2–P4 $= 0 + 2 + 2 = 4$**; P3–P4 $= 7$.

The smallest is P2–P4. The first merge doesn't depend on the linkage, since every cluster is still a single point.

</details>

### GATE DA 2024 Q42 (2 marks, MCQ)

Single-linkage clustering on x1…x5 with this distance table. Which dendrogram is produced?

| | x1 | x2 | x3 | x4 | x5 |
|---|---|---|---|---|---|
| x1 | 0 | 1 | 4 | 3 | 6 |
| x2 | 1 | 0 | 3 | 5 | 3 |
| x3 | 4 | 3 | 0 | 2 | 5 |
| x4 | 3 | 5 | 2 | 0 | 1 |
| x5 | 6 | 3 | 5 | 1 | 0 |

<details>
<summary>Show solution</summary>

**Answer: (A)**, the dendrogram on the left of the figure in §11.4.

1. The smallest entries are $d(x1, x2) = 1$ and $d(x4, x5) = 1$. Merge both at height 1.
2. Single-linkage distances to the new clusters:
   - $d(\{1,2\}, 3) = \min(4, 3) = 3$
   - $d(\{1,2\}, \{4,5\}) = \min(3, 6, 5, 3) = 3$
   - $d(3, \{4,5\}) = \min(2, 5) = 2$

   The smallest is 2, so **x3 joins {x4, x5}** at height 2.
3. $d(\{1,2\}, \{3,4,5\}) = \min(4, 3, 3, 5, 6, 3) = 3$. The final merge is at height 3.

</details>

### GATE DA 2024 Q19 (1 mark, MCQ)

k-means with $k = 3$ on 100 points. $(1, 1)$ and $(-1, 1)$ are both in cluster 3. Which point is **necessarily** also in cluster 3?
(A) (0, 0) (B) (0, 2) (C) (2, 0) (D) (0, 1)

<details>
<summary>Show solution</summary>

**Answer: (D) (0, 1)**

The final k-means cells are convex (§11.2), and $(0, 1)$ is the **midpoint** of the segment joining the two given points. Here's the direct argument: if $\|p - \mu_3\| \le \|p - \mu_j\|$ holds for $p = (1, 1)$ and for $p = (-1, 1)$, it also holds for every point between them, because each such condition defines a half-plane.

The other points lie off that segment, so they could belong to another cluster depending on where the other centroids are.

</details>

### GATE DA 2026 Q23 (1 mark, MSQ)

Match tasks to algorithms. **Answer: (B)**, with clustering → k-medoid. The full solution is in [topic 1](/machine-learning/ml-foundations/#gate-da-2026-q23-1-mark-msq).

---

## Test yourself (B): predicted 2027-style questions

**F1 (2 marks, MCQ).** Using **complete** linkage on the 2024 Q42 table, at what height does x3 first join a cluster, and which one?
(A) 2, with {x4, x5} (B) 4, with {x1, x2} (C) 3, with {x1, x2} (D) 5, with {x4, x5}

<details>
<summary>Show solution</summary>

**Answer: (B)**

After the merges at height 1:

- $d(\{1,2\}, 3) = \max(4, 3) = 4$
- $d(3, \{4,5\}) = \max(2, 5) = 5$
- $d(\{1,2\}, \{4,5\}) = \max(3, 6, 5, 3) = 6$

The smallest is 4, so x3 joins {x1, x2} at height 4. The final merge is at 6.

</details>

**F2 (2 marks, NAT).** 1-D k-means on 1, 2, 4, 7, 8, 10 with $k = 2$ and initial centroids 1 and 10. What is the final WCSS? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 9.33**

From §11.2: the clusters are {1, 2, 4} (mean 7/3) and {7, 8, 10} (mean 25/3), giving WCSS $= 14/3 + 14/3 = 9.33$.

</details>

**F3 (1 mark, NAT).** What is the medoid of {1, 2, 3, 4, 20} under absolute distance?

<details>
<summary>Show solution</summary>

**Answer: 3**

Total distance from each candidate: 1 → 25, 2 → 22, **3 → 21**, 4 → 22, 20 → 70. The mean would be 6.

</details>

**F4 (1 mark, NAT).** A point's mean distance to its own cluster is 2, and to the nearest other cluster 5. What is its silhouette value?

<details>
<summary>Show solution</summary>

**Answer: 0.6**

$(5 - 2)/\max(2, 5) = 3/5 = $ **0.6**.

</details>

**F5 (2 marks, MSQ).** Which statements about k-means are true?
(A) The WCSS never increases from one iteration to the next (B) It always finds the global minimum of WCSS (C) The WCSS at the optimum decreases as $k$ increases (D) Results depend on the initial centroids

<details>
<summary>Show solution</summary>

**Answer: A; C; D**

(B) is false: k-means converges to a **local** minimum.

</details>

**F6 (1 mark, NAT).** The single-linkage dendrogram of 2024 Q42 is cut at height 2.5. How many clusters result?

<details>
<summary>Show solution</summary>

**Answer: 2**

The merges at heights 1, 1 and 2 lie below the cut, and the merge at 3 lies above it. That leaves {x1, x2} and {x3, x4, x5}: **2** clusters.

</details>
