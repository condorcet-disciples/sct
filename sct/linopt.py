"""
Linear Optimisation for Voting System Paradoxes
================================================

Formulates a Mixed Integer Linear Program (MILP) to reverse-engineer voter
preferences that produce different winners under Plurality, Borda Count,
and Majority Judgment voting systems.

Core insight
------------
Voter ratings on a 0–4 scale simultaneously determine:
  - Ordinal rankings  →  used by Plurality (1st-place only) and Borda (full rank)
  - Cardinal scores   →  used by Majority Judgment (median rating)

By optimising over these ratings we can find populations where all three
systems disagree on the winner — a concrete demonstration of social choice
paradoxes.
"""

import math
import numpy as np

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, PULP_CBC_CMD, value

from sct.elections import Candidate, Agent, Population, PluralityVoting, BordaVoting, MajorityJudgment

# ────────────────────────────────────────────────────────────────────
#  Public API
# ────────────────────────────────────────────────────────────────────

def find_paradox_population(
    num_candidates: int = 4,
    max_score: int = 4,
    plurality_winner: int = 1,
    borda_winner: int = 2,
    mj_winner: int = 3,
    min_agents: int = 6,
    max_agents: int = 20,
    verbose: bool = True,
) -> dict | None:
    """
    Find the smallest population where Plurality, Borda, and Majority
    Judgment each elect a different winner.

    Iterates over increasing population sizes, solving a MILP at each.

    Parameters
    ----------
    num_candidates : int
        Number of candidates (default 4).
    max_score : int
        Maximum rating on the scale (0 to max_score, default 4).
    plurality_winner, borda_winner, mj_winner : int
        0-based candidate indices for each system's designated winner.
    min_agents, max_agents : int
        Range of population sizes to search.
    verbose : bool
        Print solver progress.

    Returns
    -------
    dict or None
        Keys: num_agents, scores (ndarray), medians, plurality_winner,
        borda_winner, mj_winner.  None if no feasible profile exists.
    """
    # Sanity checks
    winners = {plurality_winner, borda_winner, mj_winner}
    if len(winners) < 3:
        raise ValueError("All three winners must be distinct candidates.")
    if max(winners) >= num_candidates:
        raise ValueError("Winner indices must be < num_candidates.")

    for n in range(min_agents, max_agents + 1):
        if verbose:
            print(f"  N = {n:2d} agents … ", end="", flush=True)
        result = _solve_milp(
            n, num_candidates, max_score,
            plurality_winner, borda_winner, mj_winner,
        )
        if result is not None:
            if verbose:
                print("feasible ✓")
            return result
        if verbose:
            print("infeasible")

    if verbose:
        print(f"No solution found with ≤ {max_agents} agents.")
    return None


# ────────────────────────────────────────────────────────────────────
#  Core MILP solver
# ────────────────────────────────────────────────────────────────────

