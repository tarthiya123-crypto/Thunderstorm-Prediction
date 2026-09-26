try:
    import joblib  # type: ignore[import-not-found]
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "joblib is required to load the thunderstorm model. "
        "Install it with: pip install joblib"
    ) from exc

model = joblib.load("../models/thunderstorm_model.pkl")

FEATURES = [
    "AreaPixels",
    "MinTemp",
    "MeanTemp",
    "X",
    "Y",
    "TIR2_Mean",
    "TIR2_Min",
    "WV_Mean",
    "WV_Min",
    "BTD_TIR1_TIR2",
    "BTD_WV_TIR1"
]

def predict_clouds(df):

    X = df[FEATURES]

    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1]

    df["Prediction"] = preds
    df["Probability"] = probs

    return df