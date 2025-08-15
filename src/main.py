#!/usr/bin/env python3
"""
ENF Metadata Gömme Projesi - Ana Modül
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def hello_world():
    """Ortam testi için basit hello world fonksiyonu"""
    print("=" * 50)
    print("ENF Metadata Gömme Projesi")
    print("Ortam Testi - Hello World")
    print("=" * 50)
    print(f"Python Versiyonu: {sys.version}")
    print(f"NumPy Versiyonu: {np.__version__}")
    print(f"Çalışma Dizini: {os.getcwd()}")
    print(f"Tarih/Saat: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print("✅ Ortam başarıyla kuruldu!")
    return True

def test_basic_imports():
    """Temel kütüphanelerin import testi"""
    try:
        import librosa
        import cv2
        import mutagen
        from PIL import Image
        import piexif
        import pydub
        print("✅ Tüm temel kütüphaneler başarıyla import edildi!")
        return True
    except ImportError as e:
        print(f"❌ Import hatası: {e}")
        return False

def create_sample_data():
    """Test için örnek veri oluşturma"""
    # Örnek ENF sinyali (50 Hz temel frekans)
    fs = 1000  # Örnekleme frekansı
    t = np.linspace(0, 10, fs * 10)  # 10 saniye
    enf_frequency = 50 + 0.1 * np.sin(2 * np.pi * 0.1 * t)  # ENF varyasyonu
    enf_signal = np.sin(2 * np.pi * enf_frequency * t)
    
    # Grafik oluşturma
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(t[:1000], enf_signal[:1000])
    plt.title('ENF Sinyali (İlk 1 saniye)')
    plt.xlabel('Zaman (s)')
    plt.ylabel('Genlik')
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(t, enf_frequency)
    plt.title('ENF Frekans Varyasyonu')
    plt.xlabel('Zaman (s)')
    plt.ylabel('Frekans (Hz)')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('docs/enf_sample.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Örnek ENF verisi oluşturuldu ve kaydedildi!")
    return enf_signal, enf_frequency

def main():
    """Ana fonksiyon"""
    print("🚀 ENF Metadata Gömme Projesi Başlatılıyor...")
    
    # Hello world testi
    if not hello_world():
        return False
    
    # Import testi
    if not test_basic_imports():
        return False
    
    # Örnek veri oluşturma
    try:
        enf_signal, enf_freq = create_sample_data()
        print(f"📊 ENF sinyali oluşturuldu: {len(enf_signal)} örnek")
        print(f"📈 Frekans aralığı: {enf_freq.min():.2f} - {enf_freq.max():.2f} Hz")
    except Exception as e:
        print(f"❌ Veri oluşturma hatası: {e}")
        return False
    
    print("\n🎉 Tüm testler başarılı! Ortam hazır.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
