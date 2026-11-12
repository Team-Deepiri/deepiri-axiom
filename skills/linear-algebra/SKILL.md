---
name: linear-algebra
description: >-
  Working linear algebra toolkit — solving systems, matrix structure, determinants, vector
  spaces and the four fundamental subspaces, orthogonality and least squares, eigenvalues
  and diagonalization. Reach for it when a problem reduces to a matrix, when you need to
  know which decomposition fits, or when reading what a rank, null space, or spectrum means.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, TodoWrite
---

# Linear algebra — working toolkit

The companion to `applied-math`. That skill tells you what to look for in a system; this one tells you
how to compute it once the system turns out to be linear. Use it as a reference to dip into, not a course
to read through.

**Diagnostic first — what kind of question is this?**

| Question | Section |
|---|---|
| "Solve `Ax = b`" | Systems |
| "How many solutions, and why?" | Systems → Rank |
| "Is this transformation reversible?" | Inverses, Determinants |
| "How many independent things are really here?" | Rank, Basis and dimension |
| "What is conserved / what costs nothing?" | Four fundamental subspaces |
| "No exact solution exists — what's closest?" | Orthogonality, Least squares |
| "What are this system's natural modes / long-run behavior?" | Eigenvalues, Diagonalization |
| "This is numerically unstable" | Conditioning |

---

## 1. Systems of equations

A **linear** equation has unknowns only in numerators, only to the first power, with no products or
quotients of unknowns: `a₁x₁ + a₂x₂ + ⋯ + aₙxₙ = b`. Anything else is not this toolkit's problem until
you linearize it.

**The augmented matrix** `[A | b]` strips the equations to their coefficients. Three **elementary row
operations** — swap two rows, scale a row by a nonzero constant, add a multiple of one row to another —
change the representation without changing the solution set. That invariance is the whole method.

**Gaussian elimination** reduces to *row echelon form* (leading 1 in each nonzero row, each further right
than the one above, zero rows at the bottom), then back-substitutes. **Gauss-Jordan** continues to *reduced
row echelon form* (rref — additionally, each leading 1 is the only nonzero entry in its column), reading
the solution off directly. Gauss-Jordan does more arithmetic; Gaussian elimination plus back-substitution
is usually cheaper. rref is canonical: a matrix has exactly one.

**Reading the outcome.** Exactly three possibilities, always:

- **No solution** — a row reads `[0 0 ⋯ 0 | c]` with `c ≠ 0`, asserting `0 = c`. Inconsistent.
- **Exactly one solution** — every column has a pivot; no free variables.
- **Infinitely many** — consistent with at least one pivot-free column. Each pivot-free column is a **free
  variable**; parameterize it (`x₃ = t`) and express the pivots in terms of the free ones. **The number of
  free variables is the dimension of the solution family**, and that family's structure is often the actual
  result, not a failure to pin one down.

A **homogeneous** system (`Ax = 0`) is always consistent — `x = 0` is the trivial solution. The real
question is whether nontrivial ones exist, which they do exactly when there is a free variable. A
homogeneous system with more unknowns than equations *always* has nontrivial solutions.

## 2. Matrix arithmetic and structure

Addition and scalar multiplication are entrywise and behave as expected. **Multiplication** is not: `AB`
requires `A`'s column count to equal `B`'s row count, and **`AB ≠ BA` in general** — the single most
consequential difference from scalar arithmetic. `(AB)ᵢⱼ` is row `i` of `A` dotted with column `j` of `B`.
Think of `AB` as *composition of transformations*, applied right-to-left; the noncommutativity is then
obvious rather than surprising.

What survives from scalars: associativity `(AB)C = A(BC)`, distributivity, `A(cB) = c(AB)`.
What does not: commutativity, and cancellation — `AB = AC` does **not** imply `B = C`, and `AB = 0` does
**not** imply `A = 0` or `B = 0`.

**Transpose** `Aᵀ` flips across the diagonal. `(AB)ᵀ = BᵀAᵀ` — order reverses; this trips people constantly.
`(Aᵀ)ᵀ = A`, `(A + B)ᵀ = Aᵀ + Bᵀ`. **Trace** is the sum of diagonal entries; `tr(AB) = tr(BA)` even though
`AB ≠ BA`, and trace equals the sum of eigenvalues.

**Special forms worth recognizing on sight**, because each one buys you a shortcut:

- **Diagonal** — multiplication, powers, and inverses are entrywise. The form everything else aspires to.
- **Triangular** (upper or lower) — determinant is the product of the diagonal; solvable by direct
  substitution with no elimination needed. The eigenvalues are the diagonal entries.
