---
title: 9. Decision trees
description: How a decision tree predicts, entropy, Gini and misclassification impurity, information gain and gain ratio, building trees (ID3, C4.5, CART), continuous features, regression trees, overfitting and pruning, and ensembles.
sidebar:
  label: 9. Decision trees
  order: 9
---

**Why it matters:** 2024 Q62 gave a 10-row table and asked for the **information gain** of one attribute, a 2-mark NAT that's pure arithmetic once you know the formula. Entropy also appears across the syllabus (naive Bayes, logistic loss), and the prediction report lists decision trees as "likely" for 2027.

## Topic map

<div class="mindmap">

- **Decision trees**
  - Structure
    - internal node = a test on one feature
    - leaf = a class (or a mean value, for regression)
  - Impurity
    - entropy $-\sum p\log_2 p$
    - Gini $1 - \sum p^2$
    - misclassification $1 - \max p$
  - Choosing a split
    - information gain = parent impurity − weighted child impurity
    - gain ratio fixes the bias towards many-valued attributes
  - Algorithms
    - ID3 (entropy), C4.5 (gain ratio), CART (Gini, binary splits)
    - continuous features: thresholds between sorted values
  - Overfitting
    - pre-pruning, post-pruning
  - Ensembles
    - bagging, random forests, boosting

</div>

## 9.1 How a tree predicts

A decision tree is a flowchart. Each **internal node** tests one feature ("Pitch = S?" or "age < 30?"). Each branch is one outcome of that test, and each **leaf** gives a prediction. To classify a point, start at the root and follow the branches until you reach a leaf.

- Each test looks at **one** feature, so the regions are **axis-aligned rectangles**.
- Trees need **no feature scaling** and handle categorical and numeric features together.
- They're easy to interpret: each path is a readable rule.

## 9.2 Measuring impurity

A node is **pure** if all its examples share one class. Let $p_k$ be the fraction of class $k$ in a node.

<div class="formula">

| Measure | Formula | Pure node | Most mixed ($C$ classes) |
|---|---|---|---|
| **Entropy** | $H = -\sum_k p_k \log_2 p_k$ | 0 | $\log_2 C$ (1 bit for 2 classes) |
| **Gini index** | $G = 1 - \sum_k p_k^2$ | 0 | $1 - 1/C$ (0.5 for 2 classes) |
| **Misclassification error** | $1 - \max_k p_k$ | 0 | $1 - 1/C$ |

Convention: $0 \log_2 0 = 0$.

</div>

