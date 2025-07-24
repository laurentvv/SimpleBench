# Bench AI with Ollama/LMStudio

<div align="center">

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Bench AI Logo](https://img.shields.io/badge/Bench%20AI-LLM%20Benchmark%20Tool-blue)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

Bench AI هي أداة خفيفة وفعالة لتقييم أداء نماذج اللغة (LLMs) التي تعمل عبر [Ollama](https://ollama.com/) و LMStudio. تتيح للباحثين والمطورين مقارنة النماذج المختلفة بشكل موضوعي في مهام البرمجة والاستدلال المعيارية.

## 🎯 النتائج الحديثة

- **دقة التقييم**: تم اكتشاف 63% من الإجابات الصحيحة على HumanEval
- **طرق التقييم**: 5 نهج متكاملة (التطبيع، AST، الذكاء الاصطناعي)
- **القابلية للتكرار**: نتائج متسقة عبر التنفيذات

## ✨ الميزات

- 🚀 **سهل الاستخدام** - واجهة سطر أوامر بديهية
- 🔄 **دعم متعدد مجموعات البيانات** - متوافق مع HumanEval و CruxEval و Code-X-GLUE
- 📊 **تقييم متقدم** - يتحمل اختلافات التنسيق والمسافة البادئة والتكافؤ الوظيفي
- 📈 **تحليل مفصل** - تتضمن نصوص تحليل الأداء
- 🧩 **قابل للتوسيع** - سهل التكيف مع أنواع مختلفة من المعايير

## 🛠️ المتطلبات المسبقة

- Python 3.13.5 أو أعلى
- [Ollama](https://ollama.com/) مثبت وقيد التشغيل

## 📦 التثبيت

1. استنسخ المستودع:
   ```bash
   git clone https://github.com/laurentvv/bench-ai-ollama-lmstudio.git
   cd bench-ai-ollama-lmstudio
   ```

2. أنشئ بيئة افتراضية وثبت التبعيات:
   ```bash
   python -m venv venv
   source venv/bin/activate  # على Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🚀 تشغيل المعيار

1. تأكد من أن Ollama يعمل.

2. قم بتنزيل النموذج الذي تريد اختباره:
   ```bash
   ollama pull qwen3:14b
   ```

3. قم بتشغيل المعيار مع مجموعة البيانات التي تختارها:
   ```bash
   # لـ HumanEval
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-openai-openai-humaneval.json
   ```

## 📊 التتبع مع Weave

Bench AI متكامل مع [Weave](https://wandb.ai/site/weave)، وهي أداة قوية لتتبع وتصور تجاربك.

## 🧩 مجموعات البيانات المدعومة

يحتوي هذا المستودع على **3 ملفات مجموعات بيانات** مع **30 سؤالاً لكل منها**:

- **`sql-console-for-openai-openai-humaneval.json`** - HumanEval (30 سؤالاً)
- **`sql-console-for-cruxeval-org-cruxeval.json`** - CruxEval (30 سؤالاً)
- **`sql-console-for-google-code-x-glue-ct-code-to-text.json`** - Code-X-GLUE (30 سؤالاً)

## 💯 التقييم المتقدم

يستخدم Bench AI نهج تقييم متقدم يجمع بين طرق متعددة لاكتشاف الإجابات الصحيحة:

1. **التطبيع الأساسي**: يزيل العلامات ويطبع المسافات
2. **التطبيع المتقدم**: يتعامل بذكاء مع المسافة البادئة وفواصل الأسطر
3. **التطبيع المتطرف**: يزيل جميع المسافات وفواصل الأسطر
4. **مقارنة AST**: يحلل البنية النحوية للكود
5. **تقييم الذكاء الاصطناعي**: يستخدم نموذج لغة لاكتشاف التكافؤ الوظيفي

## 🤝 المساهمة

المساهمات مرحب بها! لا تتردد في فتح مشكلة أو إرسال طلب سحب.

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT. انظر ملف [LICENSE](LICENSE) للتفاصيل.