- **Symmetric** (`A = Aᵀ`) — the best-behaved general class. Always diagonalizable, always with *real*
  eigenvalues and an *orthogonal* eigenbasis. If your matrix is symmetric, say so early; it unlocks the
  strongest results in the subject.
- **Orthogonal** (`AᵀA = I`, so `A⁻¹ = Aᵀ`) — preserves lengths and angles. Rotations and reflections.
  Inverting is free, and numerically these are the safest matrices to work with.
- **Identity / elementary** — an elementary matrix is `I` with one row operation applied; left-multiplying
  by it *performs* that operation. This is why elimination is factorization in disguise.

## 3. Inverses

`A⁻¹` exists iff `A` is square and **nonsingular**, and then `AA⁻¹ = A⁻¹A = I`. When it exists it is unique,
and `Ax = b` has the unique solution `x = A⁻¹b`.

`(AB)⁻¹ = B⁻¹A⁻¹` — order reverses again. `(Aᵀ)⁻¹ = (A⁻¹)ᵀ`.

**Finding it:** row-reduce `[A | I]` to `[I | A⁻¹]`. If the left block cannot reach `I` — a zero row appears —
`A` is singular and has no inverse. For `2×2` only, the closed form `1/(ad − bc) · [[d, −b], [−c, a]]` is
worth memorizing.

**Do not actually invert to solve systems.** `x = A⁻¹b` is the right way to *think* and the wrong way to
*compute* — elimination is faster and numerically far better behaved. Inverting is for theory and for the
rare case where you genuinely need the inverse itself.

**The equivalence theorem** — for square `A`, all of these are the same statement, and moving between them
is most of the practical skill in the subject:

> `A` is invertible ⟺ `Ax = 0` has only the trivial solution ⟺ rref(`A`) `= I` ⟺ `A` is a product of
> elementary matrices ⟺ `Ax = b` has exactly one solution for every `b` ⟺ `det(A) ≠ 0` ⟺ the columns are
> linearly independent ⟺ the columns span `ℝⁿ` ⟺ the columns are a basis ⟺ rank `= n` ⟺ nullity `= 0` ⟺
> `0` is not an eigenvalue.

## 4. Determinants

`det(A)` is the signed volume scaling factor of the transformation `A`. That's the meaning; the formulas
are just ways to compute it.

**Computing it.** *Cofactor expansion* along any row or column — expand along whichever has the most zeros.
`O(n!)`, so it's for small or sparse matrices only. *Row reduction* is the practical method: reduce to
triangular and multiply the diagonal, tracking that a row swap flips the sign, scaling a row by `c` scales
the determinant by `c`, and adding a multiple of one row to another **leaves it unchanged**.

**Properties.** `det(AB) = det(A)det(B)` — remarkable given `AB ≠ BA`. `det(Aᵀ) = det(A)`.
`det(A⁻¹) = 1/det(A)`. `det(cA) = cⁿdet(A)` for `n×n` — the `n`th power catches people out.
**`det(A + B) ≠ det(A) + det(B)`.** Determinant is zero iff the matrix is singular iff rows/columns are
linearly dependent — a triangular or diagonal matrix's determinant is just its diagonal product.

**What it's for and not for.** It's a superb *theoretical* device — singularity tests, the characteristic
polynomial, change-of-variables Jacobians, orientation. It is a poor *numerical* one: for large matrices
it overflows, underflows, and tells you far less about near-singularity than the condition number does.
"`det` is small" is not the same as "ill-conditioned."

## 5. Vectors, dot product, cross product

A vector is magnitude and direction; in `ℝⁿ` it's an ordered tuple. **Norm** `‖v‖ = √(v·v)`.

**Dot product** `u·v = Σuᵢvᵢ = ‖u‖‖v‖cos θ`. Scalar-valued, any dimension. Zero iff the vectors are
**orthogonal** — this is the workhorse test in the entire subject. It gives you angle, projection
(`proj_u v = (u·v / u·u)u`), and via Cauchy–Schwarz (`|u·v| ≤ ‖u‖‖v‖`) most of the useful inequalities.

**Cross product** `u × v` — `ℝ³` only. Vector-valued, orthogonal to both inputs, right-hand rule,
magnitude `‖u‖‖v‖sin θ` = the area of the parallelogram they span. Zero iff the vectors are parallel.
**Anticommutative** (`u × v = −v × u`) and **not associative**.

## 6. Vector spaces, subspaces, span, independence, basis