<!-- fig:dt-impurity -->
<figure class="diagram"><svg class="dg" viewBox="0 0 560 285" role="img" aria-label="Entropy, Gini and misclassification impurity" xmlns="http://www.w3.org/2000/svg"><path class="ax" d="M60,20 V240 H520"/><text x="290.0" y="272" text-anchor="middle">p = P(class 1) in the node</text><text x="26" y="130.0" text-anchor="middle" transform="rotate(-90 26 130.0)">impurity</text><text class="t-mut" x="60.0" y="255.0" text-anchor="middle">0</text><text class="t-mut" x="175.0" y="255.0" text-anchor="middle">0.25</text><text class="t-mut" x="290.0" y="255.0" text-anchor="middle">0.5</text><text class="t-mut" x="405.0" y="255.0" text-anchor="middle">0.75</text><text class="t-mut" x="520.0" y="255.0" text-anchor="middle">1</text><line class="grid" x1="60.0" y1="138.1" x2="520.0" y2="138.1"/><text class="t-mut" x="54.0" y="142.1" text-anchor="end">0.5</text><line class="grid" x1="60.0" y1="36.3" x2="520.0" y2="36.3"/><text class="t-mut" x="54.0" y="40.3" text-anchor="end">1</text><polyline class="ink" points="60.5,237.7 62.0,231.8 63.5,226.8 65.1,222.2 66.6,217.9 68.1,213.9 69.7,210.0 71.2,206.3 72.7,202.8 74.3,199.3 75.8,196.0 77.3,192.8 78.9,189.7 80.4,186.6 82.0,183.6 83.5,180.7 85.0,177.9 86.6,175.1 88.1,172.4 89.6,169.8 91.2,167.2 92.7,164.6 94.2,162.1 95.8,159.7 97.3,157.3 98.8,154.9 100.4,152.6 101.9,150.3 103.5,148.1 105.0,145.9 106.5,143.7 108.1,141.6 109.6,139.5 111.1,137.5 112.7,135.4 114.2,133.4 115.7,131.5 117.3,129.6 118.8,127.7 120.3,125.8 121.9,124.0 123.4,122.1 124.9,120.4 126.5,118.6 128.0,116.9 129.6,115.2 131.1,113.5 132.6,111.8 134.2,110.2 135.7,108.6 137.2,107.0 138.8,105.5 140.3,103.9 141.8,102.4 143.4,100.9 144.9,99.4 146.4,98.0 148.0,96.6 149.5,95.2 151.0,93.8 152.6,92.4 154.1,91.1 155.7,89.8 157.2,88.5 158.7,87.2 160.3,85.9 161.8,84.7 163.3,83.4 164.9,82.2 166.4,81.1 167.9,79.9 169.5,78.7 171.0,77.6 172.5,76.5 174.1,75.4 175.6,74.3 177.1,73.2 178.7,72.2 180.2,71.2 181.8,70.2 183.3,69.2 184.8,68.2 186.4,67.2 187.9,66.3 189.4,65.4 191.0,64.4 192.5,63.6 194.0,62.7 195.6,61.8 197.1,61.0 198.6,60.1 200.2,59.3 201.7,58.5 203.3,57.7 204.8,57.0 206.3,56.2 207.9,55.5 209.4,54.7 210.9,54.0 212.5,53.3 214.0,52.6 215.5,52.0 217.1,51.3 218.6,50.7 220.1,50.1 221.7,49.5 223.2,48.9 224.7,48.3 226.3,47.7 227.8,47.2 229.4,46.6 230.9,46.1 232.4,45.6 234.0,45.1 235.5,44.6 237.0,44.2 238.6,43.7 240.1,43.3 241.6,42.8 243.2,42.4 244.7,42.0 246.2,41.6 247.8,41.3 249.3,40.9 250.8,40.6 252.4,40.2 253.9,39.9 255.5,39.6 257.0,39.3 258.5,39.1 260.1,38.8 261.6,38.5 263.1,38.3 264.7,38.1 266.2,37.9 267.7,37.7 269.3,37.5 270.8,37.3 272.3,37.2 273.9,37.0 275.4,36.9 276.9,36.8 278.5,36.7 280.0,36.6 281.6,36.5 283.1,36.4 284.6,36.4 286.2,36.3 287.7,36.3 289.2,36.3 290.8,36.3 292.3,36.3 293.8,36.3 295.4,36.4 296.9,36.4 298.4,36.5 300.0,36.6 301.5,36.7 303.1,36.8 304.6,36.9 306.1,37.0 307.7,37.2 309.2,37.3 310.7,37.5 312.3,37.7 313.8,37.9 315.3,38.1 316.9,38.3 318.4,38.5 319.9,38.8 321.5,39.1 323.0,39.3 324.5,39.6 326.1,39.9 327.6,40.2 329.2,40.6 330.7,40.9 332.2,41.3 333.8,41.6 335.3,42.0 336.8,42.4 338.4,42.8 339.9,43.3 341.4,43.7 343.0,44.2 344.5,44.6 346.0,45.1 347.6,45.6 349.1,46.1 350.6,46.6 352.2,47.2 353.7,47.7 355.3,48.3 356.8,48.9 358.3,49.5 359.9,50.1 361.4,50.7 362.9,51.3 364.5,52.0 366.0,52.6 367.5,53.3 369.1,54.0 370.6,54.7 372.1,55.5 373.7,56.2 375.2,57.0 376.7,57.7 378.3,58.5 379.8,59.3 381.4,60.1 382.9,61.0 384.4,61.8 386.0,62.7 387.5,63.6 389.0,64.4 390.6,65.4 392.1,66.3 393.6,67.2 395.2,68.2 396.7,69.2 398.2,70.2 399.8,71.2 401.3,72.2 402.9,73.2 404.4,74.3 405.9,75.4 407.5,76.5 409.0,77.6 410.5,78.7 412.1,79.9 413.6,81.1 415.1,82.2 416.7,83.4 418.2,84.7 419.7,85.9 421.3,87.2 422.8,88.5 424.3,89.8 425.9,91.1 427.4,92.4 429.0,93.8 430.5,95.2 432.0,96.6 433.6,98.0 435.1,99.4 436.6,100.9 438.2,102.4 439.7,103.9 441.2,105.5 442.8,107.0 444.3,108.6 445.8,110.2 447.4,111.8 448.9,113.5 450.4,115.2 452.0,116.9 453.5,118.6 455.1,120.4 456.6,122.1 458.1,124.0 459.7,125.8 461.2,127.7 462.7,129.6 464.3,131.5 465.8,133.4 467.3,135.4 468.9,137.5 470.4,139.5 471.9,141.6 473.5,143.7 475.0,145.9 476.5,148.1 478.1,150.3 479.6,152.6 481.2,154.9 482.7,157.3 484.2,159.7 485.8,162.1 487.3,164.6 488.8,167.2 490.4,169.8 491.9,172.4 493.4,175.1 495.0,177.9 496.5,180.7 498.0,183.6 499.6,186.6 501.1,189.7 502.7,192.8 504.2,196.0 505.7,199.3 507.3,202.8 508.8,206.3 510.3,210.0 511.9,213.9 513.4,217.9 514.9,222.2 516.5,226.8 518.0,231.8 519.5,237.7"/><polyline class="hl" points="60.5,239.6 62.0,238.2 63.5,236.9 65.1,235.6 66.6,234.2 68.1,232.9 69.7,231.6 71.2,230.3 72.7,229.0 74.3,227.7 75.8,226.5 77.3,225.2 78.9,224.0 80.4,222.7 82.0,221.5 83.5,220.3 85.0,219.0 86.6,217.8 88.1,216.6 89.6,215.4 91.2,214.3 92.7,213.1 94.2,211.9 95.8,210.8 97.3,209.6 98.8,208.5 100.4,207.4 101.9,206.3 103.5,205.2 105.0,204.1 106.5,203.0 108.1,201.9 109.6,200.8 111.1,199.8 112.7,198.7 114.2,197.7 115.7,196.6 117.3,195.6 118.8,194.6 120.3,193.6 121.9,192.6 123.4,191.6 124.9,190.6 126.5,189.6 128.0,188.7 129.6,187.7 131.1,186.8 132.6,185.8 134.2,184.9 135.7,184.0 137.2,183.1 138.8,182.2 140.3,181.3 141.8,180.4 143.4,179.5 144.9,178.7 146.4,177.8 148.0,177.0 149.5,176.1 151.0,175.3 152.6,174.5 154.1,173.7 155.7,172.9 157.2,172.1 158.7,171.3 160.3,170.6 161.8,169.8 163.3,169.0 164.9,168.3 166.4,167.6 167.9,166.8 169.5,166.1 171.0,165.4 172.5,164.7 174.1,164.0 175.6,163.3 177.1,162.7 178.7,162.0 180.2,161.4 181.8,160.7 183.3,160.1 184.8,159.4 186.4,158.8 187.9,158.2 189.4,157.6 191.0,157.0 192.5,156.5 194.0,155.9 195.6,155.3 197.1,154.8 198.6,154.2 200.2,153.7 201.7,153.2 203.3,152.6 204.8,152.1 206.3,151.6 207.9,151.1 209.4,150.7 210.9,150.2 212.5,149.7 214.0,149.3 215.5,148.8 217.1,148.4 218.6,148.0 220.1,147.5 221.7,147.1 223.2,146.7 224.7,146.3 226.3,146.0 227.8,145.6 229.4,145.2 230.9,144.9 232.4,144.5 234.0,144.2 235.5,143.9 237.0,143.6 238.6,143.2 240.1,142.9 241.6,142.7 243.2,142.4 244.7,142.1 246.2,141.8 247.8,141.6 249.3,141.3 250.8,141.1 252.4,140.9 253.9,140.7 255.5,140.4 257.0,140.2 258.5,140.1 260.1,139.9 261.6,139.7 263.1,139.5 264.7,139.4 266.2,139.2 267.7,139.1 269.3,139.0 270.8,138.9 272.3,138.7 273.9,138.6 275.4,138.6 276.9,138.5 278.5,138.4 280.0,138.3 281.6,138.3 283.1,138.2 284.6,138.2 286.2,138.2 287.7,138.2 289.2,138.1 290.8,138.1 292.3,138.2 293.8,138.2 295.4,138.2 296.9,138.2 298.4,138.3 300.0,138.3 301.5,138.4 303.1,138.5 304.6,138.6 306.1,138.6 307.7,138.7 309.2,138.9 310.7,139.0 312.3,139.1 313.8,139.2 315.3,139.4 316.9,139.5 318.4,139.7 319.9,139.9 321.5,140.1 323.0,140.2 324.5,140.4 326.1,140.7 327.6,140.9 329.2,141.1 330.7,141.3 332.2,141.6 333.8,141.8 335.3,142.1 336.8,142.4 338.4,142.7 339.9,142.9 341.4,143.2 343.0,143.6 344.5,143.9 346.0,144.2 347.6,144.5 349.1,144.9 350.6,145.2 352.2,145.6 353.7,146.0 355.3,146.3 356.8,146.7 358.3,147.1 359.9,147.5 361.4,148.0 362.9,148.4 364.5,148.8 366.0,149.3 367.5,149.7 369.1,150.2 370.6,150.7 372.1,151.1 373.7,151.6 375.2,152.1 376.7,152.6 378.3,153.2 379.8,153.7 381.4,154.2 382.9,154.8 384.4,155.3 386.0,155.9 387.5,156.5 389.0,157.0 390.6,157.6 392.1,158.2 393.6,158.8 395.2,159.4 396.7,160.1 398.2,160.7 399.8,161.4 401.3,162.0 402.9,162.7 404.4,163.3 405.9,164.0 407.5,164.7 409.0,165.4 410.5,166.1 412.1,166.8 413.6,167.6 415.1,168.3 416.7,169.0 418.2,169.8 419.7,170.6 421.3,171.3 422.8,172.1 424.3,172.9 425.9,173.7 427.4,174.5 429.0,175.3 430.5,176.1 432.0,177.0 433.6,177.8 435.1,178.7 436.6,179.5 438.2,180.4 439.7,181.3 441.2,182.2 442.8,183.1 444.3,184.0 445.8,184.9 447.4,185.8 448.9,186.8 450.4,187.7 452.0,188.7 453.5,189.6 455.1,190.6 456.6,191.6 458.1,192.6 459.7,193.6 461.2,194.6 462.7,195.6 464.3,196.6 465.8,197.7 467.3,198.7 468.9,199.8 470.4,200.8 471.9,201.9 473.5,203.0 475.0,204.1 476.5,205.2 478.1,206.3 479.6,207.4 481.2,208.5 482.7,209.6 484.2,210.8 485.8,211.9 487.3,213.1 488.8,214.3 490.4,215.4 491.9,216.6 493.4,217.8 495.0,219.0 496.5,220.3 498.0,221.5 499.6,222.7 501.1,224.0 502.7,225.2 504.2,226.5 505.7,227.7 507.3,229.0 508.8,230.3 510.3,231.6 511.9,232.9 513.4,234.2 514.9,235.6 516.5,236.9 518.0,238.2 519.5,239.6"/><polyline class="mut" points="60.5,239.8 62.0,239.1 63.5,238.4 65.1,237.8 66.6,237.1 68.1,236.4 69.7,235.7 71.2,235.0 72.7,234.4 74.3,233.7 75.8,233.0 77.3,232.3 78.9,231.6 80.4,231.0 82.0,230.3 83.5,229.6 85.0,228.9 86.6,228.2 88.1,227.6 89.6,226.9 91.2,226.2 92.7,225.5 94.2,224.8 95.8,224.2 97.3,223.5 98.8,222.8 100.4,222.1 101.9,221.4 103.5,220.8 105.0,220.1 106.5,219.4 108.1,218.7 109.6,218.0 111.1,217.4 112.7,216.7 114.2,216.0 115.7,215.3 117.3,214.6 118.8,214.0 120.3,213.3 121.9,212.6 123.4,211.9 124.9,211.2 126.5,210.6 128.0,209.9 129.6,209.2 131.1,208.5 132.6,207.8 134.2,207.2 135.7,206.5 137.2,205.8 138.8,205.1 140.3,204.4 141.8,203.8 143.4,203.1 144.9,202.4 146.4,201.7 148.0,201.0 149.5,200.4 151.0,199.7 152.6,199.0 154.1,198.3 155.7,197.6 157.2,197.0 158.7,196.3 160.3,195.6 161.8,194.9 163.3,194.2 164.9,193.6 166.4,192.9 167.9,192.2 169.5,191.5 171.0,190.8 172.5,190.2 174.1,189.5 175.6,188.8 177.1,188.1 178.7,187.4 180.2,186.8 181.8,186.1 183.3,185.4 184.8,184.7 186.4,184.0 187.9,183.4 189.4,182.7 191.0,182.0 192.5,181.3 194.0,180.6 195.6,180.0 197.1,179.3 198.6,178.6 200.2,177.9 201.7,177.2 203.3,176.6 204.8,175.9 206.3,175.2 207.9,174.5 209.4,173.8 210.9,173.2 212.5,172.5 214.0,171.8 215.5,171.1 217.1,170.4 218.6,169.8 220.1,169.1 221.7,168.4 223.2,167.7 224.7,167.0 226.3,166.4 227.8,165.7 229.4,165.0 230.9,164.3 232.4,163.6 234.0,163.0 235.5,162.3 237.0,161.6 238.6,160.9 240.1,160.2 241.6,159.6 243.2,158.9 244.7,158.2 246.2,157.5 247.8,156.8 249.3,156.2 250.8,155.5 252.4,154.8 253.9,154.1 255.5,153.4 257.0,152.8 258.5,152.1 260.1,151.4 261.6,150.7 263.1,150.0 264.7,149.4 266.2,148.7 267.7,148.0 269.3,147.3 270.8,146.6 272.3,146.0 273.9,145.3 275.4,144.6 276.9,143.9 278.5,143.2 280.0,142.6 281.6,141.9 283.1,141.2 284.6,140.5 286.2,139.8 287.7,139.2 289.2,138.5 290.8,138.5 292.3,139.2 293.8,139.8 295.4,140.5 296.9,141.2 298.4,141.9 300.0,142.6 301.5,143.2 303.1,143.9 304.6,144.6 306.1,145.3 307.7,146.0 309.2,146.6 310.7,147.3 312.3,148.0 313.8,148.7 315.3,149.4 316.9,150.0 318.4,150.7 319.9,151.4 321.5,152.1 323.0,152.8 324.5,153.4 326.1,154.1 327.6,154.8 329.2,155.5 330.7,156.2 332.2,156.8 333.8,157.5 335.3,158.2 336.8,158.9 338.4,159.6 339.9,160.2 341.4,160.9 343.0,161.6 344.5,162.3 346.0,163.0 347.6,163.6 349.1,164.3 350.6,165.0 352.2,165.7 353.7,166.4 355.3,167.0 356.8,167.7 358.3,168.4 359.9,169.1 361.4,169.8 362.9,170.4 364.5,171.1 366.0,171.8 367.5,172.5 369.1,173.2 370.6,173.8 372.1,174.5 373.7,175.2 375.2,175.9 376.7,176.6 378.3,177.2 379.8,177.9 381.4,178.6 382.9,179.3 384.4,180.0 386.0,180.6 387.5,181.3 389.0,182.0 390.6,182.7 392.1,183.4 393.6,184.0 395.2,184.7 396.7,185.4 398.2,186.1 399.8,186.8 401.3,187.4 402.9,188.1 404.4,188.8 405.9,189.5 407.5,190.2 409.0,190.8 410.5,191.5 412.1,192.2 413.6,192.9 415.1,193.6 416.7,194.2 418.2,194.9 419.7,195.6 421.3,196.3 422.8,197.0 424.3,197.6 425.9,198.3 427.4,199.0 429.0,199.7 430.5,200.4 432.0,201.0 433.6,201.7 435.1,202.4 436.6,203.1 438.2,203.8 439.7,204.4 441.2,205.1 442.8,205.8 444.3,206.5 445.8,207.2 447.4,207.8 448.9,208.5 450.4,209.2 452.0,209.9 453.5,210.6 455.1,211.2 456.6,211.9 458.1,212.6 459.7,213.3 461.2,214.0 462.7,214.6 464.3,215.3 465.8,216.0 467.3,216.7 468.9,217.4 470.4,218.0 471.9,218.7 473.5,219.4 475.0,220.1 476.5,220.8 478.1,221.4 479.6,222.1 481.2,222.8 482.7,223.5 484.2,224.2 485.8,224.8 487.3,225.5 488.8,226.2 490.4,226.9 491.9,227.6 493.4,228.2 495.0,228.9 496.5,229.6 498.0,230.3 499.6,231.0 501.1,231.6 502.7,232.3 504.2,233.0 505.7,233.7 507.3,234.4 508.8,235.0 510.3,235.7 511.9,236.4 513.4,237.1 514.9,237.8 516.5,238.4 518.0,239.1 519.5,239.8"/><text class="t-ink" x="290.0" y="30.3" text-anchor="middle">entropy (max 1)</text><text class="t-hl" x="290.0" y="130.1" text-anchor="middle">Gini (max 0.5)</text><text class="t-mut" x="184.2" y="215.6" text-anchor="start">misclassification</text></svg><figcaption>Impurity of a two-class node as a function of p = fraction of class 1. All three measures are 0 for a pure node and largest at p = 0.5: entropy reaches 1 bit, Gini and misclassification error reach 0.5. Entropy and Gini are smooth and strictly concave, which is why they are preferred for choosing splits.</figcaption></figure>
<!-- /fig:dt-impurity -->

