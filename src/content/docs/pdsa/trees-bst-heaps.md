---
title: 8. Trees, BST & heaps
description: Binary tree counting facts, traversals and reconstruction, BST insert/delete, and binary heaps in arrays with build-heap, insert and extract.
sidebar:
  label: 8. Trees, BST & heaps
  order: 8
---

**Why it matters:** 2024 Q28 and Q52 and 2026 Q25 are tree questions: rebuilding a tree from traversals, and counting facts about binary trees. Heaps and BSTs haven't been asked yet, but they're in the syllabus and are a natural next question ("build a heap from this array", "insert these keys into a BST").

## Topic map

<div class="mindmap">

- **Trees**
  - Binary tree facts
    - height, levels, max nodes $2^{h+1} - 1$
    - leaves = (nodes with 2 children) + 1
    - full / complete / perfect
  - Traversals
    - pre (N L R), in (L N R), post (L R N), level order
    - rebuilding: in + pre, or in + post (pre + post only for full trees)
  - Binary search tree
    - left < node < right, inorder is sorted
    - search / insert / delete in $O(h)$
  - Heap
    - complete tree stored in an array
    - parent $\lfloor (i-1)/2 \rfloor$, children $2i+1$, $2i+2$
    - build-heap $O(n)$, insert / extract $O(\log n)$
    - heapsort, priority queue, `heapq`

</div>

## 8.1 Binary tree vocabulary and counting facts

Each node has **at most two** children. **Height** $h$ is the number of edges on the longest root-to-leaf path, so a single node has height 0. **Depth** is the distance from the root. **Level** $k$ holds at most $2^k$ nodes.

| Kind | Definition |
|---|---|
| **Full** (proper) | every node has 0 or 2 children |
| **Complete** | every level is full except possibly the last, which is filled from the **left** |
| **Perfect** | every internal node has 2 children and every leaf is at the same depth |

<div class="formula">

For a binary tree with $N$ nodes, height $H$, $I$ internal nodes and $L$ leaves:

$$
H + 1 \;\le\; N \;\le\; 2^{H+1} - 1 \qquad\qquad \lceil\log_2(N+1)\rceil - 1 \;\le\; H \;\le\; N - 1
$$

$$
L = n_2 + 1 \;\;(\,n_2 = \text{nodes with two children}) \qquad\Rightarrow\qquad L \le I + 1, \text{ with equality iff the tree is full}
$$

$$
H \le I \le 2^H - 1 \qquad\qquad 1 \le L \le 2^H
$$

The number of structurally different binary trees on $n$ nodes is the Catalan number $C_n$. So is the number of different BSTs on $n$ distinct keys.

</div>

## 8.2 Traversals

| Traversal | Order | Use |
|---|---|---|
| Preorder | **N**ode, Left, Right | copy a tree; the root comes **first** |
| Inorder | Left, **N**ode, Right | gives **sorted** order for a BST |
| Postorder | Left, Right, **N**ode | delete or evaluate a tree; the root comes **last** |
| Level order | level by level, left to right | BFS with a queue |

### Rebuilding a tree from two traversals

The method, for preorder + inorder:

1. The **first** preorder element is the root.
2. Find the root in the inorder list. Everything to its left is the left subtree, everything to its right is the right subtree.
3. Split the rest of the preorder list by those subtree sizes, and recurse on each part.

For postorder + inorder, do the same but take the root from the **end** of the postorder list.

<div class="formula">

