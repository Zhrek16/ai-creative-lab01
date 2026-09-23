# Протокол воспроизводимости — вариант 7

## 1. Среда

- Дата: 23.09.2026
- ОС: Windows 10 10.0.19045-SP0
- Python: 3.14.7
- PyTorch: 2.11.0+cpu
- Diffusers: 0.40.0
- Transformers: 5.17.0
- Accelerate: 1.15.0
- Safetensors: 0.8.0
- Pillow: 12.3.0
- Device: cpu
- dtype: torch.float32
- CUDA available: False

## 2. Зафиксированные параметры

- Model ID: stabilityai/sd-turbo
- Revision: b261bac6fd2cf515557d5d0707481eafa0485ec2
- Prompt: abstract conceptual illustration about quantum computing, glowing geometric nodes connected by luminous lines, layered translucent structures suggesting quantum states and superposition, deep blue and violet palette with subtle cyan highlights, dynamic central composition, futuristic abstract space, clean visual hierarchy, conceptual scientific art, no text, no labels, no logos, no people, no realistic quantum computer, no laboratory equipment, not a technical diagram, not a photograph
- Seed: 20260917
- Steps: 1
- Guidance: 0.0
- Size: 512x512

## 3. Run 001

- Command: .\.venv\Scripts\python.exe src\generate_once.py --run-id run_001
- Time: 125.191 s
- Image size: 512x512
- Mode: RGB
- Bytes: 540700
- SHA-256: 34649cb34da7fa263563f2743fda23dfcdd7325373f729c5d0f467d8b96d6b04

## 4. Run 002

- Command: .\.venv\Scripts\python.exe src\generate_once.py --run-id run_002
- Time: 131.936 s
- Image size: 512x512
- Mode: RGB
- Bytes: 540700
- SHA-256: 34649cb34da7fa263563f2743fda23dfcdd7325373f729c5d0f467d8b96d6b04

## 5. Сравнение

- SHA-256 match: YES
- Byte-for-byte match: YES

Одинаковый SHA-256 подтверждает побайтовое совпадение двух конкретных PNG-файлов, полученных в зафиксированной среде.

## 6. Намеренная ошибка

- Изменение: CPU Generator заменён на CUDA Generator: torch.Generator(device="cuda")
- Симптом: RuntimeError при создании CUDA Generator.
- Диагностика: torch.cuda.is_available() вернул False; фактическое устройство запуска — CPU.
- Причина: установленная версия PyTorch является CPU-only сборкой и не содержит CUDA backend.
- Исправление: Generator возвращён на device="cpu".
- Повторный запуск: успешный; создан artifacts\error_run\result.png, SHA-256 совпадает с основным результатом.

## 7. Вывод

Побайтовое совпадение подтверждено в рамках фактически зафиксированной среды. Результат не доказывает универсальную воспроизводимость на других устройствах, версиях библиотек, операционных системах или вычислительных backend.
