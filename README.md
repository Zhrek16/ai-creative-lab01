# ЛР №1 — Вариант 7

**Дисциплина:** «Искусственный интеллект в креативных технологиях»  
**ЛР №1:** «Запуск открытой модели text-to-image и фиксация воспроизводимого результата»  
**Вариант:** 7

## Задание варианта 7

- Контекст: иллюстрация к статье о квантовых вычислениях.
- Изменяемый фактор/решение: абстрактность вместо псевдодокументальности.
- Обязательная проверка: повторить запуск и сравнить SHA-256.
- Артефакты: иллюстрация и карточка ограничений.
- Критерий результата: явно обозначена концептуальность.
- Ограничение/риск: не представлять изображение как схему реального устройства.

## Модель

- Model ID: `stabilityai/sd-turbo`
- Revision: `b261bac6fd2cf515557d5d0707481eafa0485ec2`
- Device: CPU
- Размер: 512×512
- Steps: 1
- Guidance scale: 0.0
- Seed: 20260917

## Результаты

Работа выполнена локально в зафиксированном CPU-окружении.

Основной результат находится в:
`artifacts/run_001/result.png`

Повторный результат:
`artifacts/run_002/result.png`

Оба изображения имеют одинаковую SHA-256 контрольную сумму.

Подробные параметры запуска, окружение, протокол воспроизводимости,
сравнение SHA-256 и журнал намеренной ошибки находятся в каталоге `reports/`.

Основной отчёт:
`reports/report.md`

## 1. Установка

Вы уже используете Python 3.14. Для текущих версий PyTorch существуют CPU wheels для CPython 3.14.

Из PowerShell, находясь в корне проекта:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Проверка:

```powershell
python -c "import sys, torch, diffusers, transformers; print(sys.version); print('torch', torch.__version__); print('diffusers', diffusers.__version__); print('transformers', transformers.__version__); print('cuda', torch.cuda.is_available())"
```

Ожидается `cuda False`, если используется CPU.

После установки:

```powershell
python -m pip freeze > reports\environment.txt
```

## 2. Первый запуск

```powershell
python src\generate_once.py --run-id run_001
```

Для сохранения консольного журнала:

```powershell
python src\generate_once.py --run-id run_001 2>&1 | Tee-Object reports\run_001.log
```

Должны появиться:

```text
artifacts/run_001/result.png
artifacts/run_001/manifest.json
```

## 3. Проверка первого результата

```powershell
python -c "from PIL import Image; im=Image.open('artifacts/run_001/result.png'); print(im.size, im.mode)"
python -m json.tool artifacts\run_001\manifest.json
```

## 4. Второй точный повтор

Не изменяйте `configs/run_config.json` и исходный код.

```powershell
python src\generate_once.py --run-id run_002
```

Проверьте:

```powershell
python -c "import hashlib; from pathlib import Path; a=hashlib.sha256(Path('artifacts/run_001/result.png').read_bytes()).hexdigest(); b=hashlib.sha256(Path('artifacts/run_002/result.png').read_bytes()).hexdigest(); print('run_001:', a); print('run_002:', b); print('MATCH:', a==b)"
```

Результат `MATCH: True` является точным совпадением байтов двух PNG в одной зафиксированной среде.

## 5. Намеренная типовая ошибка

Работа требует воспроизвести ошибку безопасным способом.

Сначала сделайте копию исходного скрипта:

```powershell
Copy-Item src\generate_once.py src\generate_error.py
```

Откройте `src\generate_error.py` и замените:

```python
torch.Generator(device="cpu")
```

на:

```python
torch.Generator(device="cuda")
```

Перед запуском:

```powershell
python -c "import torch; print('cuda available:', torch.cuda.is_available())"
```

На CPU-машине ожидается `False`.

Запуск:

```powershell
python src\generate_error.py --run-id error_run
```

Сохраните текст ошибки в `reports/error.log`.

После этого восстановите рабочий CPU-вариант:

```python
torch.Generator(device="cpu")
```

и снова выполните обычный запуск.

## 6. Карточка ограничений

Заполните `reports/limitations_card.md`.

Минимум зафиксируйте:

1. воспроизводимость подтверждена только в конкретной зафиксированной среде;
2. seed не компенсирует различия платформ и версий ПО;
3. SHA-256 проверяет байтовое совпадение файла, а не эстетическое качество;
4. изображение является концептуальной иллюстрацией и не должно выдаваться за реальную схему или фотографию квантового устройства;
5. учитываются лицензия модели и допустимые условия использования.

## 7. Что нельзя класть в итоговый архив

Не включайте:

- `.venv/`
- кэш Hugging Face / скачанные веса модели
- секретные ключи и токены

## 8. Финальная структура

```text
ai-creative-lab01/
├── .gitignore
├── README.md
├── requirements.txt
├── configs/
│   └── run_config.json
├── src/
│   ├── generate_once.py
│   ├── generate_error.py
│   └── verify_artifacts.py
├── scripts/
│   ├── setup_windows.ps1
│   ├── run_first.ps1
│   ├── run_second.ps1
│   └── run_error.ps1
├── artifacts/
│   ├── run_001/
│   │   ├── manifest.json
│   │   └── result.png
│   ├── run_002/
│   │   ├── manifest.json
│   │   └── result.png
│   └── error_run/
│       ├── manifest.json
│       └── result.png
└── reports/
    ├── environment.txt
    ├── error.log
    ├── limitations_card.md
    ├── report.md
    ├── reproducibility_protocol.md
    ├── sha256_comparison.json
    └── source_notes.md

data/ и дублирующиеся файлы manifest.json в reports/run_001/ и reports/run_002/ в итоговую структуру не входят.
```
