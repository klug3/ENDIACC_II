# ENDIACC II

# Requirements:
- Python 3.10

# Seting up virtual environment:
py -m venv .venv

.venv/Scripts/activate

python -m pip install --upgrade pip

## Install packeges all at once from requirements.txt file:
python -m pip install -r /path/to/requirements.txt


# Alternative way using Windows embeddable package (64-bit):
This way can be usefull to run ENDIACC II on Windows machines without Pyton 3.10 installed.
You can download ready package without ENDIACC (steps 1-6) as: embeddable.zip.
To create your own package proceed as follows:
1. Download Windows embeddable package from https://www.python.org/downloads/release/python-3100/
2. Unzip to new directory: dir\env\
3. Add necessary Tkinter files to python distribution. To do so, copy those files from your local Python310 directory:
- _tkinter.pyd, tcl86t.dll, tk86t.dll (located in \DLLs\ directory) to dir\env\DLLs\
- tcl directory to dir\env\
- tkinter (located in \Lib\) to dir\env\Lib
NOTE: You need to create dir\env\DLLs\ and dir\env\Lib\ directories
4. Install pip:
- copy content of: https://bootstrap.pypa.io/get-pip.py to txt file. Rename it to get-pip.py and put this file in dir\env\ directory
- open new Windows PowerShell in dir\
- run: env/python env/get-pip.py
5. Add: 
./Lib/site-packages
./Lib
./DLLs
at the begining of dir\env\python310._pth
6. Install necessary packages from dir\requirements.txt:
- run: env/python -m pip install -r env\requirements.txt
Python 3.10 environment is finally ready to use.
7. To run ENDIACC II on this environment:
- put client.py, functions.py and gui_client.py(or gui_wizard.py) in dir\env\
- put pictures directory with at least 1 .jpg picture (or 2 for wizard) in dir\pictures
- create runENDIACCII.bat file containing:
call env\python.exe env\gui_client.py  - for client
call env\python.exe env\gui_wizard.py  - for wizard
- double click on runENDIACCII.bat

# Windows embeddable packages (64-bit) for information seeker/provider and wizard are available in ./Embedded interfaces directory!