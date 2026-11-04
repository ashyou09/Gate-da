---
title: 5. Evaluation metrics
description: Confusion matrix, accuracy and its failure on imbalanced data, precision, recall, specificity, F1, the precision–recall trade-off, ROC and AUC, macro vs micro averaging, and the link to Bayes' theorem.
sidebar:
  label: 5. Evaluation metrics
  order: 5
---

**Why it matters:** 2026 Q47 gave raw counts ("6 of X's stories were labelled Y…") and asked for accuracy, precision and recall per class. The whole question is about **building the confusion matrix correctly** and reading the right row or column. The prediction report rates metrics as near-certain for 2027.

## Topic map

<div class="mindmap">

- **Evaluation metrics**
  - Confusion matrix
    - TP, FP, FN, TN; which class is "positive"
  - Basic rates
    - accuracy, error rate
    - precision (column), recall / TPR (row)
    - specificity / TNR, FPR $= 1 -$ specificity
    - F1 $=$ harmonic mean
  - Threshold effects
    - precision–recall trade-off
    - ROC curve, AUC
  - Imbalanced data
    - accuracy paradox, PR curve
  - Multi-class
    - per-class metrics, macro vs micro averaging
  - Link to probability
    - precision $= P(\text{actual} + \mid \text{predicted} +)$, which depends on the base rate

</div>

## 5.1 The confusion matrix

Choose one class to call **positive**. Every prediction then lands in one of four cells.

<!-- fig:cm-layout -->
<figure class="diagram"><svg class="dg" viewBox="0 0 700 234" role="img" aria-label="Confusion matrix layout" xmlns="http://www.w3.org/2000/svg"><text class="title" x="330" y="22" text-anchor="middle">predicted</text><text class="t-mut" x="240.0" y="50" text-anchor="middle">positive</text><text class="t-mut" x="420.0" y="50" text-anchor="middle">negative</text><text class="title" x="40" y="130" text-anchor="middle" transform="rotate(-90 40 130)">actual</text><text class="t-mut" x="140" y="99.0" text-anchor="end">positive</text><text class="t-mut" x="140" y="169.0" text-anchor="end">negative</text><rect class="box-ink" x="153" y="63" width="174" height="64" rx="6"/><text class="on-ink" x="240.0" y="90" text-anchor="middle" style="font-size:16px;font-weight:700">TP</text><text class="on-ink" x="240.0" y="110" text-anchor="middle">true positive</text><rect class="box" x="333" y="63" width="174" height="64" rx="6"/><text class="title" x="420.0" y="90" text-anchor="middle" style="font-size:16px;font-weight:700">FN</text><text class="t-mut" x="420.0" y="110" text-anchor="middle">false negative (missed)</text><rect class="box" x="153" y="133" width="174" height="64" rx="6"/><text class="title" x="240.0" y="160" text-anchor="middle" style="font-size:16px;font-weight:700">FP</text><text class="t-mut" x="240.0" y="180" text-anchor="middle">false positive (false alarm)</text><rect class="box" x="333" y="133" width="174" height="64" rx="6"/><text class="title" x="420.0" y="160" text-anchor="middle" style="font-size:16px;font-weight:700">TN</text><text class="t-mut" x="420.0" y="180" text-anchor="middle">true negative</text><rect x="148" y="58" width="184" height="144" rx="8" class="hl" style="fill:none;stroke-width:2"/><text class="t-hl" x="240.0" y="222" text-anchor="middle">precision = TP/(TP+FP)</text><rect x="148" y="58" width="364" height="74" rx="8" class="warn" style="fill:none;stroke-width:2;stroke-dasharray:6 4"/><text class="t-warn" x="522" y="99.0">recall = TP/(TP+FN)</text></svg><figcaption>The confusion matrix for a binary problem. Rows are the truth, columns the prediction. Precision reads down the 'predicted positive' column; recall reads across the 'actually positive' row.</figcaption></figure>
<!-- /fig:cm-layout -->

**Building it from words** (the GATE skill):

1. Write the **true** counts per class. These are the row totals.
2. Split each row by what the classifier **predicted**.
3. Only then read off the metrics.

"Of X's 20 stories, 6 were classified as Y" means row X is: predicted X = 14, predicted Y = 6.

## 5.2 The metrics

<div class="formula">

