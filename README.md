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