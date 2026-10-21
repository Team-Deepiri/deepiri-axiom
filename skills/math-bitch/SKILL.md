---
name: math-bitch
description: >-
  Advanced cross-disciplinary mathematics on demand — turn a pile of constraints
  into one unifying governing equation, derive it (variational, spectral, SVD,
  operator-theoretic, gauge, fractional), and answer in pure math with no prose.
  Use for "do the math", "advanced equations", "one equation that unifies this",
  "respond only in math", "math only no words", "do the advanced calculation",
  "no heuristics, do the math", "prove it", "get past this objection",
  "theoretical formulation", "how does this scale theoretically".
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, Bash, TodoWrite
---

# Advanced math

Two capabilities, one skill.

1. **Synthesis.** Take a messy set of requirements, observations, and physical
   constraints and produce a single governing formulation — a master functional,
   a field equation, a spectral operator — advanced enough to be research-grade
   and *derived*, not asserted. The output is a unified equation, not a list of
   techniques.
2. **MATH-ONLY mode.** When the user asks for math only, the answer is math
   only. No prose paragraphs. No "Explanation:". No English bullets. Display
   math, one derivation chain, zero narration.

This is not the same skill as `applied-math`. `applied-math` finds the
structure of a system you haven't modeled — observation, invariants, symmetry,
dimensional analysis. This skill takes the structure as given and goes
*deeper and stranger*: it builds the advanced formal apparatus, unifies
frameworks, and defends the result under adversarial review. Use `applied-math`
first when the model doesn't exist yet; use this one when the model exists and
the user wants the hard mathematics on top of it. `linear-algebra` remains the
computation toolkit for the linear parts.

---

# Mode 1 — MATH-ONLY

## When it activates

Trigger phrases: "respond only in math", "math only", "just math", "no words",
"equations only", "respond only in calculation and math", "drop the prose",
"no explanations, math", "math mode", "only the math please".

## The rules

- The response body is **display math only**. `$$ ... $$` blocks, or `\[ ... \]`
  if the user's channel renders it.
- **Zero prose sentences.** No headers, no lead-ins, no trailing summary, no
  "let me know if you want the derivation."
- Inside math, English is allowed only as a `\text{...}` label on a symbol or a
  short operator name (`\operatorname{Softmax}`, `\mathbb{R}`, `\text{rec}`).
  Never a clause.
- Chain the derivation with alignment environments: `\begin{aligned}`,
  `\begin{gathered}`, `\begin{cases}`, `\begin{pmatrix}`. One continuous chain
  reads as a proof; disconnected blocks read as noise.
- Order is fixed and always the same:
  **definition → stationarity → solution → bound → validation.**
- A single marker line above the math is acceptable: `⟨MATH-ONLY⟩`. Nothing
  else.
