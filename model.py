from dataclasses import dataclass

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["attendance", "practice_score", "activity", "missed_tasks"]
TARGET = "risk_level"


@dataclass
class ModelResult:
    pipeline: Pipeline
    accuracy: float
    report: dict


def train_model(data: pd.DataFrame) -> ModelResult:
    missing = set(FEATURES + [TARGET]) - set(data.columns)
    if missing:
        raise ValueError(f"CSV файлында бағандар жетіспейді: {', '.join(sorted(missing))}")

    clean = data.dropna(subset=FEATURES + [TARGET]).copy()
    x_train, x_test, y_train, y_test = train_test_split(
        clean[FEATURES], clean[TARGET], test_size=0.25, random_state=42, stratify=clean[TARGET]
    )
    preprocessing = ColumnTransformer([("numbers", StandardScaler(), FEATURES)])
    pipeline = Pipeline(
        [
            ("preprocessing", preprocessing),
            ("classifier", RandomForestClassifier(n_estimators=180, random_state=42, class_weight="balanced")),
        ]
    )
    pipeline.fit(x_train, y_train)
    prediction = pipeline.predict(x_test)
    return ModelResult(
        pipeline=pipeline,
        accuracy=accuracy_score(y_test, prediction),
        report=classification_report(y_test, prediction, output_dict=True, zero_division=0),
    )


def predict(model: Pipeline, data: pd.DataFrame) -> pd.DataFrame:
    result = data.copy()
    result["predicted_risk"] = model.predict(result[FEATURES])
    probabilities = model.predict_proba(result[FEATURES])
    result["confidence"] = probabilities.max(axis=1).round(3)
    return result

