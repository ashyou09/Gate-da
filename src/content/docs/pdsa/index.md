---
title: PDSA — Overview & PYQ analysis
description: Every Programming, Data Structures & Algorithms question from GATE DA 2024–2026, mapped to topics.
sidebar:
  label: Overview & PYQ map
---

**Programming, Data Structures & Algorithms** carried **17, 16 and 16 marks** in 2024, 2025 and 2026. It's the most stable subject in GATE DA. If you're solid here, about 16 marks are close to guaranteed.

## Official syllabus

> Programming in Python. Basic data structures: stacks, queues, linked lists, trees, hash tables. Search algorithms: linear search and binary search. Basic sorting algorithms: selection sort, bubble sort and insertion sort. Divide and conquer: mergesort, quicksort. Introduction to graph theory. Basic graph algorithms: traversals and shortest path.

Not in the DA syllabus, so don't overspend time on them: heavy dynamic programming, NP-completeness proofs, AVL rotations, B-trees (B+ trees are covered in DBMS).

## Every PDSA question, 2024–2026

| Year | Q | Marks | Type | Topic | What it tested | Answer |
|---|---|---|---|---|---|---|
| 2024 | 16 | 1 | MCQ | Stack / queue / hash | Match FIFO, LIFO, lookup | A |
| 2024 | 21 | 1 | MCQ | Hashing | Expected probes to insert, open addressing | $\frac{1}{1-\alpha}$ |
| 2024 | 14 | 1 | MCQ | Graphs | DFS edge classification | tree |
| 2024 | 28 | 1 | MSQ | Trees | Which traversal pairs rebuild a full binary tree | A;B;C |
| 2024 | 30 | 1 | NAT | Sorting | Quicksort swaps on sorted input | 0 |
| 2024 | 32 | 1 | NAT | Deque | Trace insert/remove at both ends | 17 |
| 2024 | 38 | 2 | MCQ | Python + recursion | Recursive count over a dict tree | 9 |
| 2024 | 40 | 2 | MCQ | Recurrences | Binary search comparison recurrence | $F(n)=F(\lfloor n/2\rfloor)+1$ |
| 2024 | 41 | 2 | MCQ | Python + recursion | Recursive swap reverses a list | C |
| 2024 | 45 | 2 | MCQ | Sorting | Which sort finishes after 2 passes | Selection |
| 2024 | 51 | 2 | MSQ | Graphs | Valid topological orders | B;D |
| 2025 | 18 | 1 | MCQ | Hashing | Linear probing with $h(x)=3x \bmod 10$ | 4 and 6 |
| 2025 | 23 | 1 | MCQ | Python | `extend` vs `append` | `A.extend(B)` |
| 2025 | 27 | 1 | MSQ | Searching | When binary search is $O(\log n)$ | sorted array only |
| 2025 | 29 | 1 | MSQ | Sorting | Insertion sort with exactly 2 swaps | 10, 14 |
| 2025 | 47 | 2 | MCQ | Python | Set operations + tuple assignment | Only B |
| 2025 | 58 | 2 | MSQ | Graphs | Shortest-path constraints → which edges can't exist | A;C;D |
| 2025 | 63 | 2 | NAT | Python + recursion | Recursive `f(15,10)` with float division | 160 |
| 2025 | 64 | 2 | NAT | Stack | Push/pop pseudocode trace | 24 |
| 2025 | 65 | 2 | NAT | Graphs | DFS discovery order on a structured graph | 75 |
| 2026 | 15 | 1 | MCQ | Recurrences | Expected-time recurrence of quicksort | averaged sum |
| 2026 | 16 | 1 | MCQ | Python | Mutable default argument | `[1] [1,2] [3]` |
| 2026 | 25 | 1 | MSQ | Trees | Rebuild a tree from pre-order + in-order | A;B |
| 2026 | 31 | 1 | NAT | Searching | Max comparisons, binary search, $n=1000$ | 10 |
| 2026 | 39 | 2 | MCQ | Recursion | Total stack activations of `mystery(4)` | 15 |
| 2026 | 40 | 2 | MSQ | Graphs | Reachability in the reversed graph | D |
| 2026 | 49 | 2 | MSQ | Sorting | Bubble vs insertion comparison counts | B;C;D |
| 2026 | 50 | 2 | MSQ | Python | Closures, separate enclosing lists | B;D |
| 2026 | 58 | 2 | NAT | Python + sorting | Recursive bubble pass, total swaps | 8 |

## What the table says

| Topic | Questions (3 yrs) | Verdict |
|---|---|---|
| Python semantics & code tracing | **8** | <span class="tag high">Every year</span> 2-mark NATs. Biggest single block. |
| Sorting (bubble / insertion / selection / quick) | **6** | <span class="tag high">Every year</span> Counting passes, swaps and comparisons. |
| Graphs (BFS, DFS, topological order, reachability) | **5** | <span class="tag high">Every year</span> Property-based MSQs. |
| Recursion (call counting, tracing) | 5 (overlaps Python) | <span class="tag high">Every year</span> Draw the call tree. |
| Binary search & recurrences | 4 | <span class="tag high">Every year</span> $\lfloor\log_2 n\rfloor+1$. |
| Hashing | 3 | <span class="tag med">2 of 3 yrs</span> Linear probing trace. |
| Stacks / queues / deques | 3 | <span class="tag med">2 of 3 yrs</span> Operation trace. |
| Tree traversals | 2 | <span class="tag med">2 of 3 yrs</span> Rebuild from two traversals. |
| Linked lists, heaps, shortest paths, MST, DP | 0 | <span class="tag low">Not yet asked</span> In syllabus. Learn the core facts. |

:::caution[Pattern across all 3 papers]
Almost every PDSA mark came from **tracing**: running code, a sort or a traversal by hand on paper. Very few questions asked you to recall definitions. Practise tracing slowly and carefully. Speed comes later.
:::

## Topic pages (study in this order)

1. [Python semantics & code tracing](/pdsa/python-semantics/)
2. [Recursion & call counting](/pdsa/recursion-tracing/)
3. [Asymptotic complexity & recurrences](/pdsa/complexity-recurrences/)
4. [Searching & sorting](/pdsa/searching-sorting/)
5. Graphs: BFS, DFS, topological sort, shortest paths *(next)*
6. Hashing *(next)*
7. Stacks, queues, deques & linked lists *(next)*
8. Trees, BST & heaps *(next)*
9. Divide & conquer, greedy & DP basics *(next)*
