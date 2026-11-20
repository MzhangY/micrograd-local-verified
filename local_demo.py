"""Train a tiny XOR neural network using micrograd, without torch or an API key."""
import argparse
import json
from pathlib import Path
import random

from micrograd.nn import MLP


def run_demo(steps=400, seed=42):
    random.seed(seed)
    samples = [([-1.0, -1.0], -1.0), ([-1.0, 1.0], 1.0),
               ([1.0, -1.0], 1.0), ([1.0, 1.0], -1.0)]
    model = MLP(2, [8, 8, 1])
    history = []
    for step in range(steps):
        predictions = [model(x) for x, _ in samples]
        loss = sum((prediction - target) ** 2
                   for prediction, (_, target) in zip(predictions, samples)) / len(samples)
        model.zero_grad()
        loss.backward()
        for parameter in model.parameters():
            parameter.data -= 0.05 * parameter.grad
        if step in (0, 49, 99, 199, steps - 1):
            history.append({"step": step + 1, "mse": loss.data})
    rows = [{"input": x, "target": target, "prediction": model(x).data}
            for x, target in samples]
    accuracy = sum((row["prediction"] > 0) == (row["target"] > 0)
                   for row in rows) / len(rows)
    final_mse = sum((row["prediction"] - row["target"]) ** 2 for row in rows) / len(rows)
    assert accuracy == 1.0, rows
    assert final_mse < 0.01, final_mse
    return {"task": "XOR neural network training", "seed": seed, "steps": steps,
            "parameters": len(model.parameters()), "initial_mse": history[0]["mse"],
            "final_mse": final_mse, "accuracy": accuracy, "history": history,
            "predictions": rows, "device": "CPU", "api_key_required": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(run_demo(), indent=2, ensure_ascii=False)
    print(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result + "\n", encoding="utf-8")
