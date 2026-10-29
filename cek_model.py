
from pathlib import Path
import joblib

folder = (
    Path(__file__).resolve().parent
    / "hasil_tuning"
    / "evaluasi_final"
)

for nomor in [1, 2, 3, 4, 5]:
    path = folder / f"model_final_horizon_{nomor}.joblib"

    print("\n" + "=" * 50)
    print("FILE:", path.name)

    try:
        model = joblib.load(path)

        print("Tipe objek:", type(model))

        if hasattr(model, "feature_names_"):
            print("Nama fitur model:")
            print(model.feature_names_)

        elif hasattr(model, "feature_name_"):
            print("Nama fitur model:")
            print(model.feature_name_)

        elif isinstance(model, dict):
            print("Isi dictionary:")
            print(model.keys())

            for key, value in model.items():
                if hasattr(value, "feature_names_"):
                    print(f"Nama fitur pada '{key}':")
                    print(value.feature_names_)

        else:
            print("Atribut feature_names_ tidak ditemukan.")

    except Exception as e:
        print("Gagal membaca model:", repr(e))
