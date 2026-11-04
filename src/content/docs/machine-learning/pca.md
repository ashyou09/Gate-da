---
title: 12. PCA & dimensionality reduction
description: Why reduce dimensions, PCA as maximum-variance projection, the covariance eigenvalue problem, orthogonal components, explained variance and scree plots, reconstruction error, the SVD connection, and when PCA fails.
sidebar:
  label: 12. PCA
  order: 12
---

**Why it matters:** PCA appeared **every year**:
- 2024 Q18: PCA is dimensionality reduction;
- 2025 Q60: the variance along the top direction **equals the top eigenvalue**;
- 2026 Q11: principal components are **orthogonal**, so the angle is 90°.

PCA is also where Linear Algebra (eigenvalues, SVD) meets ML, so the questions can come from either side.

## Topic map

<div class="mindmap">

- **PCA**
  - Why
    - visualise, remove noise, speed up, fight the curse of dimensionality
  - Setup
    - centre the data; covariance $C = \frac1n X^\top X$
  - First component
    - maximise $u^\top Cu$ s.t. $\|u\| = 1$ → $Cu = \lambda u$
    - the variance along $u$ equals $\lambda$, so take the largest
  - All components
    - eigenvectors of $C$, sorted by eigenvalue
    - $C$ symmetric → the components are **orthogonal**, the scores uncorrelated
  - Choosing k
    - explained variance $\lambda_j / \sum\lambda$, scree plot
    - reconstruction error $= \sum_{j > k}\lambda_j$
  - SVD link
    - $X = U\Sigma V^\top$ → PCs = columns of $V$, $\lambda = \sigma^2/n$
  - Caveats
    - scale the features; linear only; ignores labels

</div>

## 12.1 Why reduce dimensions?

Real data often has many correlated features. Height in cm and height in inches carry the same information. A 100-pixel image of a digit doesn't really have 100 independent "degrees of freedom". **Dimensionality reduction** finds a few new features that keep most of the information. That lets you **visualise** data in 2-D, **denoise** it, **speed up** later models, and fight the **curse of dimensionality** (topic 6).

- **Feature selection** keeps a subset of the original features (lasso does this, topic 3).
- **Feature extraction** builds new features from combinations of the old ones. PCA and LDA both do this.

## 12.2 The setup

1. **Centre** the data: subtract the mean of each feature, so $\sum_i x_i = 0$.
2. The **covariance matrix** is $C = \frac1n\sum_i x_ix_i^\top = \frac1n X^\top X$ (a $d \times d$ matrix). Some books divide by $n - 1$; that scales every eigenvalue equally and changes no direction.

$C$ is **symmetric** and **positive semi-definite**, so its eigenvalues are real and $\ge 0$, and its eigenvectors can be chosen **orthonormal**.

## 12.3 The first principal component: maximum variance

Project every point onto a unit direction $u$: $z_i = u^\top x_i$. The variance of these projected values is

$$
\frac1n\sum_i (u^\top x_i)^2 = u^\top\Big(\frac1n\sum_i x_ix_i^\top\Big)u = u^\top C\,u.
$$

Maximise $u^\top Cu$ subject to $u^\top u = 1$, using a Lagrange multiplier:

$$
\nabla_u\big[u^\top Cu - \lambda(u^\top u - 1)\big] = 2Cu - 2\lambda u = 0 \quad\Longrightarrow\quad Cu = \lambda u.
$$

<div class="formula">

- The optimal $u$ is an **eigenvector** of $C$.
- At an eigenvector, the projected variance is $u^\top Cu = u^\top(\lambda u) = \lambda$. **The variance along a principal direction equals its eigenvalue.**
- So **PC1 = the eigenvector with the largest eigenvalue**, and its variance is $\lambda_1$ (2025 Q60).
- **PC2** maximises the variance among directions **orthogonal** to PC1. That's the eigenvector of the second-largest eigenvalue, and so on.

</div>

