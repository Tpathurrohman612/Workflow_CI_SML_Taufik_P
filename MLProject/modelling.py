import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

# Mengonfigurasi lokasi penyimpanan pelacakan (tracking URI) ke direktori lokal.
mlflow.set_tracking_uri("file:./mlruns")

print("Memuat dataset hasil pra-pemrosesan...")
# Membaca dataset dari direktori yang sama dengan tempat skrip ini dieksekusi
df = pd.read_csv('la_liga_cleaned.csv')

# Memisahkan dataset menjadi variabel independen (fitur/X) dan variabel dependen (target/y)
X = df.drop(columns=['FTR'])
y = df['FTR']

# Memulai sesi pelacakan eksperimen menggunakan MLflow
with mlflow.start_run() as run:
    print("Memulai proses pelatihan model...")
    
    # Inisialisasi dan pelatihan algoritma Random Forest
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Menyimpan arsitektur model yang telah dilatih ke dalam direktori artefak MLflow
    mlflow.sklearn.log_model(model, "model")
    
    # Mengekstrak ID Eksperimen (Run ID) unik dari sesi yang sedang berjalan
    run_id = run.info.run_id
    
    # Menyimpan Run ID ke dalam sebuah file teks sekunder bernama 'run_id.txt'.
    with open("run_id.txt", "w") as f:
        f.write(run_id)
        
    print(f"Pelatihan selesai dengan sukses. Run ID terekam: {run_id}")