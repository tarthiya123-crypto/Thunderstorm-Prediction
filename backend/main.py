# pyright: reportMissingImports=false

from fastapi.middleware.cors import CORSMiddleware
from geolocation import pixel_to_latlon
from processor import process_insat_file
from predictor import predict_clouds
from fastapi import FastAPI, UploadFile, File
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = process_insat_file(temp_path)

    result_df = predict_clouds(df)

    alerts = result_df[
        result_df["Probability"] > 0.8
    ].copy()

    alerts["Latitude"] = alerts.apply(
        lambda row: pixel_to_latlon(
            row["X"],
            row["Y"]
        )[0],
        axis=1
    )

    alerts["Longitude"] = alerts.apply(
        lambda row: pixel_to_latlon(
            row["X"],
            row["Y"]
        )[1],
        axis=1
    )

    return {
        "total_clouds": len(result_df),
        "thunderstorm_clouds": int(
            result_df["Prediction"].sum()
        ),
        "highest_probability": float(
            result_df["Probability"].max()
        ),
        "alerts": alerts[
    [
        "CloudID",
        "Probability",
        "Latitude",
        "Longitude"
    ]
].to_dict(orient="records")
    }