A **vector space** is a set with addition and scalar multiplication satisfying the ten axioms
(closure both ways, commutativity and associativity of addition, zero vector, additive inverses,
the distributive and identity properties for scalars). The point of the abstraction: `ℝⁿ`, matrices,
polynomials, and function spaces are all vector spaces, so every theorem proved once applies to all of
them. When you notice your objects can be added and scaled sensibly, you have a vector space and this
entire toolkit becomes available.

A **subspace** is a subset that is itself a vector space. Only three things to check, and in practice
only the last two: it contains the zero vector, it is closed under addition, and it is closed under
scalar multiplication. **If it doesn't contain `0`, stop — it's not a subspace**, which is the fastest
disqualifying test.

**Span** — the set of all linear combinations of a set of vectors; always a subspace, and the smallest
one containing them.

**Linear independence** — `c₁v₁ + ⋯ + cₖvₖ = 0` only when all `cᵢ = 0`. Equivalently, no vector is a
combination of the others: nothing is redundant. Test it by putting the vectors in a matrix and checking
whether the homogeneous system has only the trivial solution. Any set containing the zero vector is
dependent. In `ℝⁿ`, more than `n` vectors are always dependent.

**Basis** — independent *and* spanning. The minimal description with no redundancy. Every vector has a
**unique** representation in a given basis, which is precisely what makes coordinates meaningful.
**Dimension** is the number of basis vectors, the same for every basis of the space.

**Change of basis.** Coordinates are relative to a chosen basis, and the basis was *your* choice, not the
system's. The transition matrix `P` converting coordinates from basis `B` to basis `C` satisfies
`[v]_C = P[v]_B`, with `P⁻¹` going back. Choosing the right basis is the entire game — this is the concrete
mechanics behind the applied-math skill's "symmetry of description" and "change of coordinates that
decouples the dynamics."

## 7. The four fundamental subspaces

For an `m×n` matrix `A`, these are what the matrix *is*, structurally:

| Subspace | Definition | Lives in | Dimension | Reads as |
|---|---|---|---|---|
| **Column space** | span of columns; all achievable `Ax` | `ℝᵐ` | rank `r` | What the system can express / reach |
| **Null space** | all `x` with `Ax = 0` | `ℝⁿ` | `n − r` (nullity) | Directions that cost nothing; the redundancy in your description |
| **Row space** | span of rows = column space of `Aᵀ` | `ℝⁿ` | rank `r` | The independent constraints, after duplicates collapse |
| **Left null space** | all `w` with `wᵀA = 0` | `ℝᵐ` | `m − r` | **Conserved quantities** — `wᵀx` is unchanged by `A` |

**Rank** is the number of pivots in rref, and equals both the row-space and column-space dimension — row
rank equals column rank, which is not obvious and is one of the deepest elementary facts here.

**Rank–nullity: `rank + nullity = n`.** The accounting identity of the whole subject. Every dimension of
your input space is either expressed or annihilated, and this is exactly the statement that "how many
independent things are really here" has a definite answer.

**Practical readings.** `Ax = b` is solvable iff `b` lies in the column space. The solution set, when
nonempty, is *one particular solution plus the entire null space* — which is why the null space is the
solution family's shape. Rank deficiency means your variables aren't independent, and the nullity counts
exactly how many redundancies there are. **The left null space is the conserved-quantity generator**: this
is the computational form of the invariant hunt.

## 8. Orthogonality, Gram–Schmidt, least squares, QR

An **inner product space** generalizes the dot product; everything below works in any of them.

**Orthogonal set** — pairwise orthogonal. **Orthonormal** — additionally all unit length. Orthonormal bases
are the good ones: coordinates are just dot products (`v = Σ(v·uᵢ)uᵢ`, no system to solve), the transition
matrix is orthogonal so its inverse is its transpose, and numerical behavior is excellent.

**Gram–Schmidt** converts any basis into an orthonormal one: take each vector in turn, subtract off its
projections onto everything already processed, normalize. Conceptually clean; numerically unstable in its
classical form for near-dependent inputs — use modified Gram–Schmidt or Householder reflections when it
matters.

**Least squares.** When `Ax = b` has no solution — the usual case with real, overdetermined data — find the
`x` minimizing `‖Ax − b‖`. The answer is the **orthogonal projection of `b` onto the column space**, given
by the normal equations `AᵀAx = Aᵀb`. The residual `b − Ax̂` is orthogonal to the column space, and that
orthogonality is a precise, checkable statement of *what your model structurally cannot capture* —
inspect it rather than discarding it. Solve via QR rather than by forming `AᵀA`, which squares the
condition number and throws away accuracy for no reason.

**QR-decomposition.** `A = QR` with `Q` orthogonal and `R` upper triangular — Gram–Schmidt, packaged. The
right default for least squares and a building block for eigenvalue algorithms.