**Why the components are orthogonal (2026 Q11):** eigenvectors of a symmetric matrix for different eigenvalues are always orthogonal. If $Cu = \lambda u$ and $Cv = \mu v$ with $\lambda \ne \mu$, then $\lambda\,u^\top v = u^\top Cv = \mu\,u^\top v$, which forces $u^\top v = 0$. So **any two principal components meet at 90°**, the first and the tenth included. The projected scores along different components are also **uncorrelated**.

<!-- fig:pca-axes -->
<figure class="diagram"><svg class="dg" viewBox="0 0 600 320" role="img" aria-label="Principal component axes on correlated data" xmlns="http://www.w3.org/2000/svg"><rect class="grid" x="30" y="20" width="340" height="280" rx="6"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="199.1" y1="173.1" x2="193.4" y2="164.7"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="181.8" y1="188.9" x2="174.6" y2="178.3"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="135.4" y1="184.1" x2="145.7" y2="199.2"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="282.7" y1="58.9" x2="301.7" y2="86.7"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="182.9" y1="202.0" x2="169.3" y2="182.1"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="225.6" y1="157.8" x2="218.2" y2="146.9"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="234.0" y1="151.8" x2="226.6" y2="140.9"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="211.0" y1="207.9" x2="185.5" y2="170.5"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="279.9" y1="113.3" x2="274.9" y2="106.0"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="273.2" y1="80.4" x2="285.5" y2="98.4"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="283.6" y1="116.9" x2="275.8" y2="105.4"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="302.0" y1="74.7" x2="307.4" y2="82.6"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="220.9" y1="162.1" x2="213.0" y2="150.6"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="199.7" y1="117.5" x2="219.2" y2="146.2"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="159.6" y1="170.6" x2="168.1" y2="183.0"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="276.2" y1="82.2" x2="286.6" y2="97.5"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="93.1" y1="212.6" x2="104.2" y2="229.0"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="176.4" y1="128.3" x2="198.7" y2="161.0"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="243.6" y1="107.8" x2="253.1" y2="121.7"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="103.0" y1="190.1" x2="121.2" y2="216.8"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="287.7" y1="85.2" x2="293.0" y2="92.9"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="255.6" y1="109.6" x2="260.3" y2="116.6"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="162.7" y1="222.6" x2="146.4" y2="198.7"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="335.4" y1="118.4" x2="309.8" y2="80.8"/><line class="grid" style="stroke:var(--gd-trap);stroke-opacity:.6" x1="236.7" y1="111.0" x2="247.0" y2="126.1"/><circle class="dot" cx="199.1" cy="173.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="257.4" cy="186.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="92.0" cy="204.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="207.5" cy="127.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="194.8" cy="177.4" r="2.4" style="opacity:.55"/><circle class="dot" cx="155.2" cy="200.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="229.8" cy="157.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="179.3" cy="175.4" r="2.4" style="opacity:.55"/><circle class="dot" cx="181.8" cy="188.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="207.6" cy="177.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="155.2" cy="185.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="178.6" cy="160.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="242.9" cy="99.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="118.0" cy="269.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="312.5" cy="116.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="156.1" cy="186.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="135.4" cy="184.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="186.6" cy="158.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="198.1" cy="131.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="266.1" cy="118.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="163.5" cy="129.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="256.4" cy="146.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="217.1" cy="114.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="195.0" cy="120.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="282.7" cy="58.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="167.9" cy="224.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="176.4" cy="137.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="182.9" cy="139.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="74.5" cy="244.4" r="2.4" style="opacity:.55"/><circle class="dot" cx="227.0" cy="159.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="170.7" cy="184.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="212.3" cy="150.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="182.9" cy="202.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="315.3" cy="142.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="138.3" cy="201.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="123.3" cy="215.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="233.3" cy="116.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="223.2" cy="176.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="222.5" cy="85.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="177.3" cy="161.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="225.6" cy="157.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="156.8" cy="192.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="242.8" cy="127.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="245.8" cy="115.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="154.8" cy="216.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="136.9" cy="225.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="205.4" cy="177.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="212.4" cy="145.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="234.0" cy="151.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="248.3" cy="144.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="286.7" cy="98.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="167.9" cy="153.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="133.3" cy="133.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="191.5" cy="176.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="119.2" cy="250.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="164.8" cy="212.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="211.0" cy="207.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="157.1" cy="194.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="228.0" cy="84.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="161.2" cy="184.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="240.8" cy="126.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="199.8" cy="134.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="169.6" cy="200.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="237.6" cy="143.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="279.9" cy="113.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="196.6" cy="138.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="144.5" cy="223.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="179.2" cy="185.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="94.6" cy="238.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="188.7" cy="193.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="240.7" cy="119.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="216.5" cy="133.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="273.2" cy="80.4" r="2.4" style="opacity:.55"/><circle class="dot" cx="223.9" cy="86.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="201.0" cy="122.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="267.8" cy="91.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="254.5" cy="129.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="204.7" cy="162.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="177.3" cy="151.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="168.9" cy="183.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="283.6" cy="116.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="241.7" cy="189.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="165.9" cy="189.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="201.2" cy="126.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="163.8" cy="177.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="249.1" cy="109.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="196.1" cy="186.4" r="2.4" style="opacity:.55"/><circle class="dot" cx="140.3" cy="186.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="302.0" cy="74.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="251.1" cy="82.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="175.3" cy="209.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="246.0" cy="118.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="192.4" cy="116.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="167.1" cy="190.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="200.3" cy="218.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="173.2" cy="150.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="220.9" cy="162.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="144.5" cy="139.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="206.7" cy="185.4" r="2.4" style="opacity:.55"/><circle class="dot" cx="153.1" cy="249.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="183.7" cy="186.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="165.3" cy="208.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="128.6" cy="202.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="319.0" cy="125.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="199.7" cy="117.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="194.0" cy="159.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="203.4" cy="131.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="178.0" cy="164.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="235.8" cy="93.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="149.2" cy="234.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="72.0" cy="232.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="253.7" cy="173.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="159.6" cy="170.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="257.7" cy="166.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="151.5" cy="211.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="185.8" cy="81.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="77.7" cy="221.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="216.0" cy="124.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="318.4" cy="62.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="259.1" cy="150.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="276.2" cy="82.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="194.7" cy="155.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="169.8" cy="205.4" r="2.4" style="opacity:.55"/><circle class="dot" cx="290.7" cy="141.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="208.2" cy="127.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="200.2" cy="136.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="269.4" cy="117.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="258.9" cy="149.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="93.1" cy="212.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="251.9" cy="140.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="224.9" cy="181.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="197.2" cy="198.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="235.2" cy="160.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="245.2" cy="162.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="296.8" cy="111.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="241.0" cy="134.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="176.4" cy="128.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="163.0" cy="192.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="173.6" cy="197.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="118.6" cy="202.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="261.2" cy="86.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="197.1" cy="240.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="247.0" cy="134.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="316.6" cy="99.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="243.6" cy="107.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="148.9" cy="116.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="205.7" cy="117.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="193.6" cy="153.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="288.7" cy="146.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="230.6" cy="110.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="110.9" cy="206.4" r="2.4" style="opacity:.55"/><circle class="dot" cx="187.5" cy="191.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="103.0" cy="190.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="229.7" cy="135.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="232.5" cy="87.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="181.8" cy="173.4" r="2.4" style="opacity:.55"/><circle class="dot" cx="174.2" cy="162.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="240.4" cy="163.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="292.7" cy="138.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="146.3" cy="130.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="287.7" cy="85.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="194.1" cy="190.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="206.4" cy="184.9" r="2.4" style="opacity:.55"/><circle class="dot" cx="147.7" cy="214.7" r="2.4" style="opacity:.55"/><circle class="dot" cx="186.7" cy="146.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="249.1" cy="173.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="218.3" cy="119.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="202.7" cy="147.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="255.6" cy="109.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="163.3" cy="183.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="105.5" cy="235.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="278.4" cy="145.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="142.6" cy="202.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="142.6" cy="186.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="99.4" cy="195.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="217.3" cy="135.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="162.7" cy="222.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="109.2" cy="189.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="153.4" cy="198.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="201.6" cy="189.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="206.8" cy="169.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="204.0" cy="168.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="170.2" cy="143.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="256.4" cy="85.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="335.4" cy="118.4" r="2.4" style="opacity:.55"/><circle class="dot" cx="207.6" cy="150.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="201.8" cy="205.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="202.9" cy="150.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="137.9" cy="207.3" r="2.4" style="opacity:.55"/><circle class="dot" cx="187.9" cy="195.5" r="2.4" style="opacity:.55"/><circle class="dot" cx="217.6" cy="156.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="179.0" cy="202.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="236.7" cy="111.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="103.3" cy="219.0" r="2.4" style="opacity:.55"/><circle class="dot" cx="190.7" cy="174.2" r="2.4" style="opacity:.55"/><circle class="dot" cx="137.5" cy="188.1" r="2.4" style="opacity:.55"/><circle class="dot" cx="107.0" cy="217.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="258.8" cy="128.8" r="2.4" style="opacity:.55"/><circle class="dot" cx="270.4" cy="140.6" r="2.4" style="opacity:.55"/><circle class="dot" cx="124.6" cy="189.8" r="2.4" style="opacity:.55"/><line class="ink" style="stroke-width:3.2" x1="303.4" y1="85.5" x2="96.6" y2="234.5"/><text class="t-ink" x="102.6" y="230.5">PC1</text><line class="hl" style="stroke-width:3.2" x1="172.1" y1="118.9" x2="227.9" y2="201.1"/><text class="t-hl" x="233.9" y="197.1">PC2</text><text class="t-mut" x="395" y="60">covariance eigenvalues</text><text class="t-ink" x="395" y="90">λ₁ = 3.44</text><text class="t-hl" x="395" y="120">λ₂ = 0.51</text><text class="t-ink" x="395" y="150">PC1 explains 87%</text><text class="t-mut" x="395" y="180">PC1 ⟂ PC2 (angle 90°)</text></svg><figcaption>200 correlated points with their principal components. PC1 (blue) points along the direction of greatest spread; PC2 (yellow) is perpendicular to it. Each axis extends 2√λ on either side of the mean. Projecting onto PC1 alone keeps most of the variance; the short perpendicular segments are what that projection throws away (the reconstruction error).</figcaption></figure>
<!-- /fig:pca-axes -->

