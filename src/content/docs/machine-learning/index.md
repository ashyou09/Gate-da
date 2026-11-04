---
title: Machine Learning
description: Every Machine Learning question from GATE DA 2024–2026, mapped to topics, with the official answers.
sidebar:
  label: Overview & PYQ map
  order: 0
---

Machine Learning is the fastest-growing subject in GATE DA: **11 → 14 → 16 marks**. The questions lean towards **small numericals** (a gradient step, an information gain, a parameter count) and **property MSQs** (what a regularizer does, which linkage uses min or max). Long derivations are rare.

## Official syllabus

> **Supervised learning:** regression and classification problems, simple linear regression, multiple linear regression, ridge regression, logistic regression, k-nearest neighbour, naive Bayes classifier, linear discriminant analysis, support vector machine, decision trees, bias-variance trade-off, cross-validation methods such as leave-one-out (LOO) cross-validation, k-folds cross-validation, multi-layer perceptron, feed-forward neural network.
> **Unsupervised learning:** clustering algorithms, k-means/k-medoid, hierarchical clustering, top-down, bottom-up: single-linkage, multiple-linkage, dimensionality reduction, principal component analysis.

## Every ML question, 2024–2026

| Year | Q | Marks | Type | Topic | What it tested | Answer |
|---|---|---|---|---|---|---|
| 2024 | 17 | 1 | MCQ | SVM | Which points can be support vectors (hard margin) | D |
| 2024 | 18 | 1 | MCQ | Foundations / PCA | PCA → dim. reduction, naive Bayes → generative, logistic → discriminative | C |
| 2024 | 19 | 1 | MCQ | Clustering | A point that must share a k-means cluster (convex cells) | (0, 1) |
| 2024 | 20 | 1 | MCQ | Naive Bayes | Parameters for $K$ binary features, 2 classes | $2K + 1$ |
| 2024 | 22 | 1 | MCQ | LDA | Fisher criterion gives $S_W^{-1}S_B u = \lambda u$ | A |
| 2024 | 33 | 1 | NAT | Logistic / sigmoid | $\sigma'(x)$ where $\sigma(x) = 0.4$ | 0.24 |
| 2024 | 42 | 2 | MCQ | Clustering | Single-linkage dendrogram from a distance table | A |
| 2024 | 43 | 2 | MCQ | Neural networks | Equivalent ReLU networks (positive inputs) | A |
| 2024 | 53 | 2 | MSQ | Linear classifiers | Which plotted datasets are linearly separable | A;D |
| 2024 | 62 | 2 | NAT | Decision trees | Information gain of an attribute | 0.12 |
| 2024 | 63 | 2 | NAT | k-NN | Smallest odd $k$ that flips the label | 5 |
| 2025 | 22 | 1 | MCQ | Linear classifiers | Perceptron update increases $f(x_n)$ | A |
| 2025 | 30 | 1 | MSQ | Clustering | Single = min distance, complete = max distance | B;D |
| 2025 | 34 | 1 | NAT | Linear regression | Least squares for $y = wx$ | 0.286 |
| 2025 | 35 | 1 | NAT | Naive Bayes | Probability of misclassification | 0.40 |
| 2025 | 42 | 2 | MCQ | Neural networks | Backprop gradients through ReLU | A |
| 2025 | 48 | 2 | MSQ | Neural networks | ReLU continuity and differentiability | A;C |
| 2025 | 53 | 2 | MSQ | SVM | Hard-margin SVM: support vectors and margin | B;C |
| 2025 | 55 | 2 | MSQ | Linear classifiers / LDA | Nearest-mean classifier is linear | B;C |
| 2025 | 60 | 2 | NAT | PCA | Variance along the top eigenvector | 100 |
| 2026 | 11 | 1 | MCQ | PCA | Angle between principal components | 90° |
| 2026 | 12 | 1 | MCQ | Foundations | Number of LOOCV splits | 900 |
| 2026 | 23 | 1 | MSQ | Foundations / clustering | Match task ↔ algorithm | B |
| 2026 | 29 | 1 | NAT | Gradient descent | One SGD step | 9.00 |
| 2026 | 36 | 2 | MCQ | Clustering | First merge in HAC (Manhattan distance) | P2, P4 |
| 2026 | 37 | 2 | MCQ | Ridge | What the L2 regularizer does | D |
| 2026 | 47 | 2 | MSQ | Metrics | Accuracy, precision, recall from counts | A;B |
| 2026 | 55 | 2 | NAT | Ridge | Regularized loss value | 7.00 |
| 2026 | 56 | 2 | NAT | Neural networks | Parameter count of an MLP | 135 |

*2024 Q27 (z-score normalisation) is counted under DBMS → data transformation, where the syllabus places it.*

## What the table says

| Topic | Questions | Verdict |
|---|---|---|
| Clustering (k-means, hierarchical, linkage) | **5** | <span class="tag high">Every year</span> Merge order and linkage definitions. |
| Neural networks (forward pass, backprop, counting) | **4** | <span class="tag high">Every year</span> Parameter counts and ReLU gradients. |
| Linear classifiers, sigmoid, perceptron | **4** | <span class="tag high">2 of 3 yrs</span> Properties of linear decision rules. |
| Foundations (types of models, CV, bias–variance) | **4** | <span class="tag high">2 of 3 yrs</span> Cheap 1-markers. |
| PCA | **3** | <span class="tag high">Every year</span> Variance = eigenvalue; components are orthogonal. |
| k-NN & naive Bayes | **3** | <span class="tag high">2 of 3 yrs</span> |
| Linear regression & gradient descent | 2 | <span class="tag med">2 of 3 yrs</span> One-line numericals. |
| Ridge / regularization | 2 | <span class="tag med">2026 ×2</span> Likely to repeat. |
| SVM | 2 | <span class="tag med">2 of 3 yrs</span> Support vectors and margin. |
| LDA | 2 | <span class="tag med">2 of 3 yrs</span> |
| Decision trees, metrics | 1 each | <span class="tag med">Once</span> Quick numericals. Learn them fully. |

Some questions test two topics at once, so the topic counts add up to more than 29.

:::tip[How to read the pattern]
Almost every ML question so far is short **once you know the definition exactly**. The skill being tested is precision: knowing exactly what single linkage, a support vector or ridge regression means.
:::

## Study material in the repo

- [revision-sheet.pdf](https://github.com/ashyou09/Gate-da/blob/main/subjects/machine-learning/revision-sheet.pdf)
- [question-bank.pdf](https://github.com/ashyou09/Gate-da/blob/main/subjects/machine-learning/question-bank.pdf)
- [notes/gradients-and-optimizers.docx](https://github.com/ashyou09/Gate-da/blob/main/subjects/machine-learning/notes/gradients-and-optimizers.docx)
- [notes/loss-functions.docx](https://github.com/ashyou09/Gate-da/blob/main/subjects/machine-learning/notes/loss-functions.docx)
