# Bench AI with Ollama/LMStudio

<div align="center">

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Bench AI Logo](https://img.shields.io/badge/Bench%20AI-LLM%20Benchmark%20Tool-blue)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

Bench AI adalah alat yang ringan dan efisien untuk mengevaluasi kinerja model bahasa (LLM) yang berjalan melalui [Ollama](https://ollama.com/) dan LMStudio. Ini memungkinkan peneliti dan pengembang untuk membandingkan berbagai model secara objektif pada tugas pemrograman dan penalaran yang terstandarisasi.

## 🎯 Hasil Terbaru

- **Akurasi evaluasi**: 63% jawaban benar terdeteksi pada HumanEval
- **Metode evaluasi**: 5 pendekatan komplementer (normalisasi, AST, AI)
- **Reproduktibilitas**: Hasil yang konsisten antar eksekusi

## ✨ Fitur

- 🚀 **Mudah digunakan** - Antarmuka baris perintah yang intuitif
- 🔄 **Dukungan multi-dataset** - Kompatibel dengan HumanEval, CruxEval, dan Code-X-GLUE
- 📊 **Evaluasi lanjutan** - Mentolerir perbedaan format, indentasi, dan kesetaraan fungsional
- 📈 **Analisis terperinci** - Skrip analisis kinerja disertakan
- 🧩 **Dapat diperluas** - Mudah diadaptasi untuk berbagai jenis benchmark

## 🛠️ Prasyarat

- Python 3.13.5 atau lebih tinggi
- [Ollama](https://ollama.com/) terinstal dan berjalan

## 📦 Instalasi

1. Clone repositori:
   ```bash
   git clone https://github.com/laurentvv/bench-ai-ollama-lmstudio.git
   cd bench-ai-ollama-lmstudio
   ```

2. Buat lingkungan virtual dan instal dependensi:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Di Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🚀 Menjalankan benchmark

1. Pastikan Ollama sedang berjalan.

2. Unduh model yang ingin Anda uji:
   ```bash
   ollama pull qwen3:14b
   ```

3. Jalankan benchmark dengan dataset pilihan Anda:
   ```bash
   # Untuk HumanEval
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-openai-openai-humaneval.json
   ```

## 📊 Pelacakan dengan Weave

Bench AI terintegrasi dengan [Weave](https://wandb.ai/site/weave), alat yang kuat untuk melacak dan memvisualisasikan eksperimen Anda.

## 🧩 Dataset yang Didukung

Repositori ini berisi **3 file dataset** dengan **30 pertanyaan masing-masing**:

- **`sql-console-for-openai-openai-humaneval.json`** - HumanEval (30 pertanyaan)
- **`sql-console-for-cruxeval-org-cruxeval.json`** - CruxEval (30 pertanyaan)
- **`sql-console-for-google-code-x-glue-ct-code-to-text.json`** - Code-X-GLUE (30 pertanyaan)

## 💯 Evaluasi Lanjutan

Bench AI menggunakan pendekatan evaluasi lanjutan yang menggabungkan beberapa metode untuk mendeteksi jawaban yang benar:

1. **Normalisasi dasar**: Menghapus tag dan menormalkan spasi
2. **Normalisasi lanjutan**: Menangani indentasi dan jeda baris secara cerdas
3. **Normalisasi ekstrem**: Menghapus semua spasi dan jeda baris
4. **Perbandingan AST**: Menganalisis struktur sintaksis kode
5. **Evaluasi AI**: Menggunakan model bahasa untuk mendeteksi kesetaraan fungsional

## 🤝 Berkontribusi

Kontribusi sangat diterima! Jangan ragu untuk membuka issue atau mengirim pull request.

## 📄 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail.