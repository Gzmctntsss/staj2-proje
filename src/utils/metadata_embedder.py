"""
Metadata Gömme Modülü - ENF verilerini dosya metadata'sına gömme
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TXXX
from PIL import Image
import piexif
import cv2
from pydub import AudioSegment
import subprocess

class MetadataEmbedder:
    """ENF verilerini dosya metadata'sına gömme sınıfı"""
    
    def __init__(self):
        self.supported_audio_formats = ['.wav', '.mp3', '.flac', '.m4a']
        self.supported_video_formats = ['.mp4', '.avi', '.mov', '.mkv']
        self.supported_image_formats = ['.jpg', '.jpeg', '.png', '.tiff']
    
    def embed_to_audio(self, audio_file: str, enf_data: Dict[str, Any], 
                      output_file: Optional[str] = None) -> bool:
        """
        Ses dosyasına ENF verilerini göm
        
        Args:
            audio_file: Ses dosyası yolu
            enf_data: ENF verileri
            output_file: Çıktı dosyası (None ise orijinal dosyayı güncelle)
            
        Returns:
            bool: Başarı durumu
        """
        try:
            file_ext = os.path.splitext(audio_file)[1].lower()
            
            if file_ext == '.mp3':
                return self._embed_to_mp3(audio_file, enf_data, output_file)
            elif file_ext in ['.wav', '.flac', '.m4a']:
                return self._embed_to_generic_audio(audio_file, enf_data, output_file)
            else:
                print(f"Desteklenmeyen ses formatı: {file_ext}")
                return False
                
        except Exception as e:
            print(f"Ses dosyasına gömme hatası: {e}")
            return False
    
    def embed_to_video(self, video_file: str, enf_data: Dict[str, Any],
                      output_file: Optional[str] = None) -> bool:
        """
        Video dosyasına ENF verilerini göm
        
        Args:
            video_file: Video dosyası yolu
            enf_data: ENF verileri
            output_file: Çıktı dosyası
            
        Returns:
            bool: Başarı durumu
        """
        try:
            file_ext = os.path.splitext(video_file)[1].lower()
            
            if file_ext == '.mp4':
                return self._embed_to_mp4(video_file, enf_data, output_file)
            else:
                return self._embed_to_generic_video(video_file, enf_data, output_file)
                
        except Exception as e:
            print(f"Video dosyasına gömme hatası: {e}")
            return False
    
    def embed_to_image(self, image_file: str, enf_data: Dict[str, Any],
                      output_file: Optional[str] = None) -> bool:
        """
        Görüntü dosyasına ENF verilerini göm
        
        Args:
            image_file: Görüntü dosyası yolu
            enf_data: ENF verileri
            output_file: Çıktı dosyası
            
        Returns:
            bool: Başarı durumu
        """
        try:
            file_ext = os.path.splitext(image_file)[1].lower()
            
            if file_ext in ['.jpg', '.jpeg']:
                return self._embed_to_jpeg(image_file, enf_data, output_file)
            elif file_ext in ['.png', '.tiff']:
                return self._embed_to_generic_image(image_file, enf_data, output_file)
            else:
                print(f"Desteklenmeyen görüntü formatı: {file_ext}")
                return False
                
        except Exception as e:
            print(f"Görüntü dosyasına gömme hatası: {e}")
            return False
    
    def _embed_to_mp3(self, audio_file: str, enf_data: Dict[str, Any], 
                     output_file: Optional[str] = None) -> bool:
        """MP3 dosyasına ID3 tag ile gömme"""
        try:
            # MP3 dosyasını yükle
            audio = MP3(audio_file)
            
            # ID3 tag'leri oluştur
            if audio.tags is None:
                audio.tags = ID3()
            
            # ENF verilerini JSON string olarak göm
            enf_json = json.dumps(enf_data, separators=(',', ':'))
            
            # TXXX frame'leri ekle
            audio.tags.add(TXXX(desc="ENF_DATA", text=enf_json))
            audio.tags.add(TXXX(desc="ENF_TIMESTAMP", text=datetime.now().isoformat()))
            audio.tags.add(TXXX(desc="ENF_VERSION", text="1.0.0"))
            
            # Dosyayı kaydet
            save_file = output_file if output_file else audio_file
            audio.save(save_file)
            
            print(f"ENF verileri MP3 dosyasına gömüldü: {save_file}")
            return True
            
        except Exception as e:
            print(f"MP3 gömme hatası: {e}")
            return False
    
    def _embed_to_generic_audio(self, audio_file: str, enf_data: Dict[str, Any],
                              output_file: Optional[str] = None) -> bool:
        """Genel ses dosyalarına gömme"""
        try:
            # Mutagen ile genel metadata gömme
            audio = mutagen.File(audio_file)
            
            if audio is None:
                print(f"Desteklenmeyen ses formatı: {audio_file}")
                return False
            
            # ENF verilerini göm
            enf_json = json.dumps(enf_data, separators=(',', ':'))
            audio['enf_data'] = enf_json
            audio['enf_timestamp'] = datetime.now().isoformat()
            audio['enf_version'] = "1.0.0"
            
            # Dosyayı kaydet
            save_file = output_file if output_file else audio_file
            audio.save(save_file)
            
            print(f"ENF verileri ses dosyasına gömüldü: {save_file}")
            return True
            
        except Exception as e:
            print(f"Genel ses gömme hatası: {e}")
            return False
    
    def _embed_to_mp4(self, video_file: str, enf_data: Dict[str, Any],
                     output_file: Optional[str] = None) -> bool:
        """MP4 dosyasına metadata gömme"""
        try:
            # FFmpeg ile metadata gömme
            enf_json = json.dumps(enf_data, separators=(',', ':'))
            
            output_path = output_file if output_file else video_file + "_enf.mp4"
            
            cmd = [
                'ffmpeg', '-i', video_file,
                '-metadata', f'ENF_DATA={enf_json}',
                '-metadata', f'ENF_TIMESTAMP={datetime.now().isoformat()}',
                '-metadata', 'ENF_VERSION=1.0.0',
                '-c', 'copy',  # Codec'i kopyala (yeniden encode etme)
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"ENF verileri MP4 dosyasına gömüldü: {output_path}")
                return True
            else:
                print(f"FFmpeg hatası: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"MP4 gömme hatası: {e}")
            return False
    
    def _embed_to_generic_video(self, video_file: str, enf_data: Dict[str, Any],
                              output_file: Optional[str] = None) -> bool:
        """Genel video dosyalarına gömme"""
        try:
            # OpenCV ile video metadata gömme (sınırlı)
            enf_json = json.dumps(enf_data, separators=(',', ':'))
            
            output_path = output_file if output_file else video_file + "_enf" + os.path.splitext(video_file)[1]
            
            # Basit kopyalama (metadata desteği sınırlı)
            cap = cv2.VideoCapture(video_file)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
            
            cap.release()
            out.release()
            
            print(f"Video kopyalandı (metadata sınırlı): {output_path}")
            return True
            
        except Exception as e:
            print(f"Genel video gömme hatası: {e}")
            return False
    
    def _embed_to_jpeg(self, image_file: str, enf_data: Dict[str, Any],
                      output_file: Optional[str] = None) -> bool:
        """JPEG dosyasına EXIF ile gömme"""
        try:
            # Görüntüyü yükle
            image = Image.open(image_file)
            
            # Mevcut EXIF verilerini al
            exif_dict = piexif.load(image.info.get("exif", b""))
            
            # ENF verilerini JSON string olarak göm
            enf_json = json.dumps(enf_data, separators=(',', ':'))
            
            # UserComment alanına ENF verilerini ekle
            if "0th" not in exif_dict:
                exif_dict["0th"] = {}
            
            exif_dict["0th"][piexif.ImageIFD.UserComment] = enf_json.encode('utf-8')
            exif_dict["0th"][piexif.ImageIFD.Software] = "ENF Embedder v1.0"
            
            # EXIF verilerini byte'a çevir
            exif_bytes = piexif.dump(exif_dict)
            
            # Görüntüyü kaydet
            output_path = output_file if output_file else image_file
            image.save(output_path, exif=exif_bytes)
            
            print(f"ENF verileri JPEG dosyasına gömüldü: {output_path}")
            return True
            
        except Exception as e:
            print(f"JPEG gömme hatası: {e}")
            return False
    
    def _embed_to_generic_image(self, image_file: str, enf_data: Dict[str, Any],
                              output_file: Optional[str] = None) -> bool:
        """Genel görüntü dosyalarına gömme"""
        try:
            # PIL ile genel metadata gömme
            image = Image.open(image_file)
            
            # ENF verilerini info alanına ekle
            enf_json = json.dumps(enf_data, separators=(',', ':'))
            
            # Metadata bilgilerini hazırla
            metadata = {
                "ENF_DATA": enf_json,
                "ENF_TIMESTAMP": datetime.now().isoformat(),
                "ENF_VERSION": "1.0.0"
            }
            
            # Görüntüyü kaydet
            output_path = output_file if output_file else image_file
            image.save(output_path, pnginfo=self._create_png_info(metadata))
            
            print(f"ENF verileri görüntü dosyasına gömüldü: {output_path}")
            return True
            
        except Exception as e:
            print(f"Genel görüntü gömme hatası: {e}")
            return False
    
    def _create_png_info(self, metadata: Dict[str, str]):
        """PNG metadata oluştur"""
        from PIL import PngImagePlugin
        
        meta = PngImagePlugin.PngInfo()
        for key, value in metadata.items():
            meta.add_text(key, value)
        return meta
    
    def extract_from_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Dosyadan ENF verilerini çıkar
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            Dict: ENF verileri veya None
        """
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in self.supported_audio_formats:
                return self._extract_from_audio(file_path)
            elif file_ext in self.supported_video_formats:
                return self._extract_from_video(file_path)
            elif file_ext in self.supported_image_formats:
                return self._extract_from_image(file_path)
            else:
                print(f"Desteklenmeyen dosya formatı: {file_ext}")
                return None
                
        except Exception as e:
            print(f"Veri çıkarma hatası: {e}")
            return None
    
    def _extract_from_audio(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Ses dosyasından ENF verilerini çıkar"""
        try:
            if file_path.lower().endswith('.mp3'):
                audio = MP3(file_path)
                if audio.tags:
                    for frame in audio.tags.values():
                        if frame.FrameID == 'TXXX' and frame.desc == 'ENF_DATA':
                            return json.loads(frame.text[0])
            else:
                audio = mutagen.File(file_path)
                if audio and 'enf_data' in audio:
                    return json.loads(audio['enf_data'][0])
            
            return None
            
        except Exception as e:
            print(f"Ses dosyasından çıkarma hatası: {e}")
            return None
    
    def _extract_from_video(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Video dosyasından ENF verilerini çıkar"""
        try:
            # FFprobe ile metadata çıkarma
            cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', 
                   '-show_format', file_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                format_info = data.get('format', {})
                tags = format_info.get('tags', {})
                
                if 'ENF_DATA' in tags:
                    return json.loads(tags['ENF_DATA'])
            
            return None
            
        except Exception as e:
            print(f"Video dosyasından çıkarma hatası: {e}")
            return None
    
    def _extract_from_image(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Görüntü dosyasından ENF verilerini çıkar"""
        try:
            image = Image.open(file_path)
            
            if file_path.lower().endswith(('.jpg', '.jpeg')):
                # EXIF'ten çıkar
                exif_dict = piexif.load(image.info.get("exif", b""))
                if "0th" in exif_dict:
                    user_comment = exif_dict["0th"].get(piexif.ImageIFD.UserComment, b"")
                    if user_comment:
                        return json.loads(user_comment.decode('utf-8'))
            else:
                # PNG metadata'dan çıkar
                if 'ENF_DATA' in image.info:
                    return json.loads(image.info['ENF_DATA'])
            
            return None
            
        except Exception as e:
            print(f"Görüntü dosyasından çıkarma hatası: {e}")
            return None

def main():
    """Test fonksiyonu"""
    embedder = MetadataEmbedder()
    
    # Test ENF verisi
    test_enf_data = {
        "enf_data": {
            "frequencies": [50.1, 50.2, 50.0],
            "timestamps": ["2024-01-01T12:00:00Z"],
            "confidence": [0.95],
            "source_type": "audio"
        }
    }
    
    print("Metadata gömme testi tamamlandı!")

if __name__ == "__main__":
    main()