| Metric | Formula | Question it answers |
|---|---|---|
| **Accuracy** | $\dfrac{TP + TN}{TP + TN + FP + FN}$ | What fraction of all predictions is right? |
| **Precision** | $\dfrac{TP}{TP + FP}$ | Of the items I **predicted** positive, how many really are? |
| **Recall** (sensitivity, TPR) | $\dfrac{TP}{TP + FN}$ | Of the items that **are** positive, how many did I catch? |
| **Specificity** (TNR) | $\dfrac{TN}{TN + FP}$ | Of the actual negatives, how many did I correctly reject? |
| **False positive rate** | $\dfrac{FP}{FP + TN} = 1 - \text{specificity}$ | How often do I raise a false alarm? |
| **F1 score** | $\dfrac{2PR}{P + R} = \dfrac{2TP}{2TP + FP + FN}$ | One number balancing P and R |
| $F_\beta$ | $\dfrac{(1 + \beta^2)PR}{\beta^2P + R}$ | $\beta > 1$ weighs recall more |

</div>

**Memory hook:**

- **Precision** looks down the **predicted** column: of what I *flagged*, how much was right?
- **Recall** looks across the **actual** row: of what *exists*, how much did I *find*?

**Why the harmonic mean for F1?** It's dominated by the **smaller** value. Precision 1.0 with recall 0.01 gives F1 ≈ 0.02, not the 0.5 an arithmetic mean would suggest. You can't score well by doing well on only one of the two.

### When does each one matter?

| Situation | Costly error | Prioritise |
|---|---|---|
| Cancer screening, fraud detection | missing a positive (FN) | **recall** |
| Spam filter, recommending a product | false alarm (FP) | **precision** |
| Balanced classes, equal costs | either | accuracy or F1 |

## 5.3 The accuracy paradox (imbalanced data)

With 990 negatives and 10 positives, a model that **always predicts negative** scores **99% accuracy**, yet its recall is **0**. On imbalanced data, report precision, recall, F1, or the area under the precision–recall curve instead of accuracy.

## 5.4 Thresholds: the precision–recall trade-off

Most classifiers output a **score** (a probability from logistic regression, a margin from an SVM), and we label something positive if score > threshold $t$.

- **Raise $t$:** fewer items get flagged. Precision usually **rises** (only confident ones are flagged), and recall **falls** or stays the same (some positives are missed).
- **Lower $t$:** more items get flagged. Recall **rises** or stays the same, and precision usually **falls**.

Recall can never go up when you raise the threshold. Precision usually goes up, but not always.

## 5.5 ROC curve and AUC

The **ROC curve** plots **TPR (recall)** against **FPR** as the threshold sweeps from $+\infty$ (flag nothing: the point (0, 0)) down to $-\infty$ (flag everything: the point (1, 1)).

**Drawing it by hand:** sort the items by score, high to low. Start at (0, 0). For each item, step **up by $1/P$** if it's a positive, or **right by $1/N$** if it's a negative.

<!-- fig:roc-example -->
<figure class="diagram"><svg class="dg" viewBox="0 0 560 320" role="img" aria-label="ROC curve of a worked example" xmlns="http://www.w3.org/2000/svg"><path class="ax" d="M70,20 V280 H370"/><text x="220.0" y="314" text-anchor="middle">false positive rate (1 − specificity)</text><text x="30" y="150.0" text-anchor="middle" transform="rotate(-90 30 150.0)">true positive rate (recall)</text><text class="t-mut" x="70.0" y="295.0" text-anchor="middle">0</text><text class="t-mut" x="145.0" y="295.0" text-anchor="middle">0.25</text><text class="t-mut" x="220.0" y="295.0" text-anchor="middle">0.5</text><text class="t-mut" x="295.0" y="295.0" text-anchor="middle">0.75</text><text class="t-mut" x="370.0" y="295.0" text-anchor="middle">1</text><text class="t-mut" x="64.0" y="284.0" text-anchor="end">0.00</text><text class="t-mut" x="64.0" y="197.3" text-anchor="end">0.33</text><text class="t-mut" x="64.0" y="110.7" text-anchor="end">0.67</text><text class="t-mut" x="64.0" y="24.0" text-anchor="end">1.00</text><polygon style="fill:var(--gd-ink);fill-opacity:.14" points="70.0,280.0 70.0,193.3 145.0,193.3 145.0,106.7 145.0,20.0 220.0,20.0 295.0,20.0 370.0,20.0 370.0,280.0"/><line class="mut" x1="70.0" y1="280.0" x2="370.0" y2="20.0"/><polyline class="ink" points="70.0,280.0 70.0,193.3 145.0,193.3 145.0,106.7 145.0,20.0 220.0,20.0 295.0,20.0 370.0,20.0"/><circle class="dot-ink" cx="70.0" cy="193.3" r="3.5"/><circle class="dot-ink" cx="145.0" cy="193.3" r="3.5"/><circle class="dot-ink" cx="145.0" cy="106.7" r="3.5"/><circle class="dot-ink" cx="145.0" cy="20.0" r="3.5"/><circle class="dot-ink" cx="220.0" cy="20.0" r="3.5"/><circle class="dot-ink" cx="295.0" cy="20.0" r="3.5"/><circle class="dot-ink" cx="370.0" cy="20.0" r="3.5"/><text class="t-ink" x="235.0" y="163.0">AUC = 0.833</text><text class="t-mut" x="256.0" y="108.4">random (0.5)</text><text class="t-mut" x="388.0" y="24.0">threshold steps:</text><text class="t-ink" x="388.0" y="42.0">0.9 (+) → up</text><text class="t-mut" x="388.0" y="59.0">0.8 (−) → right</text><text class="t-ink" x="388.0" y="76.0">0.7 (+) → up</text><text class="t-ink" x="388.0" y="93.0">0.4 (+) → up</text><text class="t-mut" x="388.0" y="110.0">0.3 (−) → right</text><text class="t-mut" x="388.0" y="127.0">0.2 (−) → right</text><text class="t-mut" x="388.0" y="144.0">0.1 (−) → right</text></svg><figcaption>ROC curve for 3 positives scored 0.9, 0.7, 0.4 and 4 negatives scored 0.8, 0.3, 0.2, 0.1. Lowering the threshold past each score moves up (a positive) or right (a negative). The shaded area is AUC = 10/12 ≈ 0.833; the dashed diagonal is a random classifier (AUC = 0.5).</figcaption></figure>
<!-- /fig:roc-example -->