| Traversals given | Unique tree? |
|---|---|
| inorder + preorder | yes |
| inorder + postorder | yes |
| preorder + postorder | **only for full binary trees** (otherwise you can't tell a lone child's side) |
| a single traversal | no (unless it's a BST, where inorder is just the sorted keys) |

</div>

## 8.3 Binary search trees

**BST property:** every key in the left subtree is less than the node, and every key in the right subtree is greater. So the **inorder traversal is sorted**, which is the fastest way to check any BST answer.

- **Search / insert:** walk down, going left if smaller and right if larger. A new key always becomes a **leaf**. Cost $O(h)$.
- **Delete** has three cases:
  1. leaf: just remove it;
  2. one child: replace the node with that child;
  3. two children: replace the key with its **inorder successor** (the minimum of the right subtree), then delete that successor. The successor has no left child, so this reduces to case 1 or 2.
- $h = \Theta(\log n)$ when balanced, but $\Theta(n)$ when keys are inserted in **sorted order** (a skewed chain).

Example: insert 45, 20, 60, 10, 30, 50, 70, 25, 35, 65.

```
              45
           /      \
         20        60
        /  \      /  \
      10    30   50   70
           /  \       /
         25    35    65
```

- Preorder: 45 20 10 30 25 35 60 50 70 65
- Postorder: 10 25 35 30 20 50 65 70 60 45
- Height 3, with 5 leaves (10, 25, 35, 50, 65).

## 8.4 Binary heaps

A **max-heap** is a **complete** binary tree in which every parent is $\ge$ its children (a min-heap uses $\le$). Because it's complete, it fits in an **array** with no gaps.

<div class="formula">

**0-based indexing:** parent$(i) = \lfloor (i-1)/2 \rfloor$, left$(i) = 2i + 1$, right$(i) = 2i + 2$

**1-based indexing:** parent$(i) = \lfloor i/2 \rfloor$, left $= 2i$, right $= 2i + 1$

The leaves are the last $\lceil n/2 \rceil$ positions. The height is $\lfloor \log_2 n \rfloor$.

| Operation | How | Cost |
|---|---|---|
| peek max | `A[0]` | $O(1)$ |
| insert | append at the end, **sift up** | $O(\log n)$ |
| extract max | move the last element to the root, **sift down** | $O(\log n)$ |
| build-heap (bottom-up) | sift down $i = \lfloor n/2 \rfloor - 1, \dots, 0$ | $\Theta(n)$ |
| build by $n$ inserts | insert one at a time | $O(n\log n)$, and can give a **different** heap |
| heapsort | build, then extract $n$ times | $\Theta(n\log n)$, in place, **not stable** |

</div>

**Why is bottom-up build-heap $\Theta(n)$?** Most nodes sit near the bottom and sift only a little: about $n/4$ nodes sift 1 level, $n/8$ sift 2 levels, and so on. Adding it up:

$$
\sum_{h \ge 0} \frac{n}{2^{h+1}} \cdot h \;=\; O(n).
$$

**Sift down:** swap the node with its **larger** child (for a max-heap) until it's at least as big as both children.

Python's `heapq` is a **min-heap** on a plain list. For a max-heap, push negated values.

---

## Summary: important points

<div class="formula">

1. $H + 1 \le N \le 2^{H+1} - 1$. Leaves $=$ (nodes with 2 children) $+ 1$. $L \le I + 1$.
2. Pre: root first. Post: root last. In: root in the middle, and sorted for a BST.
3. Inorder + pre, or inorder + post, gives a unique tree. Pre + post is unique only for **full** trees.
4. BST operations are $O(h)$. Sorted insertions give $h = n - 1$.
5. BST delete with two children: copy in the inorder successor, then delete it.
6. Heap = complete tree in an array: children $2i+1$, $2i+2$, parent $\lfloor (i-1)/2 \rfloor$.
7. Bottom-up build-heap is $\Theta(n)$. Insert and extract are $O(\log n)$. Heapsort is $\Theta(n\log n)$ and not stable.
8. $C_n$ counts binary trees with $n$ nodes and BSTs on $n$ keys.

</div>

<div class="trap">

- Height counts **edges** here (a single node has height 0). Some books count nodes. Check how the question defines it.
- Build-heap by repeated insertion and bottom-up build-heap can give **different** arrays.
- A heap is **not** sorted. Only the root is guaranteed to be the maximum.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2026 Q25 (1 mark, MSQ)

A binary tree on E, F, G, P, Q, R, S has preorder **P Q S E R F G** and inorder **S Q E P F R G**. Which are true?
(A) P is the root (B) The postorder is S E Q F G R P (C) Q has only one child (D) The left subtree of R contains G

<details>
<summary>Show solution</summary>

**Answer: A; B**

1. Preorder starts with **P**, so P is the root. Inorder splits around P into left {S, Q, E} and right {F, R, G}.
2. Left part: its preorder is Q S E, so the root is **Q**. Inorder S Q E puts **S** on Q's left and **E** on its right.
3. Right part: its preorder is R F G, so the root is **R**. Inorder F R G puts **F** on R's left and **G** on its right.

```
        P
      /   \
     Q     R
    / \   / \
   S   E F   G
```

- Postorder (L R N): S E Q F G R P. (B) is true.
- Q has two children, so (C) is false.
- G is in R's **right** subtree, so (D) is false.

</details>

### GATE DA 2024 Q28 (1 mark, MSQ)

For a **full** binary tree, which pairs of traversals are enough to rebuild it uniquely?
(A) pre + in (B) in + post (C) pre + post (D) in only

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

Inorder plus either preorder or postorder always works. Preorder plus postorder fails in general only because a node with **one** child doesn't reveal which side that child is on. A full binary tree has no one-child nodes, so (C) works too. Inorder alone doesn't fix the shape, so (D) fails.

</details>

### GATE DA 2024 Q52 (2 marks, MSQ)

For a rooted binary tree with height $H$, $I$ internal nodes, $L$ leaves and $N$ nodes in total, which are always true?
(A) $L \le I + 1$ (B) $H + 1 \le N \le 2^{H+1} - 1$ (C) $H \le I \le 2^H - 1$ (D) $H \le L \le 2^{H-1}$

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

- **(A)** $L = n_2 + 1 \le I + 1$, because $n_2 \le I$. True.
- **(B)** The minimum is a path ($H + 1$ nodes). The maximum is a perfect tree ($2^{H+1} - 1$ nodes). True.
- **(C)** Every node on the longest path except the leaf is internal, so $I \ge H$. All internal nodes sit on levels $0 \dots H-1$, so $I \le 2^H - 1$. True.
- **(D)** A path of height $H$ has only **1** leaf, and $1 < H$ once $H \ge 2$. False. (A tree can also have up to $2^H$ leaves, more than $2^{H-1}$.)

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, MCQ).** Insert 45, 20, 60, 10, 30, 50, 70, 25, 35, 65 into an empty BST. What is the postorder traversal?
(A) 10 25 35 30 20 50 65 70 60 45 (B) 10 20 25 30 35 45 50 60 65 70 (C) 45 20 10 30 25 35 60 50 70 65 (D) 10 30 25 35 20 50 70 65 60 45

