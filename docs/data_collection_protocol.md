# ENF Veri Toplama Protokolü

## 📋 Genel Bakış
Bu doküman, ENF (Elektrik Şebekesi Frekansı) verilerinin toplanması, işlenmesi ve metadata'ya gömülmesi için standart protokolleri tanımlar.

## 🎯 Veri Toplama Hedefleri
- **Ses Dosyaları**: Mikrofon kayıtları, müzik dosyaları
- **Video Dosyaları**: Kamera kayıtları, film dosyaları
- **Fotoğraf Dosyaları**: Dijital kamera görüntüleri

## 📁 Dosya Organizasyonu

### Raw Data (Ham Veri)
```
data/raw/
├── audio/
│   ├── microphone_recordings/
│   ├── music_files/
│   └── ambient_sounds/
├── video/
│   ├── camera_recordings/
│   ├── movie_files/
│   └── screen_recordings/
└── images/
    ├── digital_camera/
    ├── smartphone_camera/
    └── scanned_documents/
```

### Processed Data (İşlenmiş Veri)
```
data/processed/
├── enf_extracted/
├── metadata_embedded/
└── quality_assessed/
```

### Ground Truth (Gerçek Değerler)
```
data/ground_truth/
├── reference_enf/
├── timestamp_data/
└── location_data/
```

## 🔧 Veri Toplama Araçları

### Ses Kayıtları
- **Format**: WAV, FLAC, MP3
- **Örnekleme Frekansı**: 44.1 kHz minimum
- **Bit Derinliği**: 16-bit minimum
- **Süre**: 10 saniye - 5 dakika

### Video Kayıtları
- **Format**: MP4, AVI, MOV
- **Çözünürlük**: 720p minimum
- **Frame Rate**: 30 fps minimum
- **Süre**: 10 saniye - 2 dakika

### Fotoğraflar
- **Format**: JPEG, PNG, RAW
- **Çözünürlük**: 1920x1080 minimum
- **Metadata**: EXIF bilgileri korunmalı

## 📊 ENF Veri Kalitesi Kriterleri

### Minimum Gereksinimler
- **Frekans Çözünürlüğü**: 0.01 Hz
- **Zaman Çözünürlüğü**: 1 saniye
- **Sinyal-Gürültü Oranı**: 20 dB minimum
- **Doğruluk**: ±0.1 Hz

### Kalite Kontrol
- [ ] Ses seviyesi yeterli
- [ ] Gürültü seviyesi kabul edilebilir
- [ ] ENF sinyali tespit edilebilir
- [ ] Metadata bilgileri mevcut

## 🚀 Veri Toplama Adımları

### 1. Ön Hazırlık
- [ ] Kayıt ekipmanı kontrolü
- [ ] Ortam gürültü seviyesi ölçümü
- [ ] ENF referans sinyali hazırlama
- [ ] Dosya adlandırma standardı belirleme

### 2. Kayıt Süreci
- [ ] Ortam koşulları kaydı
- [ ] Zaman damgası ekleme
- [ ] Konum bilgisi kaydetme
- [ ] Kalite kontrol testleri

### 3. Sonrası İşlemler
- [ ] Dosya formatı kontrolü
- [ ] Metadata ekleme
- [ ] Kalite değerlendirmesi
- [ ] Arşivleme ve yedekleme

## 📈 Veri Analiz Metrikleri

### ENF Çıkarma Performansı
- **Başarı Oranı**: %95 minimum
- **Hata Oranı**: %5 maksimum
- **İşlem Süresi**: 10 saniye maksimum

### Metadata Gömme Performansı
- **Gömme Başarısı**: %100
- **Dosya Boyutu Artışı**: %1 maksimum
- **Kalite Kaybı**: Yok

## 🔍 Test Senaryoları

### Senaryo 1: Temel ENF Çıkarma
- **Giriş**: 10 saniye ses kaydı
- **Beklenen**: 50 Hz ENF sinyali
- **Kabul Kriteri**: Frekans ±0.1 Hz

### Senaryo 2: Metadata Gömme
- **Giriş**: ENF verisi + dosya
- **Beklenen**: Gömülmüş metadata
- **Kabul Kriteri**: %100 başarı

### Senaryo 3: Performans Testi
- **Giriş**: 100 dosya batch
- **Beklenen**: 10 saniye işlem
- **Kabul Kriteri**: Zaman aşımı yok

## 📝 Raporlama

### Günlük Rapor
- Toplanan dosya sayısı
- Kalite metrikleri
- Karşılaşılan sorunlar
- İyileştirme önerileri

### Haftalık Özet
- İlerleme durumu
- Performans analizi
- Risk değerlendirmesi
- Sonraki adımlar

## 🚨 Risk Yönetimi

### Teknik Riskler
- **Düşük Kalite Veri**: Kalite kontrol protokolleri
- **Ekipman Arızası**: Yedek ekipman
- **Yazılım Hataları**: Test ve doğrulama

### Operasyonel Riskler
- **Zaman Aşımı**: Proje planı güncelleme
- **Kaynak Yetersizliği**: Alternatif çözümler
- **Kalite Düşüşü**: Sürekli iyileştirme

## 📚 Referanslar
- ENF Teorisi ve Uygulamaları
- Ses/Video İşleme Standartları
- Metadata Formatları
- Kalite Kontrol Metodları


