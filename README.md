# AI Radar: Hybrid Object Tracking System

[![Türkçe](https://img.shields.io/badge/Dil-Türkçe-red)](#türkçe) [![English](https://img.shields.io/badge/Language-English-blue)](#english)

---

## Türkçe

**AI Radar**, YOLOv8'in nesne tespit gücünü OpenCV'nin CSRT algoritmasının yüksek performanslı takip kararlılığı ile harmanlayan gerçek zamanlı bir bilgisayarlı görü aracıdır.

### Nasıl Çalışır?
* **Arama Modu (YOLOv8 + ByteTrack):** Sistem kamera görüntüsünü sürekli tarar, `yolov8n.pt` modeli ile nesneleri tespit eder ve ByteTrack algoritmasını kullanarak her birine benzersiz bir kimlik (ID) atar.
* **Kilitlenme Modu (OpenCV CSRT):** Kullanıcı belirli bir ID'yi tuşlayıp kilitlenme komutu verdiğinde, sistem YOLO'yu arka plana alarak seçili nesne üzerinde bir CSRT izleyicisi başlatır. Bu sayede işlem yükü hafifler, FPS artar ve pürüzsüz bir takip sağlanır.
* **Otomatik Kurtarma:** Hedef nesne belirlenen eşik (15 kare) boyunca görüş alanından tamamen çıkarsa, sistem kilidi otomatik olarak kaldırır ve Arama Moduna geri döner.

### Kullanılan Teknolojiler
* **Ultralytics YOLOv8:** Gerçek zamanlı, hafif nesne tespiti için (Nano model).
* **OpenCV (Contrib):** Arayüz çizimleri ve CSRT takip algoritması için.
* **PyTorch:** YOLO'nun çalışması için temel kütüphane; donanım ivmesi için **Apple Silicon (MPS)** ve **NVIDIA (CUDA)** mimarilerini otomatik tanır.
* **ByteTrack:** Arama modunda çoklu nesne takibi ve kimlik ataması için.

### Kurulum
1. Repoyu bilgisayarınıza indirin:
   ```bash
   git clone [https://github.com/mehmet-topaktas/AI-Radar.git](https://github.com/mehmet-topaktas/AI-Radar.git)
   cd AI-Radar

2. Sanal ortam (virtual environment) oluşturun ve aktifleştirin:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Windows için: venv\Scripts\activate

3. Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt

###  Kontroller
0-9: Hedef nesnenin ID numarasını girin.
t: Takip (Track) - Girilen ID'ye kilitlenir.
c: İptal (Cancel) - Takibi bırakıp Arama Moduna döner.
Backspace: Yazılan ID'yi siler.
q: Uygulamadan çıkış yapar.

###  Geliştirici
 ** Mehmet Topaktaş**

 ----------------------------

 # 🎯 AI Radar: Hybrid Object Tracking System

[![Türkçe](https://img.shields.io/badge/Dil-Türkçe-red)](#türkçe) [![English](https://img.shields.io/badge/Language-English-blue)](#english)

---

## English

**AI Radar** is a real-time computer vision tool that combines the object detection power of YOLOv8 with the high-performance tracking stability of OpenCV's CSRT algorithm.

### How It Works?
* **Search Mode (YOLOv8 + ByteTrack):** The system continuously scans the camera feed, detects objects using the `yolov8n.pt` model, and assigns a unique ID to each using the ByteTrack algorithm.
* **Lock-on Mode (OpenCV CSRT):** When the user selects a specific ID and issues a lock-on command, the system moves YOLO to the background and initiates a CSRT tracker on the selected object. This reduces the processing load, increases FPS, and ensures smooth tracking.
* **Auto-Recovery:** If the target object completely leaves the field of view for a set threshold (15 frames), the system automatically releases the lock and reverts to Search Mode.

### Technologies Used
* **Ultralytics YOLOv8:** For real-time, lightweight object detection (Nano model).
* **OpenCV (Contrib):** For interface rendering and the CSRT tracking algorithm.
* **PyTorch:** The core library for running YOLO; automatically detects **Apple Silicon (MPS)** and **NVIDIA (CUDA)** architectures for hardware acceleration.
* **ByteTrack:** For multi-object tracking and ID assignment in Search Mode.

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/mehmet-topaktas/AI-Radar.git](https://github.com/mehmet-topaktas/AI-Radar.git)
   cd AI-Radar

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # for Windows: venv\Scripts\activate

3. Install required dependencies:
    ```bash
    pip install -r requirements.txt

### Controls
0-9: Type the ID of the target object.
t: Track - Lock onto the entered ID.
c: Cancel - Cancel tracking and return to Search Mode.
Backspace: Delete the typed ID.
q: Quit the application.

### Developer
** Mehmet Topaktaş**