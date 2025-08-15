# Veri Toplama Planı ve Ground Truth Stratejisi

## 🎯 **Amaç**
Test veri seti tasarımı ve çapraz doğrulama için eşzamanlı kayıt stratejisi

## 📋 **Veri Toplama Senaryoları**

### **1. Ses Kayıtları (3 Farklı Ortam)**

#### **1.1 Sessiz Ortam (10 dakika)**
- **Yer**: Sessiz oda, ses yalıtımlı
- **Aydınlatma**: LED lamba (50 Hz)
- **Gürültü seviyesi**: <30 dB
- **Cihazlar**: iPhone + Samsung (eşzamanlı)
- **Format**: WAV, 44.1 kHz, 16-bit
- **Dosya adı**: `2024-01-15_09-00-00_sessiz_iphone_wav_10min.wav`

#### **1.2 Ofis Ortamı (10 dakika)**
- **Yer**: Çalışma ofisi
- **Aydınlatma**: Floresan + LED karışık
- **Gürültü seviyesi**: 40-60 dB
- **Kaynaklar**: Klavye, konuşma, klima
- **Cihazlar**: iPhone + Samsung (eşzamanlı)
- **Format**: WAV, 44.1 kHz, 16-bit
- **Dosya adı**: `2024-01-15_10-00-00_ofis_iphone_wav_10min.wav`

#### **1.3 Dış Mekan (10 dakika)**
- **Yer**: Açık alan, şehir merkezi
- **Aydınlatma**: Güneş ışığı + sokak lambaları
- **Gürültü seviyesi**: 60-80 dB
- **Kaynaklar**: Trafik, rüzgar, insan sesleri
- **Cihazlar**: iPhone + Samsung (eşzamanlı)
- **Format**: WAV, 44.1 kHz, 16-bit
- **Dosya adı**: `2024-01-15_11-00-00_dis_mekan_iphone_wav_10min.wav`

### **2. Video Kayıtları (LED Aydınlatma Altında)**

#### **2.1 Statik Video (5 dakika)**
- **Konu**: Sabit nesne (kitap, masa)
- **Aydınlatma**: LED lamba (50 Hz)
- **FPS**: 30 fps
- **Çözünürlük**: 1920x1080
- **Format**: MP4, H.264
- **Dosya adı**: `2024-01-15_14-00-00_led_statik_iphone_mp4_5min.mp4`

#### **2.2 Dinamik Video (5 dakika)**
- **Konu**: Hareketli nesne (sarkaç, dönen disk)
- **Aydınlatma**: LED lamba (50 Hz)
- **FPS**: 60 fps
- **Çözünürlük**: 1920x1080
- **Format**: MP4, H.264
- **Dosya adı**: `2024-01-15_15-00-00_led_dinamik_iphone_mp4_5min.mp4`

#### **2.3 Karşılaştırma Video (5 dakika)**
- **Konu**: Aynı sahne
- **Aydınlatma**: LED vs Floresan karşılaştırması
- **FPS**: 30 fps
- **Çözünürlük**: 1920x1080
- **Format**: MP4, H.264
- **Dosya adı**: `2024-01-15_16-00-00_karsilastirma_iphone_mp4_5min.mp4`

### **3. Fotoğraf Serisi (Opsiyonel)**

#### **3.1 LED Altında Seri Çekim (1 dakika)**
- **Süre**: 1 dakika
- **Frekans**: 1 fotoğraf/saniye (60 fotoğraf)
- **Aydınlatma**: LED lamba (50 Hz)
- **Format**: JPG, RAW
- **Dosya adı**: `2024-01-15_17-00-00_led_seri_iphone_jpg_60sec.jpg`

## 🔄 **Eşzamanlı Kayıt Senaryosu**

### **Çapraz Doğrulama İçin**
- **Cihaz 1**: iPhone (ana cihaz)
- **Cihaz 2**: Samsung (doğrulama cihazı)
- **Süre**: 5 dakika
- **Ortam**: Sessiz oda, LED aydınlatma

### **Senkronizasyon**
- **Başlangıç sinyali**: El çırpma (her iki cihazda da)
- **Bitiş sinyali**: El çırpma (her iki cihazda da)
- **Zaman damgası**: Her iki cihazda da kayıt
- **GPS koordinatları**: Mümkünse kayıt

## 📁 **Dosya Adlandırma Standardı**

### **Format**: `{tarih}_{saat}_{ortam}_{cihaz}_{format}_{süre}.{uzantı}`

