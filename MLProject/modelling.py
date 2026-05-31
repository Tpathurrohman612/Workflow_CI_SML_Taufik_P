import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

# Menetapkan direktori lokal untuk penyimpanan log dan artefak eksperimen
mlflow.set_tracking_uri("file:./mlruns")

print("[INFO] Memuat dataset...")
# Membaca dataset yang telah dibersihkan
df = pd.read_csv('la_liga_cleaned.csv')

# Memisahkan variabel independen (fitur) dan dependen (target)
X = df.drop(columns=['FTR'])
y = df['FTR']

# Memulai sesi pelacakan eksperimen MLflow
with mlflow.start_run() as run:
    print("[INFO] Melatih model RandomForest...")
    
    # Menginisialisasi dan melatih model algoritma Random Forest
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Mendefinisikan lingkungan Conda secara dinamis 
    # (Bypass kendala pembacaan YAML dan Terms of Service Anaconda)
    custom_env = {
        "name": "la-liga-env",
        "channels": ["conda-forge", "nodefaults"],
        "dependencies": [
            "python=3.12.7",
            "pip",
            {"pip": ["mlflow==2.19.0", "scikit-learn==1.5.2", "pandas"]}
        ]
    }
    
    # Menyimpan arsitektur model beserta konfigurasi lingkungannya
    mlflow.sklearn.log_model(model, "model", conda_env=custom_env)
    
    # Mengekstrak dan menyimpan Run ID ke dalam file teks untuk alur CI/CD
    run_id = run.info.run_id
    with open("run_id.txt", "w") as f:
        f.write(run_id)
        
    print(f"[INFO] Pelatihan selesai. Run ID: {run_id}")