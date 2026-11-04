---
title: 7. Linear discriminant analysis
description: Fisher's criterion, between-class and within-class scatter, the generalized eigenvalue equation S_W⁻¹S_B u = λu, the two-class closed form, LDA as a Gaussian generative classifier, and its relation to nearest-mean classification and PCA.
sidebar:
  label: 7. LDA
  order: 7
---

**Why it matters:** 2024 Q22 asked which equation the Fisher direction satisfies, and 2025 Q55 tested the nearest-mean classifier, which is LDA's simplest special case. 2026 Q23 used LDA as a **feature-extraction** method. Learn the one derivation on this page and all three are immediate.

## Topic map

<div class="mindmap">

- **LDA**
  - Goal
    - find a direction $u$ along which the classes separate best
  - Fisher criterion
    - $J(u) = \dfrac{u^\top S_B u}{u^\top S_W u}$
    - between-class scatter $S_B$, within-class scatter $S_W$
  - Solution
    - $S_W^{-1}S_B\,u = \lambda u$, with $\lambda = J(u^*)$
    - two classes: $u^* \propto S_W^{-1}(\mu_1 - \mu_2)$
    - at most $C - 1$ useful directions
  - As a classifier
    - Gaussian classes with **shared** covariance → linear boundary
    - $\Sigma = \sigma^2 I$, equal priors → nearest mean
    - different covariances → QDA (quadratic)
  - vs PCA
    - LDA is supervised, PCA is unsupervised

</div>

## 7.1 The goal: a direction that separates the classes

Project every point onto a unit direction $u$: $z = u^\top x$. Each class becomes a little cloud of numbers on a line. We want a $u$ where the two clouds are

1. **far apart**: their projected means differ a lot, and
2. **tight**: each cloud has a small spread.

Only looking at the means isn't enough:

