"""Additional reproducible CPU checks added by this verification fork."""
import math

import pytest

from micrograd.engine import Value
from micrograd.nn import MLP
from local_demo import run_demo


@pytest.mark.parametrize("a,b", [(0.7, 1.2), (-0.8, 0.4), (2.0, -0.3)])
def test_gradient_matches_finite_difference(a, b):
    def expression(x, y):
        return (x * y + x ** 2) / (y ** 2 + 1)
    x, y = Value(a), Value(b)
    expression(x, y).backward()
    eps = 1e-6
    expected_a = (expression(a + eps, b) - expression(a - eps, b)) / (2 * eps)
    expected_b = (expression(a, b + eps) - expression(a, b - eps)) / (2 * eps)
    assert math.isclose(x.grad, expected_a, rel_tol=1e-5, abs_tol=1e-6)
    assert math.isclose(y.grad, expected_b, rel_tol=1e-5, abs_tol=1e-6)


def test_zero_grad_clears_all_parameters():
    model = MLP(2, [4, 1])
    model([1.0, -1.0]).backward()
    assert any(parameter.grad != 0 for parameter in model.parameters())
    model.zero_grad()
    assert all(parameter.grad == 0 for parameter in model.parameters())


def test_xor_training_converges():
    result = run_demo()
    assert result["accuracy"] == 1.0
    assert result["final_mse"] < 0.01
    assert result["final_mse"] < result["initial_mse"]
