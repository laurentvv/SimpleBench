# Bench AI with Ollama/LMStudio

<div align="center">

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Bench AI Logo](https://img.shields.io/badge/Bench%20AI-LLM%20Benchmark%20Tool-blue)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

Bench AI एक हल्का और कुशल उपकरण है जो [Ollama](https://ollama.com/) और LMStudio के माध्यम से चलने वाले भाषा मॉडल (LLMs) के प्रदर्शन का मूल्यांकन करने के लिए है। यह शोधकर्ताओं और डेवलपर्स को मानकीकृत प्रोग्रामिंग और तर्क कार्यों पर विभिन्न मॉडलों की वस्तुनिष्ठ तुलना करने की अनुमति देता है।

## 🎯 हाल के परिणाम

- **मूल्यांकन सटीकता**: HumanEval पर 63% सही उत्तर का पता लगाया गया
- **मूल्यांकन विधियां**: 5 पूरक दृष्टिकोण (सामान्यीकरण, AST, AI)
- **पुनरुत्पादनीयता**: निष्पादन में सुसंगत परिणाम

## ✨ विशेषताएं

- 🚀 **उपयोग में आसान** - सहज कमांड लाइन इंटरफेस
- 🔄 **मल्टी-डेटासेट समर्थन** - HumanEval, CruxEval और Code-X-GLUE के साथ संगत
- 📊 **उन्नत मूल्यांकन** - फॉर्मेटिंग, इंडेंटेशन और कार्यात्मक समानता के अंतर को सहन करता है
- 📈 **विस्तृत विश्लेषण** - प्रदर्शन विश्लेषण स्क्रिप्ट शामिल
- 🧩 **विस्तार योग्य** - विभिन्न प्रकार के बेंचमार्क के लिए अनुकूलित करना आसान

## 🛠️ आवश्यकताएं

- Python 3.13.5 या उच्चतर
- [Ollama](https://ollama.com/) स्थापित और चल रहा हो

## 📦 स्थापना

1. रिपॉजिटरी क्लोन करें:
   ```bash
   git clone https://github.com/laurentvv/bench-ai-ollama-lmstudio.git
   cd bench-ai-ollama-lmstudio
   ```

2. वर्चुअल एनवायरनमेंट बनाएं और निर्भरताएं स्थापित करें:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows पर: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🚀 बेंचमार्क चलाना

1. सुनिश्चित करें कि Ollama चल रहा है।

2. जिस मॉडल का आप परीक्षण करना चाहते हैं उसे डाउनलोड करें:
   ```bash
   ollama pull qwen3:14b
   ```

3. अपनी पसंद के डेटासेट के साथ बेंचमार्क चलाएं:
   ```bash
   # HumanEval के लिए
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-openai-openai-humaneval.json
   ```

## 📊 Weave के साथ ट्रैकिंग

Bench AI [Weave](https://wandb.ai/site/weave) के साथ एकीकृत है, जो आपके प्रयोगों को ट्रैक करने और विज़ुअलाइज़ करने के लिए एक शक्तिशाली उपकरण है।

## 🧩 समर्थित डेटासेट

यह रिपॉजिटरी में **3 डेटासेट फाइलें** हैं जिनमें **प्रत्येक में 30 प्रश्न** हैं:

- **`sql-console-for-openai-openai-humaneval.json`** - HumanEval (30 प्रश्न)
- **`sql-console-for-cruxeval-org-cruxeval.json`** - CruxEval (30 प्रश्न)
- **`sql-console-for-google-code-x-glue-ct-code-to-text.json`** - Code-X-GLUE (30 प्रश्न)

## 💯 उन्नत मूल्यांकन

Bench AI एक उन्नत मूल्यांकन दृष्टिकोण का उपयोग करता है जो सही उत्तरों का पता लगाने के लिए कई विधियों को जोड़ता है:

1. **बुनियादी सामान्यीकरण**: टैग हटाता है और स्थानों को सामान्य बनाता है
2. **उन्नत सामान्यीकरण**: इंडेंटेशन और लाइन ब्रेक को बुद्धिमानी से संभालता है
3. **चरम सामान्यीकरण**: सभी स्थान और लाइन ब्रेक हटाता है
4. **AST तुलना**: कोड की वाक्यविन्यास संरचना का विश्लेषण करता है
5. **AI मूल्यांकन**: कार्यात्मक समानता का पता लगाने के लिए भाषा मॉडल का उपयोग करता है

## 🤝 योगदान

योगदान का स्वागत है! कृपया एक issue खोलने या pull request भेजने में संकोच न करें।

## 📄 लाइसेंस

यह प्रोजेक्ट MIT लाइसेंस के तहत लाइसेंस प्राप्त है। विवरण के लिए [LICENSE](LICENSE) फाइल देखें।