<!-- fig:lda-projection -->
<figure class="diagram"><svg class="dg" viewBox="0 0 620 290" role="img" aria-label="LDA projection direction compared with the mean-difference direction" xmlns="http://www.w3.org/2000/svg"><rect class="grid" x="30" y="20" width="300" height="250" rx="6"/><line class="hl" x1="72.5" y1="127.4" x2="303.7" y2="187.3"/><line class="ink" x1="101.7" y1="80.3" x2="274.5" y2="234.4"/><circle class="dot" cx="129.3" cy="195.6" r="3.2"/><circle class="dot" cx="153.9" cy="146.8" r="3.2"/><circle class="dot" cx="215.6" cy="102.8" r="3.2"/><circle class="dot" cx="140.4" cy="177.7" r="3.2"/><circle class="dot" cx="198.3" cy="91.1" r="3.2"/><circle class="dot" cx="177.1" cy="155.8" r="3.2"/><circle class="dot" cx="122.4" cy="152.5" r="3.2"/><circle class="dot" cx="174.0" cy="166.6" r="3.2"/><circle class="dot" cx="161.3" cy="167.3" r="3.2"/><circle class="dot" cx="137.0" cy="175.5" r="3.2"/><circle class="dot" cx="133.3" cy="161.2" r="3.2"/><circle class="dot" cx="162.2" cy="157.1" r="3.2"/><circle class="dot" cx="183.2" cy="116.6" r="3.2"/><circle class="dot" cx="91.9" cy="207.7" r="3.2"/><circle class="dot" cx="121.4" cy="182.8" r="3.2"/><circle class="dot" cx="107.6" cy="190.5" r="3.2"/><circle class="dot" cx="163.3" cy="151.4" r="3.2"/><circle class="dot" cx="118.4" cy="188.9" r="3.2"/><circle class="dot" cx="116.4" cy="206.4" r="3.2"/><circle class="dot" cx="175.0" cy="155.5" r="3.2"/><circle class="dot" cx="217.1" cy="91.4" r="3.2"/><circle class="dot" cx="76.1" cy="211.6" r="3.2"/><circle class="dot" cx="116.0" cy="183.7" r="3.2"/><circle class="dot" cx="166.9" cy="176.5" r="3.2"/><circle class="dot" cx="154.6" cy="157.6" r="3.2"/><circle class="dot" cx="207.8" cy="130.4" r="3.2"/><circle class="dot" cx="197.8" cy="137.0" r="3.2"/><circle class="dot" cx="150.3" cy="170.8" r="3.2"/><circle class="dot" cx="229.5" cy="84.0" r="3.2"/><circle class="dot" cx="273.2" cy="47.8" r="3.2"/><circle class="dot" cx="202.6" cy="100.9" r="3.2"/><circle class="dot" cx="138.0" cy="167.8" r="3.2"/><circle class="dot" cx="225.1" cy="103.6" r="3.2"/><circle class="dot" cx="173.4" cy="138.6" r="3.2"/><circle class="dot" cx="192.1" cy="129.4" r="3.2"/><circle class="dot" cx="158.2" cy="146.4" r="3.2"/><circle class="dot" cx="169.6" cy="155.7" r="3.2"/><circle class="dot" cx="204.9" cy="134.7" r="3.2"/><circle class="dot" cx="111.6" cy="209.1" r="3.2"/><circle class="dot" cx="208.0" cy="116.6" r="3.2"/><rect class="dot-warn" x="166.8" y="212.1" width="6" height="6"/><rect class="dot-warn" x="228.7" y="161.2" width="6" height="6"/><rect class="dot-warn" x="153.4" y="193.7" width="6" height="6"/><rect class="dot-warn" x="156.7" y="206.6" width="6" height="6"/><rect class="dot-warn" x="209.7" y="166.3" width="6" height="6"/><rect class="dot-warn" x="207.6" y="138.3" width="6" height="6"/><rect class="dot-warn" x="187.0" y="198.0" width="6" height="6"/><rect class="dot-warn" x="128.3" y="227.4" width="6" height="6"/><rect class="dot-warn" x="194.3" y="166.8" width="6" height="6"/><rect class="dot-warn" x="189.3" y="183.2" width="6" height="6"/><rect class="dot-warn" x="177.9" y="193.0" width="6" height="6"/><rect class="dot-warn" x="217.1" y="159.3" width="6" height="6"/><rect class="dot-warn" x="214.5" y="123.4" width="6" height="6"/><rect class="dot-warn" x="231.3" y="167.9" width="6" height="6"/><rect class="dot-warn" x="287.1" y="91.2" width="6" height="6"/><rect class="dot-warn" x="168.1" y="177.1" width="6" height="6"/><rect class="dot-warn" x="210.8" y="168.3" width="6" height="6"/><rect class="dot-warn" x="181.8" y="197.7" width="6" height="6"/><rect class="dot-warn" x="212.1" y="139.2" width="6" height="6"/><rect class="dot-warn" x="195.5" y="163.2" width="6" height="6"/><rect class="dot-warn" x="293.5" y="112.1" width="6" height="6"/><rect class="dot-warn" x="221.5" y="154.6" width="6" height="6"/><rect class="dot-warn" x="162.9" y="213.4" width="6" height="6"/><rect class="dot-warn" x="209.3" y="152.0" width="6" height="6"/><rect class="dot-warn" x="186.3" y="176.7" width="6" height="6"/><rect class="dot-warn" x="242.1" y="128.0" width="6" height="6"/><rect class="dot-warn" x="248.7" y="120.1" width="6" height="6"/><rect class="dot-warn" x="231.7" y="110.9" width="6" height="6"/><rect class="dot-warn" x="237.7" y="134.3" width="6" height="6"/><rect class="dot-warn" x="241.6" y="148.7" width="6" height="6"/><rect class="dot-warn" x="195.0" y="157.5" width="6" height="6"/><rect class="dot-warn" x="238.1" y="110.4" width="6" height="6"/><rect class="dot-warn" x="210.5" y="182.6" width="6" height="6"/><rect class="dot-warn" x="296.6" y="71.2" width="6" height="6"/><rect class="dot-warn" x="162.9" y="173.4" width="6" height="6"/><rect class="dot-warn" x="211.4" y="187.7" width="6" height="6"/><rect class="dot-warn" x="191.3" y="182.1" width="6" height="6"/><rect class="dot-warn" x="280.8" y="115.2" width="6" height="6"/><rect class="dot-warn" x="198.7" y="172.3" width="6" height="6"/><rect class="dot-warn" x="193.1" y="187.4" width="6" height="6"/><text class="t-hl" x="72.5" y="119.4" text-anchor="start">μ₂ − μ₁</text><text class="t-ink" x="269.9" y="226.7">Fisher u</text><text class="title" x="360" y="50">projected on μ₂ − μ₁: overlap</text><line class="hl" x1="360" y1="70" x2="600" y2="70"/><circle class="dot" cx="420.7" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="433.2" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="493.8" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="427.9" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="467.8" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="465.7" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="395.7" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="465.9" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="450.1" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="422.8" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="412.6" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="447.4" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="458.5" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="378.4" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="405.9" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="391.6" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="446.7" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="404.5" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="408.7" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="462.9" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="491.4" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="360.0" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="399.5" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="460.7" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="438.1" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="494.5" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="484.5" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="437.6" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="504.1" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="545.3" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="476.8" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="421.1" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="506.0" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="454.5" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="474.4" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="438.4" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="456.2" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="492.5" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="403.6" cy="62.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="489.6" cy="62.0" r="2.8" style="opacity:.8"/><rect class="dot-warn" x="476.3" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="534.8" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="452.5" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="461.6" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="512.8" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="499.6" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="496.3" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="433.8" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="493.7" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="493.6" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="483.0" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="519.5" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="502.6" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="540.5" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="581.5" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="464.7" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="514.9" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="489.7" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="505.6" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="493.9" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="597.4" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="523.1" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="471.9" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="506.9" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="487.4" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="539.0" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="544.2" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="519.4" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="535.9" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="546.2" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="491.0" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="527.2" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="520.0" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="585.9" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="456.8" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="523.1" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="495.7" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="582.7" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="501.3" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="500.0" y="75.0" width="5.2" height="5.2" style="opacity:.85"/><text class="title" x="360" y="160">projected on Fisher u: separated</text><line class="ink" x1="360" y1="180" x2="600" y2="180"/><circle class="dot" cx="451.9" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="405.7" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="433.6" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="438.7" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="381.6" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="463.4" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="360.0" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="477.8" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="456.5" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="428.5" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="395.4" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="439.1" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="401.8" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="408.0" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="414.2" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="404.1" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="430.7" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="420.1" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="449.0" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="458.9" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="415.4" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="387.0" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="406.2" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="483.6" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="426.6" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="470.9" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="465.4" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="443.3" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="423.6" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="434.4" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="407.2" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="416.0" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="452.0" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="425.0" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="441.2" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="412.4" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="449.8" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="473.7" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="445.4" cy="172.0" r="2.8" style="opacity:.8"/><circle class="dot" cx="445.8" cy="172.0" r="2.8" style="opacity:.8"/><rect class="dot-warn" x="557.2" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="573.2" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="499.5" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="529.2" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="548.8" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="493.3" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="567.0" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="517.1" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="522.4" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="543.8" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="541.6" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="549.0" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="478.1" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="590.0" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="547.5" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="494.8" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="554.3" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="557.3" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="503.0" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="518.0" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="597.4" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="548.0" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="552.7" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="521.7" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="526.5" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="535.7" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="532.5" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="485.5" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="539.5" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="572.9" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="506.3" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="496.0" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="580.3" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="527.4" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="478.9" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="591.4" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="545.3" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="580.6" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="540.3" y="185.0" width="5.2" height="5.2" style="opacity:.85"/><rect class="dot-warn" x="558.3" y="185.0" width="5.2" height="5.2" style="opacity:.85"/></svg><figcaption>Two elongated classes. Projecting onto the line joining the means (yellow) mixes the classes because it ignores their shape; the Fisher direction u ∝ S_W⁻¹(μ₁ − μ₂) (blue) tilts away from the long axis of the clouds, so the projected classes barely overlap. Right: the 1-D projections on each direction.</figcaption></figure>
<!-- /fig:lda-projection -->

