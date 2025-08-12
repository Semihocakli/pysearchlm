"""
PySearch - PDF Akademik Makale Analiz Kütüphanesi

Gemini-2.5-pro URL Context özelliği ile PDF'leri analiz eder ve
LaTeX formatında akademik özetler oluşturur.

Kullanım:
    from pysearch import PDFAnalyzer
    
    analyzer = PDFAnalyzer()
    result = analyzer.method(url, api_key="your_key", language="tr")

Veya:
    from pysearch import analyze_pdf
    
    result = analyze_pdf(url, api_key="your_key", language="tr")
"""

from .pysearchlm import PDFAnalyzer, PDFSummarizer, analyze_pdf
from .utils.config import Config

__version__ = "1.0.1"
__author__ = "Semih Ocakli"
__email__ = "semihocakli35@gmail.com"

# Ana export'lar
__all__ = [
    "PDFAnalyzer",
    "PDFSummarizer", 
    "analyze_pdf",
    "Config"
]

# Kütüphane bilgileri
__description__ = "LLM tabanlı PDF akademik makale analiz ve LaTeX özet oluşturma kütüphanesi"
__license__ = "MIT"
__url__ = "https://github.com/semihocakli/pysearchlm"

# Desteklenen diller
SUPPORTED_LANGUAGES = Config.SUPPORTED_LANGUAGES

# Hızlı kullanım için yardımcı fonksiyonlar
def get_supported_languages():
    """Desteklenen dilleri döndür"""
    return SUPPORTED_LANGUAGES.copy()

def check_requirements():
    """Sistem gereksinimlerini kontrol et"""
    try:
        import google.generativeai
        import requests
        return True
    except ImportError as e:
        print(f"Eksik paket: {e}")
        return False

# Başlatma mesajı
print("PySearchLM v1.0.1 - PDF Akademik Makale Analiz Kütüphanesi")
print("Gemini-2.5-pro ile güçlendirilmiştir.")