## 12.4 The same answer from minimising reconstruction error

Another way to see it: find the $k$-dimensional subspace that best approximates the data, minimising the total squared **perpendicular** distance from each point to the subspace. The answer is the same top-$k$ eigenvectors. Maximising the variance kept and minimising the information thrown away are the same problem, because the two always add up to the total variance.

<div class="formula">

$$
\text{total variance} = \operatorname{trace}(C) = \sum_{j=1}^{d}\lambda_j
$$

$$
\text{explained variance ratio of PC}_j = \frac{\lambda_j}{\sum_i\lambda_i}, \qquad
\text{mean squared reconstruction error keeping } k = \sum_{j > k}\lambda_j
$$

</div>

### Choosing k

<!-- fig:pca-scree -->
<figure class="diagram"><svg class="dg" viewBox="0 0 520 285" role="img" aria-label="Scree plot and cumulative explained variance" xmlns="http://www.w3.org/2000/svg"><path class="ax" d="M60,20 V240 H480"/><text x="270.0" y="272" text-anchor="middle">principal component</text><text x="20" y="130.0" text-anchor="middle" transform="rotate(-90 20 130.0)">fraction of variance</text><line class="grid" x1="60.0" y1="187.6" x2="480.0" y2="187.6"/><text class="t-mut" x="54.0" y="191.6" text-anchor="end">0.25</text><line class="grid" x1="60.0" y1="135.2" x2="480.0" y2="135.2"/><text class="t-mut" x="54.0" y="139.2" text-anchor="end">0.5</text><line class="grid" x1="60.0" y1="82.9" x2="480.0" y2="82.9"/><text class="t-mut" x="54.0" y="86.9" text-anchor="end">0.75</text><line class="grid" x1="60.0" y1="51.4" x2="480.0" y2="51.4"/><text class="t-mut" x="54.0" y="55.4" text-anchor="end">0.9</text><line class="grid" x1="60.0" y1="30.5" x2="480.0" y2="30.5"/><text class="t-mut" x="54.0" y="34.5" text-anchor="end">1</text><rect class="box-ink" x="86.5" y="135.2" width="44" height="104.8" rx="3" style="opacity:.85"/><text class="t-mut" x="108.5" y="255.0" text-anchor="middle">1</text><rect class="box-ink" x="167.2" y="187.6" width="44" height="52.4" rx="3" style="opacity:.85"/><text class="t-mut" x="189.2" y="255.0" text-anchor="middle">2</text><rect class="box-ink" x="248.0" y="213.8" width="44" height="26.2" rx="3" style="opacity:.85"/><text class="t-mut" x="270.0" y="255.0" text-anchor="middle">3</text><rect class="box-ink" x="328.8" y="226.9" width="44" height="13.1" rx="3" style="opacity:.85"/><text class="t-mut" x="350.8" y="255.0" text-anchor="middle">4</text><rect class="box-ink" x="409.5" y="226.9" width="44" height="13.1" rx="3" style="opacity:.85"/><text class="t-mut" x="431.5" y="255.0" text-anchor="middle">5</text><polyline class="hl" points="108.5,135.2 189.2,82.9 270.0,56.7 350.8,43.6 431.5,30.5"/><circle class="dot-hl" cx="108.5" cy="135.2" r="4"/><text class="t-hl" x="108.5" y="126.2" text-anchor="middle">0.5</text><circle class="dot-hl" cx="189.2" cy="82.9" r="4"/><text class="t-hl" x="189.2" y="73.9" text-anchor="middle">0.75</text><circle class="dot-hl" cx="270.0" cy="56.7" r="4"/><text class="t-hl" x="270.0" y="47.7" text-anchor="middle">0.875</text><circle class="dot-hl" cx="350.8" cy="43.6" r="4"/><text class="t-hl" x="350.8" y="34.6" text-anchor="middle">0.938</text><circle class="dot-hl" cx="431.5" cy="30.5" r="4"/><text class="t-hl" x="431.5" y="21.5" text-anchor="middle">1</text><text class="t-warn" x="476.0" y="65.4" text-anchor="end">90% line</text></svg><figcaption>A scree plot for eigenvalues 4, 2, 1, 0.5, 0.5 (total 8). Bars show each component's share of the variance (50%, 25%, 12.5%, 6.25%, 6.25%); the line is the cumulative share. Keeping 90% of the variance needs 4 components.</figcaption></figure>
<!-- /fig:pca-scree -->