**Entropy values worth memorising** (two classes):

| Split | 1:1 | 1:3 | 2:3 | 1:4 | 1:2 |
|---|---|---|---|---|---|
| $H$ | 1 | 0.811 | 0.971 | 0.722 | 0.918 |

These let you do most GATE entropy questions without a calculator. For example, $H(4{:}6) = H(2{:}3) = 0.971$.

## 9.3 Information gain

To choose a split, compare the impurity **before** and the weighted impurity **after**:

<div class="formula">

$$
\text{IG}(S, A) = H(S) - \sum_{v \in \text{values}(A)} \frac{|S_v|}{|S|}\,H(S_v)
$$

Choose the attribute with the **largest** gain. The same formula with Gini in place of $H$ gives the **Gini gain** (used by CART).

</div>

**The procedure for a table question:**

1. Count the classes in the whole table and compute $H(\text{parent})$.
2. For each value of the attribute, count the classes in that subset and compute its $H$.
3. Weight each child by its share of the rows, then subtract from the parent.

<!-- fig:dt-cricket -->
<figure class="diagram"><svg class="dg" viewBox="0 0 600 260" role="img" aria-label="Information gain of the first split" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="215.0" y="10" width="170" height="62" rx="8"/><text class="title" x="300" y="30" text-anchor="middle">all 10 matches</text><text x="300" y="48" text-anchor="middle">4 G · 6 B</text><text class="t-ink" x="300" y="64" text-anchor="middle">H = 0.971</text><rect class="box" x="65.0" y="150" width="170" height="62" rx="8"/><text class="title" x="150" y="170" text-anchor="middle">Pitch = S</text><text x="150" y="188" text-anchor="middle">3 G · 2 B</text><text class="t-ink" x="150" y="204" text-anchor="middle">H = 0.971</text><rect class="box" x="365.0" y="150" width="170" height="62" rx="8"/><text class="title" x="450" y="170" text-anchor="middle">Pitch = F</text><text x="450" y="188" text-anchor="middle">1 G · 4 B</text><text class="t-ink" x="450" y="204" text-anchor="middle">H = 0.722</text><line class="ax" x1="300" y1="72" x2="150" y2="150"/><line class="ax" x1="300" y1="72" x2="450" y2="150"/><text class="t-mut" x="205" y="112" text-anchor="end">5/10</text><text class="t-mut" x="395" y="112">5/10</text><text class="t-hl" x="300" y="245" text-anchor="middle">IG = 0.971 − (0.5·0.971 + 0.5·0.722) = 0.125</text></svg><figcaption>The first split for the 2024 Q62 cricket data (Green G / Blue B). The root has 4 G, 6 B (entropy 0.971). Splitting on Pitch gives S: 3 G, 2 B (0.971) and F: 1 G, 4 B (0.722). Weighted child entropy = 0.846, so IG(Pitch) = 0.971 − 0.846 = 0.125. Splitting on Format would gain only 0.020.</figcaption></figure>
<!-- /fig:dt-cricket -->

