# pysearchlm

PDF akademik makalelerini analiz edip LaTeX formatında kapsamlı teknik özetler oluşturan LLM tabanlı kütüphane. Google Gemini API'sinin güçlü URL Context özelliği sayesinde PDF'leri doğrudan URL üzerinden işler.

## Özellikler

- 🧠 **Gemini 2.5-pro** API entegrasyonu 
- 📄 **URL Context** özelliği - PDF indirme gerektirmez
- 📝 **LaTeX formatında** kapsamlı özetler
- 🌍 **Çok dilli destek** (tr, en, fr, de, es, it, nl, pt, ru)
- 📚 **Akademik odaklı** promptlar
- 📊 **Tablo/formül** optimizasyonları

## Kurulum

Gerekli bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

API anahtarınızı çevre değişkeni olarak ayarlayın:

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Linux/macOS
export GEMINI_API_KEY="your-api-key-here"

# veya .env dosyası kullanın
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

## Temel Kullanım

```python
# En basit kullanım
from pysearchlm import PDFAnalyzer

url = "https://arxiv.org/pdf/1706.03762.pdf"
analyzer = PDFAnalyzer()
result = analyzer.analyze_pdf(url)

```

## Dil Seçenekleri

```python
# İngilizce özet
result_en = analyzer.analyze_pdf(url, language="en")

# Diğer diller
# tr, en, fr, de, es, it, nl, pt, ru desteklenir
result_fr = analyzer.analyze_pdf(url, language="fr")
```

## Toplu Analiz

```python
urls = [
    "https://arxiv.org/pdf/1706.03762.pdf",
    "https://arxiv.org/pdf/1810.04805.pdf"
]

results = analyzer.analyze_multiple_pdfs(urls, language="tr")
```

## Proje Yapısı

```
pysearchlm/
│
├── core/
│   ├── llm_client.py     # Gemini API entegrasyonu 
│   ├── pdf_processor.py  # URL doğrulama ve hazırlama
│   └── latex_generator.py # LaTeX çıktı oluşturma
│
├── utils/
│   ├── config.py         # Konfigürasyon ayarları
│   └── helpers.py        # Yardımcı fonksiyonlar
│
├── examples/             # Örnek kullanımlar
├── pysearchlm.py         # Ana API sınıfı 
└── __init__.py           # Paket konfigürasyonu
```

## Çıktı Örnekleri

LaTeX dosyaları `output/` klasörüne kaydedilir:

```
output/
└── Attention_Is_All_You_Need_tr_20250812_180145.tex
```

## Notlar

- PDF dosyaları indirilmez, Gemini doğrudan URL'den içeriği analiz eder
- LaTeX çıktılarında tablo, formül, algoritma gibi özel öğeler için optimizasyon sağlanır
- Token limitlerini dikkate alın (Gemini API sınırlamaları)

## Lisans


Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
