---
title: 5. Graphs — traversals & shortest paths
description: Graph vocabulary, adjacency lists, BFS, DFS and edge types, topological sort, reachability, Dijkstra, Bellman-Ford and minimum spanning trees.
sidebar:
  label: 5. Graphs
  order: 5
---

**Why it matters:** graphs appeared in all three papers (2024 Q14 and Q51, 2025 Q58 and Q65, 2026 Q40). Almost every one was a **property question**: what a traversal guarantees, which orders are valid, which edges can't exist. If you know exactly what BFS, DFS and topological order promise, these become quick marks.

## Topic map

<div class="mindmap">

- **Graphs**
  - Vocabulary
    - directed / undirected, weighted
    - degree, path, cycle, connected, DAG
    - $\sum \deg = 2E$, tree has $V-1$ edges
  - Representation
    - adjacency matrix $\Theta(V^2)$
    - adjacency list $\Theta(V+E)$
  - Traversals
    - BFS: queue, levels, unweighted shortest paths
    - DFS: stack/recursion, discovery & finish times, edge types
  - DAG tools
    - topological order (Kahn, DFS finish times)
    - cycle detection = back edge
  - Shortest paths
    - BFS (unweighted), Dijkstra ($w \ge 0$), Bellman-Ford (negative edges)
  - Minimum spanning tree
    - Kruskal, Prim, cut property

</div>

## 5.1 Vocabulary you must be fluent in

A **graph** $G = (V, E)$ is a set of vertices joined by edges. Write $n = |V|$ and $m = |E|$.

| Term | Meaning |
|---|---|
| Undirected / directed | edge $\{u, v\}$ works both ways / edge $(u, v)$ goes from $u$ to $v$ only |
| Degree | number of edges at a vertex. Directed graphs split it into in-degree and out-degree |
| Path / cycle | a sequence of edges / a path that returns to its start |
| Connected | every vertex reachable from every other (undirected) |
| Strongly connected | every vertex reachable from every other **following edge directions** |
| DAG | directed acyclic graph: directed, with no directed cycle |
| Tree | connected and acyclic. Equivalently, connected with exactly $n - 1$ edges |
| Simple graph | no self-loops and no parallel edges |

<div class="formula">

**Counting facts**

$$
\sum_{v} \deg(v) = 2m \quad\text{(handshake lemma)} \qquad\Rightarrow\qquad \text{the number of odd-degree vertices is even}
$$

$$
\text{simple undirected: } m \le \binom n2 = \frac{n(n-1)}{2} \qquad \text{simple directed: } m \le n(n-1)
$$

A tree on $n$ vertices has exactly $n - 1$ edges. A forest with $k$ components has $n - k$ edges.

</div>

## 5.2 Storing a graph

| | Adjacency matrix | Adjacency list |
|---|---|---|
| Space | $\Theta(n^2)$ | $\Theta(n + m)$ |
| "Is $(u, v)$ an edge?" | $O(1)$ | $O(\deg u)$ |
| List the neighbours of $u$ | $\Theta(n)$ | $\Theta(\deg u)$ |
| BFS / DFS total | $\Theta(n^2)$ | $\Theta(n + m)$ |

In Python, the standard form is a dict of lists: `adj = {'A': ['B', 'C'], ...}`.

**The order of each adjacency list decides which vertex a traversal visits next.** GATE always tells you the order ("alphabetical", "decreasing vertex number"). Use exactly that order.

## 5.3 Breadth-first search (BFS)

BFS explores in **rings**: first the source, then everything at distance 1, then everything at distance 2, and so on. A **queue** (FIFO) is what enforces that order.

