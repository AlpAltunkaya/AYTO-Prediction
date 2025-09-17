# Trigger warning: Sexism
# To make the code correctly identify possible couples, man's name
# needs to be written first, followed by the woman's name.

from __future__ import annotations

import math
import time
from typing import Dict, List, Optional, Sequence, Tuple

# ===== AYTO VIP 2025 (current through MN3) =====
# Cast (normalized spellings). 11 men, 11 women incl. 'SIT' as dummy.
MEN: Sequence[str] = [
    "Calvin O.", "Calvin S.", "Kevin", "Leandro", "Lennert",
    "Nico", "Olli", "Rob", "Sidar", "Xander", "Jonny",
]
WOMEN: Sequence[str] = [
    "Antonia", "Ariel", "Beverly", "Elli", "Hati",
    "Henna", "Joanna", "Nelly", "Sandra", "Viki", "SIT",  # 'SIT' is the sitter slot
]
MEN_IDX: Dict[str, int] = {name: idx for idx, name in enumerate(MEN)}
WOMEN_IDX: Dict[str, int] = {name: idx for idx, name in enumerate(WOMEN)}

# Weekly seatings (Matching Nights) and beam counts.
# IMPORTANT: We exclude the ('<man>','SIT') pair from each night list,
# because beams count ONLY real couples, not the sitter.
MATCHING_NIGHTS: Sequence[Tuple[Sequence[Tuple[str, str]], int]] = [
    # MN1 — beams = 2
    ([
        ("Leandro", "Viki"),
        ("Calvin O.", "Hati"),
        ("Jonny", "Henna"),
        ("Sidar", "Nelly"),
        ("Kevin", "Sandra"),
        ("Rob", "Joanna"),
        ("Nico", "Ariel"),
        ("Lennert", "Antonia"),
        ("Xander", "Elli"),
        ("Calvin S.", "Beverly"),
        ("Olli", "SIT"),
    ], 2),
    # MN2 — beams = 2
    ([
        ("Calvin S.", "Joanna"),
        ("Rob", "Nelly"),
        ("Kevin", "Sandra"),
        ("Nico", "Ariel"),
        ("Sidar", "Beverly"),
        ("Olli", "Henna"),
        ("Calvin O.", "Hati"),
        ("Leandro", "Viki"),
        ("Jonny", "Antonia"),
        ("Xander", "Elli"),
        ("Lennert", "SIT"),
    ], 2),
    # MN3 — beams = 2 (Xander & Elli confirmed PM, sat out together)
    ([
        ("Calvin S.", "Joanna"),
        ("Olli", "Antonia"),
        ("Nico", "Beverly"),
        ("Calvin O.", "Ariel"),
        ("Rob", "Hati"),
        ("Leandro", "Henna"),
        ("Kevin", "Sandra"),
        ("Jonny", "Viki"),
        ("Lennert", "Nelly"),
        ("Sidar", "SIT"),
    ], 2),
]

# Truth Booth results. Store both PM and NM so the solver can fix/disallow pairs.
TRUTH_BOOTH_RESULTS: Sequence[Tuple[str, str, str]] = [
    ("Jonny", "Beverly", "NM"),
    ("Leandro", "Sandra", "NM"),
    ("Calvin S.", "Nelly", "NM"),
    ("Xander", "Elli", "PM"),
]

# ===== Helper utilities =====
def validate_inputs(
    nights: Sequence[Tuple[Sequence[Tuple[str, str]], int]],
    tbs: Sequence[Tuple[str, str, str]],
) -> None:
    men_set = set(MEN)
    women_set = set(WOMEN)
    for night_idx, (seats, beams) in enumerate(nights, start=1):
        seen_men = set()
        seen_women = set()
        sitter_count = 0
        if beams < 0 or beams > len(MEN):
            raise ValueError(f"Matching Night {night_idx}: invalid beam count {beams}")
        for man, woman in seats:
            if man == "SIT":
                raise ValueError(f"Matching Night {night_idx}: 'SIT' cannot occupy a man slot")
            if man not in men_set:
                raise ValueError(f"Matching Night {night_idx}: unknown man '{man}'")
            if woman not in women_set:
                raise ValueError(f"Matching Night {night_idx}: unknown woman '{woman}'")
            if man in seen_men:
                raise ValueError(f"Matching Night {night_idx}: duplicate man '{man}'")
            seen_men.add(man)
            if woman == "SIT":
                sitter_count += 1
            else:
                if woman in seen_women:
                    raise ValueError(f"Matching Night {night_idx}: duplicate woman '{woman}'")
                seen_women.add(woman)
        if sitter_count not in (0, 1):
            raise ValueError(f"Matching Night {night_idx}: expected 0 or 1 sitter, saw {sitter_count}")
    for man, woman, result in tbs:
        if man not in men_set or woman not in women_set:
            raise ValueError(f"Truth Booth entry references unknown pair {man}×{woman}")
        if result not in {"PM", "NM"}:
            raise ValueError(f"Truth Booth result for {man}×{woman} must be 'PM' or 'NM', got {result!r}")


