---
title: Artificial Intelligence
description: Every Artificial Intelligence question from GATE DA 2024–2026, mapped to topics, with the official answers.
sidebar:
  label: Overview & PYQ map
  order: 0
---

AI swung **11 → 3 → 8 marks**, the most volatile subject in the paper. Its questions are among the most **predictable** in GATE DA, though. Every search, game-tree and logic question so far was solved by **tracing an algorithm or a truth table by hand**.

## Official syllabus

> **Search:** informed, uninformed, adversarial. **Logic:** propositional, predicate. **Reasoning under uncertainty:** conditional independence representation, exact inference through variable elimination, and approximate inference through sampling.

## Every AI question, 2024–2026

| Year | Q | Marks | Type | Topic | What it tested | Answer |
|---|---|---|---|---|---|---|
| 2024 | 23 | 1 | MCQ | A* heuristics | Which combination of admissible heuristics is admissible | $\lvert h_1 - h_2\rvert$ |
| 2024 | 24 | 1 | MCQ | Bayesian networks | False conditional-independence claim (collider) | C |
| 2024 | 25 | 1 | MCQ | Alpha–beta | α = highest for MAX, β = lowest for MIN | C |
| 2024 | 29 | 1 | MSQ | Propositional logic | Which formulas are tautologies | B;C;D |
| 2024 | 44 | 2 | MCQ | Uninformed search | BFS vs DFS states expanded to reach goal 6 | equal |
| 2024 | 54 | 2 | MSQ | First-order logic | Translating "all balls are round except rugby balls" | A;C |
| 2024 | 64 | 2 | NAT | Bayesian networks | Joint probability from CPTs | 0.125 |
| 2025 | 15 | 1 | MCQ | Propositional logic | $p \to q \equiv \lnot p \lor q$ | A |
| 2025 | 26 | 1 | MSQ | BN inference | Exact (VE) vs approximate (sampling) | C;D |
| 2025 | 43 | 2 | MCQ | Alpha–beta | Ranges of x and y that cause pruning | C |
| 2025 | 44 | 2 | MCQ | A* | Expansion order on a weighted graph | C |
| 2026 | 13 | 1 | MCQ | Search | A* is not uninformed | C |
| 2026 | 14 | 1 | MCQ | First-order logic | ∀ must pair with ⇒, not ∧ | C |
| 2026 | 24 | 1 | MSQ | Propositional logic | What "X entails Y" means | A;B;C |
| 2026 | 30 | 1 | NAT | Minimax | MAX's best move in a 2-ply game | 2 |
| 2026 | 38 | 2 | MCQ | Propositional logic | Formalising an English rule | B |
| 2026 | 48 | 2 | MSQ | First-order logic | Which quantified sentences are not valid | B;C;D |

## What the table says

| Topic | Questions | Verdict |
|---|---|---|
| Propositional logic | **4** | <span class="tag high">Every year</span> Truth tables and equivalences. |
| Adversarial search (minimax, α–β) | **3** | <span class="tag high">Every year</span> Trace the tree. |
| First-order logic | **3** | <span class="tag high">2 of 3 yrs</span> ∀⇒ / ∃∧ translation. |
| Informed search (A*) | 2 | <span class="tag high">2 of 3 yrs</span> |
| Uninformed search | 2 | <span class="tag med">2 of 3 yrs</span> |
| Bayesian networks | 2 | <span class="tag med">2024</span> Factorisation and independence. |
| Inference (VE, sampling) | 1 | <span class="tag med">2025</span> Exact vs approximate. |

:::tip[Cheap marks]
AI questions are short and deterministic. A careful trace of minimax, A* or a truth table always gives the exact answer, and there's nothing to estimate.
:::

## Study material in the repo

- [revision-sheet.pdf](https://github.com/ashyou09/Gate-da/blob/main/subjects/ai/revision-sheet.pdf)
- [question-bank.pdf](https://github.com/ashyou09/Gate-da/blob/main/subjects/ai/question-bank.pdf)