- Keep enough components to reach a cumulative share of 90–95%, or
- look for the **elbow** in the scree plot, where the eigenvalues level off.

## 12.5 The algorithm

1. Centre the data (and **standardise** it if the features have different units).
2. Compute the covariance $C = \frac1nX^\top X$.
3. Find the eigenvalues and eigenvectors of $C$ and sort them in decreasing order of eigenvalue.
4. Keep the top $k$ eigenvectors as the columns of $U_k$ ($d \times k$).
5. **Project:** $z = U_k^\top(x - \mu)$, the new $k$-dimensional features.
6. **Reconstruct** (if needed): $\hat x = \mu + U_kz$.

### Worked example

Centred points: $(2, 2), (-2, -2), (1, -1), (-1, 1)$.

- $C = \frac14\sum x x^\top = \frac14\begin{pmatrix}4 + 4 + 1 + 1 & 4 + 4 - 1 - 1\\ \cdot & 4 + 4 + 1 + 1\end{pmatrix} = \begin{pmatrix}2.5 & 1.5\\ 1.5 & 2.5\end{pmatrix}$
- Eigenvalues: $2.5 \pm 1.5$, so $\lambda_1 = 4$ and $\lambda_2 = 1$. For a matrix $\begin{pmatrix}a & b\\ b & a\end{pmatrix}$, the eigenvalues are $a \pm b$, with eigenvectors $(1, 1)/\sqrt2$ and $(1, -1)/\sqrt2$.
- **PC1** $= (1, 1)/\sqrt2$ with variance 4. **PC2** $= (1, -1)/\sqrt2$ with variance 1. They're orthogonal.
- PC1 explains $4/5 = 80\%$ of the variance.
- Scores on PC1: $2\sqrt2, -2\sqrt2, 0, 0$. Their variance is $(8 + 8 + 0 + 0)/4 = 4 = \lambda_1$. ✓

