"""
PySearch - PDF Akademik Makale Analiz Kütüphanesi
Ana API sınıfı ve kullanıcı arayüzü
"""
from typing import Dict, Any, Optional
import os
from core.pdf_processor import PDFURLHandler
from core.llm_client import GeminiClient
from core.latex_generator import LaTeXGenerator
from utils.config import Config


class PDFAnalyzer:
    """
    PDF akademik makale analiz ve özet oluşturma sınıfı
    
    Gemini-2.5-pro URL Context özelliği ile PDF analizi yapar
    """
    
    def __init__(self, api_key: Optional[str] = None, output_dir: str = "output"):
        """
        PDF Analyzer'ı başlat
        
        Args:
            api_key: Gemini API anahtarı
            output_dir: Çıktı dosyaları klasörü
        """
        # Modülleri başlat
        self.url_handler = PDFURLHandler()
        self.llm_client = GeminiClient(api_key)
        self.latex_generator = LaTeXGenerator(output_dir)
        
        # API bağlantısını test et
        if not self.llm_client.test_api_connection():
            raise Exception("Gemini API bağlantısı başarısız! API anahtarını kontrol edin.")
        
    
    def analyze_pdf(self, url: str, api_key: Optional[str] = None, language: str = "tr") -> Dict[str, Any]:
        """
        Ana işlem metodu - PDF URL'sini analiz et ve LaTeX özet oluştur
        
        Args:
            url: PDF dosyasının URL'si
            api_key: Gemini API anahtarı (opsiyonel)
            language: Hedef dil ("tr" veya "en")
            
        Returns:
            İşlem sonucu bilgileri
        """
        try:
            # Bilgi amaçlı kısa günlükler (emoji yok)
            print("PDF analizi başlıyor...")
            print(f"URL: {url}")
            print(f"Dil: {Config.get_language_name(language)}")
            
            # 1. URL'yi doğrula ve hazırla
            print("URL doğrulanıyor...")
            url_info = self.url_handler.prepare_url_for_gemini(url)
            print(f"URL doğrulandı: {url_info['content_type']}")
            
            if url_info.get('size_mb'):
                print(f"Dosya boyutu: {url_info['size_mb']} MB")
            
            # 2. API anahtarını güncelle (gerekirse)
            if api_key:
                self.llm_client = GeminiClient(api_key)
            
            # 3. Gemini ile PDF'i analiz et
            print("Gemini ile PDF analizi...")
            analysis_result = self.llm_client.analyze_pdf_from_url(url, language)
            
            if not analysis_result['success']:
                raise Exception(f"PDF analizi başarısız: {analysis_result['error']}")
            
            print(f"Analiz tamamlandı (token: {analysis_result['token_count']})")
            
            # 4. LaTeX dosyasını oluştur
            print("LaTeX dosyası oluşturuluyor...")
            latex_result = self.latex_generator.save_latex_file(
                analysis_result['latex_summary'],
                analysis_result
            )
            
            if not latex_result['success']:
                raise Exception(f"LaTeX dosyası oluşturulamadı: {latex_result['error']}")
            
            print(f"LaTeX dosyası kaydedildi: {latex_result['filename']}")
            
            # 5. Sonuç bilgilerini birleştir
            final_result = {
                'success': True,
                'source_url': url,
                'language': language,
                'model_used': analysis_result['model_used'],
                'latex_file': {
                    'path': latex_result['file_path'],
                    'filename': latex_result['filename'],
                    'title': latex_result.get('title'),
                    'size_bytes': latex_result['size_bytes']
                },
                'analysis_stats': {
                    'token_count': analysis_result['token_count'],
                    'line_count': latex_result['line_count']
                },
                'url_info': url_info,
                'created_at': latex_result['created_at']
            }
            
            print("İşlem başarıyla tamamlandı.")
            print(f"Dosya: {latex_result['file_path']}")
            
            return final_result
            
        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e),
                'source_url': url,
                'language': language
            }
            
            print(f"Hata: {str(e)}")
            return error_result
    
    def analyze_multiple_pdfs(self, 
                            urls: list, 
                            api_key: Optional[str] = None, 
                            language: str = "tr") -> Dict[str, Any]:
        """
        Birden fazla PDF'i analiz et
        
        Args:
            urls: PDF URL'leri listesi
            api_key: Gemini API anahtarı
            language: Hedef dil
            
        Returns:
            Toplu analiz sonuçları
        """
        results = {
            'total_pdfs': len(urls),
            'successful': 0,
            'failed': 0,
            'results': [],
            'errors': []
        }
        
        print(f"Toplu PDF analizi başlıyor: {len(urls)} dosya")
        
        for i, url in enumerate(urls, 1):
            print(f"PDF {i}/{len(urls)}")
            
            try:
                result = self.analyze_pdf(url, api_key, language)
                results['results'].append(result)
                
                if result['success']:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append({
                        'url': url,
                        'error': result.get('error', 'Bilinmeyen hata')
                    })
                    
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({
                    'url': url,
                    'error': str(e)
                })
                print(f"PDF {i} analizi başarısız: {str(e)}")
        
        print("Toplu analiz tamamlandı:")
        print(f"Başarılı: {results['successful']}")
        print(f"Başarısız: {results['failed']}")
        
        return results
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Desteklenen diller listesi"""
        return Config.SUPPORTED_LANGUAGES.copy()
    
    def validate_url(self, url: str) -> Dict[str, Any]:
        """URL doğrulama (test için)"""
        return self.url_handler.validate_pdf_url(url)


# Kullanım kolaylığı için alias
class PDFSummarizer(PDFAnalyzer):
    """PDFAnalyzer için alternatif isim"""
    pass


# Geriye uyumluluk için fonksiyon arayüzü
def analyze_pdf(url: str, api_key: Optional[str] = None, language: str = "tr") -> Dict[str, Any]:
    """
    Tek PDF analizi için fonksiyon arayüzü
    
    Args:
        url: PDF URL'si
        api_key: Gemini API anahtarı
        language: Hedef dil
        
    Returns:
        Analiz sonucu
    """
    analyzer = PDFAnalyzer(api_key)
    return analyzer.analyze_pdf(url, api_key, language)