<div class="formula">

- **AUC** (area under the ROC curve) $=$ the probability that a randomly chosen positive gets a **higher score** than a randomly chosen negative, with ties counted as ½.
- Computing it: count the (positive, negative) pairs ranked correctly and divide by $P \times N$.
- AUC $= 1$ is a perfect ranking. AUC $= 0.5$ is random (the diagonal). AUC $< 0.5$ means the scores are inverted: flip them.
- AUC depends only on the **ranking** of the scores, not on any threshold or on the scale of the scores.

</div>

In the example, positive 0.9 beats all 4 negatives, 0.7 beats 3 (not 0.8), and 0.4 beats 3. So AUC $= \frac{4 + 3 + 3}{3 \times 4} = \frac{10}{12} = 0.833$.

## 5.6 More than two classes

Compute precision and recall **for each class** (treating that class as positive and all the others as negative), then average:

- **Macro average:** the plain mean of the per-class values. Every class counts equally, so rare classes matter.
- **Micro average:** pool all the TP, FP and FN counts first, then compute. For single-label multi-class problems, micro-precision $=$ micro-recall $=$ micro-F1 $=$ **accuracy**.

In a multi-class confusion matrix (rows = truth, columns = prediction), class $k$ has **precision $= C_{kk}/\text{column}_k$ sum** and **recall $= C_{kk}/\text{row}_k$ sum**.

## 5.7 The probability view (and the Bayes link)

- **Recall** $= P(\text{predicted} + \mid \text{actual} +)$, the sensitivity of a test.
- **Precision** $= P(\text{actual} + \mid \text{predicted} +)$, which Bayes' theorem gives as

$$
\text{precision} = \frac{\text{sens}\cdot\pi}{\text{sens}\cdot\pi + (1 - \text{spec})(1 - \pi)},
$$

where $\pi$ is the prevalence (base rate). For a **rare** condition, even a good test has low precision. This is the same calculation as the disease-test PYQs in Probability (for example 2026 Q57).

---

## Summary: important points

<div class="formula">

1. Fix the positive class. Rows = truth, columns = prediction.
2. Precision $= TP/(TP + FP)$ uses the predicted column. Recall $= TP/(TP + FN)$ uses the actual row.
3. Specificity $= TN/(TN + FP)$ and FPR $= 1 -$ specificity.
4. F1 $= 2PR/(P + R) = 2TP/(2TP + FP + FN)$ is pulled towards the smaller of P and R.
5. Accuracy misleads on imbalanced data (always predicting "negative" can score 99%).
6. Raising the threshold never increases recall, and usually increases precision.
7. ROC is TPR vs FPR. AUC $=$ P(random positive outscores random negative). Random $= 0.5$.
8. Macro = mean of per-class values. Micro = pooled counts, which equals accuracy for single-label multi-class.

</div>

<div class="trap">

