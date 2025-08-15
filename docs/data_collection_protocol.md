# Veri Toplama Protokolü ve Test Senaryoları

## Veri Toplama Stratejisi

### 1. Ses Kayıtları

#### Ortam Senaryoları
1. **Sessiz Ortam** (10 dakika)
   - Yer: Sessiz oda
   - Aydınlatma: LED lamba
   - Cihaz: 2 farklı telefon/kayıt cihazı
   - Format: WAV, 44.1 kHz, 16-bit

2. **Ofis Ortamı** (10 dakika)
   - Yer: Çalışma ofisi
   - Aydınlatma: Floresan + LED
   - Gürültü: Klavye, konuşma sesleri
   - Format: WAV, 44.1 kHz, 16-bit

3. **Dış Mekan** (10 dakika)
   - Yer: Açık alan
   - Aydınlatma: Güneş ışığı
   - Gürültü: Trafik, rüzgar
   - Format: WAV, 44.1 kHz, 16-bit

### 2. Video Kayıtları

#### LED Aydınlatma Senaryoları
1. **Statik Video** (5 dakika)
   - Konu: Sabit nesne
   - Aydınlatma: LED lamba
   - FPS: 30 fps
   - Format: MP4, H.264

2. **Dinamik Video** (5 dakika)
   - Konu: Hareketli nesne
   - Aydınlatma: LED lamba
   - FPS: 60 fps
   - Format: MP4, H.264

3. **Karşılaştırma Video** (5 dakika)
   - Konu: Aynı sahne
   - Aydınlatma: LED vs Floresan
   - FPS: 30 fps
   - Format: MP4, H.264

### 3. Fotoğraf Serisi (Opsiyonel)

#### LED Altında Seri Çekim
- Süre: 1 dakika
- Frekans: 1 fotoğraf/saniye
- Aydınlatma: LED lamba
- Format: JPG, RAW

## Dosya Adlandırma Standardı

### Format: `{tarih}_{saat}_{ortam}_{cihaz}_{format}_{süre}.{uzantı}`

#### Örnekler:
```
2024-01-15_14-30-00_sessiz_iphone_wav_10min.wav
2024-01-15_14-45-00_ofis_samsung_wav_10min.wav
2024-01-15_15-00-00_dis_mekan_iphone_wav_10min.wav
2024-01-15_15-15-00_led_statik_iphone_mp4_5min.mp4
2024-01-15_15-25-00_led_dinamik_samsung_mp4_5min.mp4
2024-01-15_15-35-00_led_seri_iphone_jpg_60sec.jpg
```

## Eşzamanlı Kayıt Senaryosu

### Çapraz Doğrulama İçin
1. **İki Cihazla Eşzamanlı Kayıt**
   - Cihaz 1: iPhone (ana cihaz)
   - Cihaz 2: Samsung (doğrulama cihazı)
   - Süre: 5 dakika
   - Ortam: Sessiz oda, LED aydınlatma

2. **Senkronizasyon**
   - Başlangıç sinyali: El çırpma
   - Bitiş sinyali: El çırpma
   - Zaman damgası: Her iki cihazda da

## Test Senaryoları

### Senaryo 1: Temel ENF Çıkarma
- **Amaç**: ENF sinyalinin başarıyla çıkarılabilmesi
- **Veri**: Sessiz ortam ses kaydı
- **Beklenen Sonuç**: 50 Hz ± 0.1 Hz frekans tespiti

### Senaryo 2: Gürültülü Ortam
- **Amaç**: Gürültü altında ENF çıkarma
- **Veri**: Ofis ortamı ses kaydı
- **Beklenen Sonuç**: %80+ doğruluk oranı

### Senaryo 3: Video ENF
- **Amaç**: Video dosyalarından ENF çıkarma
- **Veri**: LED altında video kaydı
- **Beklenen Sonuç**: Flicker analizi ile ENF tespiti

### Senaryo 4: Metadata Gömme
- **Amaç**: ENF verilerinin metadata'ya gömülmesi
- **Veri**: Çıkarılan ENF verileri
- **Beklenen Sonuç**: Metadata'da ENF verilerinin görünmesi

### Senaryo 5: Doğrulama
- **Amaç**: Gömülen verilerin doğruluğunu kontrol
- **Veri**: Metadata'dan çıkarılan ENF verileri
- **Beklenen Sonuç**: Orijinal verilerle %95+ uyum

## Çekim Takvimi

### Gün 1: Ses Kayıtları
- 09:00-09:10: Sessiz ortam (iPhone)
- 09:15-09:25: Sessiz ortam (Samsung)
- 10:00-10:10: Ofis ortamı (iPhone)
- 10:15-10:25: Ofis ortamı (Samsung)
- 11:00-11:10: Dış mekan (iPhone)
- 11:15-11:25: Dış mekan (Samsung)

### Gün 2: Video Kayıtları
- 09:00-09:05: LED statik video (iPhone)
- 09:10-09:15: LED statik video (Samsung)
- 10:00-10:05: LED dinamik video (iPhone)
- 10:10-10:15: LED dinamik video (Samsung)
- 11:00-11:05: Karşılaştırma video (iPhone)

### Gün 3: Eşzamanlı Kayıt
- 09:00-09:05: Eşzamanlı ses kaydı
- 10:00-10:05: Eşzamanlı video kaydı

## Kalite Kontrol

### Kayıt Öncesi
- [ ] Cihazların şarj durumu kontrol edildi
- [ ] Depolama alanı yeterli
- [ ] Aydınlatma koşulları uygun
- [ ] Gürültü seviyesi ölçüldü

### Kayıt Sırasında
- [ ] Cihazlar sabit tutuldu
- [ ] Zaman damgaları kaydedildi
- [ ] Başlangıç/bitiş sinyalleri verildi

### Kayıt Sonrası
- [ ] Dosyalar yedeklendi
- [ ] Dosya bütünlüğü kontrol edildi
- [ ] Metadata bilgileri kaydedildi
- [ ] Dosya adlandırma standardına uyuldu

## Veri Organizasyonu

```
data/
├── raw/
│   ├── audio/
│   │   ├── sessiz/
│   │   ├── ofis/
│   │   └── dis_mekan/
│   ├── video/
│   │   ├── led_statik/
│   │   ├── led_dinamik/
│   │   └── karsilastirma/
│   └── images/
│       └── led_seri/
├── processed/
│   ├── enf_extracted/
│   └── metadata_embedded/
└── ground_truth/
    ├── reference_enf/
    └── validation_data/
```

