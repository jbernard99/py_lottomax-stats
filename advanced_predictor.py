import sqlite3
from itertools import combinations
from typing import List
import numpy as np


class AdvancedLottoMaxPredictor:
    """Recommend LottoMax numbers using pairwise statistics."""

    def __init__(self, db_path: str = "LottoMax_results.db", alpha: float = 0.01):
        self.db_path = db_path
        self.alpha = alpha  # Exponential decay factor
        self.n_numbers = 50  # LottoMax draws numbers from 1..50

    def _fetch_results(self) -> List[List[int]]:
        """Fetch historical winning combinations."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        rows = cur.execute(
            "SELECT winning_combo FROM results ORDER BY date"
        ).fetchall()
        conn.close()
        return [list(map(int, row[0].strip("[]").split(", "))) for row in rows]

    def _compute_weights(self, n_draws: int) -> np.ndarray:
        """Return exponential decay weights from oldest to newest draws."""
        indices = np.arange(n_draws)
        return np.exp(-self.alpha * (n_draws - 1 - indices))

    def _number_probabilities(self, combos: List[List[int]], smoothing: float = 1e-6) -> np.ndarray:
        """Return weighted probability for each number with smoothing."""
        n_draws = len(combos)
        weights = self._compute_weights(n_draws)
        counts = np.zeros(self.n_numbers, dtype=float)
        for draw, w in zip(combos, weights):
            for num in draw:
                if 1 <= num <= self.n_numbers:
                    counts[num - 1] += w
        counts += smoothing  # ensure unseen numbers still get some mass
        return counts / counts.sum()

    def _pair_matrix(self, combos: List[List[int]]) -> np.ndarray:
        """Return symmetric matrix of weighted pair frequencies."""
        n_draws = len(combos)
        weights = self._compute_weights(n_draws)
        pair_counts = np.zeros((self.n_numbers, self.n_numbers), dtype=float)
        for draw, w in zip(combos, weights):
            for a, b in combinations(draw, 2):
                if 1 <= a <= self.n_numbers and 1 <= b <= self.n_numbers:
                    pair_counts[a - 1, b - 1] += w
                    pair_counts[b - 1, a - 1] += w
        if pair_counts.sum() == 0:
            return pair_counts
        return pair_counts / pair_counts.sum()

    def _triple_matrix(self, combos: List[List[int]], smoothing: float = 1e-6) -> np.ndarray:
        """Return matrix of weighted triple frequencies.

        The matrix is indexed by sorted triples (i < j < k) and normalised to
        probabilities. A small ``smoothing`` term is added so unseen triples have
        non-zero probability.
        """
        n_draws = len(combos)
        weights = self._compute_weights(n_draws)
        triple_counts = np.zeros(
            (self.n_numbers, self.n_numbers, self.n_numbers), dtype=float
        )
        for draw, w in zip(combos, weights):
            for a, b, c in combinations(draw, 3):
                if (
                    1 <= a <= self.n_numbers
                    and 1 <= b <= self.n_numbers
                    and 1 <= c <= self.n_numbers
                ):
                    i, j, k = sorted((a, b, c))
                    triple_counts[i - 1, j - 1, k - 1] += w
        triple_counts += smoothing
        if triple_counts.sum() == 0:
            return triple_counts
        return triple_counts / triple_counts.sum()

    def _score_candidates(
        self,
        remaining: np.ndarray,
        selected: List[int],
        num_probs: np.ndarray,
        pair_probs: np.ndarray,
        triple_probs: np.ndarray,
    ) -> np.ndarray:
        """Return probability scores for remaining numbers."""
        scores = num_probs[remaining - 1].copy()
        for s in selected:
            scores += pair_probs[remaining - 1, s - 1]
        if len(selected) >= 2:
            for a, b in combinations(selected, 2):
                for idx, r in enumerate(remaining):
                    i, j, k = sorted((int(r), a, b))
                    scores[idx] += triple_probs[i - 1, j - 1, k - 1]
        # Normalise to probabilities
        if scores.sum() == 0:
            return np.ones_like(scores) / len(scores)
        return scores / scores.sum()

    def recommend_combinations(self, k: int = 7, n_sets: int = 3) -> List[List[int]]:
        """Return ``n_sets`` recommended combinations of ``k`` numbers."""
        combos = self._fetch_results()
        if not combos:
            raise ValueError("No historical data available")
        num_probs = self._number_probabilities(combos)
        pair_probs = self._pair_matrix(combos)
        triple_probs = self._triple_matrix(combos)
        results = []
        rng = np.random.default_rng()
        for _ in range(n_sets):
            selected: List[int] = []
            remaining = np.arange(1, self.n_numbers + 1)
            for _ in range(k):
                prob = self._score_candidates(
                    remaining, selected, num_probs, pair_probs, triple_probs
                )
                choice = rng.choice(remaining, p=prob)
                selected.append(int(choice))
                remaining = remaining[remaining != choice]
            results.append(sorted(selected))
        return results


if __name__ == "__main__":
    predictor = AdvancedLottoMaxPredictor(alpha=0.02)
    combos = predictor.recommend_combinations()
    for i, combo in enumerate(combos, start=1):
        print(f"Recommendation {i}: {combo}")