def tb_contradiction_reason(tbs: Sequence[Tuple[str, str, str]]) -> Optional[str]:
    pm_pairs = set()
    nm_pairs = set()
    pm_by_man: Dict[str, str] = {}
    pm_by_woman: Dict[str, str] = {}
    for man, woman, result in tbs:
        key = (man, woman)
        if result == "PM":
            if key in nm_pairs:
                return f"Contradiction: {man}×{woman} flagged both PM and NM"
            other_woman = pm_by_man.get(man)
            if other_woman and other_woman != woman:
                return f"Contradiction: {man} confirmed PM with both {other_woman} and {woman}"
            other_man = pm_by_woman.get(woman)
            if other_man and other_man != man:
                return f"Contradiction: {woman} confirmed PM with both {other_man} and {man}"
            pm_pairs.add(key)
            pm_by_man[man] = woman
            pm_by_woman[woman] = man
        else:
            if key in pm_pairs:
                return f"Contradiction: {man}×{woman} flagged both PM and NM"
            nm_pairs.add(key)
    return None


def build_night_maps(nights: Sequence[Tuple[Sequence[Tuple[str, str]], int]]) -> List[List[int]]:
    night_maps: List[List[int]] = []
    n = len(MEN)
    for seats, _ in nights:
        arr = [-1] * n
        for man, woman in seats:
            if woman == "SIT":
                continue
            arr[MEN_IDX[man]] = WOMEN_IDX[woman]
        night_maps.append(arr)
    return night_maps


def solve_exact(
    nights: Sequence[Tuple[Sequence[Tuple[str, str]], int]],
    tbs: Sequence[Tuple[str, str, str]],
    progress: Optional[callable] = None,
):
    validate_inputs(nights, tbs)
    reason = tb_contradiction_reason(tbs)
    if reason:
        return {"solutions": [], "marginals": [], "nodes": 0, "elapsed": 0.0, "reason": reason}

    n = len(MEN)
    allowed = [[True] * n for _ in range(n)]
    fixed: Dict[int, int] = {}

    for man, woman, result in tbs:
        i = MEN_IDX[man]
        j = WOMEN_IDX[woman]
        if result == "NM":
            allowed[i][j] = False
    for man, woman, result in tbs:
        if result != "PM":
            continue
        i = MEN_IDX[man]
        j = WOMEN_IDX[woman]
        fixed[i] = j
        for c in range(n):
            allowed[i][c] = False
            allowed[c][j] = False
        allowed[i][j] = True

    night_maps = build_night_maps(nights)
    assign = [-1] * n
    used_w = [False] * n
    for man_idx, woman_idx in fixed.items():
        assign[man_idx] = woman_idx
        used_w[woman_idx] = True

    men_order = sorted(
        range(n),
        key=lambda idx: (0 if idx in fixed else 1, sum(1 for ok in allowed[idx] if ok)),
    )

    solutions: List[Tuple[int, ...]] = []
    nodes = 0
    start_time = time.perf_counter()

    def beams_ok_prefix(prefix_len: int) -> bool:
        for arr, (_, need) in zip(night_maps, nights):
            hits = 0
            for pos in range(prefix_len):
                man = men_order[pos]
                woman = assign[man]
                if woman != -1 and arr[man] == woman:
                    hits += 1
            if hits > need:
                return False
            potential = 0
            for pos in range(prefix_len, n):
                man = men_order[pos]
                target = arr[man]
                if target == -1:
                    continue
                if used_w[target]:
                    continue
                if not allowed[man][target]:
                    continue
                potential += 1
            if hits + potential < need:
                return False
        return True

    def backtrack(pos: int) -> None:
        nonlocal nodes
        nodes += 1
        if progress and nodes % 200 == 0:
            progress(nodes, len(solutions), time.perf_counter() - start_time)
        if pos == n:
            for arr, (_, need) in zip(night_maps, nights):
                hits = sum(1 for man_idx in range(n) if arr[man_idx] != -1 and assign[man_idx] == arr[man_idx])
                if hits != need:
                    return
            solutions.append(tuple(assign))
            return

        man = men_order[pos]
        if assign[man] != -1:
            if beams_ok_prefix(pos + 1):
                backtrack(pos + 1)
            return

        for woman in range(n):
            if not allowed[man][woman] or used_w[woman]:
                continue
            assign[man] = woman
            used_w[woman] = True
            if beams_ok_prefix(pos + 1):
                backtrack(pos + 1)
            used_w[woman] = False
            assign[man] = -1

    first_free = 0
    while first_free < n and assign[men_order[first_free]] != -1:
        first_free += 1
    if beams_ok_prefix(first_free):
        backtrack(first_free)

    elapsed = time.perf_counter() - start_time

    marginals = compute_marginals(solutions, n)
    return {"solutions": solutions, "marginals": marginals, "nodes": nodes, "elapsed": elapsed, "reason": None}


