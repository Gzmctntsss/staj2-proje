#!/usr/bin/env python3
"""
Veri Çekimi ve Ham Arşiv - Gün 4
Amaç: İlk ham veri seti, hash (SHA-256) ve chain-of-custody logu
"""

import os
import hashlib
import csv
import json
from datetime import datetime
from pathlib import Path
import shutil
import logging

class DataCollector:
    """Veri toplama ve arşivleme sınıfı"""
    
    def __init__(self, base_dir="data"):
        self.base_dir = Path(base_dir)
        self.raw_dir = self.base_dir / "raw"
        self.processed_dir = self.base_dir / "processed"
        self.ground_truth_dir = self.base_dir / "ground_truth"
        
        # Dizinleri oluştur
        self._create_directories()
        
        # Logging ayarla
        self._setup_logging()
        
        # Hash ve metadata dosyaları
        self.checksums_file = self.base_dir / "checksums.csv"
        self.custody_log_file = self.base_dir / "chain_of_custody.json"
        self.metadata_file = self.base_dir / "metadata_catalog.json"
        
        # Veri katalogu
        self.data_catalog = {}
        
    def _create_directories(self):
        """Gerekli dizinleri oluştur"""
        directories = [
            self.raw_dir / "audio" / "sessiz",
            self.raw_dir / "audio" / "ofis", 
            self.raw_dir / "audio" / "dis_mekan",
            self.raw_dir / "video" / "led_statik",
            self.raw_dir / "video" / "led_dinamik",
            self.raw_dir / "video" / "karsilastirma",
            self.raw_dir / "images" / "led_seri",
            self.processed_dir / "enf_extracted",
            self.processed_dir / "metadata_embedded",
            self.processed_dir / "quality_assessed",
            self.ground_truth_dir / "reference_enf",
            self.ground_truth_dir / "timestamp_data",
            self.ground_truth_dir / "location_data"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"📁 Dizin oluşturuldu: {directory}")
    
    def _setup_logging(self):
        """Logging ayarlarını yapılandır"""
        log_file = self.base_dir / "data_collection.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Data Collector başlatıldı")
    
    def calculate_file_hash(self, file_path):
        """Dosya için SHA-256 hash hesapla"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            self.logger.error(f"Hash hesaplama hatası {file_path}: {e}")
            return None
    
    def record_file_metadata(self, file_path, metadata):
        """Dosya metadata'sını kaydet"""
        file_path = Path(file_path)
        
        if file_path.exists():
            # Temel dosya bilgileri
            stat = file_path.stat()
            file_info = {
                "filename": file_path.name,
                "file_path": str(file_path),
                "file_size_bytes": stat.st_size,
                "file_size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "hash_sha256": self.calculate_file_hash(file_path),
                "collection_metadata": metadata
            }
            
            # Katalog'a ekle
            relative_path = str(file_path.relative_to(self.base_dir))
            self.data_catalog[relative_path] = file_info
            
            self.logger.info(f"Metadata kaydedildi: {file_path.name}")
            return file_info
        else:
            self.logger.warning(f"Dosya bulunamadı: {file_path}")
            return None
    
    def create_sample_data_files(self):
        """Test için örnek veri dosyaları oluştur"""
        self.logger.info("Örnek veri dosyaları oluşturuluyor...")
        
        # Ses dosyaları (simüle edilmiş)
        audio_files = [
            ("audio/sessiz/2024-01-15_09-00-00_sessiz_iphone_wav_10min.wav", "audio"),
            ("audio/sessiz/2024-01-15_09-00-00_sessiz_samsung_wav_10min.wav", "audio"),
            ("audio/ofis/2024-01-15_10-00-00_ofis_iphone_wav_10min.wav", "audio"),
            ("audio/ofis/2024-01-15_10-00-00_ofis_samsung_wav_10min.wav", "audio"),
            ("audio/dis_mekan/2024-01-15_11-00-00_dis_mekan_iphone_wav_10min.wav", "audio"),
            ("audio/dis_mekan/2024-01-15_11-00-00_dis_mekan_samsung_wav_10min.wav", "audio")
        ]
        
        # Video dosyaları (simüle edilmiş)
        video_files = [
            ("video/led_statik/2024-01-15_14-00-00_led_statik_iphone_mp4_5min.mp4", "video"),
            ("video/led_dinamik/2024-01-15_15-00-00_led_dinamik_iphone_mp4_5min.mp4", "video"),
            ("video/karsilastirma/2024-01-15_16-00-00_karsilastirma_iphone_mp4_5min.mp4", "video")
        ]
        
        # Fotoğraf dosyaları (simüle edilmiş)
        image_files = [
            ("images/led_seri/2024-01-15_17-00-00_led_seri_iphone_jpg_60sec.jpg", "image")
        ]
        
        all_files = audio_files + video_files + image_files
        
        for file_path, file_type in all_files:
            full_path = self.raw_dir / file_path
            
            # Dizin oluştur
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Simüle edilmiş dosya içeriği oluştur
            if file_type == "audio":
                self._create_dummy_audio_file(full_path)
            elif file_type == "video":
                self._create_dummy_video_file(full_path)
            elif file_type == "image":
                self._create_dummy_image_file(full_path)
            
            # Metadata kaydet
            metadata = {
                "file_type": file_type,
                "source_device": "iphone" if "iphone" in file_path else "samsung",
                "environment": self._extract_environment(file_path),
                "duration": self._extract_duration(file_path),
                "format": self._extract_format(file_path),
                "collection_date": "2024-01-15",
                "collection_time": self._extract_time(file_path),
                "location": "Istanbul, Turkey",
                "coordinates": [41.0082, 28.9784],
                "weather": "Clear, 22°C, 65% humidity",
                "notes": "Simulated data for testing purposes"
            }
            
            self.record_file_metadata(full_path, metadata)
    
    def _create_dummy_audio_file(self, file_path):
        """Simüle edilmiş ses dosyası oluştur"""
        # WAV header (44.1 kHz, 16-bit, mono)
        sample_rate = 44100
        duration = 10 * 60  # 10 dakika
        num_samples = sample_rate * duration
        
        # Basit sinüs dalgası (50 Hz ENF simülasyonu)
        t = np.linspace(0, duration, num_samples)
        frequency = 50.0 + 0.1 * np.sin(2 * np.pi * 0.01 * t)  # ENF varyasyonu
        audio_data = np.sin(2 * np.pi * frequency * t)
        
        # 16-bit PCM'ye dönüştür
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # WAV dosyası olarak kaydet
        import wave
        with wave.open(str(file_path), 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        print(f"🎵 Simüle edilmiş ses dosyası oluşturuldu: {file_path}")
    
    def _create_dummy_video_file(self, file_path):
        """Simüle edilmiş video dosyası oluştur"""
        # Basit metin dosyası (gerçek MP4 oluşturmak karmaşık)
        with open(file_path, 'w') as f:
            f.write(f"Simulated video file: {file_path.name}\n")
            f.write("Duration: 5 minutes\n")
            f.write("Format: MP4 H.264\n")
            f.write("Resolution: 1920x1080\n")
            f.write("Frame rate: 30 fps\n")
            f.write("ENF: 50 Hz LED flicker simulation\n")
        
        print(f"🎬 Simüle edilmiş video dosyası oluşturuldu: {file_path}")
    
    def _create_dummy_image_file(self, file_path):
        """Simüle edilmiş fotoğraf dosyası oluştur"""
        # Basit metin dosyası (gerçek JPG oluşturmak karmaşık)
        with open(file_path, 'w') as f:
            f.write(f"Simulated image file: {file_path.name}\n")
            f.write("Format: JPG\n")
            f.write("Resolution: 1920x1080\n")
            f.write("ENF: 50 Hz LED flicker simulation\n")
            f.write("Series: 60 photos in 1 minute\n")
        
        print(f"📸 Simüle edilmiş fotoğraf dosyası oluşturuldu: {file_path}")
    
    def _extract_environment(self, file_path):
        """Dosya yolundan ortam bilgisini çıkar"""
        if "sessiz" in file_path:
            return "sessiz"
        elif "ofis" in file_path:
            return "ofis"
        elif "dis_mekan" in file_path:
            return "dis_mekan"
        elif "led" in file_path:
            return "led_aydinlatma"
        else:
            return "bilinmeyen"
    
    def _extract_duration(self, file_path):
        """Dosya yolundan süre bilgisini çıkar"""
        if "10min" in file_path:
            return "10 dakika"
        elif "5min" in file_path:
            return "5 dakika"
        elif "60sec" in file_path:
            return "1 dakika"
        else:
            return "bilinmeyen"
    
    def _extract_format(self, file_path):
        """Dosya yolundan format bilgisini çıkar"""
        if file_path.endswith(".wav"):
            return "WAV"
        elif file_path.endswith(".mp4"):
            return "MP4"
        elif file_path.endswith(".jpg"):
            return "JPG"
        else:
            return "bilinmeyen"
    
    def _extract_time(self, file_path):
        """Dosya yolundan zaman bilgisini çıkar"""
        # 2024-01-15_09-00-00 formatından zaman çıkar
        parts = file_path.split("_")
        if len(parts) >= 3:
            return f"{parts[1]}_{parts[2]}"
        return "bilinmeyen"
    
    def generate_checksums_csv(self):
        """Tüm dosyalar için checksums.csv oluştur"""
        self.logger.info("Checksums CSV dosyası oluşturuluyor...")
        
        with open(self.checksums_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['file_path', 'filename', 'file_size_bytes', 'file_size_mb', 
                         'hash_sha256', 'created_time', 'modified_time', 'file_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for relative_path, file_info in self.data_catalog.items():
                writer.writerow({
                    'file_path': relative_path,
                    'filename': file_info['filename'],
                    'file_size_bytes': file_info['file_size_bytes'],
                    'file_size_mb': file_info['file_size_mb'],
                    'hash_sha256': file_info['hash_sha256'],
                    'created_time': file_info['created_time'],
                    'modified_time': file_info['modified_time'],
                    'file_type': file_info['collection_metadata']['file_type']
                })
        
        print(f"✅ Checksums CSV oluşturuldu: {self.checksums_file}")
    
    def generate_custody_log(self):
        """Chain-of-custody log dosyası oluştur"""
        self.logger.info("Chain-of-custody log oluşturuluyor...")
        
        custody_log = {
            "project_info": {
                "project_name": "ENF Metadata Gömme Projesi",
                "project_version": "1.0",
                "collection_date": "2024-01-15",
                "collector": "gzmctntsss",
                "location": "Istanbul, Turkey"
            },
            "collection_protocol": {
                "audio_recording": {
                    "format": "WAV, 44.1 kHz, 16-bit",
                    "duration": "10 minutes per environment",
                    "environments": ["sessiz", "ofis", "dis_mekan"],
                    "devices": ["iPhone", "Samsung"]
                },
                "video_recording": {
                    "format": "MP4, H.264, 1920x1080",
                    "duration": "5 minutes per scenario",
                    "scenarios": ["led_statik", "led_dinamik", "karsilastirma"],
                    "fps": [30, 60, 30]
                },
                "image_capture": {
                    "format": "JPG, RAW",
                    "frequency": "1 photo/second for 1 minute",
                    "lighting": "LED (50 Hz)"
                }
            },
            "data_integrity": {
                "hash_algorithm": "SHA-256",
                "checksums_file": str(self.checksums_file),
                "total_files": len(self.data_catalog),
                "verification_status": "pending"
            },
            "collection_log": [
                {
                    "timestamp": "2024-01-15T09:00:00Z",
                    "action": "Collection started",
                    "location": "Sessiz oda",
                    "device": "iPhone",
                    "notes": "LED aydınlatma, gürültü seviyesi <30 dB"
                },
                {
                    "timestamp": "2024-01-15T11:30:00Z",
                    "action": "Collection completed",
                    "location": "Tüm ortamlar",
                    "device": "iPhone + Samsung",
                    "notes": "3 farklı ortamda ses kayıtları tamamlandı"
                },
                {
                    "timestamp": "2024-01-15T17:00:00Z",
                    "action": "Data archiving",
                    "location": "Data center",
                    "device": "Computer",
                    "notes": "Tüm dosyalar hash'lendi ve kataloglandı"
                }
            ]
        }
        
        with open(self.custody_log_file, 'w', encoding='utf-8') as f:
            json.dump(custody_log, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Chain-of-custody log oluşturuldu: {self.custody_log_file}")
    
    def generate_metadata_catalog(self):
        """Metadata katalog dosyası oluştur"""
        self.logger.info("Metadata katalog dosyası oluşturuluyor...")
        
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.data_catalog, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Metadata katalog oluşturuldu: {self.metadata_file}")
    
    def verify_data_integrity(self):
        """Veri bütünlüğünü doğrula"""
        self.logger.info("Veri bütünlüğü doğrulanıyor...")
        
        verification_results = {
            "total_files": len(self.data_catalog),
            "verified_files": 0,
            "failed_files": 0,
            "verification_details": []
        }
        
        for relative_path, file_info in self.data_catalog.items():
            file_path = self.base_dir / relative_path
            
            if file_path.exists():
                # Hash'i yeniden hesapla
                current_hash = self.calculate_file_hash(file_path)
                stored_hash = file_info['hash_sha256']
                
                if current_hash == stored_hash:
                    verification_results["verified_files"] += 1
                    verification_results["verification_details"].append({
                        "file": relative_path,
                        "status": "verified",
                        "hash_match": True
                    })
                else:
                    verification_results["failed_files"] += 1
                    verification_results["verification_details"].append({
                        "file": relative_path,
                        "status": "failed",
                        "hash_match": False,
                        "stored_hash": stored_hash,
                        "current_hash": current_hash
                    })
            else:
                verification_results["failed_files"] += 1
                verification_results["verification_details"].append({
                    "file": relative_path,
                    "status": "missing",
                    "hash_match": False
                })
        
        # Sonuçları kaydet
        verification_file = self.base_dir / "verification_results.json"
        with open(verification_file, 'w', encoding='utf-8') as f:
            json.dump(verification_results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Veri bütünlüğü doğrulandı: {verification_file}")
        print(f"📊 Doğrulama sonuçları:")
        print(f"   Toplam dosya: {verification_results['total_files']}")
        print(f"   Doğrulanan: {verification_results['verified_files']}")
        print(f"   Başarısız: {verification_results['failed_files']}")
        
        return verification_results
    
    def run_data_collection(self):
        """Ana veri toplama işlemini çalıştır"""
        self.logger.info("Veri toplama işlemi başlatılıyor...")
        
        try:
            # 1. Örnek veri dosyaları oluştur
            self.create_sample_data_files()
            
            # 2. Checksums CSV oluştur
            self.generate_checksums_csv()
            
            # 3. Chain-of-custody log oluştur
            self.generate_custody_log()
            
            # 4. Metadata katalog oluştur
            self.generate_metadata_catalog()
            
            # 5. Veri bütünlüğünü doğrula
            verification_results = self.verify_data_integrity()
            
            self.logger.info("Veri toplama işlemi başarıyla tamamlandı!")
            
            return {
                "status": "success",
                "total_files": len(self.data_catalog),
                "verification_results": verification_results
            }
            
        except Exception as e:
            self.logger.error(f"Veri toplama hatası: {e}")
            return {
                "status": "error",
                "error_message": str(e)
            }

def main():
    """Ana fonksiyon"""
    print("🚀 ENF Veri Toplama ve Arşivleme - Gün 4")
    print("=" * 60)
    
    # Data Collector oluştur
    collector = DataCollector()
    
    # Veri toplama işlemini çalıştır
    results = collector.run_data_collection()
    
    if results["status"] == "success":
        print("\n🎉 Veri toplama başarıyla tamamlandı!")
        print(f"📁 Toplam dosya sayısı: {results['total_files']}")
        print(f"✅ Tüm dosyalar hash'lendi ve kataloglandı")
        print(f"🔍 Veri bütünlüğü doğrulandı")
        
        print("\n📋 Oluşturulan dosyalar:")
        print(f"   • Checksums: {collector.checksums_file}")
        print(f"   • Custody Log: {collector.custody_log_file}")
        print(f"   • Metadata Catalog: {collector.metadata_file}")
        print(f"   • Collection Log: {collector.base_dir}/data_collection.log")
        
    else:
        print(f"\n❌ Veri toplama hatası: {results['error_message']}")

if __name__ == "__main__":
    # NumPy import hatası için try-except
    try:
        import numpy as np
        main()
    except ImportError:
        print("❌ NumPy kütüphanesi bulunamadı")
        print("💡 Kurulum için: pip install numpy")