def _solve_milp(
    N: int,    # number of agents
    C: int,    # number of candidates
    S: int,    # max score  (ratings ∈ {0, …, S})
    pw: int,   # plurality  winner index
    bw: int,   # borda      winner index
    mw: int,   # majority-j winner index
) -> dict | None:
    """
    Solve the MILP for a fixed population size N.

    Variables
    ---------
    s[i][j]        ∈ {0,…,S}   score agent i gives candidate j
    q[i][j][j']    ∈ {0,1}     1 iff s[i][j] > s[i][j']
    first[i][j]    ∈ {0,1}     1 iff j is agent i's top choice
    z[i][j][v]     ∈ {0,1}     1 iff s[i][j] ≥ v
    mu[j][v]       ∈ {0,1}     1 iff median of candidate j is exactly v
    med[j]         ∈ {0,…,S}   MJ median score of candidate j
    """
    BIG_M = S + 1                   # big-M for score linking
    maj   = math.ceil(N * 0.5)      # majority threshold

    prob = LpProblem("VotingParadox", LpMinimize)
    prob += 0                        # feasibility only, no objective

    # ── Decision variables ──────────────────────────────────────

    s = [
        [LpVariable(f"s_{i}_{j}", 0, S, cat="Integer") for j in range(C)]
        for i in range(N)
    ]

    q = [
        [[LpVariable(f"q_{i}_{j}_{jp}", cat="Binary") for jp in range(C)]
         for j in range(C)]
        for i in range(N)
    ]

    first = [
        [LpVariable(f"f_{i}_{j}", cat="Binary") for j in range(C)]
        for i in range(N)
    ]

    z = [
        [[LpVariable(f"z_{i}_{j}_{v}", cat="Binary") for v in range(S + 1)]
         for j in range(C)]
        for i in range(N)
    ]

    med = [LpVariable(f"med_{j}", 0, S, cat="Integer") for j in range(C)]

    mu = [
        [LpVariable(f"mu_{j}_{v}", cat="Binary") for v in range(S + 1)]
        for j in range(C)
    ]

    # ── 1  Pairwise preference ↔ scores (strict ordering) ──────

    for i in range(N):
        for j in range(C):
            for jp in range(j + 1, C):
                # antisymmetry: exactly one direction holds
                prob += q[i][j][jp] + q[i][jp][j] == 1
                # linking:  q=1 ⟹ s[j] ≥ s[j']+1  and vice-versa
                prob += s[i][j] - s[i][jp] >= 1 - BIG_M * (1 - q[i][j][jp])
                prob += s[i][jp] - s[i][j] >= 1 - BIG_M * q[i][j][jp]

    # ── 2  First-place indicators ───────────────────────────────

    for i in range(N):
        prob += lpSum(first[i]) == 1              # one top choice per agent
        for j in range(C):
            for jp in range(C):
                if j != jp:
                    prob += first[i][j] <= q[i][j][jp]   # top ⟹ beats all

    # ── 3  Threshold indicators for MJ ──────────────────────────

    for i in range(N):
        for j in range(C):
            prob += z[i][j][0] == 1               # s ≥ 0 always holds
            for v in range(1, S + 1):
                # z=1 ⟺ s ≥ v  (forward + backward via big-M)
                prob += s[i][j] >= v - BIG_M * (1 - z[i][j][v])
                prob += s[i][j] <= (v - 1) + (S - v + 1) * z[i][j][v]
                # monotonicity: if s ≥ v then also s ≥ v-1
                prob += z[i][j][v] <= z[i][j][v - 1]

    # ── 4  Median computation ───────────────────────────────────

    for j in range(C):
        prob += lpSum(mu[j]) == 1                 # one median level
        prob += med[j] == lpSum(v * mu[j][v] for v in range(S + 1))

        for v in range(S + 1):
            # mu[j][v]=1 ⟹ at least 'maj' agents scored ≥ v
            prob += (
                lpSum(z[i][j][v] for i in range(N))
                >= maj - N * (1 - mu[j][v])
            )
            # mu[j][v]=1 ⟹ fewer than 'maj' agents scored ≥ v+1
            if v < S:
                prob += (
                    lpSum(z[i][j][v + 1] for i in range(N))
                    <= maj - 1 + N * (1 - mu[j][v])
                )

    # ── 5  Plurality winner ─────────────────────────────────────

    plur = [lpSum(first[i][j] for i in range(N)) for j in range(C)]
    for j in range(C):
        if j != pw:
            prob += plur[pw] >= plur[j] + 1       # strict plurality win

    # ── 6  Borda winner ─────────────────────────────────────────
    #    Borda score of j = Σ_i (# candidates j beats)
    #    which equals the standard Borda count with weights [C-1, …, 0]

    borda = [
        lpSum(q[i][j][jp] for i in range(N) for jp in range(C) if jp != j)
        for j in range(C)
    ]
    for j in range(C):
        if j != bw:
            prob += borda[bw] >= borda[j] + 1     # strict Borda win

    # ── 7  Majority Judgment winner ─────────────────────────────

    for j in range(C):
        if j != mw:
            prob += med[mw] >= med[j] + 1         # strict MJ win

    # ── Solve ───────────────────────────────────────────────────

    prob.solve(PULP_CBC_CMD(msg=0))

    if prob.status != 1:
        return None

    scores = np.array(
        [[int(round(value(s[i][j]))) for j in range(C)] for i in range(N)]
    )
    medians = [int(round(value(med[j]))) for j in range(C)]

    return {
        "num_agents": N,
        "scores": scores,
        "medians": medians,
        "plurality_winner": pw,
        "borda_winner": bw,
        "mj_winner": mw,
    }