def compute_marginals(solutions: Sequence[Tuple[int, ...]], n: int) -> List[List[float]]:
    marg = [[0.0] * n for _ in range(n)]
    if not solutions:
        return marg
    total = float(len(solutions))
    for sol in solutions:
        for man_idx, woman_idx in enumerate(sol):
            marg[man_idx][woman_idx] += 1 / total
    return marg


def rank_solutions_by_marginals(
    solutions: Sequence[Tuple[int, ...]],
    marginals: Sequence[Sequence[float]],
) -> List[int]:
    eps = 1e-12
    scored = []
    for idx, sol in enumerate(solutions):
        score = 0.0
        for man_idx, woman_idx in enumerate(sol):
            if WOMEN[woman_idx] == "SIT":
                continue
            p = max(marginals[man_idx][woman_idx], eps)
            score += math.log(p)
        scored.append((score, idx))
    scored.sort(reverse=True)
    return [idx for _, idx in scored]


def extract_pairs(sol: Sequence[int]) -> Dict[str, str]:
    return {MEN[i]: WOMEN[sol[i]] for i in range(len(MEN))}


def format_full(mapping: Dict[str, str]) -> str:
    sitter = next((man for man, woman in mapping.items() if woman == "SIT"), None)
    sitter_text = f"Sitter: {sitter}" if sitter else "Sitter: (none)"
    pairs = ", ".join(f"{man}–{woman}" for man, woman in mapping.items() if woman != "SIT")
    return f"{sitter_text} | {pairs}"


def top_candidates_per_man(marginals: Sequence[Sequence[float]], limit: int = 3):
    for man_idx, man in enumerate(MEN):
        options = [
            (WOMEN[woman_idx], marginals[man_idx][woman_idx])
            for woman_idx in range(len(WOMEN))
            if WOMEN[woman_idx] != "SIT"
        ]
        options.sort(key=lambda item: item[1], reverse=True)
        yield man, options[:limit]


def truth_booth_voi(solutions: Sequence[Tuple[int, ...]]) -> List[Dict[str, object]]:
    if not solutions:
        return []
    n = len(MEN)
    total = len(solutions)
    counts = [[0] * n for _ in range(n)]
    for sol in solutions:
        for man_idx, woman_idx in enumerate(sol):
            counts[man_idx][woman_idx] += 1
    h_before = math.log2(total)
    rows = []
    for man_idx, man in enumerate(MEN):
        for woman_idx, woman in enumerate(WOMEN):
            if woman == "SIT":
                continue
            yes = counts[man_idx][woman_idx]
            if yes == 0 or yes == total:
                continue
            p_yes = yes / total
            info = h_before - (p_yes * math.log2(yes) + (1 - p_yes) * math.log2(total - yes))
            rows.append(
                {
                    "man": man,
                    "woman": woman,
                    "p_yes": p_yes,
                    "info": info,
                    "yes": yes,
                    "no": total - yes,
                    "total": total,
                }
            )
    rows.sort(key=lambda row: (-row["info"], -row["yes"], row["man"], row["woman"]))
    return rows


def main() -> None:
    result = solve_exact(MATCHING_NIGHTS, TRUTH_BOOTH_RESULTS)
    reason = result.get("reason")
    if reason:
        print(f"❌ {reason}")
        return

    solutions: List[Tuple[int, ...]] = result["solutions"]
    print(f"Explored {result['nodes']:,} search nodes in {result['elapsed']:.3f}s.")
    print(f"Feasible matchings: {len(solutions):,}")

    if not solutions:
        return

    sitter_idx = WOMEN_IDX["SIT"]
    if not all(sol.count(sitter_idx) == 1 for sol in solutions):
        raise AssertionError("Every solution must contain exactly one sitter assignment")

    marginals = result["marginals"]
    order = rank_solutions_by_marginals(solutions, marginals)
    top_k = min(10, len(order))
    print(f"\nTop {top_k} matchings by posterior score:")
    for rank, idx in enumerate(order[:top_k], start=1):
        mapping = extract_pairs(solutions[idx])
        print(f"  #{rank}: {format_full(mapping)}")

    print("\nTop candidates per man:")
    for man, options in top_candidates_per_man(marginals):
        formatted = ", ".join(f"{woman} ({prob:.3f})" for woman, prob in options if prob > 0)
        print(f"  {man}: {formatted}")

    print("\nTruth Booth information gain (top 10):")
    voi = truth_booth_voi(solutions)[:10]
    if not voi:
        print("  No informative Truth-Booth candidates remain (all pairs at 0% or 100%).")
    else:
        for entry in voi:
            print(
                f"  {entry['man']} × {entry['woman']}: P(yes)={entry['p_yes']:.3f}, "
                f"info={entry['info']:.3f} bits (yes={entry['yes']}, no={entry['no']}, total={entry['total']})"
            )


if __name__ == "__main__":
    main()