## 12.6 The SVD connection

Write the centred data matrix ($n \times d$) as $X = U\Sigma V^\top$. Then

$$
C = \frac1nX^\top X = \frac1n V\Sigma^\top U^\top U\Sigma V^\top = V\,\frac{\Sigma^2}{n}\,V^\top.
$$

<div class="formula">

- The **principal directions** are the **right singular vectors** (the columns of $V$).
- The **eigenvalues** are $\lambda_j = \sigma_j^2/n$, where $\sigma_j$ are the singular values.
- The **scores** are $XV = U\Sigma$.
- In practice PCA is computed with the SVD, which is more numerically stable than forming $X^\top X$.

</div>

## 12.7 When to be careful

- **Scale matters.** A feature in rupees has a huge variance and will dominate PC1. Standardise first, which is the same as running PCA on the **correlation** matrix.
- **Unsupervised.** PCA ignores labels, so it may throw away a low-variance direction that separates the classes. LDA wouldn't (topic 7).
- **Linear.** It finds flat subspaces only. Curved structure needs kernel PCA or other non-linear methods.
- **The sign is arbitrary.** $u$ and $-u$ are equally valid principal components.
- At most $\min(n - 1, d)$ components have non-zero variance.

---

## Summary: important points

<div class="formula">

1. Centre the data. $C = \frac1nX^\top X$ is symmetric and PSD.
2. Principal components are eigenvectors of $C$, sorted by eigenvalue. The variance along PC$_j$ is $\lambda_j$.
3. The components are mutually **orthogonal** (90°), and their scores are uncorrelated.
4. Total variance $= \operatorname{trace}(C) = \sum\lambda_j$. Explained ratio $= \lambda_j/\sum\lambda$.
5. Keeping $k$ components loses $\sum_{j > k}\lambda_j$ (mean squared reconstruction error).
6. Maximising the kept variance is the same as minimising the reconstruction error.
7. SVD: PCs = right singular vectors, $\lambda_j = \sigma_j^2/n$.
8. Standardise the features. PCA is unsupervised and linear.