<details>
<summary>Show solution</summary>

**Answer: (A)**

Draw the tree as in §8.3, then read left, right, node. (B) is the inorder (sorted) and (C) is the preorder, both common distractors.

</details>

**F2 (2 marks, MCQ).** In that same BST, delete 20, then delete 45, each time using the inorder **successor**. What is the preorder afterwards?

<details>
<summary>Show solution</summary>

**Answer: 50 25 10 30 35 60 70 65**

1. **Delete 20** (two children). Its successor is the minimum of {30, 25, 35}, which is **25**. Copy 25 into 20's place, then delete the old 25 (a leaf). Preorder: 45 25 10 30 35 60 50 70 65.
2. **Delete 45** (the root, two children). Its successor is the minimum of the right subtree, which is **50**. Copy 50 into the root, then delete the old 50 (a leaf).

Preorder: **50 25 10 30 35 60 70 65**.

</details>

**F3 (2 marks, MCQ).** Build a max-heap from `[3, 9, 2, 1, 4, 5, 8, 7]` with the bottom-up method (0-based indexing). What is the resulting array?

<details>
<summary>Show solution</summary>

**Answer: [9, 7, 8, 3, 4, 5, 2, 1]**

$n = 8$, so sift down $i = 3, 2, 1, 0$.

| $i$ | Value | Children | Action | Array |
|---|---|---|---|---|
| 3 | 1 | 7 | swap with 7 | [3, 9, 2, 7, 4, 5, 8, 1] |
| 2 | 2 | 5, 8 | swap with 8 | [3, 9, 8, 7, 4, 5, 2, 1] |
| 1 | 9 | 7, 4 | no swap | — |
| 0 | 3 | 9, 8 | swap with 9, then at index 1 swap with 7, then at index 3 the child is 1, so stop | [9, 7, 8, 3, 4, 5, 2, 1] |

That's 4 swaps in total. Inserting the elements one at a time instead gives `[9, 7, 8, 4, 3, 2, 5, 1]`, a **different** valid heap.

</details>

**F4 (1 mark, NAT).** Run extract-max once on the heap from F3. What value is now at index 2?

<details>
<summary>Show solution</summary>

**Answer: 5**

Remove 9 and move the last element, 1, to the root: [1, 7, 8, 3, 4, 5, 2].

- At the root, swap with the larger child, 8 (index 2): [8, 7, 1, 3, 4, 5, 2].
- At index 2, the children are 5 and 2. Swap with 5: [8, 7, **5**, 3, 4, 1, 2].

</details>

**F5 (1 mark, NAT).** Preorder **A B D E C F G** and inorder **D B E A F C G**. What is the postorder?

<details>
<summary>Show solution</summary>

**Answer: D E B F G C A**

The root is A. The left part is {D, B, E} with root B (D on its left, E on its right). The right part is {F, C, G} with root C (F on its left, G on its right). Reading left, right, node gives D E B F G C A.

</details>

**F6 (1 mark, NAT).** How many structurally different BSTs can be built from the keys {1, 2, 3, 4}?

<details>
<summary>Show solution</summary>

**Answer: 14**

$C_4 = \frac{1}{5}\binom84 = \frac{70}{5} = 14$.

</details>