### The bias towards many-valued attributes, and gain ratio

An attribute like "Match number" has a different value in every row, so every child is pure and its IG is **as large as possible**. Yet it's useless for prediction. **C4.5** divides by the **split information**:

$$
\text{GainRatio}(S, A) = \frac{\text{IG}(S, A)}{-\sum_v \frac{|S_v|}{|S|}\log_2\frac{|S_v|}{|S|}}.
$$

Many small branches make the split information large, which penalises them.

## 9.4 Building the whole tree

Grow the tree greedily, top-down:

1. If the node is pure, or a stopping rule is met, make it a leaf that predicts the majority class.
2. Otherwise, pick the split with the best gain, create the children, and recurse on each.

| Algorithm | Split criterion | Splits | Notes |
|---|---|---|---|
| **ID3** | information gain | multi-way on categorical features | no pruning, no numeric features |
| **C4.5** | gain ratio | multi-way, plus numeric thresholds | handles missing values, pruning |
| **CART** | Gini (classification) / variance (regression) | always **binary** | cost-complexity pruning |

**Continuous features:** sort the values and try thresholds at the **midpoints** between consecutive values where the class changes. Pick the threshold with the best gain.

The greedy choice is **locally** optimal at each node. Finding the globally smallest consistent tree is NP-hard.