</div>

<div class="trap">

- Variance along a direction is $u^\top Cu$, which equals $\lambda$ only when $u$ is a **unit eigenvector**.
- Principal components are orthogonal, so **any** pair is at 90°, not just consecutive ones.
- Don't confuse eigenvalues (variances) with singular values. $\lambda = \sigma^2/n$.
- PCA without centring gives the wrong directions.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2026 Q11 (1 mark, MCQ)

PCA reduces 100 features to 10. What is the angle $\theta$ between the first and the tenth principal components?
(A) 0° (B) 90° (C) 90° < θ ≤ 180° (D) 0 < θ < 90°

<details>
<summary>Show solution</summary>

**Answer: (B) 90°**

Principal components are eigenvectors of the symmetric covariance matrix, so they're mutually orthogonal (§12.3).

</details>

### GATE DA 2025 Q60 (2 marks, NAT)

$n$ observations $x^{(i)} \in \mathbb{R}^{100}$ with $\sum_i x^{(i)} = 0$. The covariance matrix has eigenvalues $\lambda_i = 100^{2-i}$ for $1 \le i \le 100$. $u$ is the unit direction of maximum variance. What is $\frac1n\sum_i (u^\top x^{(i)})^2$?

<details>
<summary>Show solution</summary>

**Answer: 100**

