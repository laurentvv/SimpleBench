# Bench AI with Ollama/LMStudio

<div align="center">

[![English](https://img.shields.io/badge/lang-en-blue.svg)](../README.md) [![中文](https://img.shields.io/badge/lang-zh-blue.svg)](README.zh.md) [![हिंदी](https://img.shields.io/badge/lang-hi-blue.svg)](README.hi.md) [![Español](https://img.shields.io/badge/lang-es-blue.svg)](README.es.md) [![Français](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md) [![العربية](https://img.shields.io/badge/lang-ar-blue.svg)](README.ar.md) [![বাংলা](https://img.shields.io/badge/lang-bn-blue.svg)](README.bn.md) [![Русский](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md) [![Português](https://img.shields.io/badge/lang-pt-blue.svg)](README.pt.md) [![Bahasa Indonesia](https://img.shields.io/badge/lang-id-blue.svg)](README.id.md)

![Bench AI Logo](https://img.shields.io/badge/Bench%20AI-LLM%20Benchmark%20Tool-blue)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

Bench AI হল একটি হালকা এবং দক্ষ টুল যা [Ollama](https://ollama.com/) এবং LMStudio এর মাধ্যমে চালিত ভাষা মডেল (LLMs) এর কর্মক্ষমতা মূল্যায়নের জন্য। এটি গবেষক এবং ডেভেলপারদের মানসম্মত প্রোগ্রামিং এবং যুক্তি কাজে বিভিন্ন মডেলের বস্তুনিষ্ঠ তুলনা করতে সাহায্য করে।

## 🎯 সাম্প্রতিক ফলাফল

- **মূল্যায়ন নির্ভুলতা**: HumanEval এ ৬৩% সঠিক উত্তর সনাক্ত করা হয়েছে
- **মূল্যায়ন পদ্ধতি**: ৫টি পরিপূরক পদ্ধতি (স্বাভাবিকীকরণ, AST, AI)
- **পুনরুৎপাদনযোগ্যতা**: সম্পাদনা জুড়ে সামঞ্জস্যপূর্ণ ফলাফল

## ✨ বৈশিষ্ট্য

- 🚀 **ব্যবহার সহজ** - স্বজ্ঞাত কমান্ড লাইন ইন্টারফেস
- 🔄 **মাল্টি-ডেটাসেট সাপোর্ট** - HumanEval, CruxEval এবং Code-X-GLUE এর সাথে সামঞ্জস্যপূর্ণ
- 📊 **উন্নত মূল্যায়ন** - ফরম্যাটিং, ইন্ডেন্টেশন এবং কার্যকরী সমতার পার্থক্য সহ্য করে
- 📈 **বিস্তারিত বিশ্লেষণ** - কর্মক্ষমতা বিশ্লেষণ স্ক্রিপ্ট অন্তর্ভুক্ত
- 🧩 **সম্প্রসারণযোগ্য** - বিভিন্ন ধরনের বেঞ্চমার্কের জন্য সহজে অভিযোজিত

## 🛠️ পূর্বশর্ত

- Python 3.13.5 বা উচ্চতর
- [Ollama](https://ollama.com/) ইনস্টল এবং চালু

## 📦 ইনস্টলেশন

1. রিপোজিটরি ক্লোন করুন:
   ```bash
   git clone https://github.com/laurentvv/bench-ai-ollama-lmstudio.git
   cd bench-ai-ollama-lmstudio
   ```

2. ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন এবং নির্ভরতা ইনস্টল করুন:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows এ: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🚀 বেঞ্চমার্ক চালানো

1. নিশ্চিত করুন যে Ollama চালু আছে।

2. আপনি যে মডেল পরীক্ষা করতে চান তা ডাউনলোড করুন:
   ```bash
   ollama pull qwen3:14b
   ```

3. আপনার পছন্দের ডেটাসেট দিয়ে বেঞ্চমার্ক চালান:
   ```bash
   # HumanEval এর জন্য
   python run_benchmark_production.py --model_name=qwen3:14b --dataset_source=sql-console-for-openai-openai-humaneval.json
   ```

## 📊 Weave দিয়ে ট্র্যাকিং

Bench AI [Weave](https://wandb.ai/site/weave) এর সাথে একীভূত, যা আপনার পরীক্ষা-নিরীক্ষা ট্র্যাক এবং ভিজ্যুয়ালাইজ করার জন্য একটি শক্তিশালী টুল।

## 🧩 সমর্থিত ডেটাসেট

এই রিপোজিটরিতে **৩টি ডেটাসেট ফাইল** রয়েছে যার **প্রতিটিতে ৩০টি প্রশ্ন**:

- **`sql-console-for-openai-openai-humaneval.json`** - HumanEval (৩০টি প্রশ্ন)
- **`sql-console-for-cruxeval-org-cruxeval.json`** - CruxEval (৩০টি প্রশ্ন)
- **`sql-console-for-google-code-x-glue-ct-code-to-text.json`** - Code-X-GLUE (৩০টি প্রশ্ন)

## 💯 উন্নত মূল্যায়ন

Bench AI একটি উন্নত মূল্যায়ন পদ্ধতি ব্যবহার করে যা সঠিক উত্তর সনাক্ত করতে একাধিক পদ্ধতি একত্রিত করে:

1. **মৌলিক স্বাভাবিকীকরণ**: ট্যাগ সরিয়ে দেয় এবং স্থান স্বাভাবিক করে
2. **উন্নত স্বাভাবিকীকরণ**: ইন্ডেন্টেশন এবং লাইন ব্রেক বুদ্ধিমত্তার সাথে পরিচালনা করে
3. **চরম স্বাভাবিকীকরণ**: সমস্ত স্থান এবং লাইন ব্রেক সরিয়ে দেয়
4. **AST তুলনা**: কোডের সিনট্যাক্টিক কাঠামো বিশ্লেষণ করে
5. **AI মূল্যায়ন**: কার্যকরী সমতা সনাক্ত করতে ভাষা মডেল ব্যবহার করে

## 🤝 অবদান

অবদান স্বাগত! একটি ইস্যু খুলতে বা পুল রিকোয়েস্ট জমা দিতে দ্বিধা করবেন না।

## 📄 লাইসেন্স

এই প্রকল্পটি MIT লাইসেন্সের অধীনে লাইসেন্সপ্রাপ্ত। বিস্তারিত জানতে [LICENSE](LICENSE) ফাইল দেখুন।