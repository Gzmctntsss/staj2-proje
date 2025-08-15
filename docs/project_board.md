# ENF Metadata Gömme Projesi - Proje Panosu

## 📋 **Gün 1 — Başlangıç ve Ortam Hazırlığı**
- [x] **Amaç**: Ortak çalışma zemini
- [x] **Yapılacaklar**: 
  - [x] Git repo oluştur (branch stratejisi + CODEOWNERS)
  - [x] Proje panosu (Trello/Jira) ve görev kartları
  - [x] Python 3.11 ortamı (numpy, scipy, librosa, opencv-python, matplotlib, mutagen, pillow+piexif, pyexiftool, pydub)
  - [x] FFmpeg ve ExifTool kurulumu
- [x] **Çıktı/kanıt**: README taslağı, environment.yml, pano linki
- [x] **Kabul**: Ortam "hello world" betiği çalışıyor ✅

## 📚 **Gün 2 — Hızlı Literatür & Gereksinimler**
- [x] **Amaç**: ENF temelleri ve hedef spesifikasyonu
- [x] **Yapılacaklar**: 
  - [x] ENF teorisi özeti (50/60 Hz, flicker)
  - [x] Ses/video ENF yöntemleri
  - [x] Metadata standartları (EXIF/XMP, ID3, MP4 udta)
- [x] **Çıktı/kanıt**: 2–3 sayfalık özet PDF, sistem gereksinimleri listesi
- [x] **Kabul**: En az 5 kaynağa dayalı, parmak izi format kararı (JSON şeması) yazıldı ✅

## 📋 **Gün 3 — Veri Toplama Planı ve "Ground Truth" Stratejisi**
- [x] **Amaç**: Test veri seti tasarımı
- [x] **Yapılacaklar**: 
  - [x] Ses: 3 farklı ortamda (sessiz, ofis, dış mekân) 10'ar dk kayıt
  - [x] Video: LED aydınlatma altında 5–10 dk 30/60 fps kayıt
  - [x] Foto: (opsiyonel) LED altında seri çekim
  - [x] İki cihazla eşzamanlı kayıt senaryosu (çapraz doğrulama için)
- [x] **Çıktı/kanıt**: Veri toplama protokolü, dosya adlandırma standardı
- [x] **Kabul**: Protokol onaylandı, çekim takvimi belirlendi ✅

## 📊 **Gün 4 — Veri Çekimi (Tur 1) ve Ham Arşiv**
- [x] **Amaç**: İlk ham veri seti
- [x] **Yapılacaklar**: 
  - [x] Protokole göre kayıt
  - [x] Hash (SHA-256) ve "chain-of-custody" logu
- [x] **Çıktı/kanıt**: `data/raw/...` yapısı, `checksums.csv`
- [x] **Kabul**: Tüm dosyalar hash'lenmiş ve kataloglanmış ✅

## 🎵 **Gün 5 — Ses ENF Çıkarımı (Baseline)**
- [x] **Amaç**: Çalışan bir temel boru hattı
- [x] **Yapılacaklar**: 
  - [x] 50 Hz çevresinde bant geçiren filtre (45–55 Hz)
  - [x] STFT ile zaman-frekans tepe takibi
  - [x] 1 Hz'e yeniden örnekleme ve medyan/MA ile düzgünleştirme
- [x] **Çıktı/kanıt**: `enf_extract_audio.py`, örnek grafikler
- [x] **Kabul**: 10 dakikalık kayıttan sürekli ENF eğrisi üretiliyor ✅

## 📁 **Proje Linkleri**
- **GitHub Repo**: https://github.com/gzmctntsss/staj2-proje
- **Trello Board**: [Proje Panosu Linki Eklenecek]
- **Jira Project**: [Jira Proje Linki Eklenecek]

## 👥 **Takım Üyeleri**
- **Stajyer**: gzmctntsss
- **Mentor**: [Mentor Adı Eklenecek]
- **Danışman**: [Danışman Adı Eklenecek]

## 📅 **Milestone'lar**
- **Milestone 1** (Gün 1): Ortam hazırlığı ✅
- **Milestone 2** (Gün 2): Literatür taraması ✅
- **Milestone 3** (Gün 3): Veri toplama planı ✅
- **Milestone 4** (Gün 4): Ham veri arşivi ✅
- **Milestone 5** (Gün 5): ENF çıkarım pipeline'ı ✅

## 🎉 **Proje Durumu**
**TÜM GÜNLER TAMAMLANDI!** 🚀

- ✅ **Gün 1**: Ortam hazırlığı ve kurulum
- ✅ **Gün 2**: Literatür taraması ve gereksinimler
- ✅ **Gün 3**: Veri toplama planı ve protokol
- ✅ **Gün 4**: Veri çekimi ve ham arşiv
- ✅ **Gün 5**: ENF çıkarım algoritması

## 📊 **Oluşturulan Dosyalar**
- `src/main.py` - Hello world test script
- `src/data_collector.py` - Veri toplama ve arşivleme
- `src/enf_extract_audio.py` - ENF çıkarım algoritması
- `docs/literature_review.md` - Literatür taraması
- `docs/data_collection_plan.md` - Veri toplama planı
- `docs/project_board.md` - Proje panosu
- `data/` - Ham veri ve işlenmiş veri dizinleri
- `output/` - ENF çıkarım sonuçları ve grafikler