The data is centred, so the expression is the variance along $u$, which is $u^\top Cu$. For the direction of maximum variance, this equals the **largest** eigenvalue.

The eigenvalues are $100^{1}, 100^{0}, 100^{-1}, \dots$, a decreasing sequence. The largest is $\lambda_1 = 100^{2-1} = $ **100**.

</details>

### GATE DA 2024 Q18 (1 mark, MCQ)

Match PCA, naive Bayes and logistic regression with dimensionality reduction, generative and discriminative. **Answer: (C)**, with PCA → dimensionality reduction. The full solution is in [topic 1](/machine-learning/ml-foundations/#gate-da-2024-q18-1-mark-mcq).

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** The covariance eigenvalues are 5, 3, 1, 1. What fraction of the total variance do the first two principal components explain?

<details>
<summary>Show solution</summary>

**Answer: 0.8**

$(5 + 3)/(5 + 3 + 1 + 1) = 8/10 = $ **0.8**.

</details>

**F2 (1 mark, NAT).** For the eigenvalues in F1, what is the mean squared reconstruction error if only PC1 is kept?

<details>
<summary>Show solution</summary>

**Answer: 5**

It's the sum of the discarded eigenvalues: $3 + 1 + 1 = $ **5**.

</details>

**F3 (2 marks, MCQ).** The covariance matrix is $\begin{pmatrix}3 & 1\\ 1 & 3\end{pmatrix}$. What are the first principal direction and the variance along it?
(A) $(1, 1)/\sqrt2$, 4 (B) $(1, -1)/\sqrt2$, 4 (C) $(1, 1)/\sqrt2$, 2 (D) $(1, 0)$, 3

<details>
<summary>Show solution</summary>

**Answer: (A)**

For $\begin{pmatrix}a & b\\ b & a\end{pmatrix}$ the eigenvalues are $a \pm b = 4, 2$. The eigenvector of $4$ is $(1, 1)/\sqrt2$. Along $(1, 0)$ the variance is only $3 < 4$.

</details>

**F4 (2 marks, NAT).** A centred data matrix with $n = 10$ rows has singular values 6 and 2. What fraction of the variance does PC1 explain?

<details>
<summary>Show solution</summary>

**Answer: 0.9**

$\lambda = \sigma^2/n$: $3.6$ and $0.4$. The fraction is $3.6/4.0 = $ **0.9**. (The $1/n$ cancels, so $36/40$ gives the same result.)

</details>

**F5 (1 mark, NAT).** The data mean is $\mu = (2, 3)$ and PC1 is $u = (1, 1)/\sqrt2$. What is the PC1 score of $x = (4, 5)$? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 2.83**

$u^\top(x - \mu) = \frac{(2 + 2)}{\sqrt2} = 2\sqrt2 = $ **2.83**.

</details>

**F6 (2 marks, NAT).** The eigenvalues are 4, 2, 1, 0.5, 0.5. What is the smallest number of components that keeps at least 90% of the variance?

<details>
<summary>Show solution</summary>

**Answer: 4**

The cumulative shares are 0.5, 0.75, 0.875, **0.9375**. The share first reaches 90% at 4 components.

</details>

**F7 (2 marks, MSQ).** Which statements about PCA are true?
(A) The projected scores on different principal components are uncorrelated (B) PCA uses class labels to choose directions (C) Standardising the features can change the principal components (D) The sum of all eigenvalues equals the trace of the covariance matrix

<details>
<summary>Show solution</summary>

**Answer: A; C; D**

(B) is false: PCA is unsupervised. LDA is the method that uses labels.

</details>