Projecting onto the line joining the means makes the means as far apart as possible, but elongated clouds spread out along it and overlap. Fisher's idea is to maximise the **ratio** of separation to spread.

## 7.2 Fisher's criterion

For two classes with means $\mu_1, \mu_2$, define:

<div class="formula">

$$
S_B = (\mu_1 - \mu_2)(\mu_1 - \mu_2)^\top \qquad \text{(between-class scatter)}
$$

$$
S_W = \sum_{x \in C_1}(x - \mu_1)(x - \mu_1)^\top + \sum_{x \in C_2}(x - \mu_2)(x - \mu_2)^\top \qquad \text{(within-class scatter)}
$$

After projecting onto $u$:

- (difference of projected means)$^2 = \big(u^\top(\mu_1 - \mu_2)\big)^2 = u^\top S_B u$
- (sum of projected within-class scatters) $= u^\top S_W u$

$$
J(u) = \frac{u^\top S_B\,u}{u^\top S_W\,u}
$$

</div>

$J$ doesn't change if you scale $u$, so only the **direction** matters.

## 7.3 Solving it: an eigenvalue problem

Set the gradient of $J$ to zero (quotient rule):

$$
\nabla J = 0 \;\Longrightarrow\; (u^\top S_W u)\,S_B u = (u^\top S_B u)\,S_W u \;\Longrightarrow\; S_B u = J(u)\,S_W u.
$$