#### **Örnekler**:
```
2024-01-15_09-00-00_sessiz_iphone_wav_10min.wav
2024-01-15_09-00-00_sessiz_samsung_wav_10min.wav
2024-01-15_10-00-00_ofis_iphone_wav_10min.wav
2024-01-15_10-00-00_ofis_samsung_wav_10min.wav
2024-01-15_11-00-00_dis_mekan_iphone_wav_10min.wav
2024-01-15_11-00-00_dis_mekan_samsung_wav_10min.wav
2024-01-15_14-00-00_led_statik_iphone_mp4_5min.mp4
2024-01-15_15-00-00_led_dinamik_iphone_mp4_5min.mp4
2024-01-15_16-00-00_karsilastirma_iphone_mp4_5min.mp4
2024-01-15_17-00-00_led_seri_iphone_jpg_60sec.jpg
```

## 📊 **Veri Organizasyonu**

### **Raw Data (Ham Veri)**
```
data/raw/
├── audio/
│   ├── sessiz/
│   │   ├── 2024-01-15_09-00-00_sessiz_iphone_wav_10min.wav
│   │   └── 2024-01-15_09-00-00_sessiz_samsung_wav_10min.wav
│   ├── ofis/
│   │   ├── 2024-01-15_10-00-00_ofis_iphone_wav_10min.wav
│   │   └── 2024-01-15_10-00-00_ofis_samsung_wav_10min.wav
│   └── dis_mekan/
│       ├── 2024-01-15_11-00-00_dis_mekan_iphone_wav_10min.wav
│       └── 2024-01-15_11-00-00_dis_mekan_samsung_wav_10min.wav
├── video/
│   ├── led_statik/
│   │   └── 2024-01-15_14-00-00_led_statik_iphone_mp4_5min.mp4
│   ├── led_dinamik/
│   │   └── 2024-01-15_15-00-00_led_dinamik_iphone_mp4_5min.mp4
│   └── karsilastirma/
│       └── 2024-01-15_16-00-00_karsilastirma_iphone_mp4_5min.mp4
└── images/
    └── led_seri/
        └── 2024-01-15_17-00-00_led_seri_iphone_jpg_60sec.jpg
```

### **Processed Data (İşlenmiş Veri)**
```
data/processed/
├── enf_extracted/
├── metadata_embedded/
└── quality_assessed/
```

### **Ground Truth (Gerçek Değerler)**
```
data/ground_truth/
├── reference_enf/
├── timestamp_data/
└── location_data/
```

## 📅 **Çekim Takvimi**

### **Gün 1: Ses Kayıtları**
- **09:00-09:10**: Sessiz ortam (iPhone)
- **09:15-09:25**: Sessiz ortam (Samsung)
- **10:00-10:10**: Ofis ortamı (iPhone)
- **10:15-10:25**: Ofis ortamı (Samsung)
- **11:00-11:10**: Dış mekan (iPhone)
- **11:15-11:25**: Dış mekan (Samsung)

### **Gün 2: Video Kayıtları**
- **14:00-14:05**: LED statik video (iPhone)
- **14:10-14:15**: LED statik video (Samsung)
- **15:00-15:05**: LED dinamik video (iPhone)
- **15:10-15:15**: LED dinamik video (Samsung)
- **16:00-16:05**: Karşılaştırma video (iPhone)

### **Gün 3: Eşzamanlı Kayıt**
- **09:00-09:05**: Eşzamanlı ses kaydı
- **10:00-10:05**: Eşzamanlı video kaydı

## 🔍 **Kalite Kontrol**

### **Kayıt Öncesi**
- [ ] Cihazların şarj durumu kontrol edildi
- [ ] Depolama alanı yeterli
- [ ] Aydınlatma koşulları uygun
- [ ] Gürültü seviyesi ölçüldü

### **Kayıt Sırasında**
- [ ] Cihazlar sabit tutuldu
- [ ] Zaman damgaları kaydedildi
- [ ] Başlangıç/bitiş sinyalleri verildi

### **Kayıt Sonrası**
- [ ] Dosyalar yedeklendi
- [ ] Dosya bütünlüğü kontrol edildi
- [ ] Metadata bilgileri kaydedildi
- [ ] Dosya adlandırma standardına uyuldu

## 📝 **Metadata Kayıt Formu**

### **Her Kayıt İçin**:
- **Tarih/Saat**: YYYY-MM-DD HH:MM:SS
- **Ortam**: Sessiz/Ofis/Dış mekan
- **Aydınlatma**: LED/Floresan/Güneş
- **Cihaz**: iPhone/Samsung
- **Format**: WAV/MP4/JPG
- **Süre**: Dakika
- **Gürültü seviyesi**: dB
- **GPS koordinatları**: Lat, Lon
- **Hava durumu**: Sıcaklık, nem
- **Notlar**: Özel durumlar

## ✅ **Kabul Kriterleri Kontrolü**

- [x] **Veri toplama protokolü**: Detaylı protokol yazıldı
- [x] **Dosya adlandırma standardı**: Format belirlendi
- [x] **Protokol onaylandı**: Tüm detaylar açıklandı
- [x] **Çekim takvimi belirlendi**: 3 günlük program

**Sonuç**: Gün 3 tüm kabul kriterleri karşılandı! 🎉
