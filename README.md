# ENF Metadata Gömme Projesi

## Proje Açıklaması
Bu proje, Elektrik Şebekesi Frekansı (ENF) verilerini ses, video ve fotoğraf dosyalarının metadata'sına gömme işlemini gerçekleştirir.

## Kurulum

### Gereksinimler
- Python 3.11+
- FFmpeg
- ExifTool

### Python Bağımlılıkları
```bash
conda env create -f environment.yml
conda activate enf-metadata
```

### Sistem Bağımlılıkları
- **FFmpeg**: Ses/video işleme için
- **ExifTool**: Metadata işleme için

## Proje Yapısı
```
staj2/
├── src/
│   ├── audio/
│   ├── video/
│   ├── image/
│   └── utils/
├── data/
│   ├── raw/
│   ├── processed/
│   └── ground_truth/
├── tests/
├── docs/
└── notebooks/
```

## Kullanım
```bash
python src/main.py
```

## Katkıda Bulunma
Bu proje staj kapsamında geliştirilmektedir.

