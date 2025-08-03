import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from advanced_predictor import AdvancedLottoMaxPredictor


def test_triple_weight_influences_scores():
    predictor = AdvancedLottoMaxPredictor()
    remaining = np.array([3, 4, 5])
    selected = [1, 2]
    num_probs = np.zeros(predictor.n_numbers)
    pair_probs = np.zeros((predictor.n_numbers, predictor.n_numbers))
    triple_probs = np.zeros((predictor.n_numbers, predictor.n_numbers, predictor.n_numbers))
    triple_probs[0, 1, 2] = 1.0  # triple (1,2,3)
    scores = predictor._score_candidates(remaining, selected, num_probs, pair_probs, triple_probs)
    assert np.isclose(scores[0], 1.0)
    assert np.allclose(scores[1:], 0.0)


def test_smoothing_gives_non_zero_probabilities():
    predictor = AdvancedLottoMaxPredictor()
    combos = [[1, 2, 3, 4, 5, 6, 7]]
    num_probs = predictor._number_probabilities(combos)
    assert num_probs[7] > 0  # number 8 has non-zero probability
    triple_probs = predictor._triple_matrix(combos)
    assert triple_probs[7, 8, 9] > 0  # triple (8,9,10) unseen but non-zero