<div class="formula">

Writing $\lambda = J(u^*)$, the optimum satisfies the **generalized eigenvalue problem**

$$
S_B\,u^* = \lambda\,S_W\,u^* \quad\Longleftrightarrow\quad S_W^{-1}S_B\,u^* = \lambda\,u^* \quad (S_W \text{ invertible}).
$$

$u^*$ is the eigenvector of $S_W^{-1}S_B$ with the **largest** eigenvalue, and that eigenvalue **is** the maximum value of $J$.

**Two classes, closed form.** $S_B u = (\mu_1 - \mu_2)\big[(\mu_1 - \mu_2)^\top u\big]$ always points along $\mu_1 - \mu_2$. So

$$
u^* \propto S_W^{-1}(\mu_1 - \mu_2), \qquad \lambda_{\max} = (\mu_1 - \mu_2)^\top S_W^{-1}(\mu_1 - \mu_2).
$$

**$C$ classes.** $S_B = \sum_c n_c(\mu_c - \mu)(\mu_c - \mu)^\top$ has rank at most $C - 1$, so LDA gives **at most $C - 1$** discriminant directions. That's 1 for two classes.

</div>

### Worked example

Class A: (1,2), (2,3), (3,3), (2,1). Class B: (5,4), (6,5), (7,5), (6,3).

| Quantity | Value |
|---|---|
| $\mu_A$, $\mu_B$ | (2, 2.25), (6, 4.25) |
| $\mu_A - \mu_B$ | (−4, −2) |
| Scatter of A $= \sum (x - \mu_A)(x - \mu_A)^\top$ | $\begin{pmatrix}2 & 1\\ 1 & 2.75\end{pmatrix}$ |
| Scatter of B | the same, $\begin{pmatrix}2 & 1\\ 1 & 2.75\end{pmatrix}$ |
| $S_W$ | $\begin{pmatrix}4 & 2\\ 2 & 5.5\end{pmatrix}$ |
| $u^* = S_W^{-1}(\mu_A - \mu_B)$ | **(−1, 0)**, i.e. the $x$-axis |
| $J(u^*) = \lambda_{\max}$ | **4** |
| $J$ along the mean difference $(4, 2)$ | 3.39 (worse) |

Check $u^*$: $S_W(-1, 0)^\top = (-4, -2)^\top = \mu_A - \mu_B$. ✓ The two clouds are tilted, so the best direction is not the line joining the means.