- In a 2-class problem, "precision of class Y" treats **Y** as the positive class. Its TP is the correctly classified Y items.
- Don't swap rows and columns. Re-read which one is the prediction.
- AUC is a ranking measure. It doesn't tell you the accuracy at any particular threshold.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2026 Q47 (2 marks, MSQ)

20 stories by author X and 10 by author Y are classified. 6 of X's stories are labelled Y, and 2 of Y's stories are labelled X. Treating X and Y as the two classes, which statements are true?
(A) Accuracy is 11/15 (B) The precision of class X is higher than the precision of class Y (C) The recall of class X is higher than the recall of class Y (D) Accuracy is 14/15

<details>
<summary>Show solution</summary>

**Answer: A; B**

Confusion matrix (rows = truth, columns = prediction):

| | pred X | pred Y | total |
|---|---|---|---|
| **true X** | 14 | 6 | 20 |
| **true Y** | 2 | 8 | 10 |
| **total** | 16 | 14 | 30 |

- **Accuracy** $= (14 + 8)/30 = 22/30 = 11/15$. (A) is true and (D) is false.
- **Precision X** $= 14/16 = 0.875$ and **precision Y** $= 8/14 \approx 0.571$. (B) is true.
- **Recall X** $= 14/20 = 0.70$ and **recall Y** $= 8/10 = 0.80$. X is lower, so (C) is false.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (2 marks, NAT).** TP = 40, FP = 10, FN = 20, TN = 30. What is the F1 score? (3 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.727**

$P = 40/50 = 0.8$ and $R = 40/60 = 0.667$. F1 $= \frac{2 \times 0.8 \times 0.667}{0.8 + 0.667} = 0.727$.

Check with the shortcut: $2TP/(2TP + FP + FN) = 80/110 = 0.727$. ✓

</details>

**F2 (1 mark, NAT).** For the same matrix, what is the false positive rate?

<details>
<summary>Show solution</summary>

**Answer: 0.25**

FPR $= FP/(FP + TN) = 10/40 = $ **0.25**. Specificity is $0.75$.

</details>

**F3 (2 marks, NAT).** Three positives get scores 0.9, 0.7 and 0.4. Four negatives get scores 0.8, 0.3, 0.2 and 0.1. What is the ROC AUC? (3 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.833**

Correctly ordered (positive, negative) pairs: $4 + 3 + 3 = 10$ out of $3 \times 4 = 12$. So $10/12 = $ **0.833**.

</details>

**F4 (2 marks, MSQ).** A dataset has 990 negatives and 10 positives. A model predicts "negative" for every item. Which statements are true?
(A) Accuracy is 0.99 (B) Recall is 0 (C) Precision is 1 (D) Specificity is 1

<details>
<summary>Show solution</summary>

**Answer: A; B; D**

- Recall $= 0/10 = 0$.
- Specificity $= 990/990 = 1$.
- Precision $= 0/0$ is **undefined** (no positive predictions), so (C) is false.

</details>

**F5 (2 marks, NAT).** A 3-class confusion matrix (rows = truth A, B, C; columns = prediction A, B, C) is $\begin{pmatrix}50 & 5 & 5\\ 10 & 30 & 10\\ 0 & 5 & 15\end{pmatrix}$. What is the macro-averaged precision? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.69**

Column sums are 60, 40, 30.

- Precision A $= 50/60 = 0.833$
- Precision B $= 30/40 = 0.75$
- Precision C $= 15/30 = 0.5$

Macro precision $= (0.833 + 0.75 + 0.5)/3 = 0.694 \approx$ **0.69**. (Micro precision equals accuracy $= 95/130 = 0.731$.)

</details>

**F6 (2 marks, NAT).** A disease affects 1% of people. A test has sensitivity 0.9 and specificity 0.95. What is the precision of a positive result? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.15**

$$\frac{0.9 \times 0.01}{0.9 \times 0.01 + 0.05 \times 0.99} = \frac{0.009}{0.0585} = 0.154.$$

Most positives are false alarms, because the disease is rare.

</details>

**F7 (1 mark, MSQ).** The decision threshold of a probabilistic classifier is raised from 0.5 to 0.8. Which statements are guaranteed?
(A) Recall does not increase (B) Precision strictly increases (C) The number of predicted positives does not increase (D) The ROC curve changes

<details>
<summary>Show solution</summary>

**Answer: A; C**

Fewer items cross the higher bar, so (C) holds, and the true positives can only drop, so (A) holds. Precision *usually* rises but isn't guaranteed to. The ROC curve is built from **all** thresholds, so changing the operating threshold doesn't change it.

</details>
