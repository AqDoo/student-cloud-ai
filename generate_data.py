from pathlib import Path

import numpy as np
import pandas as pd


def generate_students(count: int = 240, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    attendance = rng.integers(45, 101, count)
    practice = np.clip(attendance * 0.55 + rng.normal(28, 12, count), 20, 100)
    activity = rng.integers(0, 101, count)
    missed = np.clip(np.round((100 - attendance) / 7 + rng.normal(1, 1.5, count)), 0, 14)
    final_score = np.clip(
        0.38 * attendance + 0.42 * practice + 0.20 * activity - 1.1 * missed
        + rng.normal(0, 5, count),
        0,
        100,
    )
    risk = np.where(final_score < 60, "Жоғары", np.where(final_score < 75, "Орташа", "Төмен"))
    return pd.DataFrame(
        {
            "student_id": [f"ST{i:03d}" for i in range(1, count + 1)],
            "attendance": attendance,
            "practice_score": practice.round(1),
            "activity": activity,
            "missed_tasks": missed.astype(int),
            "final_score": final_score.round(1),
            "risk_level": risk,
        }
    )


if __name__ == "__main__":
    output = Path(__file__).parent / "data" / "students.csv"
    output.parent.mkdir(exist_ok=True)
    generate_students().to_csv(output, index=False)
    print(f"Деректер сақталды: {output}")