## 7.4 LDA as a classifier (the generative view)

Assume each class is Gaussian with its **own mean** but a **shared covariance** $\Sigma$: $x \mid y = k \sim \mathcal{N}(\mu_k, \Sigma)$, with prior $\pi_k$. The log-posterior is

$$
\ln P(y = k \mid x) = x^\top \Sigma^{-1}\mu_k - \tfrac12\mu_k^\top\Sigma^{-1}\mu_k + \ln\pi_k + \text{const}.
$$

The quadratic term $x^\top\Sigma^{-1}x$ is the **same for every class**, so it cancels when you compare classes. The decision boundary is therefore **linear**.

<div class="formula">

| Assumption | Boundary | Name |
|---|---|---|
| shared $\Sigma$ | linear | **LDA** |
| $\Sigma = \sigma^2 I$ and equal priors | perpendicular bisector of the means | **nearest-mean classifier** (2025 Q55) |
| a different $\Sigma_k$ per class | quadratic | **QDA** |

For two classes with equal priors, LDA predicts class 2 when $w^\top x + b > 0$, with $w = \Sigma^{-1}(\mu_2 - \mu_1)$. This is the same direction as Fisher's $u^*$.

</div>

So Fisher's geometric idea (best projection) and the probabilistic model (Gaussian classes, shared covariance) lead to the **same direction**. That's why both go by the name LDA.

## 7.5 LDA vs PCA

| | LDA | PCA |
|---|---|---|
| Uses labels? | **yes** (supervised) | no (unsupervised) |
| Objective | maximise class separation $J(u)$ | maximise variance $u^\top\Sigma u$ |
| Directions available | at most $C - 1$ | up to $d$ |
| Eigenproblem | $S_W^{-1}S_B$ | covariance $\Sigma$ |
| Directions orthogonal? | not necessarily | yes |

PCA can throw away exactly the direction that separates the classes, if that direction has low overall variance. LDA won't.

---

## Summary: important points

<div class="formula">

1. $J(u) = \dfrac{u^\top S_B u}{u^\top S_W u}$: between-class separation over within-class spread.
2. $S_B = (\mu_1 - \mu_2)(\mu_1 - \mu_2)^\top$ and $S_W = \sum_{\text{classes}}\sum (x - \mu_c)(x - \mu_c)^\top$.
3. The optimum satisfies $S_W^{-1}S_B\,u = \lambda u$, with $\lambda = J(u^*)$ the **largest** eigenvalue.
4. Two classes: $u^* \propto S_W^{-1}(\mu_1 - \mu_2)$.
5. At most $C - 1$ discriminant directions.
6. Gaussian classes with a shared covariance give a linear boundary (LDA). $\Sigma = \sigma^2 I$ with equal priors gives the nearest-mean rule. Different covariances give QDA.
7. LDA is supervised and generative. It's used both as a classifier and for feature extraction.

</div>

<div class="trap">

- The order matters: it's $S_W^{-1}S_B$, not $S_B S_W^{-1}$ and not $S_B S_W$. These have different eigenvectors.
- $J$ is a **ratio** of scatters, not a difference.
- LDA directions needn't be orthogonal (unlike PCA).

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q22 (1 mark, MCQ)

$S_B$ and $S_W$ are the between-class and within-class scatter matrices of a binary dataset. The Fisher direction $u^*$ maximises $J(u) = \frac{u^\top S_B u}{u^\top S_W u}$. If $\lambda = J(u^*)$, $S_W$ is non-singular and $S_B \ne 0$, which equation must $(u^*, \lambda)$ satisfy?
(A) $S_W^{-1}S_B u^* = \lambda u^*$ (B) $S_W u^* = \lambda S_B u^*$ (C) $S_B S_W u^* = \lambda u^*$ (D) $u^{*\top}u^* = \lambda^2$

<details>
<summary>Show solution</summary>

**Answer: (A)**