## 9.5 Regression trees

The leaf predicts the **mean** target of its examples. A split is chosen to **minimise the total squared error** (equivalently, to maximise the variance reduction) of the children:

$$
\text{SSE} = \sum_{i \in L}(y_i - \bar y_L)^2 + \sum_{i \in R}(y_i - \bar y_R)^2.
$$

For example, with $x = 1..6$ and $y = (5, 6, 5, 20, 22, 21)$, the split $x < 3.5$ cuts the SSE from 370.8 to **2.67**, by separating the low group from the high group.

## 9.6 Overfitting and pruning

A fully grown tree can memorise the training set: **zero training error, poor test error**. That's high variance, because a small change in the data can change the whole tree.

- **Pre-pruning** (stop early): set a maximum depth, a minimum number of samples per leaf, or a minimum gain.
- **Post-pruning**: grow the full tree, then cut back subtrees that don't improve **validation** error. Reduced-error pruning and cost-complexity pruning (which minimises error $+\, \alpha \times$ number of leaves) are the standard methods.

Deeper trees mean lower bias and higher variance (topic 1's table).

## 9.7 Ensembles (high-variance trees, averaged)

- **Bagging:** train many trees on bootstrap samples (sampling with replacement) and average or vote. This **reduces variance**.
- **Random forest:** bagging, plus each split considers only a **random subset of features**. This decorrelates the trees and reduces variance further.
- **Boosting** (AdaBoost, gradient boosting): train shallow trees **one after another**, each focusing on the previous trees' errors. This mainly **reduces bias**.

---

## Summary: important points

<div class="formula">

1. Entropy $-\sum p\log_2p$ ranges over $[0, \log_2C]$. Gini $1 - \sum p^2$ ranges over $[0, 1 - 1/C]$. Both are 0 for a pure node.
2. IG $= H(\text{parent}) - \sum\frac{n_v}{n}H(\text{child}_v)$. Choose the largest.
3. Useful values: $H(1{:}1) = 1$, $H(1{:}3) = 0.811$, $H(2{:}3) = 0.971$, $H(1{:}4) = 0.722$.
4. IG favours many-valued attributes. Gain ratio (C4.5) corrects this.
5. ID3 uses entropy, C4.5 uses gain ratio, CART uses Gini with binary splits.
6. Regression trees predict leaf means and split to minimise SSE.
7. Full trees overfit, so use pre- or post-pruning. Bagging and forests cut variance; boosting cuts bias.
8. Trees need no scaling, and their boundaries are axis-parallel.

</div>

<div class="trap">

- Use **log base 2** for entropy unless the question says otherwise.
- **Weight** each child's entropy by its share of the rows. Don't just average them.
- IG uses the **parent's** entropy. Don't subtract children from each other.
- An ID-like attribute gets maximal IG and is still useless.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q62 (2 marks, NAT)

Ten cricket matches with attributes Pitch ∈ {S, F} and Format ∈ {O, T}, and target Winner ∈ {Green, Blue}:

| Match | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Pitch | S | S | F | S | F | F | S | F | F | S |
| Format | T | T | O | O | T | O | O | T | O | O |
| Winner | G | B | B | B | G | B | G | B | B | G |

What is the information gain of Pitch with respect to the target? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.12**

1. **Parent:** Green in matches 1, 5, 7, 10, so 4 G and 6 B. $H = H(2{:}3) = 0.971$.
2. **Pitch = S** (matches 1, 2, 4, 7, 10): Green in 1, 7, 10 → 3 G, 2 B. $H = 0.971$.
3. **Pitch = F** (matches 3, 5, 6, 8, 9): Green in 5 → 1 G, 4 B. $H = 0.722$.
4. Weighted children: $0.5 \times 0.971 + 0.5 \times 0.722 = 0.846$.
5. IG $= 0.971 - 0.846 = 0.1245 \approx$ **0.12**.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (2 marks, NAT).** For the same table, what is IG(Format)? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.02**

- Format = T (1, 2, 5, 8): 2 G, 2 B, so $H = 1$.
- Format = O (3, 4, 6, 7, 9, 10): 2 G, 4 B, so $H = H(1{:}2) = 0.918$.
- Weighted: $0.4 \times 1 + 0.6 \times 0.918 = 0.951$.
- IG $= 0.971 - 0.951 = $ **0.02**.

Pitch (0.12) is the better root.

</details>

**F2 (2 marks, NAT).** For the same table, what is the Gini gain of splitting on Pitch?

<details>
<summary>Show solution</summary>

**Answer: 0.08**

- Parent: $1 - 0.4^2 - 0.6^2 = 0.48$.
- S: $1 - 0.6^2 - 0.4^2 = 0.48$. F: $1 - 0.2^2 - 0.8^2 = 0.32$.
- Weighted: $0.5(0.48) + 0.5(0.32) = 0.40$.
- Gain $= 0.48 - 0.40 = $ **0.08**.

</details>

**F3 (1 mark, NAT).** A node holds 8 examples with class counts 2, 2 and 4. What is its entropy in bits?

<details>
<summary>Show solution</summary>

**Answer: 1.5**

$-\big(\frac14\log_2\frac14 + \frac14\log_2\frac14 + \frac12\log_2\frac12\big) = \frac14(2) + \frac14(2) + \frac12(1) = $ **1.5**.

</details>

**F4 (1 mark, NAT).** What is the maximum possible entropy (in bits) of a node with 4 classes?

<details>
<summary>Show solution</summary>

**Answer: 2**

$\log_2 4 = 2$, reached when all four classes are equally frequent.

</details>

**F5 (2 marks, NAT).** Feature $x = 1, 2, 3, 4, 5, 6$ with classes A, A, B, A, B, B. Among the thresholds 1.5, 2.5, 3.5, 4.5 and 5.5, what is the highest information gain? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.46**

The parent has 3 A and 3 B, so $H = 1$.

- Threshold 2.5: left {A, A} has $H = 0$; right {B, A, B, B} has $H(1{:}3) = 0.811$. IG $= 1 - \frac46 \times 0.811 = 0.459$.
- Threshold 4.5 gives the same value by symmetry.
- The others are lower (1.5 and 5.5 give 0.19; 3.5 gives 0.08).

The best is **0.46**.

</details>

**F6 (2 marks, MSQ).** Which statements are true?
(A) A unique-ID attribute always has the maximum information gain (B) Gain ratio penalises attributes with many values (C) A fully grown tree typically has zero training error on consistent data (D) Decision trees require features to be standardised

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

(D) is false: each split compares a single feature with a threshold, so scaling doesn't change the tree.

</details>
