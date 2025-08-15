"""
ENF (Electric Network Frequency) Çıkarma Modülü
"""

import numpy as np
import librosa
import cv2
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional
import json
from datetime import datetime

class ENFExtractor:
    """ENF sinyali çıkarma sınıfı"""
    
    def __init__(self, target_freq: float = 50.0, tolerance: float = 0.1):
        """
        Args:
            target_freq: Hedef ENF frekansı (Hz)
            tolerance: Kabul edilebilir frekans toleransı (Hz)
        """
        self.target_freq = target_freq
        self.tolerance = tolerance
        self.freq_range = (target_freq - tolerance, target_freq + tolerance)
        
    def extract_from_audio(self, audio_file: str, 
                          window_size: int = 4096,
                          hop_size: int = 1024) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Ses dosyasından ENF sinyali çıkarma
        
        Args:
            audio_file: Ses dosyası yolu
            window_size: FFT pencere boyutu
            hop_size: Pencere atlama boyutu
            
        Returns:
            frequencies: ENF frekans değerleri
            timestamps: Zaman damgaları
            confidence: Güven skorları
        """
        # Ses dosyasını yükle
        y, sr = librosa.load(audio_file, sr=None)
        
        # STFT hesapla
        stft = librosa.stft(y, n_fft=window_size, hop_length=hop_size)
        
        # Spektrogram hesapla
        spectrogram = np.abs(stft) ** 2
        
        # ENF frekans bandını filtrele
        freq_bins = librosa.fft_frequencies(sr=sr, n_fft=window_size)
        enf_mask = (freq_bins >= self.freq_range[0]) & (freq_bins <= self.freq_range[1])
        
        # ENF frekanslarını çıkar
        enf_spectrogram = spectrogram[enf_mask, :]
        enf_freq_bins = freq_bins[enf_mask]
        
        # Her zaman dilimi için en güçlü frekansı bul
        frequencies = []
        confidence = []
        
        for i in range(enf_spectrogram.shape[1]):
            power_spectrum = enf_spectrogram[:, i]
            if len(power_spectrum) > 0 and np.sum(power_spectrum) > 0:
                max_idx = np.argmax(power_spectrum)
                freq = enf_freq_bins[max_idx]
                conf = power_spectrum[max_idx] / np.sum(power_spectrum)
                
                frequencies.append(freq)
                confidence.append(conf)
            else:
                # Varsayılan değerler
                frequencies.append(self.target_freq)
                confidence.append(0.0)
        
        # Zaman damgaları
        timestamps = librosa.times_like(np.array(frequencies), sr=sr, hop_length=hop_size)
        
        return np.array(frequencies), timestamps, np.array(confidence)
    
    def extract_from_video(self, video_file: str,
                          roi: Optional[Tuple[int, int, int, int]] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Video dosyasından ENF sinyali çıkarma (LED flicker analizi)
        
        Args:
            video_file: Video dosyası yolu
            roi: İlgi alanı (x, y, width, height)
            
        Returns:
            frequencies: ENF frekans değerleri
            timestamps: Zaman damgaları
            confidence: Güven skorları
        """
        cap = cv2.VideoCapture(video_file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        brightness_values = []
        timestamps = []
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # ROI uygula
            if roi:
                x, y, w, h = roi
                frame = frame[y:y+h, x:x+w]
            
            # Ortalama parlaklık hesapla
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            brightness_values.append(brightness)
            
            # Zaman damgası
            timestamp = frame_count / fps
            timestamps.append(timestamp)
            
            frame_count += 1
            
        cap.release()
        
        # Flicker analizi
        brightness_signal = np.array(brightness_values)
        timestamps = np.array(timestamps)
        
        # FFT analizi
        fft_result = fft(brightness_signal)
        freqs = fftfreq(len(brightness_signal), 1/fps)
        
        # ENF frekans bandını filtrele
        enf_mask = (freqs >= self.freq_range[0]) & (freqs <= self.freq_range[1])
        enf_freqs = freqs[enf_mask]
        enf_power = np.abs(fft_result[enf_mask])
        
        # En güçlü frekansı bul
        max_idx = np.argmax(enf_power)
        dominant_freq = enf_freqs[max_idx]
        confidence = enf_power[max_idx] / np.sum(enf_power)
        
        # Tüm zaman dilimleri için aynı frekansı kullan
        frequencies = np.full_like(timestamps, dominant_freq)
        confidences = np.full_like(timestamps, confidence)
        
        return frequencies, timestamps, confidences
    
    def save_enf_data(self, frequencies: np.ndarray, 
                     timestamps: np.ndarray, 
                     confidence: np.ndarray,
                     source_type: str,
                     output_file: str):
        """ENF verilerini JSON formatında kaydet"""
        
        enf_data = {
            "enf_data": {
                "frequencies": frequencies.tolist(),
                "timestamps": [datetime.fromtimestamp(ts).isoformat() for ts in timestamps],
                "confidence": confidence.tolist(),
                "source_type": source_type,
                "extraction_method": "STFT" if source_type == "audio" else "LED_Flicker",
                "sampling_rate": len(timestamps) / (timestamps[-1] - timestamps[0]) if len(timestamps) > 1 else 1
            },
            "metadata": {
                "embedding_timestamp": datetime.now().isoformat(),
                "software_version": "1.0.0",
                "algorithm_version": "1.0.0"
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(enf_data, f, indent=2)
    
    def plot_enf_analysis(self, frequencies: np.ndarray, 
                         timestamps: np.ndarray, 
                         confidence: np.ndarray,
                         output_file: str = None):
        """ENF analiz sonuçlarını görselleştir"""
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        # Frekans zaman serisi
        ax1.plot(timestamps, frequencies, 'b-', linewidth=1)
        ax1.axhline(y=self.target_freq, color='r', linestyle='--', alpha=0.7)
        ax1.set_ylabel('Frekans (Hz)')
        ax1.set_title('ENF Frekans Zaman Serisi')
        ax1.grid(True, alpha=0.3)
        
        # Güven skoru
        ax2.plot(timestamps, confidence, 'g-', linewidth=1)
        ax2.set_ylabel('Güven Skoru')
        ax2.set_title('ENF Güven Skoru')
        ax2.grid(True, alpha=0.3)
        
        # Frekans histogramı
        ax3.hist(frequencies, bins=50, alpha=0.7, color='orange')
        ax3.axvline(x=self.target_freq, color='r', linestyle='--', alpha=0.7)
        ax3.set_xlabel('Frekans (Hz)')
        ax3.set_ylabel('Frekans')
        ax3.set_title('ENF Frekans Dağılımı')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()

def main():
    """Test fonksiyonu"""
    extractor = ENFExtractor(target_freq=50.0, tolerance=0.1)
    
    # Test için örnek veri oluştur
    fs = 1000
    t = np.linspace(0, 10, fs * 10)
    enf_freq = 50 + 0.1 * np.sin(2 * np.pi * 0.1 * t)
    enf_signal = np.sin(2 * np.pi * enf_freq * t)
    
    # Test dosyası oluştur
    import soundfile as sf
    test_file = "test_audio.wav"
    sf.write(test_file, enf_signal, fs)
    
    # ENF çıkar
    frequencies, timestamps, confidence = extractor.extract_from_audio(test_file)
    
    # Sonuçları kaydet
    extractor.save_enf_data(frequencies, timestamps, confidence, "audio", "test_enf_data.json")
    extractor.plot_enf_analysis(frequencies, timestamps, confidence, "test_enf_analysis.png")
    
    print(f"ENF analizi tamamlandı!")
    print(f"Ortalama frekans: {np.mean(frequencies):.3f} Hz")
    print(f"Ortalama güven: {np.mean(confidence):.3f}")

if __name__ == "__main__":
    main()