From §7.3, $\nabla J = 0$ gives $S_B u^* = J(u^*)\,S_W u^* = \lambda S_W u^*$. Multiply on the left by $S_W^{-1}$.

(B) has $\lambda$ on the wrong side (it would hold with $1/\lambda$). (C) has the wrong matrix product. (D) is unrelated.

</details>

### GATE DA 2025 Q55 (2 marks, MSQ)

The nearest-mean classifier $f(x) = \|\mu_r - x\|^2 - \|\mu_g - x\|^2$. Which are correct? **Answer: B; C** ($f$ is linear in $x$). The full solution is in [topic 4, §4.7](/machine-learning/logistic-linear-classifiers/#47-the-nearest-mean-classifier-is-linear). In LDA terms, this is the case $\Sigma = \sigma^2 I$ with equal priors.

---

## Test yourself (B): predicted 2027-style questions

**F1 (2 marks, MCQ).** Two classes have $\mu_1 - \mu_2 = (4, 4)$ and $S_W = \operatorname{diag}(2, 8)$. Which vector is in the Fisher LDA direction?
(A) (1, 1) (B) (4, 1) (C) (1, 4) (D) (2, 8)

<details>
<summary>Show solution</summary>

**Answer: (B)**

$S_W^{-1}(\mu_1 - \mu_2) = (4/2, 4/8) = (2, 0.5) \propto (4, 1)$. The direction with large within-class spread (the second axis, variance 8) gets less weight.

</details>

**F2 (1 mark, NAT).** LDA is applied to data with 4 classes and 10 features. What is the maximum number of useful discriminant directions?

<details>
<summary>Show solution</summary>

**Answer: 3**

$\min(C - 1, d) = \min(3, 10) = $ **3**, because $S_B$ has rank at most $C - 1$.

</details>

**F3 (2 marks, NAT).** For the worked example in §7.3, what is the maximum value of Fisher's $J$?

<details>
<summary>Show solution</summary>

**Answer: 4**

$\lambda_{\max} = (\mu_A - \mu_B)^\top S_W^{-1}(\mu_A - \mu_B)$. With $S_W^{-1}(\mu_A - \mu_B) = (-1, 0)$, this is $(-4, -2)\cdot(-1, 0) = $ **4**.

</details>

**F4 (2 marks, MCQ).** Classes 1 and 2 are Gaussian with means (0, 0) and (2, 2), shared covariance $\Sigma = \begin{pmatrix}1 & 0.5\\ 0.5 & 1\end{pmatrix}$ and equal priors. LDA classifies $x = (2, 0.5)$ as
(A) class 1 (B) class 2 (C) exactly on the boundary (D) it can't be decided without the data

<details>
<summary>Show solution</summary>

**Answer: (B)**

- $w = \Sigma^{-1}(\mu_2 - \mu_1) = (4/3, 4/3)$.
- $b = -\frac12(\mu_2^\top\Sigma^{-1}\mu_2 - \mu_1^\top\Sigma^{-1}\mu_1) = -\frac83$.
- Score at $x$: $\frac43(2 + 0.5) - \frac83 = \frac{10}{3} - \frac83 = \frac23 > 0$, so **class 2**.

LDA compares **Mahalanobis** distances $(x - \mu_k)^\top\Sigma^{-1}(x - \mu_k)$, not Euclidean ones. Here they are $\approx 4.33$ to $\mu_1$ and $3.0$ to $\mu_2$, so class 2 is nearer. In this case the Euclidean distances (2.06 vs 1.5) happen to agree, but with a strongly correlated $\Sigma$ they can disagree.

</details>

**F5 (2 marks, MSQ).** Which statements are true?
(A) LDA uses class labels, PCA does not (B) LDA assumes each class has its own covariance matrix (C) With a shared covariance, the LDA decision boundary is linear (D) LDA directions are always mutually orthogonal

<details>
<summary>Show solution</summary>

**Answer: A; C**

(B) describes QDA. (D) is false: the eigenvectors of $S_W^{-1}S_B$ needn't be orthogonal, because that matrix isn't symmetric in general.

</details>