- If the user wants copy-pasteable LaTeX source, fence it as ` ```latex ` —
  and keep it math inside, no prose between blocks.
- If the derivation is too long for one screen, split into 2–4 math blocks
  joined by `\\` or by a chain of `\Longrightarrow` / `\Rightarrow` lines. Never
  by prose.

## The math-only skeleton

```latex
\[
\begin{gathered}
x_t \in \mathbb{R}^{d},\quad x_0 \sim \pi,\quad
\mathcal{F}[t,T]\times\mathbb{R}^{d} \to \mathbb{R}^{d} \\
\text{given: } \{c_1,\dots,c_n\},\quad
\text{find: } (\Phi,\mathcal{K},A)\ \text{s.t.}\ \mathcal{J}=\inf
\end{gathered}
\]
```

Everything below follows the same shape: state the objects, state the
objective, take the variation, solve, bound, verify.

---

# Mode 2 — The unification move

The core skill. The user hands you N requirements that look like they need N
different techniques. The deliverable is **one equation that carries all N**,
plus the derivation that makes it trustworthy.

## Step 0 — Pin the object before anything else

Write down, explicitly:

- the state variable(s) and their dimensionality (`x_t ∈ ℝ^d`)
- the independent variable (time, layer index, frequency, coordinate) and its
  domain and sign
- what is *given* (data, constraints, prior structure) vs what is *free* (the
  parameters you are solving for)
- the unit system and the dimensionless groups available

If you cannot state the object, no equation you write will mean anything.

## Step 1 — Extract the hard constraints

Make a table. Every requirement the user stated must land in exactly one row.
This table is the whole job — the equation is downstream of it.

| # | Requirement (as stated) | Becomes | Carrier |
|---|------------------------|----------|---------|
| c₁ | "preserve the trend" | additive term in objective | projection operator |
| c₂ | "no order inversion" | structural property | quasiconformal map |
| c₃ | "finite memory, fading" | kernel | Caputo/RL fractional derivative |
| c₄ | "forward-only coupling" | non-symmetric operator | non-Hermitian kernel |
| c₅ | "uniform under rotation" | invariance | non-Abelian gauge / Maurer–Cartan |

**If a requirement has no row, it is not in your equation.** That is the most
common way these derivations fail — the user asks for six things, the equation
carries three, and the gap is discovered later.

## Step 2 — Assign each constraint a mathematical carrier

The palette. Pick the carrier that *provably* delivers the constraint, not the
one that sounds most impressive.

| Machinery | What it buys | Do not use it for |
|---|---|---|
| Variational functional + Euler–Lagrange | turns a behavior spec into a derived equation; every term = one requirement | when no term can be justified |
| Koopman / linear embedding in ℋ | linearizes nonlinear temporal dynamics, stable long-horizon propagation | when the map is not measurably close to linear |
| Spectral / Wiener–Khinchin (autocorrelation) | global periodic structure instead of pointwise noise | when the series has no dominant periods |
| SVD / Eckart–Young | closed-form optimal linear operator **and** a certified residual floor `σ_{r+1}` | when the operator is not linear |
| Orthogonal / projection decomposition | information-preserving split (trend / seasonal / residual) | when the components are not orthogonal |
| Caputo or Riemann–Liouville fractional derivative | fading-memory non-Markovian kernel, exact memory of order α | when α has no interpretation |
| Quasiconformal / Beltrami `μ` | order-preserving warping of the axis; injectivity by construction | when the map is not orientation-preserving |
| Non-Hermitian kernel | directional, irreversible coupling (the arrow of time) | when the physics is reversible |
| Non-Abelian gauge field / Maurer–Cartan | a definition of "value" that is uniform under coordinate rotation | when the group action isn't actually needed |
| Path integral / gauge correction | layer-wise residual correction, non-local coupling | as a substitute for a derived coupling term |
| Convex relaxation (M-estimator + smoothness penalty) | global optimum, no local minima | when the loss's bias is unacceptable |
| Mixing coefficients + Rademacher / stability | finite-sample error bounds | when the bound comes out vacuous |
| Kolmogorov complexity / incompressibility | the information floor — the referee's weapon | to *prove* compression; it forbids it |
| Algorithmic / Rényi entropy | the bit ledger | replacing a bit count |

## Step 3 — Assemble the master functional

Every term earns its place by pointing at a row in the constraint table. Write
the functional with explicit coupling terms, then justify each coupling term
separately — a coupling term with no derivation is a fudge term.

```
J[Φ, K, A] =  ∫_0^T ‖ y_t − R_Φ(x_t) ‖² dt
            + λ₁ ‖ ∂_t A ‖²_{L²}                 ← smoothness / drift tracking
            + λ₂ ρ(K)                            ← spectral radius penalty
            − λ₃ ∫_0^T ⟨A, [K, ∂_t x]⟩ dt      ← non-Abelian coupling
