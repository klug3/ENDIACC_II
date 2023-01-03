# Requirements:
## python version:
- Python 3.10

## Before setting up Python environment ensure that you have installed:
- Java 8.0 or higher required: https://www.java.com/pl/download/
- Microsoft Visual C++ Redistributable (https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)

## Seting up the environment:
### Create virtual environment and activate it:
py -m venv .venv
./venv/Scripts/activate
If you cannot run a script in Windows 10 you need to:
1. Open PowerShell as Administrator
1.1. Press Windows+R
1.2. Type powershell and press CTRL+SHIFT+ENTER
2. Execute command:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted

### Upgrade pip:
python -m pip install --upgrade pip

### Install all packages at once:
python -m pip install -r requirements.txt

### Download necessary pipeline for polish language:
python -m spacy download pl_core_news_lg

### Activate ipykernel for jupyter notebooks
python -m ipykernel install --user --name=.venv

### Necessary packages:
- spacy:
python -m pip install spacy
python -m spacy download pl_core_news_lg

- pandas:
python -m pip install pandas

- language-tool-python:
python -m pip install language-tool-python
(Java 8.0 or higher required: https://www.java.com/pl/download/)

- seaborn
python -m pip install seaborn

- scipy
python -m pip install scipy

### Using GPU to speed-up spaCy module:
-Install CUDA Toolkit
https://developer.nvidia.com/cuda-downloads
-python -m pip install -U 'spacy[cuda117]'
- Do not forget to uncomment: spacy.require_gpu() line
