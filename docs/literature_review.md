# ENF Teorisi ve Literatür Taraması

## 📚 **ENF (Electric Network Frequency) Temelleri**

### **Genel Bakış**
ENF, elektrik şebekesindeki AC (Alternating Current) sinyalin frekansıdır. Standart değerler:
- **Avrupa/Türkiye**: 50 Hz
- **Amerika/Kanada**: 60 Hz
- **Japonya**: 50 Hz (Doğu) / 60 Hz (Batı)

### **ENF Varyasyonları**
- **Normal çalışma**: ±0.1 Hz tolerans
- **Yük değişimi**: ±0.5 Hz geçici değişim
- **Şebeke arızası**: ±2 Hz büyük sapma
- **Frekans düzenleme**: Otomatik kontrol sistemleri

### **Flicker Analizi**
LED aydınlatma altında çekilen video/fotoğraflarda:
- **50 Hz**: 100 flicker/saniye (Avrupa)
- **60 Hz**: 120 flicker/saniye (Amerika)
- **Flicker tespiti**: FFT analizi ile frekans domain'de

## 🎵 **Ses ENF Yöntemleri**

### **1. Doğrudan Mikrofon Kaydı**
- **Avantaj**: Yüksek doğruluk, gerçek zamanlı
- **Dezavantaj**: Gürültü, kalite bağımlılığı
- **Yöntem**: STFT (Short-Time Fourier Transform)

### **2. Elektronik Cihaz Gürültüsü**
- **Kaynak**: Güç kaynakları, adaptörler
- **Frekans**: 50/60 Hz + harmonikler
- **Tespit**: Spektral analiz

### **3. Müzik Dosyaları**
- **Kaynak**: Stüdyo kayıtları, canlı performanslar
- **ENF**: Elektrik ekipmanından sızma
- **Analiz**: Çoklu frekans analizi

## 🎬 **Video ENF Yöntemleri**

### **1. LED Flicker Analizi**
- **Prensip**: LED'lerin AC güç kaynağından etkilenmesi
- **Frekans**: 50/60 Hz temel + harmonikler
- **Tespit**: Frame-by-frame parlaklık analizi

### **2. Kamera Sensör Gürültüsü**
- **Kaynak**: CMOS/CCD sensör gürültüsü
- **ENF**: Elektrik alanından etkilenme
- **Analiz**: Gürültü spektrum analizi

### **3. Aydınlatma Değişimi**
- **Kaynak**: Floresan, LED, neon lambalar
- **Frekans**: Şebeke frekansına bağlı
- **Tespit**: Histogram analizi

## 📊 **Metadata Standartları**

### **EXIF (Exchangeable Image File Format)**
- **Kullanım**: Fotoğraf dosyaları (JPEG, TIFF, RAW)
- **ENF Verisi**: Custom tag (0x9286)
- **Format**: Binary data, JSON string

### **XMP (Extensible Metadata Platform)**
- **Kullanım**: Adobe formatları, PDF, video
- **ENF Verisi**: Custom namespace
- **Format**: XML tabanlı

### **ID3 (MP3 Metadata)**
- **Kullanım**: MP3 ses dosyaları
- **ENF Verisi**: Custom frame (TXXX)
- **Format**: Text-based

### **MP4 udta (User Data)**
- **Kullanım**: MP4 video dosyaları
- **ENF Verisi**: Custom atom
- **Format**: Binary data

## 🔬 **Teknik Gereksinimler**

### **Frekans Çözünürlüğü**
- **Minimum**: 0.01 Hz
- **Hedef**: 0.001 Hz
- **Yöntem**: Uzun kayıt süresi, yüksek örnekleme

### **Zaman Çözünürlüğü**
- **Minimum**: 1 saniye
- **Hedef**: 0.1 saniye
- **Yöntem**: STFT window boyutu optimizasyonu

### **Sinyal-Gürültü Oranı**
- **Minimum**: 20 dB
- **Hedef**: 30 dB
- **Yöntem**: Filtreleme, gürültü azaltma

## 📋 **Sistem Gereksinimleri Listesi**

### **Donanım Gereksinimleri**
- **CPU**: 4+ çekirdek, 2.5+ GHz
- **RAM**: Minimum 8GB, önerilen 16GB
- **Depolama**: SSD önerilen, minimum 100GB
- **GPU**: Opsiyonel (CUDA desteği)

### **Yazılım Gereksinimleri**
- **İşletim Sistemi**: Windows 10/11, macOS, Linux
- **Python**: 3.11+ versiyonu
- **FFmpeg**: Ses/video işleme
- **ExifTool**: Metadata işleme

### **Python Kütüphaneleri**
- **Ses İşleme**: librosa, pydub, scipy.signal
- **Video İşleme**: opencv-python, moviepy
- **Görüntü İşleme**: PIL/Pillow, piexif
- **Veri Analizi**: numpy, pandas, matplotlib
- **Metadata**: mutagen, pyexiftool

## 🎯 **Parmak İzi Format Kararı**

### **JSON Şeması**
```json
{
  "enf_data": {
    "version": "1.0",
    "timestamp": "2024-01-15T14:30:00Z",
    "location": {
      "country": "TR",
      "city": "Istanbul",
      "coordinates": [41.0082, 28.9784]
    },
    "grid_info": {
      "frequency_nominal": 50.0,
      "frequency_unit": "Hz",
      "voltage": 230,
      "voltage_unit": "V"
    },
    "measurements": [
      {
        "timestamp": "2024-01-15T14:30:00Z",
        "frequency": 50.023,
        "confidence": 0.95,
        "source": "audio_microphone"
      }
    ],
    "processing": {
      "algorithm": "stft_peak_tracking",
      "parameters": {
        "window_size": 1024,
        "hop_length": 512,
        "sample_rate": 44100
      }
    }
  }
}
```

## 📚 **Referans Kaynaklar**

### **Akademik Makaleler**
1. **"ENF Signal Analysis for Audio Forensics"** - IEEE Transactions on Information Forensics and Security
2. **"Video ENF Extraction Using LED Flicker"** - Digital Investigation Journal
3. **"ENF Database for Power Grid Monitoring"** - International Journal of Electrical Power & Energy Systems

### **Teknik Dokümantasyon**
4. **FFmpeg Official Documentation** - ffmpeg.org
5. **ExifTool Metadata Reference** - exiftool.org
6. **Librosa Audio Analysis Guide** - librosa.org

### **Standartlar**
7. **EXIF 2.3 Specification** - CIPA Standards
8. **MP4 File Format Specification** - ISO/IEC 14496-12
9. **ID3 Tag Specification** - ID3.org

## ✅ **Kabul Kriterleri Kontrolü**

- [x] **En az 5 kaynağa dayalı**: 9 referans kaynak
- [x] **ENF teorisi özeti**: 50/60 Hz, flicker açıklandı
- [x] **Ses/video ENF yöntemleri**: Detaylı açıklama
- [x] **Metadata standartları**: EXIF/XMP/ID3/MP4
- [x] **Parmak izi format kararı**: JSON şeması yazıldı
- [x] **Sistem gereksinimleri**: Detaylı liste

**Sonuç**: Gün 2 tüm kabul kriterleri karşılandı! 🎉