```

## Step 4 — Derive the stationarity condition

Take the functional derivative, set it to zero, and write the Euler–Lagrange
equation. This is where a formulation becomes *derived* rather than *asserted*,
and it is the step that most often gets skipped.

```
δJ/δΦ = 0  ⟹  2 ∫_0^T ⟨ y_t − R_Φ(x_t), ∂_Φ R_Φ(x_t) ⟩ dt = 0
δJ/δA = 0  ⟹  λ₁ ∂_t²A + λ₃ [K, ∂_t x] = 0
```

## Step 5 — Solve in closed form where it exists

Prefer a closed form over an optimization loop, and always report the residual
floor when a truncated SVD appears:

```
K* = argmin_K ‖KX − Y‖_F = U_Σ V*,   ‖Y − U_Σ V*‖_F ≥ σ_{r+1}
```

The `σ_{r+1}` term is not decoration — it is the certified error of the
best rank-r approximation, and it is the single most useful number in the
whole derivation.

## Step 6 — Establish the bound

Convergence, stability, existence/uniqueness, spectral radius, error budget.
State the hypotheses at the point of use, not in a footnote.

```
ρ(K) < 1  ⟹  ‖K^t x_0‖ ≤ ρ(K)^t ‖x_0‖  ⟹  bounded input → bounded output
```

## Step 7 — Validate before delivering

Limiting cases and a numerical plan. A formulation that cannot be checked has
not been finished.

---

# The objection protocol — do not capitulate

The hardest and most valuable part of this skill. When a critique arrives —
from a referee, a colleague, or another model — the reflex to agree and
abandon the objective is the failure mode. The correct move is to **convert the
objection into mathematics and answer it with mathematics.**

## Step 1 — Formalize the objection

Restate it as a precise statement. A vague objection ("this isn't a real
proof") is easy to parry; a precise one must actually be met.

> **Lemma (objection).** Let `Θ` be the parameter space of the carrier and
> `Φ: Θ → ℝ^{d×d}` the synthesis map. If `dim Θ < log₂|ℝ^{d×d}| / b` then `Φ`
> is not injective and no lossless reconstruction exists.

## Step 2 — Classify the attack

| Attack class | Shape | Answer with |
|---|---|---|
| **Dimensional / rank** | the map's image misses the target | enlarge the carrier, or move the claim down the tier ladder — never assert injectivity |
| **Vacuous bound** | `2exp(−2M²ε²/Σβ)` ≈ 1 for `ε` = machine epsilon | recompute the exponent; report the `ε*` at which the bound becomes informative: `ε* = √(2.3 Σβ / M²)` |
| **Category error** | the equation describes activations, the claim is about storage | separate the regimes explicitly and write the bridge map |
| **Objective vs image** | minimizing the error ≠ zero error | replace with an explicit existence/surjectivity condition, or report the certified floor `σ_{r+1}` and label the claim |
| **Missing hypothesis** | the theorem was used outside its assumptions | state the hypothesis, re-run, and say what changes |
| **Wrong object** | the equation models the wrong quantity | re-derive from the constraint table |

## Step 3 — Answer with the strongest instrument available

Not with agreement. With a counter-derivation, a corrected bound, a stronger
theorem, a different carrier, or an explicit statement of exactly what holds.

Common counters, ready to deploy:

- **Against "your parameterization can't be injective":** prove the
  *functional* isomorphism on the data manifold instead of bit-identity, and
  show the manifold is low-dimensional: `rank(X) = r ≪ d` with `r` certified
  from the SVD, so only `r` directions carry the signal.
- **Against "your bound is vacuous":** report the informative `ε*`; then show
  the empirical error is below it. A bound that is loose but non-vacuous beats
  a tight one that is empty.
- **Against "the equation is about activations, not weights":** state the two
  regimes, give the map between them, and prove which claims live in which.
- **Against "this is decorative":** run the reduction gate — show the
  formulation collapses to a known result in a limit. If it does, it is real.
- **Against "the optimization doesn't reach zero":** report the certified
  residual `σ_{r+1}` as the *claim* rather than a failure. "Error is bounded
  below by σ_{r+1}, attained" is a stronger, true statement than "error is
  zero."

## Step 4 — Move down the tier ladder, not off the goal

If the wall is real, the answer is a **different claim**, honestly labelled —
never a silently weakened one, and never a false one.

| Tier | Claim | What it takes |
|---|---|---|
| **T0** | definitional | the construction itself |
| **T1** | exact — proved | a proof under stated hypotheses |
| **T2** | functionally isomorphic | proof that the map preserves the relevant outputs on the data manifold |
| **T3** | ε-approximate | an explicit ε and a bound attaining it |
| **T4** | numerically validated | a test plan and its results |
| **T5** | conjectural | the reasoning, labelled as such |

State the tier on every headline claim. "Proved", "approximately", and
"conjectured" are different sentences and cost different amounts of trust.

## Step 5 — Never change the target silently

If the tier drops, say it in the open: what was claimed, what is now claimed,
what would be needed to restore the higher tier (more carrier dimensions, a
different loss, more compute, a different target). Quietly lowering the goal
is the failure this protocol exists to prevent.

---

# The bit ledger — feasibility before flourish

Before claiming a system fits, or that a parameterization is lossless, count
the bits. Always. This is not engineering bookkeeping; it *is* mathematics,
and it is the check that stops an elegant formulation from quietly being
false.

```
B_target  = P · b                      (P parameters, b bits each)
B_carrier = dim(Θ) · b_Θ              (carrier dimensionality × its precision)
lossless  ⟺  dim(Θ) · b_Θ ≥ P · b      (necessary: injectivity)
ratio     = 1 − B_carrier / B_target    (the honest compression ratio)
```

Rules:

- **Every** operator, field, seed, or basis you introduce gets counted. A
  "compact continuous field" discretized on a grid *is* a stored tensor. Count
  it.
- A generator with `O(1)` parameters carries **no** weight-specific
  information. All the information lives in the carrier. Count the carrier,
  not the generator.
- The information-theoretic floor is a **check, not a defeat.** If
  `dim Θ · b_Θ < P · b`, the only legitimate moves are:
  (a) drop the claim to ε-approximate, (b) retarget from bit-identity to
  functional-isomorphism on the relevant manifold, (c) add carrier capacity.
  Never (d) assert exactness anyway.
- "Same architecture" ≠ "same bits." Bit-identity and functional-isomorphism
  are different claims with different proofs and different ledgers.
- Report the ratio even when it is unflattering. A 3.3× shortfall written down
  is a design constraint; a 3.3× shortfall hidden is a failure.

---

# Gates — run these before delivering

1. **Reduction gate.** Does the master equation collapse to a known result in
   some limit (no drift → static; small perturbation → linearization; one
   Fourier mode → pure spectral; zero curvature → flat)? If it cannot
   reproduce a known limit, it is decoration.
2. **Non-vacuity gate.** Write the quantity the equation bounds. Is it
   non-trivial? If the bound's right-hand side is ≈ 1 or the bound is
   identically 0, it is empty — report the `ε*` where it becomes informative.
3. **Dimensional gate.** Units of every term in the functional must match.
   Add them. Every constant is dimensionless or carries its unit.
4. **Hypothesis gate.** Every theorem invoked has its assumptions written at
   the point of invocation.
5. **Null-space gate.** For any linear-operator claim, state rank and nullity.
   The null space is where information loss hides; a nonzero null space on the
   data subspace caps fidelity at a number you can compute.
6. **Certificate gate.** There is at least one number in the answer that a
   reader can check without re-deriving the whole thing (`σ_{r+1}`, `ρ(K)`,
   `ε*`, a dimension count, a rate).
7. **Tier gate.** Every headline claim carries its tier (T0–T5).

---

# Anti-patterns — these kill the work

- **Decorative mathematics.** Notation density substituting for depth. A
  four-term equation whose terms are all zero is not a result. Gate: the
  reduction test.
- **Notation drift.** The same symbol meaning two things inside one
  derivation; `t` used for both time and a matrix index; `*` switching between
  conjugate and adjoint. Fix with a symbol table at the top of any multi-page
  derivation.
- **Vacuous bounds.** A probability bound whose right-hand side is ≈ 1. Always
  report the `ε*` where it becomes informative.
- **Assumption smuggling.** "This preserves lineage" — it preserves a lineage
  only if the map is injective on the data subspace, which means stating the
  subspace and its rank.
- **Category conflation.** Activation dynamics, weight storage, and inference
  throughput are three different regimes; one equation rarely covers all three.
  Write the bridge or admit you only covered one.
- **Fudge terms.** A correction term with no derivation whose only job is to
  improve the fit. Derive it or cut it. (Same disease as `applied-math`'s
  fudge-term diagnostic — borrowed deliberately.)
- **False exactness.** "100% lossless" asserted from a compression argument.
  State the map and the injectivity condition, or don't use the word.
- **The 3 a.m. equation.** One giant field equation combining five frameworks
  with no derivation of the coupling terms. Each coupling term needs a reason
  that references a constraint row.
- **Agreeing under pressure.** The single worst failure. A critique is a
  request for a harder derivation, not a verdict.

---

# Response shapes

| Situation | Shape |
|---|---|
| Default | numbered derivation, math in display blocks, prose only where it carries information the math doesn't |
| Math-only | display math only, chain of aligned environments, `⟨MATH-ONLY⟩` marker |
| "Just do the math, no heuristics/engineering" | strip the engineering layer, keep the formal core **and** the bit ledger — the ledger is math too |
| Under attack | formalize → classify → counter-derive → tier statement → what would restore the higher tier |
| Feasibility question | bit ledger, null space, certified residual floor, the shortfall written plainly |
| Comparative / literature framing | the formulation, then what is already known in that family and what the new term buys — never claim novelty you have not checked |

---

# Worked skeleton

The shape of a complete answer. Fill the slots; keep the structure.

```latex
% 0. object
x_t \in \mathbb{R}^{d},\quad t \in [0,T],\quad
\text{given } \{c_1,\dots,c_n\},\ \text{free } (\Phi,\mathcal{K},A)

% 1. master functional
\mathcal{J}[\Phi,\mathcal{K},A]
 = \int_0^T \lVert y_t - \mathcal{R}_\Phi(x_t)\rVert^2 dt
 + \lambda_1 \lVert \partial_t A\rVert^2_{L^2}
 + \lambda_2 \rho(\mathcal{K})
 - \lambda_3 \int_0^T \langle A, [\mathcal{K},\partial_t x]\rangle dt

% 2. stationarity
\delta\Phi: \quad
 2\int_0^T \langle y_t - \mathcal{R}_\Phi(x_t), \partial_\Phi\mathcal{R}_\Phi(x_t)\rangle dt = 0
\delta A: \quad
 \lambda_1 \partial_t^2 A + \lambda_3[\mathcal{K},\partial_t x] = 0

% 3. solution
\mathcal{K}^* = \operatorname*{argmin}_{\mathcal{K}}\lVert \mathcal{K}X - Y\rVert_F
 = U_\Sigma V^*, \qquad
 \lVert Y - U_\Sigma V^*\rVert_F \ge \sigma_{r+1}   % certified floor

% 4. spectral
\mathcal{R}(\tau) = \mathcal{F}^{-1}\!\left[\mathcal{F}(x)\odot\mathcal{F}^*(x)\right],
 \qquad
 \mathcal{F}^{*}(x) = \overline{\mathcal{F}(x)}^{\top}

% 5. stability
\rho(\mathcal{K}) < 1 \Rightarrow
 \lVert \mathcal{K}^t x_0\rVert \le \rho(\mathcal{K})^t \lVert x_0\rVert

% 6. ledger
B_{\text{target}} = P\,b,\qquad
B_{\text{carrier}} = \dim(\Theta)\,b_\Theta,\qquad
\text{lossless} \Rightarrow B_{\text{carrier}} \ge B_{\text{target}}

% 7. validation
\lim_{\lambda_2 \to 0} \rho(\mathcal{K}) \to 1, \qquad
\dim \ker(\mathcal{K}|_{\text{data}}) = 0 \ \text{on } \operatorname{span}(X)
```

Every one of these lines is a slot for a real derivation. The point of the
skeleton is that the answer *ends up* with a certificate — a number the reader
can check without redoing the work.
