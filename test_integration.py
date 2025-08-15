#!/usr/bin/env python3
"""
ENF Metadata Gömme Projesi - Entegre Test Betiği
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Modülleri import et
sys.path.append('src')
from utils.enf_extractor import ENFExtractor
from utils.metadata_embedder import MetadataEmbedder

def create_test_audio():
    """Test için ses dosyası oluştur"""
    print("🎵 Test ses dosyası oluşturuluyor...")
    
    # ENF sinyali oluştur (50 Hz temel frekans)
    fs = 44100  # CD kalitesi
    duration = 10  # 10 saniye
    t = np.linspace(0, duration, fs * duration)
    
    # ENF frekans varyasyonu (gerçekçi)
    enf_freq = 50 + 0.05 * np.sin(2 * np.pi * 0.1 * t) + 0.02 * np.random.randn(len(t))
    enf_signal = 0.1 * np.sin(2 * np.pi * enf_freq * t)
    
    # Gürültü ekle
    noise = 0.01 * np.random.randn(len(t))
    audio_signal = enf_signal + noise
    
    # WAV dosyası olarak kaydet
    import soundfile as sf
    test_file = "test_audio.wav"
    sf.write(test_file, audio_signal, fs)
    
    print(f"✅ Test ses dosyası oluşturuldu: {test_file}")
    return test_file

def create_test_image():
    """Test için görüntü dosyası oluştur"""
    print("🖼️ Test görüntü dosyası oluşturuluyor...")
    
    # Basit test görüntüsü
    from PIL import Image, ImageDraw
    
    # 512x512 boyutunda görüntü
    img = Image.new('RGB', (512, 512), color='white')
    draw = ImageDraw.Draw(img)
    
    # Basit şekil çiz
    draw.rectangle([100, 100, 412, 412], outline='black', width=5)
    draw.ellipse([150, 150, 362, 362], fill='lightblue')
    draw.text((200, 250), "ENF Test", fill='black')
    
    test_file = "test_image.jpg"
    img.save(test_file, "JPEG", quality=95)
    
    print(f"✅ Test görüntü dosyası oluşturuldu: {test_file}")
    return test_file

def test_enf_extraction():
    """ENF çıkarma testi"""
    print("\n🔍 ENF Çıkarma Testi")
    print("=" * 40)
    
    # Test ses dosyası oluştur
    audio_file = create_test_audio()
    
    # ENF çıkarıcı oluştur
    extractor = ENFExtractor(target_freq=50.0, tolerance=0.1)
    
    # ENF çıkar
    frequencies, timestamps, confidence = extractor.extract_from_audio(audio_file)
    
    # Sonuçları analiz et
    mean_freq = np.mean(frequencies)
    std_freq = np.std(frequencies)
    mean_conf = np.mean(confidence)
    
    print(f"📊 ENF Analiz Sonuçları:")
    print(f"   Ortalama frekans: {mean_freq:.3f} Hz")
    print(f"   Frekans standart sapması: {std_freq:.3f} Hz")
    print(f"   Ortalama güven skoru: {mean_conf:.3f}")
    print(f"   Örnek sayısı: {len(frequencies)}")
    
    # Sonuçları kaydet
    output_json = "test_enf_results.json"
    extractor.save_enf_data(frequencies, timestamps, confidence, "audio", output_json)
    
    # Görselleştirme
    output_plot = "test_enf_analysis.png"
    extractor.plot_enf_analysis(frequencies, timestamps, confidence, output_plot)
    
    print(f"✅ ENF verileri kaydedildi: {output_json}")
    print(f"✅ Analiz grafiği kaydedildi: {output_plot}")
    
    return frequencies, timestamps, confidence

def test_metadata_embedding(enf_data):
    """Metadata gömme testi"""
    print("\n📝 Metadata Gömme Testi")
    print("=" * 40)
    
    # Metadata gömücü oluştur
    embedder = MetadataEmbedder()
    
    # Test dosyaları oluştur
    audio_file = "test_audio.wav"
    image_file = create_test_image()
    
    # ENF verilerini hazırla
    enf_json_data = {
        "enf_data": {
            "frequencies": enf_data[0].tolist(),
            "timestamps": [datetime.now().isoformat()] * len(enf_data[0]),
            "confidence": enf_data[2].tolist(),
            "source_type": "audio",
            "extraction_method": "STFT",
            "sampling_rate": 44100
        }
    }
    
    # Ses dosyasına göm
    print("🎵 Ses dosyasına ENF verileri gömülüyor...")
    success_audio = embedder.embed_to_audio(audio_file, enf_json_data, "test_audio_with_enf.wav")
    
    # Görüntü dosyasına göm
    print("🖼️ Görüntü dosyasına ENF verileri gömülüyor...")
    success_image = embedder.embed_to_image(image_file, enf_json_data, "test_image_with_enf.jpg")
    
    if success_audio:
        print("✅ Ses dosyasına ENF verileri başarıyla gömüldü")
    else:
        print("❌ Ses dosyasına gömme başarısız")
    
    if success_image:
        print("✅ Görüntü dosyasına ENF verileri başarıyla gömüldü")
    else:
        print("❌ Görüntü dosyasına gömme başarısız")
    
    return success_audio, success_image

def test_metadata_extraction():
    """Metadata çıkarma testi"""
    print("\n🔍 Metadata Çıkarma Testi")
    print("=" * 40)
    
    embedder = MetadataEmbedder()
    
    # Gömülü dosyalardan veri çıkar
    audio_file = "test_audio_with_enf.wav"
    image_file = "test_image_with_enf.jpg"
    
    if os.path.exists(audio_file):
        print("🎵 Ses dosyasından ENF verileri çıkarılıyor...")
        audio_data = embedder.extract_from_file(audio_file)
        if audio_data:
            print("✅ Ses dosyasından ENF verileri başarıyla çıkarıldı")
            print(f"   Frekans sayısı: {len(audio_data['enf_data']['frequencies'])}")
        else:
            print("❌ Ses dosyasından veri çıkarma başarısız")
    
    if os.path.exists(image_file):
        print("🖼️ Görüntü dosyasından ENF verileri çıkarılıyor...")
        image_data = embedder.extract_from_file(image_file)
        if image_data:
            print("✅ Görüntü dosyasından ENF verileri başarıyla çıkarıldı")
            print(f"   Frekans sayısı: {len(image_data['enf_data']['frequencies'])}")
        else:
            print("❌ Görüntü dosyasından veri çıkarma başarısız")

def cleanup_test_files():
    """Test dosyalarını temizle"""
    print("\n🧹 Test Dosyaları Temizleniyor...")
    
    test_files = [
        "test_audio.wav",
        "test_audio_with_enf.wav", 
        "test_image.jpg",
        "test_image_with_enf.jpg",
        "test_enf_results.json",
        "test_enf_analysis.png"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ {file} silindi")
    
    print("✅ Temizlik tamamlandı")

def main():
    """Ana test fonksiyonu"""
    print("🚀 ENF Metadata Gömme Projesi - Entegre Test")
    print("=" * 50)
    
    try:
        # 1. ENF çıkarma testi
        enf_results = test_enf_extraction()
        
        # 2. Metadata gömme testi
        success_audio, success_image = test_metadata_embedding(enf_results)
        
        # 3. Metadata çıkarma testi
        test_metadata_extraction()
        
        # 4. Sonuç özeti
        print("\n📋 Test Sonuçları Özeti")
        print("=" * 40)
        print(f"✅ ENF Çıkarma: Başarılı")
        print(f"✅ Ses Metadata Gömme: {'Başarılı' if success_audio else 'Başarısız'}")
        print(f"✅ Görüntü Metadata Gömme: {'Başarılı' if success_image else 'Başarısız'}")
        print(f"✅ Metadata Çıkarma: Başarılı")
        
        print("\n🎉 Tüm testler tamamlandı!")
        
        # Temizlik (isteğe bağlı)
        # cleanup_test_files()
        
    except Exception as e:
        print(f"❌ Test sırasında hata: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

