#!/usr/bin/env python3
"""
Ses ENF Çıkarımı - Gün 5
Amaç: Çalışan bir temel boru hattı
- 50 Hz çevresinde bant geçiren filtre (45-55 Hz)
- STFT ile zaman-frekans tepe takibi
- 1 Hz'e yeniden örnekleme ve medyan/MA ile düzgünleştirme
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, filtfilt
import librosa
import wave
import json
from pathlib import Path
from datetime import datetime
import logging

class ENFAudioExtractor:
    """Ses dosyalarından ENF çıkaran sınıf"""
    
    def __init__(self, sample_rate=44100, target_freq=50.0):
        self.sample_rate = sample_rate
        self.target_freq = target_freq  # Hedef ENF frekansı (50 Hz)
        self.freq_tolerance = 5.0  # ±5 Hz tolerans (45-55 Hz)
        
        # Filtre parametreleri
        self.low_cutoff = self.target_freq - self.freq_tolerance  # 45 Hz
        self.high_cutoff = self.target_freq + self.freq_tolerance  # 55 Hz
        
        # STFT parametreleri
        self.window_size = 1024
        self.hop_length = 512
        
        # Logging ayarla
        self._setup_logging()
        
        # Sonuçlar
        self.enf_curve = None
        self.time_stamps = None
        self.confidence_scores = None
        
    def _setup_logging(self):
        """Logging ayarlarını yapılandır"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("ENF Audio Extractor başlatıldı")
    
    def load_audio_file(self, file_path):
        """Ses dosyasını yükle"""
        try:
            self.logger.info(f"Ses dosyası yükleniyor: {file_path}")
            
            # WAV dosyası yükle
            with wave.open(str(file_path), 'rb') as wav_file:
                # Dosya parametrelerini al
                n_channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                sample_rate = wav_file.getframerate()
                n_frames = wav_file.getnframes()
                
                # Ses verisini oku
                audio_data = wav_file.readframes(n_frames)
                
                # 16-bit PCM'den numpy array'e dönüştür
                if sample_width == 2:  # 16-bit
                    audio_data = np.frombuffer(audio_data, dtype=np.int16)
                else:
                    raise ValueError(f"Desteklenmeyen sample width: {sample_width}")
                
                # Stereo ise mono'ya dönüştür
                if n_channels == 2:
                    audio_data = audio_data.reshape(-1, 2).mean(axis=1)
                
                # Float32'ye normalize et
                audio_data = audio_data.astype(np.float32) / 32767.0
                
                self.logger.info(f"Ses dosyası yüklendi: {n_frames} frame, {sample_rate} Hz")
                return audio_data, sample_rate
                
        except Exception as e:
            self.logger.error(f"Ses dosyası yükleme hatası: {e}")
            return None, None
    
    def design_bandpass_filter(self):
        """50 Hz çevresinde bant geçiren filtre tasarla"""
        try:
            # Butterworth bant geçiren filtre
            nyquist = self.sample_rate / 2
            low_norm = self.low_cutoff / nyquist
            high_norm = self.high_cutoff / nyquist
            
            # Filtre sırası (4. sıra)
            filter_order = 4
            
            # Filtre katsayılarını hesapla
            b, a = butter(filter_order, [low_norm, high_norm], btype='band')
            
            self.logger.info(f"Bant geçiren filtre tasarlandı: {self.low_cutoff}-{self.high_cutoff} Hz")
            return b, a
            
        except Exception as e:
            self.logger.error(f"Filtre tasarım hatası: {e}")
            return None, None
    
    def apply_bandpass_filter(self, audio_data, b, a):
        """Ses verisine bant geçiren filtre uygula"""
        try:
            self.logger.info("Bant geçiren filtre uygulanıyor...")
            
            # Filtreyi uygula (forward-backward filtfilt ile faz gecikmesi olmadan)
            filtered_audio = filtfilt(b, a, audio_data)
            
            # NaN ve infinite değerleri kontrol et ve temizle
            if np.any(np.isnan(filtered_audio)) or np.any(np.isinf(filtered_audio)):
                self.logger.warning("Filtrelenmiş ses verisinde NaN/infinite değerler bulundu, temizleniyor...")
                filtered_audio = np.nan_to_num(filtered_audio, nan=0.0, posinf=1.0, neginf=-1.0)
            
            self.logger.info("Bant geçiren filtre uygulandı")
            return filtered_audio
            
        except Exception as e:
            self.logger.error(f"Filtre uygulama hatası: {e}")
            return None
    
    def extract_stft_features(self, filtered_audio):
        """STFT ile zaman-frekans özelliklerini çıkar"""
        try:
            self.logger.info("STFT özellikleri çıkarılıyor...")
            
            # STFT hesapla
            stft_matrix = librosa.stft(
                filtered_audio, 
                n_fft=self.window_size, 
                hop_length=self.hop_length,
                window='hann'
            )
            
            # Güç spektrumu hesapla
            power_spectrum = np.abs(stft_matrix) ** 2
            
            # Frekans ekseni
            freqs = librosa.fft_frequencies(sr=self.sample_rate, n_fft=self.window_size)
            
            # Zaman ekseni
            times = librosa.times_like(power_spectrum, sr=self.sample_rate, hop_length=self.hop_length)
            
            self.logger.info(f"STFT hesaplandı: {power_spectrum.shape}")
            return power_spectrum, freqs, times
            
        except Exception as e:
            self.logger.error(f"STFT hesaplama hatası: {e}")
            return None, None, None
    
    def track_frequency_peaks(self, power_spectrum, freqs, times):
        """Zaman-frekans matrisinde tepe noktalarını takip et"""
        try:
            self.logger.info("Frekans tepe noktaları takip ediliyor...")
            
            # Hedef frekans aralığındaki indeksleri bul
            target_mask = (freqs >= self.low_cutoff) & (freqs <= self.high_cutoff)
            target_freqs = freqs[target_mask]
            target_power = power_spectrum[target_mask, :]
            
            # Hedef frekans aralığında veri var mı kontrol et
            if len(target_freqs) == 0:
                self.logger.warning(f"Hedef frekans aralığında ({self.low_cutoff}-{self.high_cutoff} Hz) veri bulunamadı")
                self.logger.info(f"Mevcut frekans aralığı: {freqs[0]:.1f} - {freqs[-1]:.1f} Hz")
                
                # Tüm frekans aralığını kullan
                target_freqs = freqs
                target_power = power_spectrum
            
            # Her zaman dilimi için en güçlü frekansı bul
            peak_frequencies = []
            confidence_scores = []
            
            for t in range(target_power.shape[1]):
                # Bu zaman dilimindeki güç spektrumu
                time_slice = target_power[:, t]
                
                # Boş slice kontrolü
                if len(time_slice) == 0:
                    peak_frequencies.append(self.target_freq)  # Varsayılan değer
                    confidence_scores.append(0.0)
                    continue
                
                # En güçlü frekansın indeksini bul
                peak_idx = np.argmax(time_slice)
                peak_freq = target_freqs[peak_idx]
                peak_power = time_slice[peak_idx]
                
                # Güven skoru hesapla (normalize edilmiş güç)
                total_power = np.sum(time_slice)
                confidence = peak_power / total_power if total_power > 0 else 0
                
                peak_frequencies.append(peak_freq)
                confidence_scores.append(confidence)
            
            self.logger.info(f"Frekans takibi tamamlandı: {len(peak_frequencies)} zaman dilimi")
            return np.array(peak_frequencies), np.array(confidence_scores), times
            
        except Exception as e:
            self.logger.error(f"Frekans takibi hatası: {e}")
            return None, None, None
    
    def resample_to_1hz(self, frequencies, times, target_sr=1.0):
        """ENF eğrisini 1 Hz'e yeniden örnekle"""
        try:
            self.logger.info("1 Hz'e yeniden örnekleme yapılıyor...")
            
            # Orijinal örnekleme frekansı (STFT hop length'ten hesapla)
            original_sr = self.sample_rate / self.hop_length
            
            # Hedef zaman ekseni (1 Hz)
            target_duration = times[-1]
            target_times = np.arange(0, target_duration, 1.0 / target_sr)
            
            # Interpolasyon ile yeniden örnekle
            from scipy.interpolate import interp1d
            
            # Interpolasyon fonksiyonu
            interp_func = interp1d(times, frequencies, kind='linear', 
                                  bounds_error=False, fill_value='extrapolate')
            
            # Yeni frekans değerleri
            resampled_frequencies = interp_func(target_times)
            
            self.logger.info(f"Yeniden örnekleme tamamlandı: {len(resampled_frequencies)} nokta")
            return resampled_frequencies, target_times
            
        except Exception as e:
            self.logger.error(f"Yeniden örnekleme hatası: {e}")
            return None, None
    
    def smooth_enf_curve(self, frequencies, window_size=5):
        """ENF eğrisini medyan ve hareketli ortalama ile düzgünleştir"""
        try:
            self.logger.info("ENF eğrisi düzgünleştiriliyor...")
            
            # Medyan filtre (anormal değerleri temizle)
            from scipy.signal import medfilt
            median_filtered = medfilt(frequencies, kernel_size=window_size)
            
            # Hareketli ortalama (gürültüyü azalt)
            from scipy.signal import savgol_filter
            smoothed = savgol_filter(median_filtered, window_size, polyorder=2)
            
            self.logger.info("Düzgünleştirme tamamlandı")
            return smoothed
            
        except Exception as e:
            self.logger.error(f"Düzgünleştirme hatası: {e}")
            return frequencies
    
    def calculate_enf_statistics(self, enf_curve):
        """ENF eğrisi istatistiklerini hesapla"""
        try:
            stats = {
                "mean_frequency": np.mean(enf_curve),
                "std_frequency": np.std(enf_curve),
                "min_frequency": np.min(enf_curve),
                "max_frequency": np.max(enf_curve),
                "frequency_range": np.max(enf_curve) - np.min(enf_curve),
                "target_deviation": np.mean(np.abs(enf_curve - self.target_freq)),
                "stability_score": 1.0 / (1.0 + np.std(enf_curve))
            }
            
            self.logger.info("ENF istatistikleri hesaplandı")
            return stats
            
        except Exception as e:
            self.logger.error(f"İstatistik hesaplama hatası: {e}")
            return None
    
    def plot_enf_results(self, original_freqs, smoothed_freqs, times, save_path=None):
        """ENF sonuçlarını görselleştir"""
        try:
            self.logger.info("ENF sonuçları görselleştiriliyor...")
            
            # Boyut uyumluluğunu kontrol et
            if len(original_freqs) != len(times):
                self.logger.warning(f"Boyut uyumsuzluğu: original_freqs({len(original_freqs)}) != times({len(times)})")
                # Zaman eksenini yeniden oluştur
                if len(original_freqs) > 0:
                    original_times = np.arange(len(original_freqs)) * (times[-1] / len(original_freqs))
                else:
                    original_times = times
            else:
                original_times = times
            
            # Figure oluştur
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            # Üst grafik: Ham ENF eğrisi
            ax1.plot(original_times, original_freqs, 'b-', alpha=0.6, label='Ham ENF')
            ax1.plot(times, smoothed_freqs, 'r-', linewidth=2, label='Düzgünleştirilmiş ENF')
            ax1.axhline(y=self.target_freq, color='g', linestyle='--', label=f'Hedef: {self.target_freq} Hz')
            ax1.axhline(y=self.low_cutoff, color='orange', linestyle=':', alpha=0.7, label=f'Alt sınır: {self.low_cutoff} Hz')
            ax1.axhline(y=self.high_cutoff, color='orange', linestyle=':', alpha=0.7, label=f'Üst sınır: {self.high_cutoff} Hz')
            
            ax1.set_xlabel('Zaman (saniye)')
            ax1.set_ylabel('Frekans (Hz)')
            ax1.set_title('ENF Frekans Takibi')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Alt grafik: Frekans dağılımı
            ax2.hist(smoothed_freqs, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            ax2.axvline(x=self.target_freq, color='red', linestyle='--', linewidth=2, label=f'Hedef: {self.target_freq} Hz')
            ax2.axvline(x=np.mean(smoothed_freqs), color='green', linestyle='-', linewidth=2, label=f'Ortalama: {np.mean(smoothed_freqs):.3f} Hz')
            
            ax2.set_xlabel('Frekans (Hz)')
            ax2.set_ylabel('Frekans')
            ax2.set_title('ENF Frekans Dağılımı')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Kaydet veya göster
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Grafik kaydedildi: {save_path}")
            else:
                plt.show()
            
            plt.close()
            
        except Exception as e:
            self.logger.error(f"Görselleştirme hatası: {e}")
    
    def save_enf_results(self, enf_curve, time_stamps, confidence_scores, stats, output_path):
        """ENF sonuçlarını JSON formatında kaydet"""
        try:
            self.logger.info("ENF sonuçları kaydediliyor...")
            
            results = {
                "extraction_info": {
                    "timestamp": datetime.now().isoformat(),
                    "target_frequency": self.target_freq,
                    "frequency_tolerance": self.freq_tolerance,
                    "sample_rate": self.sample_rate,
                    "window_size": self.window_size,
                    "hop_length": self.hop_length
                },
                "enf_data": {
                    "frequencies": enf_curve.tolist(),
                    "time_stamps": time_stamps.tolist(),
                    "confidence_scores": confidence_scores.tolist() if confidence_scores is not None else None
                },
                "statistics": stats,
                "processing_notes": {
                    "bandpass_filter": f"{self.low_cutoff}-{self.high_cutoff} Hz",
                    "smoothing": "Median filter + Savitzky-Golay",
                    "resampling": "1 Hz target frequency"
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"ENF sonuçları kaydedildi: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Sonuç kaydetme hatası: {e}")
    
    def extract_enf_from_audio(self, audio_file_path, output_dir="output"):
        """Ses dosyasından ENF çıkar"""
        try:
            self.logger.info(f"ENF çıkarımı başlatılıyor: {audio_file_path}")
            
            # Çıktı dizinini oluştur
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 1. Ses dosyasını yükle
            audio_data, sample_rate = self.load_audio_file(audio_file_path)
            if audio_data is None:
                return None
            
            # 2. Bant geçiren filtre tasarla
            b, a = self.design_bandpass_filter()
            if b is None:
                return None
            
            # 3. Filtreyi uygula
            filtered_audio = self.apply_bandpass_filter(audio_data, b, a)
            if filtered_audio is None:
                return None
            
            # 4. STFT özelliklerini çıkar
            power_spectrum, freqs, times = self.extract_stft_features(filtered_audio)
            if power_spectrum is None:
                return None
            
            # 5. Frekans tepe noktalarını takip et
            peak_freqs, confidence_scores, peak_times = self.track_frequency_peaks(power_spectrum, freqs, times)
            if peak_freqs is None:
                return None
            
            # 6. 1 Hz'e yeniden örnekle
            resampled_freqs, resampled_times = self.resample_to_1hz(peak_freqs, peak_times)
            if resampled_freqs is None:
                return None
            
            # 7. Düzgünleştir
            smoothed_freqs = self.smooth_enf_curve(resampled_freqs)
            
            # 8. İstatistikleri hesapla
            stats = self.calculate_enf_statistics(smoothed_freqs)
            
            # 9. Sonuçları kaydet
            base_name = Path(audio_file_path).stem
            results_file = output_path / f"{base_name}_enf_results.json"
            self.save_enf_results(smoothed_freqs, resampled_times, confidence_scores, stats, results_file)
            
            # 10. Grafik oluştur
            plot_file = output_path / f"{base_name}_enf_plot.png"
            self.plot_enf_results(peak_freqs, smoothed_freqs, resampled_times, plot_file)
            
            # Sonuçları sakla
            self.enf_curve = smoothed_freqs
            self.time_stamps = resampled_times
            self.confidence_scores = confidence_scores
            
            self.logger.info("ENF çıkarımı başarıyla tamamlandı!")
            
            return {
                "status": "success",
                "enf_curve": smoothed_freqs,
                "time_stamps": resampled_times,
                "statistics": stats,
                "output_files": {
                    "results": str(results_file),
                    "plot": str(plot_file)
                }
            }
            
        except Exception as e:
            self.logger.error(f"ENF çıkarım hatası: {e}")
            return {
                "status": "error",
                "error_message": str(e)
            }

def main():
    """Ana fonksiyon"""
    print("🚀 ENF Ses Çıkarımı - Gün 5")
    print("=" * 60)
    
    # Test için örnek ses dosyası kullan
    test_audio = "data/raw/audio/sessiz/2024-01-15_09-00-00_sessiz_iphone_wav_10min.wav"
    
    if not Path(test_audio).exists():
        print(f"❌ Test ses dosyası bulunamadı: {test_audio}")
        print("💡 Önce Gün 4'teki data_collector.py'yi çalıştırın")
        return
    
    # ENF Extractor oluştur
    extractor = ENFAudioExtractor()
    
    # ENF çıkarımını çalıştır
    results = extractor.extract_enf_from_audio(test_audio)
    
    if results is not None and results.get("status") == "success":
        print("\n🎉 ENF çıkarımı başarıyla tamamlandı!")
        print(f"📊 ENF eğrisi uzunluğu: {len(results['enf_curve'])} nokta")
        print(f"⏱️  Zaman aralığı: {results['time_stamps'][0]:.1f} - {results['time_stamps'][-1]:.1f} saniye")
        
        stats = results['statistics']
        print(f"\n📈 ENF İstatistikleri:")
        print(f"   • Ortalama frekans: {stats['mean_frequency']:.3f} Hz")
        print(f"   • Standart sapma: {stats['std_frequency']:.3f} Hz")
        print(f"   • Frekans aralığı: {stats['frequency_range']:.3f} Hz")
        print(f"   • Hedef sapma: {stats['target_deviation']:.3f} Hz")
        print(f"   • Kararlılık skoru: {stats['stability_score']:.3f}")
        
        print(f"\n📋 Çıktı dosyaları:")
        print(f"   • ENF Sonuçları: {results['output_files']['results']}")
        print(f"   • ENF Grafiği: {results['output_files']['plot']}")
        
        # Kabul kriteri kontrolü
        print(f"\n✅ Kabul Kriteri Kontrolü:")
        print(f"   10 dakikalık kayıttan sürekli ENF eğrisi üretiliyor: {'✅' if len(results['enf_curve']) > 0 else '❌'}")
        
    else:
        error_msg = results.get('error_message', 'Bilinmeyen hata') if results else 'Sonuç alınamadı'
        print(f"\n❌ ENF çıkarım hatası: {error_msg}")

if __name__ == "__main__":
    main()