# ────────────────────────────────────────────────────────────────────
#  Verification helpers
# ────────────────────────────────────────────────────────────────────

def build_population(
    scores: np.ndarray,
    candidate_names: list[str] | None = None,
):
    """
    Convert a score matrix into sct election objects.

    Parameters
    ----------
    scores : ndarray of shape (N, M)
    candidate_names : list[str], optional

    Returns
    -------
    (list[Candidate], list[Agent], Population)
    """
    N, M = scores.shape
    if candidate_names is None:
        candidate_names = [f"candidate_{j+1}" for j in range(M)]

    candidates = [Candidate(name) for name in candidate_names]
    agents = [
        Agent({candidates[j]: int(scores[i, j]) for j in range(M)})
        for i in range(N)
    ]
    return candidates, agents, Population(candidates, agents)


def verify_solution(
    scores: np.ndarray,
    candidate_names: list[str] | None = None,
) -> dict:
    """
    Run the actual election code on a score matrix.

    Returns dict with keys 'plurality', 'borda', 'majority_judgment',
    each containing 'winner' (str) and 'scores' (dict).
    """
    candidates, agents, pop = build_population(scores, candidate_names)

    systems = {
        "plurality":        PluralityVoting(pop),
        "borda":            BordaVoting(pop),
        "majority_judgment": MajorityJudgment(pop),
    }

    def fmt(d):
        return {c.name: float(v) for c, v in d.items()}

    return {
        name: {
            "winner": sys.get_winner(),
            "scores": fmt(sys.run_election()),
        }
        for name, sys in systems.items()
    }


def print_solution(result: dict, candidate_names: list[str] | None = None):
    """Pretty-print a MILP solution and verify against the election code."""
    scores = result["scores"]
    N, M = scores.shape
    if candidate_names is None:
        candidate_names = [f"candidate_{j+1}" for j in range(M)]

    print(f"\n{'=' * 62}")
    print(f"  VOTING PARADOX — {N} agents, {M} candidates")
    print(f"{'=' * 62}")

    # Score table
    col_w = max(len(n) for n in candidate_names) + 2
    hdr = "  Agent │ " + " │ ".join(f"{n:>{col_w}}" for n in candidate_names)
    print(f"\n{hdr}")
    print("  " + "─" * (len(hdr) - 2))
    for i in range(N):
        row = f"  {i+1:5d} │ " + " │ ".join(
            f"{scores[i, j]:>{col_w}d}" for j in range(M)
        )
        print(row)

    # Designated winners
    print(f"\n  Designated winners (from optimiser):")
    print(f"    Plurality:          {candidate_names[result['plurality_winner']]}")
    print(f"    Borda:              {candidate_names[result['borda_winner']]}")
    print(f"    Majority Judgment:  {candidate_names[result['mj_winner']]}")

    # Verification
    v = verify_solution(scores, candidate_names)
    print(f"\n  Verified winners (from election code):")
    for sys_name, data in v.items():
        print(f"    {sys_name:22s}  winner = {data['winner']:20s}  {data['scores']}")
    print()


# ────────────────────────────────────────────────────────────────────
#  Entry point
# ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    names = ["Business-as-usual", "Slow cars", "Few cars", "No cars"]

    print("Searching for a voting paradox …\n")
    result = find_paradox_population(
        num_candidates=4,
        plurality_winner=0,   # Business-as-usual wins Plurality
        borda_winner=1,       # Slow cars          wins Borda
        mj_winner=2,          # Few cars            wins Majority Judgment
        min_agents=5,
        max_agents=15,
        verbose=True,
    )

    if result is not None:
        print_solution(result, names)
    else:
        print("No paradox population found in the given range.")
