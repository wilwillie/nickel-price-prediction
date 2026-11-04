from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageOps


BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = (
    BASE_DIR
    / "hasil_tuning"
    / "evaluasi_final"
)

FEATURES = [
    "LME Nickel Stock",
    "LME Aluminium Price",
    "LME Copper Price",
    "LME Zinc Price",
    "Iron Ore Price",
    "Dollar Index",
    "WTI Price",
    "LME Nickel Price Lag 1",
    "LME Nickel Price Lag 2",
    "LME Nickel Price Lag 3",
]

HORIZONS = [1, 2, 3, 4, 5]

MODEL_FILES = {
    1: MODEL_DIR / "model_final_horizon_1.joblib",
    2: MODEL_DIR / "model_final_horizon_2.joblib",
    3: MODEL_DIR / "model_final_horizon_3.joblib",
    4: MODEL_DIR / "model_final_horizon_4.joblib",
    5: MODEL_DIR / "model_final_horizon_5.joblib",
}

EVALUATION = pd.DataFrame({
    "Horizon (hari)": [1, 2, 3, 4, 5],
    "Skema": ["80:20", "80:20", "80:20", "80:20", "80:20"],
    "Jumlah Data Uji": [595, 595, 594, 594, 594],
    "MAE": [
        536.3788, 662.3807, 827.8417, 929.6537, 949.3268
    ],
    "RMSE": [
        633.8613, 826.1914, 989.3937, 1137.2799, 1092.9267
    ],
    "MAPE (%)": [
        3.3708, 4.0928, 5.1143, 5.6962, 5.9050
    ],
    "R2": [
        0.6975, 0.4861, 0.2605, 0.0229, 0.0976
    ],
})


# ==================================================
# MEMUAT MODEL
# ==================================================

@st.cache_resource
def load_model(path_string):
    return joblib.load(path_string)


def load_nickel_image(filename):
    with Image.open(BASE_DIR / "img" / filename) as image:
        return ImageOps.pad(
            image.convert("RGB"),
            (900, 600),
            method=Image.Resampling.LANCZOS,
            color="#172A32"
        )


def load_company_image(filename):
    with Image.open(BASE_DIR / "img" / filename) as image:
        company_image = image.convert("RGBA")
        company_image.thumbnail(
            (900, 900),
            resample=Image.Resampling.LANCZOS
        )
        canvas = Image.new("RGB", (900, 900), "#172A32")
        position = (
            (canvas.width - company_image.width) // 2,
            (canvas.height - company_image.height) // 2
        )
        canvas.paste(company_image, position, company_image)
        return canvas


def load_circular_portrait(filename):
    with Image.open(BASE_DIR / "img" / filename) as image:
        portrait = ImageOps.fit(
            image.convert("RGBA"),
            (600, 600),
            method=Image.Resampling.LANCZOS
        )
        circular_mask = Image.new("L", portrait.size, 0)
        ImageDraw.Draw(circular_mask).ellipse(
            (0, 0, portrait.width - 1, portrait.height - 1),
            fill=255
        )
        portrait.putalpha(circular_mask)
        return portrait

