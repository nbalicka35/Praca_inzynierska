## Instalacja
Aplikacja działa na wersji Python 3.11.0 lub nowszej. Jest ona wymagana do uruchomienia aplikacji.
### 1. Sklonuj lub pobierz repozytorium
```bash
git clone https://github.com/username/Praca_inzynierska.git
cd Praca_inzynierska
```

### 2. Utwórz środowisko wirtualne
```bash
python -m venv .venv
```

### 3. Aktywuj środowisko wirtualne

**Windows (PowerShell):**
```powershell
.venv\Scripts\activate
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

### 4. Zainstaluj zależności

**Z obsługą GPU (NVIDIA CUDA 13.0):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
pip install PyQt5 opencv-python Pillow numpy
```

**Bez GPU (tylko CPU):**
```bash
pip install torch torchvision
pip install PyQt5 opencv-python Pillow numpy
```

**Pozostałe biblioteki:**
```bash
pip install -r requirements.txt
```

### 5. Sprawdź instalację
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"
```

## Uruchomienie aplikacji
```bash
python app/src/main.py
```

## Struktura projektu
```
Praca_inzynierska/
├── app/
│   ├── src/
│   │   ├── main.py              # Główny plik aplikacji
│   │   ├── Card.py              # Komponent karty UI
│   │   ├── TopBar.py            # Pasek górny
│   │   ├── ThemesManager.py     # Zarządzanie motywami
│   │   ├── Translator.py        # Tłumaczenia (EN/PL)
│   │   ├── ScaleManager.py      # Skalowanie UI
│   │   ├── SettingsManager.py   # Zapisywanie ustawień
│   │   └── MsgDialog.py         # Okna dialogowe
│   └── utils/
│       ├── BrainTumorClassifier.py  # Klasyfikator
│       ├── ResNet34Model.py         # Model sieci
│       ├── GradCAM.py               # Wizualizacja GradCAM
│       └── HistogramEqualization.py # Preprocessing
├── config/
│   └── resnet34.pth             # Wagi modelu
├── requirements.txt                # Lista wszystkich potrzebnych pakietów
├── DatasetDivider.ipynb            # Losowy podział zbioru od nowa
├── GradCAM.ipynb                   # Przykładowe wizualizacje
├── main_noRandomDivision.ipynb     # Analiza danych + eksperymenty na oryginalnym zbiorze z Kaggle
├── main_RandomDivision.ipynb       # Analiza danych + eksperymenty na zbiorze po losowym podziale
└── README.md
```