# ⚽ Workflow CI/CD ML: Pelatihan Model La Liga

![Python](https://img.shields.io/badge/Python-3.12.7-blue?style=flat-square&logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-1.5.2-F7931E?style=flat-square&logo=scikit-learn)
![MLflow](https://img.shields.io/badge/MLflow-2.19.0-0194E2?style=flat-square&logo=mlflow)
![Docker](https://img.shields.io/badge/Docker-Image_Build-2496ED?style=flat-square&logo=docker)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=flat-square&logo=github-actions)

## 📖 Deskripsi Proyek

Repositori ini berisi implementasi _Continuous Integration_ (CI) otomatis untuk alur kerja Machine Learning menggunakan dataset La Liga. Proyek ini menunjukkan bagaimana mengotomatiskan siklus hidup model ML—mulai dari pelatihan model algoritma Random Forest, pelacakan metrik dan artefak dengan MLflow, hingga pembungkusan (_containerization_) model menggunakan Docker.

## ✨ Fitur Utama Pipeline CI/CD

Pipeline dieksekusi secara otomatis setiap kali ada pembaruan (_push_) ke branch `main` menggunakan konfigurasi **GitHub Actions**. Alur kerjanya meliputi:

1. **🤖 Pelatihan Model MLflow:** Menjalankan `MLProject` lokal yang akan melatih `RandomForestClassifier` menggunakan Python 3.12.7 dan Scikit-Learn 1.5.2.
2. **📂 Pelacakan & Artefak Otomatis:** Menyimpan arsitektur model beserta konfigurasi Conda environment-nya ke direktori lokal `mlruns`. GitHub Actions kemudian otomatis menyimpan (_commit_) artefak eksperimen ini kembali ke repositori GitHub.
3. **🐳 Pembuatan Image Docker:** Mengekstrak Run ID terbaru dan menjalankan `mlflow models generate-dockerfile` untuk membangun Docker image bernama `la-liga-model:latest`.
4. **☁️ Distribusi Model:** Model yang sudah di-_containerized_ didorong (_push_) secara otomatis ke Docker Hub publik.

## 📂 Struktur Direktori

```text
📦 Workflow_CI_SML_Taufik_P
 ┣ 📂 .github/workflows
 ┃ ┗ 📜 ci.yml            # Konfigurasi pipeline CI/CD GitHub Actions
 ┗ 📂 MLProject
   ┣ 📜 conda.yaml        # Definisi environment Conda
   ┣ 📜 modelling.py      # Skrip utama pelatihan algoritma Random Forest
   ┣ 📜 la_liga_cleaned.csv # Dataset bersih
   ┣ 📂 mlruns            # Direktori pelacakan eksperimen & artefak model
   ┗ 📜 tautan_docker_hub.txt # Informasi Docker Hub (opsional)
```

## 🔧 Teknologi & Dependensi

- Python 3.12.7
- `mlflow==2.19.0`
- `scikit-learn==1.5.2`
- `pandas`
- `RandomForestClassifier`
- GitHub Actions
- Docker

## 🧠 Alur Kerja Proyek

1. `MLProject/modelling.py` memuat dataset `MLProject/la_liga_cleaned.csv`.
2. Memisahkan fitur (`X`) dan target (`y`) dengan kolom target `FTR`.
3. Melatih model `RandomForestClassifier` dan mencatatnya ke MLflow.
4. Menyimpan artefak model ke direktori lokal `MLProject/mlruns/`.
5. Menyimpan `run_id` ke file `MLProject/run_id.txt` untuk digunakan pipeline.
6. GitHub Actions menjalankan proyek MLflow, membangun Docker image, dan mendorong image ke Docker Hub.

## 🚀 Detail GitHub Actions CI

Pipeline di `.github/workflows/ci.yml`:

- meng-**checkout** kode sumber
- menyiapkan Python 3.12.7
- menginstal dependensi `mlflow`, `pandas`, dan `scikit-learn`
- menjalankan `mlflow run . --env-manager=local` di folder `MLProject`
- membaca `run_id` dari `run_id.txt`
- meng-commit dan push artefak `MLProject/mlruns/` ke repository jika ada perubahan
- membuat Dockerfile model dengan `mlflow models generate-dockerfile`
- membangun Docker image `la-liga-model:latest`
- login ke Docker Hub dan push image

## 📁 File Penting

- `.github/workflows/ci.yml` - pipeline CI/CD GitHub Actions
- `MLProject/conda.yaml` - definisi environment
- `MLProject/modelling.py` - skrip pelatihan dan logging MLflow
- `MLProject/la_liga_cleaned.csv` - dataset bersih
- `MLProject/mlruns/` - artefak eksperimen MLflow
- `MLProject/tautan_docker_hub.txt` - informasi Docker Hub

## 🧪 Cara Menjalankan Proyek

1. Buka terminal pada folder root repository `d:\Workflow_CI_SML_Taufik_P`.
2. Pastikan Conda sudah terpasang, lalu buat dan aktifkan environment:
   ```bash
   conda env create -f MLProject/conda.yaml
   conda activate la-liga.env
   ```
3. Masuk ke folder `MLProject`:
   ```bash
   cd MLProject
   ```
4. Jalankan skrip pelatihan model:
   ```bash
   python modelling.py
   ```
5. Untuk menjalankan sebagai MLflow project lokal:
   ```bash
   mlflow run . --env-manager=local
   ```
6. Setelah `run_id` tersedia, buat Docker image:
   ```bash
   mlflow models generate-dockerfile -m "runs:/$(cat run_id.txt)/model" -d docker_build_dir --env-manager=virtualenv
   docker build -t la-liga-model:latest docker_build_dir/
   ```
7. Push Docker image ke Docker Hub:
   ```bash
   echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
   docker tag la-liga-model:latest $DOCKER_USERNAME/la-liga-model:latest
   docker push $DOCKER_USERNAME/la-liga-model:latest
   ```

## 💡 Catatan Tambahan

- Pastikan file dataset `MLProject/la_liga_cleaned.csv` tersedia sebelum menjalankan `modelling.py`.
- Jika menggunakan GitHub Actions, atur `DOCKER_USERNAME` dan `DOCKER_PASSWORD` di secrets repository.
- `MLProject/mlruns/` berisi artefak eksperimen MLflow; GitHub Actions dapat menyertakannya kembali pada commit jika berubah.
- Proyek ini berfokus pada pelatihan lokal dan build Docker; penyesuaian lebih lanjut mungkin diperlukan untuk deploy produksi.

## 👤 Author
**Taufik Pathurrohman**
* 🎓 **Sistem Informasi (FST) – Universitas Terbuka (Bandung)**
* 🤖 **AI & Machine Learning Enthusiast** 
* 🚀 **Pijak in Collaboration with IBM SkillsBuild**
* 🐙 **GitHub:** [@tpathurrohman612](https://github.com/tpathurrohman612)

---
*Jika Anda memiliki pertanyaan atau saran terkait proyek ini, jangan ragu untuk menghubungi atau membuat issue di repositori ini!*