**LU-decomposition.** `A = LU`, lower times upper triangular — Gaussian elimination, packaged. Use it when
solving `Ax = b` repeatedly for many different `b` with the same `A`: factor once, then each solve is two
cheap triangular substitutions. Needs partial pivoting (`PA = LU`) for stability in general.

## 9. Linear transformations

`T: V → W` is linear iff `T(u + v) = T(u) + T(v)` and `T(cu) = cT(u)`. Every linear transformation between
finite-dimensional spaces **is** a matrix once you fix bases — the matrix and the transformation are the
same object seen two ways, and fluency means switching between the views without friction.

**Kernel** (what maps to zero) is the null space; **range** is the column space. So rank–nullity is a
statement about transformations: `dim(kernel) + dim(range) = dim(domain)`.

Recognizable geometric examples in `ℝ²`/`ℝ³` worth knowing by their matrices: rotation, reflection,
projection (idempotent: `P² = P`), scaling, shear, and contraction/dilation.

## 10. Eigenvalues, eigenvectors, diagonalization

`Av = λv` with `v ≠ 0`. The eigenvector is a direction the transformation **doesn't rotate** — it only
scales it, by `λ`. These are the system's natural axes, and finding them is what "discovering the right
coordinates" means concretely.

**Finding them.** Solve the characteristic equation `det(A − λI) = 0` for the eigenvalues, then for each
`λ` find the null space of `(A − λI)` — the eigenspace. Fine by hand up to `3×3`; beyond that use
numerical methods, because root-finding on the characteristic polynomial is badly conditioned.

**Facts worth carrying.** Sum of eigenvalues = trace; product = determinant — two free checks on any
computation. Triangular and diagonal matrices have their diagonal as eigenvalues. `A` is singular iff `0`
is an eigenvalue. Eigenvectors for *distinct* eigenvalues are automatically independent. Symmetric real
matrices always have real eigenvalues and an orthonormal eigenbasis.

**Diagonalization.** `A = PDP⁻¹` where `D` is diagonal with the eigenvalues and `P` has the eigenvectors as
columns. Possible iff there are `n` independent eigenvectors — guaranteed when all eigenvalues are distinct,
and guaranteed for symmetric matrices, but **not** in general. A matrix with a repeated eigenvalue whose
eigenspace is too small is **defective** and cannot be diagonalized; that defectiveness is a real structural
fact about the system, not a computational obstacle to route around (Jordan form is the general answer).

**Why it matters.** `Aᵏ = PDᵏP⁻¹` makes powers trivial, which means long-run behavior of any iterated
process is read straight off the eigenvalues: `|λ| > 1` grows, `|λ| < 1` decays, `|λ| = 1` persists, and the
**dominant** eigenvalue determines asymptotic behavior. Coupled dynamics decouple in the eigenbasis — each
mode evolves independently. And the **eigenvalue gap is the scale separation**: the ratio of the largest to
the smallest `|λ|` is precisely the fast/slow ratio the approximation analysis needs, so the thing you were
told to estimate rather than assume is a computation, not a guess.

## 11. Numerical cautions

- **Condition number** `κ(A) = ‖A‖‖A⁻¹‖` measures how much the output error amplifies input error. Large
  `κ` means a formally solvable system whose answer is untrustworthy. **This, not a small determinant, is
  the near-singularity diagnostic.** An ill-conditioned model is itself a finding — it usually means the
  variables are nearly redundant, which points straight back at the state-variable search.
- **Never form `AᵀA`** for least squares when QR is available: it squares the condition number.
- **Never invert to solve.** Factor and substitute.
- Prefer orthogonal transformations (QR, Householder, Givens) — they don't amplify error.
- Exact-zero tests are meaningless in floating point. "Rank" and "singular" in practice mean "below a
  tolerance," and choosing that tolerance is a modeling decision you should make consciously.

---

# Rules

- Say what the matrix *means* before computing with it — transformation, constraint set, transition rule,
  or data layout. The interpretation determines which tool applies.
- Reach for structure before brute force: symmetric, triangular, orthogonal, and sparse each have a
  shortcut, and recognizing one saves more than any optimization.
- Report rank and conditioning alongside any solve. A solution without them is unfalsifiable.
- Distinguish "no solution" from "infinitely many" explicitly, and when it's the latter, describe the
  solution *family* rather than picking an arbitrary member and calling it the answer.
- Check trace and determinant against your eigenvalues. Free verification, always worth it.
- When a matrix won't diagonalize or won't condition, treat that as information about the system, not as
  an obstacle to be worked around.
