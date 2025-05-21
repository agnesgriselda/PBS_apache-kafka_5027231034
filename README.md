## Problem Based Learning - Apache Kafka (Big Data & Data Lakehouse 2025)
### Agnes Zenobia Griselda Petrina - 5027231034 (B)

# Pemrosesan Data Sensor Real-time dengan Kafka dan PySpark

Proyek ini mendemonstrasikan alur pemrosesan data sensor suhu dan kelembaban secara real-time menggunakan Apache Kafka sebagai message broker dan Apache Spark (PySpark) untuk konsumsi, pemrosesan, dan analisis data streaming.

## Daftar Isi
1.  [Persiapan Awal (Setup)](#️-persiapan-awal-setup)
    *   [Setup `winutils.exe`](#1-setup-winutilsexe)
    *   [Setup Virtual Environment (Opsional)](#2-setup-virtual-environment-opsional)
2.  [Menjalankan Kafka & Zookeeper](#️-menjalankan-kafka--zookeeper)
3.  [Membuat Kafka Topics](#-membuat-kafka-topics)
4.  [Menjalankan Kafka Producers](#-menjalankan-kafka-producers)
    *   [Producer Suhu](#-producer-suhu)
    *   [Producer Kelembaban](#-producer-kelembaban)
5.  [Konsumsi & Olah Data dengan PySpark](#-konsumsi--olah-data-dengan-pyspark)
    *   [File: `consumer_pyspark.py`](#-file-consumer_pysparkpy)
6.  [Menjalankan PySpark Consumer](#-menjalankan-pyspark-consumer)
7.  [Struktur Direktori](#-struktur-direktori)
8.  [Catatan Tambahan](#-catatan-tambahan)

## ⚙️ Persiapan Awal (Setup)

Bagian ini menjelaskan langkah-langkah persiapan yang diperlukan sebelum menjalankan aplikasi.

### 1. Setup `winutils.exe`
`winutils.exe` diperlukan agar Apache Spark dapat berjalan dengan baik di lingkungan sistem operasi Windows.

1.  **Unduh `winutils.exe`**:
    *   Kunjungi repositori [steveloughran/winutils](https://github.com/steveloughran/winutils).
    *   Navigasi ke direktori yang sesuai dengan versi Hadoop yang Anda gunakan atau yang kompatibel dengan versi Spark Anda (misalnya, `hadoop-3.3.1/bin/`). Jika ragu, versi untuk Hadoop 3.0.0 atau 3.3.1 seringkali bekerja dengan Spark 3.x.
    *   Unduh file `winutils.exe` dari direktori `bin` tersebut.

2.  **Simpan `winutils.exe`**:
    *   Buat direktori `C:\hadoop\bin` jika belum ada.
    *   Simpan file `winutils.exe` yang telah diunduh ke `C:\hadoop\bin\winutils.exe`.

3.  **Tambahkan ke Environment Variable**:
    Anda dapat melakukan ini melalui Command Prompt atau secara manual melalui System Properties.

    *   **Melalui Command Prompt (sebagai Administrator)**:
        Buka Command Prompt sebagai Administrator dan jalankan perintah berikut:
        ```cmd
        setx HADOOP_HOME "C:\hadoop" /M
        setx PATH "%PATH%;%HADOOP_HOME%\bin" /M
        ```
        **Penting**: Setelah menjalankan perintah `setx`, Anda perlu menutup dan membuka kembali semua jendela terminal (Command Prompt, PowerShell, Git Bash, dll.) agar perubahan environment variable diterapkan.

    *   **Secara Manual melalui System Properties**:
        1.  Cari "environment variables" di Windows Search dan pilih "Edit the system environment variables".
        2.  Pada dialog "System Properties" yang muncul, klik tombol "Environment Variables...".
        3.  Di bawah bagian "System variables" (untuk semua pengguna) atau "User variables" (hanya untuk pengguna saat ini):
            *   Klik "New..." untuk membuat variabel `HADOOP_HOME`:
                *   Variable name: `HADOOP_HOME`
                *   Variable value: `C:\hadoop`
            *   Klik OK.
        4.  Cari variabel `Path` (atau `PATH`) di daftar yang sama, pilih, dan klik "Edit...".
        5.  Pada dialog "Edit environment variable", klik "New" dan tambahkan entri baru: `%HADOOP_HOME%\bin`
        6.  Klik OK pada semua dialog yang terbuka untuk menyimpan perubahan.

        **Penting**: Setelah mengubah Environment Variables melalui GUI, Anda **harus menutup dan membuka kembali** semua jendela Command Prompt, PowerShell, atau terminal lainnya agar perubahan dapat diterapkan.

### 2. Setup Virtual Environment (Opsional)
Penggunaan virtual environment sangat disarankan untuk mengisolasi dependensi proyek dan menghindari konflik antar library.

1.  **Buat Virtual Environment**:
    Buka terminal atau Command Prompt di direktori root proyek Anda dan jalankan:
    ```bash
    python -m venv .venv
    ```
    Ini akan membuat direktori bernama `.venv` yang berisi instalasi Python dan package manager pip yang terisolasi.

2.  **Aktifkan Virtual Environment**:
    *   Di Windows (Command Prompt atau PowerShell):
        ```bash
        .venv\Scripts\activate
        ```
    *   Di macOS/Linux (bash/zsh):
        ```bash
        source .venv/bin/activate
        ```
    Setelah diaktifkan, nama virtual environment (misalnya, `(.venv)`) akan muncul di awal prompt terminal Anda.

3.  **Install Library yang Dibutuhkan**:
    Dengan virtual environment aktif, install library yang diperlukan menggunakan pip:
    ```bash
    pip install kafka-python pyspark
    ```
    *   `kafka-python`: Library Python untuk berinteraksi dengan Kafka (digunakan oleh producer).
    *   `pyspark`: Library Python untuk Apache Spark.

## 🛰️ Menjalankan Kafka & Zookeeper

Apache Kafka memerlukan Apache Zookeeper untuk manajemen cluster. Keduanya perlu dijalankan sebelum aplikasi producer dan consumer dapat berfungsi.

*Pastikan Anda telah mengunduh dan mengekstrak Kafka. Contoh di bawah menggunakan path `C:\kafka_2.12-3.9.1`. Sesuaikan path ini dengan lokasi Kafka di sistem Anda.*

1.  **Jalankan Zookeeper**:
    *   Buka terminal atau Command Prompt **baru**.
    *   Pindah ke direktori instalasi Kafka Anda:
        ```bash
        cd C:\kafka_2.12-3.9.1
        ```
    *   Jalankan Zookeeper server:
        ```bash
        .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
        ```
        ![zookeper](https://github.com/user-attachments/assets/37a54691-a6db-4a0d-a0fc-9200107e5a6a)

    *   Biarkan terminal ini tetap berjalan. Zookeeper harus terus aktif selama Kafka digunakan.

2.  **Jalankan Kafka Broker**:
    *   Buka terminal atau Command Prompt **baru lainnya**.
    *   Pindah ke direktori instalasi Kafka Anda:
        ```bash
        cd C:\kafka_2.12-3.9.1
        ```
    *   Jalankan Kafka server (broker):
        ```bash
        .\bin\windows\kafka-server-start.bat .\config\server.properties
        ```
        ![kafka](https://github.com/user-attachments/assets/185b12e5-f3af-49f2-9615-7f44350320da)

    *   Biarkan terminal ini juga tetap berjalan. Kafka broker harus terus aktif.

## 📡 Membuat Kafka Topics

Topics di Kafka adalah kategori atau feed name tempat pesan dipublikasikan. Kita akan membuat dua topic: satu untuk data sensor suhu dan satu lagi untuk data sensor kelembaban.

1.  **Buka Terminal Baru**:
    Buka terminal atau Command Prompt **baru**.
2.  **Pindah ke Direktori Kafka**:
    ```bash
    cd C:\kafka_2.12-3.9.1
    ```
3.  **Buat Topic `sensor-suhu-gudang`**:
    ```bash
    .\bin\windows\kafka-topics.bat --create --topic sensor-suhu-gudang --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    ```
4.  **Buat Topic `sensor-kelembaban-gudang`**:
    ```bash
    .\bin\windows\kafka-topics.bat --create --topic sensor-kelembaban-gudang --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    ```
    *   `--bootstrap-server localhost:9092`: Menentukan alamat Kafka broker.
    *   `--partitions 1`: Jumlah partisi untuk topic. Untuk kesederhanaan, kita gunakan 1.
    *   `--replication-factor 1`: Jumlah replika untuk setiap partisi. Karena kita menjalankan satu broker, ini harus 1.

![1](https://github.com/user-attachments/assets/00c71221-b7a9-410c-bede-8377f5e8e80f)

5.  **(Opsional) Verifikasi Topic**:
    Anda dapat memeriksa apakah topic telah berhasil dibuat dengan perintah:
    ```bash
    .\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
    ```
    Anda akan melihat `sensor-suhu-gudang` dan `sensor-kelembaban-gudang` dalam daftar.

## 🤖 Menjalankan Kafka Producers

Producer adalah aplikasi yang bertugas mengirimkan data (pesan) ke Kafka topics. Kita akan memiliki dua producer terpisah.

*(Pastikan Zookeeper dan Kafka Broker sudah berjalan. Jika Anda menggunakan virtual environment, pastikan sudah diaktifkan di terminal tempat Anda akan menjalankan producer).*

### 🔹 Producer Suhu

*   **File**: `producer_suhu.py` (Anda perlu membuat file Python ini).
*   **Fungsi**: Mengirimkan data simulasi suhu ke topic `sensor-suhu-gudang`.
*   **Contoh data yang dikirim**:
    ```json
    {"gudang_id": "G1", "suhu": 85}
    ```

*   **Jalankan Producer Suhu**:
    1.  Buka terminal atau Command Prompt baru di direktori proyek Anda (tempat file `producer_suhu.py` berada).
    2.  Aktifkan virtual environment jika digunakan: `.venv\Scripts\activate`
    3.  Jalankan script:
        ```bash
        python producer_suhu.py
        ```
![2 1](https://github.com/user-attachments/assets/0c7e8710-9936-417d-ad8e-5bf5179ce290)

### 🔹 Producer Kelembaban

*   **File**: `producer_kelembaban.py` (Anda perlu membuat file Python ini).
*   **Fungsi**: Mengirimkan data simulasi kelembaban ke topic `sensor-kelembaban-gudang`.
*   **Contoh data yang dikirim**:
    ```json
    {"gudang_id": "G1", "kelembaban": 75}
    ```

*   **Jalankan Producer Kelembaban**:
    1.  Buka terminal atau Command Prompt baru di direktori proyek Anda (tempat file `producer_kelembaban.py` berada).
    2.  Aktifkan virtual environment jika digunakan: `.venv\Scripts\activate`
    3.  Jalankan script:
        ```bash
        python producer_kelembaban.py
        ```
![2 2](https://github.com/user-attachments/assets/63c6ac58-4106-4597-8d87-78d509c81d83)

Kedua producer ini akan berjalan terus menerus, mengirimkan data secara periodik.

## 📜 Konsumsi & Olah Data dengan PySpark

Consumer adalah aplikasi yang membaca data dari Kafka topics dan melakukan pemrosesan lebih lanjut. Dalam kasus ini, kita menggunakan PySpark untuk structured streaming.

*(Pastikan Zookeeper, Kafka Broker, dan kedua Producer sudah berjalan).*

### 🔹 File: `consumer_pyspark.py`
Anda perlu membuat file Python ini yang berisi logika PySpark. Script ini akan melakukan:

**a. Konsumsi Data dari Kafka**
*   Menggunakan `spark.readStream.format("kafka")` untuk terhubung dan membaca data dari topic `sensor-suhu-gudang` dan `sensor-kelembaban-gudang`.
*   Contoh kode dasar untuk membaca stream dari Kafka dalam `consumer_pyspark.py`:
    ```python
    # Inisialisasi SparkSession
    spark = SparkSession.builder.appName("SensorDataConsumer").getOrCreate()

    # Baca stream dari topic suhu
    suhu_stream_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "sensor-suhu-gudang") \
        .load()

    # Baca stream dari topic kelembaban
    kelembaban_stream_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "sensor-kelembaban-gudang") \
        .load()
    
    # (Logika pemrosesan, transformasi, dan output akan ditambahkan di sini)
    ```

**b. Filtering dan Peringatan Individual:**
*   Data dari masing-masing stream akan di-filter berdasarkan ambang batas tertentu.
*   Misalnya:
    *   Jika `suhu > 80` → munculkan `[Peringatan Suhu Tinggi]`
    *   Jika `kelembaban > 70` → munculkan `[Peringatan Kelembaban Tinggi]`
*   Contoh output yang mungkin muncul di console dari filtering ini:
    ```text
    -------------------------------------------
    Batch: ...
    -------------------------------------------
    [Peringatan Suhu Tinggi]
    Gudang G2: suhu 85.0°C

    -------------------------------------------
    Batch: ...
    -------------------------------------------
    [Peringatan Kelembaban Tinggi]
    Gudang G3: kelembaban 74.0%
    ```

**c. Gabungkan Stream dan Deteksi Kondisi Kritis (Join)**
*   Stream data suhu dan kelembaban akan digabungkan (join) berdasarkan `gudang_id`.
*   Watermarking akan digunakan untuk menangani data yang datang terlambat dan mendefinisikan window waktu untuk join (misalnya, data suhu dan kelembaban untuk gudang yang sama yang tiba dalam rentang ±10 detik satu sama lain).
*   Jika suhu **DAN** kelembaban sama-sama tinggi untuk gudang yang sama dalam rentang waktu yang berdekatan, maka akan dideteksi sebagai `[PERINGATAN KRITIS]`.
*   Contoh output yang mungkin muncul di console dari kondisi kritis ini:
    ```text
    -------------------------------------------
    Batch: ...
    -------------------------------------------
    [PERINGATAN KRITIS]
    Gudang: G2
      - Suhu: 85.0°C
      - Kelembaban: 72.0%
      - Status: Bahaya tinggi! Barang berisiko rusak
    ```

## 🚀 Menjalankan PySpark Consumer

Untuk menjalankan aplikasi PySpark streaming:

1.  **Buka Terminal Baru**:
    Buka terminal atau Command Prompt baru di direktori root proyek Anda (tempat file `consumer_pyspark.py` berada).

2.  **Aktifkan Virtual Environment (jika digunakan)**:
    ```bash
    .venv\Scripts\activate
    ```

3.  **Set `PYSPARK_PYTHON` (jika menggunakan virtual environment)**:
    Ini memberitahu Spark untuk menggunakan interpreter Python dari virtual environment Anda.
    *   Di Windows (Command Prompt):
        ```bash
        set PYSPARK_PYTHON=.\.venv\Scripts\python.exe
        ```
    *   Di Windows (PowerShell):
        ```powershell
        $env:PYSPARK_PYTHON = ".\.venv\Scripts\python.exe"
        ```
    *   Di macOS/Linux (bash/zsh):
        ```bash
        export PYSPARK_PYTHON="./.venv/bin/python"
        ```

4.  **Jalankan Script PySpark dengan `spark-submit`**:
    ```bash
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 consumer_pyspark.py
    ```
    *   `--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5`: Ini memberitahu Spark untuk mengunduh dan menyertakan library konektor Kafka-SQL.
        *   **Penting tentang Versi Package**:
            *   `3.5.5` adalah contoh versi. Pastikan versi package (`spark-sql-kafka-0-10_2.12:X.Y.Z`) **sesuai dengan versi Apache Spark** yang Anda gunakan. `_2.12` merujuk pada versi Scala yang digunakan Spark.
            *   Anda dapat mencari versi yang kompatibel di [Maven Repository (misalnya, untuk spark-sql-kafka-0-10_2.12)](https://mvnrepository.com/artifact/org.apache.spark/spark-sql-kafka-0-10_2.12). Ganti `3.5.5` dengan versi yang sesuai (misalnya, jika Anda menggunakan Spark 3.3.0, Anda mungkin memerlukan package versi 3.3.0).
            *   Jika versi `3.5.5` yang Anda sebutkan sebelumnya ada dan kompatibel dengan Spark Anda, gunakan itu. Periksa Maven Central untuk ketersediaan.
    *   `consumer_pyspark.py`: Nama file script PySpark Anda.

    ✅ Pastikan file `consumer_pyspark.py` berada di direktori kerja yang sama tempat Anda menjalankan perintah `spark-submit`.

Aplikasi Spark Streaming akan mulai berjalan dan memproses data dari Kafka, menampilkan output ke console.

![3](https://github.com/user-attachments/assets/f25848f0-7845-4517-9301-aad30575e893)

![4](https://github.com/user-attachments/assets/10fbde64-141c-491a-b034-1774402804c2)


## 📁 Struktur Direktori

Struktur direktori proyek yang disarankan akan terlihat seperti ini:

```text
kafka/
├── producer_suhu.py
├── producer_kelembaban.py
├── consumer_pyspark.py
├── README.md
└── .venv/                # Direktori virtual environment (opsional, dibuat jika Anda menggunakannya)              # Direktori virtual environment (opsional)
