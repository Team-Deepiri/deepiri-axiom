---
name: symbolic-regression
description: >-
  Discover candidate governing equations directly from measured data — sparse regression
  (SINDy and relatives), symbolic regression search (PySR/gplearn-style), and data-driven
  coordinates (DMD, autoencoders) — as hypothesis generators feeding the disciplined
  `applied-math` validation loop. Use when you have dense time-series or snapshot data and
  no trusted equation yet.
allowed-tools: Read, Write, Bash, Glob, Grep, WebSearch, WebFetch, TodoWrite
---

# Symbolic and sparse-regression model discovery

Companion to `applied-math`. That skill is the disciplined, largely hand-driven process for inventing
structure; this one is the computational toolkit for when you have data dense enough that a machine
search over candidate equations can propose structure faster than hand derivation — with the same
non-negotiable requirement that every proposal gets run back through `applied-math`'s validation stages
before being trusted. A computer finding a sparse fit is a hypothesis, not a result.

## Choosing a technique

| Situation | Reach for |
|---|---|
| You already trust a set of state variables and want the governing equation | **Sparse regression (SINDy family).** Build a library of candidate terms, solve for the sparsest coefficient vector reproducing observed derivatives or transitions. |
| Derivatives are noisy or only available from finite differences | **Weak/integral-form SINDy.** Regress against integrated quantities instead of pointwise derivatives — far more robust to measurement noise. |
| Dynamics genuinely span multiple time scales | **Multiscale sparse regression.** Resample and fit fast and slow components on separate, appropriately-chosen sampling intervals rather than one global fit. |
| You don't yet trust a term library or functional form at all | **Symbolic regression search** (genetic-programming or search-based, e.g. PySR-style tools). Searches over expression trees rather than coefficients of a fixed basis — slower and more prone to spurious fits, but doesn't require committing to a basis first. |
| You suspect the raw measured variables aren't the right state, but have no candidate re-description | **Data-driven coordinates** — dynamic mode decomposition for (locally) linear systems, autoencoders or diffusion maps for nonlinear ones. Produces candidate coordinates to feed back into the state-variable search, not a final answer. |
| You want to estimate a nearly-conserved quantity or fast/slow split directly from snapshots | **DMD spectrum.** Eigenvalues near the unit circle (continuous case: near zero) are your candidate slow modes; the rest are fast. Ties directly into the linear-algebraic lens in `applied-math`. |

## Procedure

1. **Do the plain-language inventory and dimensional analysis first**, even when you plan to fit. Use
   established units and known symmetries to constrain the candidate term library or search space —
   restrict to dimensionally consistent terms, or terms respecting a known relabeling/reflective symmetry,
   rather than searching an unconstrained space. This is where most of the real leverage lives: a
   constrained search converges faster and produces far fewer spurious fits than an unconstrained one.
2. **Prefer more data cleaning and more structure over more model complexity.** Denoise or use a weak
   formulation before reaching for a bigger term library — a bigger library fit to noisy derivatives
   reliably produces spurious terms that happen to cancel noise, not real physics.
3. **Fit with sparsity promoted explicitly** (thresholding, L1 penalty, or equivalent) rather than a dense
   least-squares fit. The whole value of the sparse-regression family is that a small number of real terms
   should dominate; a dense fit that "explains" the data with many small coefficients is evidence the
   library or the data quality is wrong, not evidence the system is complicated.
4. **Bootstrap or ensemble the fit** across resampled subsets of the data and keep only terms that appear
   in most of the ensemble. A term that only survives on one particular slice of the data is very likely
   fitting noise specific to that slice.
5. **Check every discovered term against the invariants and symmetries already established.** A term
   violating a confirmed conservation law or symmetry is a red flag on the fit (wrong library, wrong
   preprocessing, insufficient sparsity) far more often than it is a genuine discovery that the invariant
   doesn't hold — treat it as a bug to chase down first.
6. **Route every surviving candidate through `applied-math`'s validation stage**: held-out data, limiting
   cases, adversarial stress test, and an explicit statement of domain of validity. A discovered equation
   that has not been through this is a candidate, not a governing equation.

## Mistakes

- Treating a sparse fit's *existence* as confirmation of structure — sparsity only guarantees the fit is
  parsimonious given the library offered, not that the library contained the right terms.
- Skipping the dimensional/symmetry constraint step and searching an unconstrained library "to be safe" —
  this produces more spurious terms, not fewer, because an unconstrained search has more ways to overfit
  noise.
- Using a single fit on a single dataset as the final answer instead of an ensemble.
- Accepting learned coordinates (autoencoder latents, DMD modes) as a finished state-variable discovery
  without checking they're actually interpretable and traceable back to something measurable — an opaque
  coordinate that fits well but explains nothing is a dead end for applied work, however good the fit.
- Fitting free coefficients before checking the discovered functional form against known limiting cases —
  the same ordering mistake `applied-math` warns against for hand-derived models, and just as costly here.

## Output shape

```markdown
## Data available — density, noise level, what's directly measured vs. derived
## Candidate state variables and units (from applied-math inventory)
## Established invariants/symmetries used to constrain the search
## Technique chosen and why (sparse regression / symbolic search / data-driven coordinates)
## Library or search space, and what was excluded and why
## Fit result — sparsity level, ensemble stability, terms that survived
## Consistency check against known invariants, symmetries, and limiting cases
## Validation against held-out data
## Domain of validity and where the fit is expected to fail
```
