@echo off
echo Building ShiroAI Separator Pro...
echo.

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Install spleeter from local directory if available
if exist "spleeter" (
    pip install -e spleeter/
) else (
    echo Warning: spleeter directory not found. Make sure to include spleeter in the build directory.
)

REM Build executable
python build_exe.py

echo.
echo Build completed! Check the 'dist' folder.
pause@echo off
echo Building ShiroAI Separator Pro...
echo.

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Install spleeter from local directory if available
if exist "spleeter" (
    pip install -e spleeter/
) else (
    echo Warning: spleeter directory not found. Make sure to include spleeter in the build directory.
)

REM Build executable
python build_exe.py

echo.
echo Build completed! Check the 'dist' folder.
pause