```python
from collections import deque
def bfs(adj, s):
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:              # in the given adjacency order
            if v not in dist:         # first time seen = shortest
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

<div class="formula">

- Time $\Theta(n + m)$ with adjacency lists.
- In an **unweighted** graph, `dist[v]` is the **shortest-path length** from $s$. This is BFS's main guarantee.
- Vertices leave the queue in non-decreasing order of distance.
- In an **undirected** BFS, every non-tree edge joins vertices whose levels differ by **at most 1**.

</div>

## 5.4 Depth-first search (DFS)

DFS goes **as deep as possible** before backing up. It's usually written recursively, so the call stack does the work.

```python
def dfs(adj, u, seen, order):
    seen.add(u); order.append(u)       # discovered
    for v in adj[u]:
        if v not in seen:
            dfs(adj, v, seen, order)
    # u finishes here, after all its descendants
```

Give each vertex a **discovery time** $d[u]$ and a **finish time** $f[u]$, using one clock that ticks at every discovery and every finish.

**Parenthesis theorem:** for any two vertices, their intervals $[d, f]$ are either **nested** (one is a descendant of the other) or **disjoint**. They never partly overlap.

### Edge classification

When DFS looks along an edge $(u, v)$, the colour of $v$ at that moment decides the edge's type:

| $v$ is… | Edge type | Meaning |
|---|---|---|
| white (not yet seen) | **tree** | DFS goes to $v$ through this edge |
| gray (started, not finished) | **back** | $v$ is an ancestor of $u$, so there's a **cycle** |
| black, and $d[u] < d[v]$ | **forward** | $v$ is a descendant reached another way (directed only) |
| black, and $d[u] > d[v]$ | **cross** | a different branch (directed only) |

<div class="formula">

- **Undirected** DFS produces only **tree** and **back** edges.
- A **directed** graph has a cycle **if and only if** DFS finds a back edge.
- DFS does **not** give shortest paths.

</div>

## 5.5 Topological order (DAGs only)

A **topological order** lists the vertices so that every edge $u \to v$ has $u$ **before** $v$. One exists **if and only if** the graph is a DAG.

**Kahn's algorithm (BFS style):** repeatedly output a vertex with in-degree 0, then delete its outgoing edges. If vertices remain but none has in-degree 0, there's a cycle.

**DFS method:** run DFS and list the vertices in **decreasing finish time**.

**Checking a proposed order** (the GATE question): go through every edge and make sure its tail appears before its head. One violated edge rules the order out.

**Counting orders:** if the DAG splits into independent chains after some point, count the ways to interleave them. Two chains of lengths $a$ and $b$ interleave in $\binom{a+b}{a}$ ways.

## 5.6 Reachability and the reversed graph

$G^R$ is $G$ with every edge reversed. A path $v \to \dots \to u$ in $G$ is exactly a path $u \to \dots \to v$ in $G^R$.

<div class="formula">

$u$ is reachable from $v$ in $G$ $\iff$ $v$ is reachable from $u$ in $G^R$.

A traversal from $s$ visits **exactly the set of vertices reachable from $s$**, whether it's BFS or DFS. Only the visiting order differs.

</div>

## 5.7 Shortest paths in weighted graphs

| Situation | Algorithm | Time |
|---|---|---|
| unweighted (or all weights equal) | BFS | $O(n + m)$ |
| weights $\ge 0$ | **Dijkstra** | $O((n + m)\log n)$ with a binary heap |
| some negative weights, no negative cycle | **Bellman-Ford** | $O(nm)$ |
| DAG, any weights | relax edges in topological order | $O(n + m)$ |
| all pairs | Floyd-Warshall | $O(n^3)$ |

**Relaxing** an edge $(u, v)$ with weight $w$ means: if $d[u] + w < d[v]$, set $d[v] = d[u] + w$.

**Dijkstra** is greedy. It repeatedly takes the unfinished vertex with the smallest $d$, fixes that value, and relaxes its outgoing edges. That's correct only when no edge is negative: a negative edge could later lower a value that was already fixed.

**Bellman-Ford** relaxes **every** edge $n - 1$ times. If an $n$th round still improves something, there's a **negative cycle**.

**Subpaths of shortest paths are shortest paths.** 2025 Q58 is built entirely on this fact.

## 5.8 Minimum spanning tree (MST)

A **spanning tree** connects all $n$ vertices using $n - 1$ edges. An **MST** is the one with the smallest total weight (connected, undirected, weighted graphs only).

- **Kruskal:** sort the edges by weight and add each one unless it creates a cycle (checked with union-find). $O(m\log m)$.
- **Prim:** grow one tree from a start vertex, always adding the cheapest edge that leaves the tree. $O(m\log n)$ with a heap.
- **Cut property:** the lightest edge crossing any cut belongs to some MST. If all weights are distinct, the MST is **unique**.
- The MST is **not** a shortest-path tree. They answer different questions.

---

## Summary: important points

<div class="formula">

1. $\sum \deg = 2m$. A tree has $n - 1$ edges. A simple undirected graph has at most $\binom n2$ edges.
2. BFS uses a queue, gives shortest paths in **unweighted** graphs, and runs in $O(n + m)$.
3. DFS uses a stack or recursion and gives discovery and finish times. Undirected DFS has only tree and back edges.
4. A back edge exists $\iff$ there's a cycle. A topological order exists $\iff$ the graph is a DAG.
5. To check a topological order, test every edge: tail before head.
6. Reachable from $v$ in $G$ $\iff$ reaches $v$ in $G^R$. BFS and DFS visit the same **set** of vertices, in different orders.
7. Dijkstra needs weights $\ge 0$. Bellman-Ford handles negative edges and detects negative cycles in $O(nm)$.
8. Every subpath of a shortest path is itself a shortest path.
9. Kruskal and Prim build an MST with $n - 1$ edges. Distinct weights mean a unique MST.

</div>

<div class="trap">

- Follow the **given** adjacency order. Visiting neighbours in your own order changes the answer.
- Don't use Dijkstra when there are negative edges.
- "Shortest path" in an **unweighted** graph means BFS, never DFS.
- A topological order isn't unique. The question asks which orders are **valid**, not which one is "the" order.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q51 (2 marks, MSQ)

The DAG has edges $P \to Q$, $R \to Q$, $Q \to S$, $Q \to V$, $S \to U$, $V \to T$. Which are valid topological orders?
(A) PQRSTUV (B) PRQVSUT (C) PQRSVUT (D) PRQSVTU

<details>
<summary>Show solution</summary>

**Answer: B; D**

Check the constraints edge by edge.

- $Q$ must come after **both** $P$ and $R$. In (A) and (C), $Q$ is in position 2, before $R$, so both are invalid.
- (B) P R Q V S U T: $Q$ comes after P and R ✓, before S and V ✓; S before U ✓; V before T ✓. Valid.
- (D) P R Q S V T U: $Q$ comes after P and R ✓, before S and V ✓; S before U ✓; V before T ✓. Valid.

**Bonus:** how many valid orders are there in total? P and R can come in 2 orders, then Q. After Q, the chains S→U and V→T interleave in $\binom42 = 6$ ways. Total $2 \times 6 = 12$.

</details>

### GATE DA 2025 Q65 (2 marks, NAT)

$V = \{0, 1, \dots, 100\}$, with an edge $(i, j)$ whenever $0 < j - i \le 2$. Each adjacency list is in **decreasing** vertex order. DFS starts at 0. How many vertices are discovered **after** vertex 50?

<details>
<summary>Show solution</summary>

**Answer: 75**

From $i$, the out-neighbours are $i + 2$ and $i + 1$, in that order. So DFS always jumps $+2$ first:

$$0 \to 2 \to 4 \to \dots \to 100.$$

Vertex 100 has no out-edges. Backtracking to 98, its next neighbour 99 is unvisited, so 99 is discovered. All of 99's neighbours are visited. Backtracking to 96 discovers 97, and so on down to 1.

The discovery order is $0, 2, 4, \dots, 100$ (51 vertices), then $99, 97, \dots, 1$ (50 vertices).

Vertex 50 is the 26th vertex discovered. After it come the evens $52, \dots, 100$ (25 vertices) and all 50 odds: $25 + 50 = $ **75**.

</details>

### GATE DA 2025 Q58 (2 marks, MSQ)

$G$ is simple, unweighted and undirected, with vertices a b c d (top row) and e f g h (bottom row). These are given as shortest paths: $a{-}b{-}c{-}d$ (from a to d), $e{-}f{-}g{-}h$ (from e to h), $a{-}f{-}c{-}h$ (from a to h). Which are **NOT** edges of $G$?
(A) (b, d) (B) (b, g) (C) (b, h) (D) (e, g)

<details>
<summary>Show solution</summary>

**Answer: A; C; D**

Each given shortest path has length 3. Any edge that would create a shorter path between its endpoints is impossible.

- (b, d) would give $a{-}b{-}d$, length 2, shorter than 3 for a to d. **Not an edge.**
- (b, h) would give $a{-}b{-}h$, length 2, for a to h. **Not an edge.**
- (e, g) would give $e{-}g{-}h$, length 2, for e to h. **Not an edge.**
- (b, g) gives no shortcut for any of the three pairs, so it **can** be an edge.

The idea tested: **a shortest path has no shortcuts.**

</details>

### GATE DA 2026 Q40 (2 marks, MSQ)

$G$ is directed, may have cycles, and may not be strongly connected. $G^R$ reverses every edge. A BFS or DFS from $v$ visits only the vertices reachable from $v$. Which statements must always be true?

(A) If $u$ is reachable in the BFS of $G^R$ from $v$, then $u$ is reachable in the DFS of $G$ from $v$.
(B) The BFS of $G^R$ from $v$ visits exactly the same vertices as the DFS of $G$ from $v$.
(C) The BFS order in $G^R$ is the reverse of the DFS order in $G$.
(D) If $u$ is reachable in the DFS of $G$ from $v$, then $v$ is reachable in the BFS of $G^R$ from $u$.

<details>
<summary>Show solution</summary>

**Answer: D**

- **(D)** A path $v \to u$ in $G$, reversed edge by edge, is a path $u \to v$ in $G^R$. Always true.
- **(A)** and **(B)** compare "reachable *from* $v$ in $G^R$" (vertices that can reach $v$ in $G$) with "reachable *from* $v$ in $G$". These are different sets. Counterexample: $G$ has the single edge $v \to x$. Then $G^R$ from $v$ visits only $\{v\}$, while $G$ from $v$ visits $\{v, x\}$. Both fail.
- **(C)** Traversal orders aren't related this way at all.

</details>

### GATE DA 2024 Q14 (1 mark, MCQ)

DFS on an undirected, unweighted graph from $s$. $d[u]$ is the shortest-path distance from $s$ to $u$. Edge $(u, v)$ has $d[u] < d[v]$ and is explored first in the direction $u \to v$. It becomes a ___ edge.
(A) tree (B) cross (C) back (D) gray

<details>
<summary>Show solution</summary>

**Official answer: (A) tree**

The intended reasoning: in an **undirected** DFS, the only edge types are tree and back. That rules out (B), and (D) isn't an edge type at all. When an edge is explored for the first time from $u$ and $v$ hasn't been discovered yet, $v$ is white, so the edge becomes a **tree** edge.

Be careful with this one. In some graphs, $v$ can be a gray ancestor of $u$ even though $d[u] < d[v]$, which would make the edge a back edge. The paper's key still says **(A)**. In the exam, eliminate the impossible options first (cross and gray can't occur in undirected DFS), then choose between tree and back.

</details>

---

## Test yourself (B): predicted 2027-style questions

Graph for F1 and F2: undirected, with edges A–B, A–C, B–D, C–D, C–E, D–F, E–F. Every adjacency list is in alphabetical order.

**F1 (1 mark, MCQ).** What is the DFS discovery order from A?
(A) A B C D E F (B) A B D C E F (C) A B D F E C (D) A C E F D B

<details>
<summary>Show solution</summary>

**Answer: (B)**

- A's first neighbour is B, so go to B.
- B's neighbours are A (seen) and D, so go to D.
- D's neighbours are B (seen), C, F. C comes first, so go to C.
- C's neighbours are A, D (seen) and E, so go to E.
- E's neighbours are C (seen) and F, so go to F.

Order: A, B, D, C, E, F. (A) is the BFS order, which is a common distractor.

</details>

**F2 (1 mark, NAT).** In the same graph, what is the shortest-path distance (number of edges) from A to F?

<details>
<summary>Show solution</summary>

**Answer: 3**

BFS levels: A at 0. B and C at 1. D and E at 2. F at 3 (through D or E).

</details>

**F3 (2 marks, NAT).** A directed graph has weighted edges S→A (4), S→B (1), B→A (2), B→C (5), A→C (1), A→D (5), C→D (3). What is the Dijkstra distance from S to D?

<details>
<summary>Show solution</summary>

**Answer: 7**

| Vertex fixed | $d$ after relaxing its edges |
|---|---|
| S (0) | A = 4, B = 1 |
| B (1) | A = min(4, 1 + 2) = 3, C = 6 |
| A (3) | C = min(6, 3 + 1) = 4, D = 8 |
| C (4) | D = min(8, 4 + 3) = 7 |
| D (7) | — |

The path is S → B → A → C → D, with cost $1 + 2 + 1 + 3 = 7$.

</details>

**F4 (2 marks, NAT).** A DAG has edges a→b, a→c, b→d, c→d, and a fifth vertex e with no edges. How many topological orders does it have?

<details>
<summary>Show solution</summary>

**Answer: 10**

Ignoring e: a must come first and d last, with b and c in either order. That's 2 orders. Vertex e can be placed in any of 5 positions in each. Total $2 \times 5 = 10$.

</details>

**F5 (2 marks, NAT).** What is the weight of the MST of the graph with edges A–B 4, A–C 3, B–C 1, B–D 2, C–D 4, C–E 5, D–E 7, D–F 6, E–F 3?

<details>
<summary>Show solution</summary>

**Answer: 14**

Kruskal, taking edges in increasing order of weight:

- B–C (1) ✓
- B–D (2) ✓
- A–C (3) ✓
- E–F (3) ✓
- A–B (4): A and B are already connected, so skip.
- C–D (4): skip, cycle.
- C–E (5) ✓

That's 5 edges for 6 vertices, so stop. Weight $1 + 2 + 3 + 3 + 5 = 14$.

</details>

**F6 (2 marks, MSQ).** Which statements are always true?
(A) A simple undirected graph with 10 vertices and 46 edges must be connected (B) A directed graph with a topological order has no back edges in any DFS (C) BFS from $s$ finds shortest paths in a graph whose edge weights are all 5 (D) Dijkstra gives correct distances on every directed graph that has no negative cycle

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

- **(A)** A disconnected simple graph on 10 vertices has at most $\binom92 = 36$ edges (one vertex isolated, the rest complete). $46 > 36$, so the graph must be connected. True.
- **(B)** It's a DAG, so it has no cycle and therefore no back edge. True.
- **(C)** All weights are equal, so path cost $= 5 \times$ hop count. True.
- **(D)** No negative *cycle* isn't enough. Counterexample: S→A (2), S→B (4), B→A (−3), A→C (1). Dijkstra fixes A = 2, then C = 3, and only then processes B. Even though A drops to 1 at that point, C is already final at 3. The true distance to C is $4 - 3 + 1 = 2$. False. Use Bellman-Ford for negative edges.

</details>
