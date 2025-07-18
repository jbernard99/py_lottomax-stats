import sqlite3
from typing import List
import numpy as np

class LottoMaxPredictor:
    """Predict LottoMax numbers using weighted frequency analysis."""
    def __init__(self, db_path: str = "LottoMax_results.db", alpha: float = 0.01):
        self.db_path = db_path
        self.alpha = alpha  # Exponential decay factor for weighting recency
        self.n_numbers = 50  # LottoMax draws numbers from 1..50

    def _fetch_results(self) -> List[List[int]]:
        """Fetch winning combinations from the database as lists of ints."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        rows = cur.execute("SELECT winning_combo FROM results ORDER BY date").fetchall()
        conn.close()
        combos = [list(map(int, row[0].strip('[]').split(', '))) for row in rows]
        return combos

    def _compute_weights(self, n_draws: int) -> np.ndarray:
        """Return exponential decay weights from oldest to newest draws."""
        indices = np.arange(n_draws)
        return np.exp(-self.alpha * (n_draws - 1 - indices))

    def _probabilities(self, combos: List[List[int]]) -> np.ndarray:
        """Compute weighted probability for each number."""
        n_draws = len(combos)
        weights = self._compute_weights(n_draws)
        counts = np.zeros(self.n_numbers, dtype=float)
        for draw, w in zip(combos, weights):
            for num in draw:
                if 1 <= num <= self.n_numbers:
                    counts[num - 1] += w
        if counts.sum() == 0:
            raise ValueError("No data available to compute probabilities")
        return counts / counts.sum()

    def recommend_numbers(self, k: int = 7, method: str = "top") -> List[int]:
        """Return recommended numbers using the specified method."""
        combos = self._fetch_results()
        probs = self._probabilities(combos)
        if method == "random":
            choices = np.random.choice(np.arange(1, self.n_numbers + 1), size=k, replace=False, p=probs)
            return [int(x) for x in choices]
        # Default: pick top-k probabilities
        top = np.argsort(probs)[-k:][::-1] + 1
        return [int(x) for x in top]

if __name__ == "__main__":
    predictor = LottoMaxPredictor(alpha=0.02)
    print("Suggested numbers:", predictor.recommend_numbers())
