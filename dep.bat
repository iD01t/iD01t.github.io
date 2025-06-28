@echo off
REM ================================================================
REM Desktop Assistant Pro - Bulletproof Windows 11 Installer
REM Handles Python installation, dependencies, and configuration
REM Created for cross-platform deployment and monetization
REM ================================================================

setlocal EnableDelayedExpansion
color 0A
title Desktop Assistant Pro - Windows 11 Installer

echo.
echo ===============================================
echo    DESKTOP ASSISTANT PRO - INSTALLER
echo ===============================================
echo.
echo Checking system compatibility and dependencies...
echo.

REM Create installation log
set LOG_FILE=%~dp0installation_log.txt
echo Installation started at %date% %time% > "%LOG_FILE%"

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Not running as administrator.
    echo Some installations may require elevated privileges.
    echo.
    pause
)

REM ================================================================
REM STEP 1: Check Windows Version
REM ================================================================
echo [STEP 1] Checking Windows version...
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
if "%VERSION%" lss "10.0" (
    echo [ERROR] Windows 10 or higher required. Found version: %VERSION%
    echo [ERROR] Please upgrade your Windows version.
    pause
    exit /b 1
)
echo [OK] Windows version compatible: %VERSION%
echo Windows version check passed >> "%LOG_FILE%"

REM ================================================================
REM STEP 2: Check Python Installation
REM ================================================================
echo.
echo [STEP 2] Checking Python installation...

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Python not found in PATH.
    echo.
    echo Checking common Python locations...
    
    REM Check common Python installation paths
    set PYTHON_FOUND=0
    for %%P in (
        "C:\Python39\python.exe"
        "C:\Python310\python.exe"
        "C:\Python311\python.exe"
        "C:\Python312\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "%APPDATA%\Python\Python39\Scripts\python.exe"
        "%APPDATA%\Python\Python310\Scripts\python.exe"
        "%APPDATA%\Python\Python311\Scripts\python.exe"
        "%APPDATA%\Python\Python312\Scripts\python.exe"
    ) do (
        if exist %%P (
            echo [FOUND] Python at %%P
            set PYTHON_PATH=%%P
            set PYTHON_FOUND=1
            goto :python_found
        )
    )
    
    :python_found
    if !PYTHON_FOUND! equ 0 (
        echo [ERROR] Python not found on this system.
        echo.
        echo Please install Python 3.9+ from https://python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        echo.
        echo After installing Python, run this installer again.
        pause
        exit /b 1
    ) else (
        echo [WARNING] Python found but not in PATH.
        echo Adding Python to current session PATH...
        for %%P in (!PYTHON_PATH!) do set PYTHON_DIR=%%~dpP
        set PATH=!PYTHON_DIR!;!PATH!
        set PATH=!PYTHON_DIR!Scripts;!PATH!
    )
) else (
    echo [OK] Python found in PATH
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python version: %PYTHON_VERSION%

REM Check if Python version is 3.9+
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% lss 3 (
    echo [ERROR] Python 3.9+ required. Found: %PYTHON_VERSION%
    echo Please upgrade Python and run this installer again.
    pause
    exit /b 1
)

if %MAJOR% equ 3 if %MINOR% lss 9 (
    echo [ERROR] Python 3.9+ required. Found: %PYTHON_VERSION%
    echo Please upgrade Python and run this installer again.
    pause
    exit /b 1
)

echo [OK] Python version compatible: %PYTHON_VERSION%
echo Python version check passed: %PYTHON_VERSION% >> "%LOG_FILE%"

REM ================================================================
REM STEP 3: Check and Upgrade pip
REM ================================================================
echo.
echo [STEP 3] Checking pip installation...

python -m pip --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] pip not found. Installing pip...
    python -m ensurepip --upgrade
    if !errorLevel! neq 0 (
        echo [ERROR] Failed to install pip.
        echo Please install pip manually and run this installer again.
        pause
        exit /b 1
    )
)

echo [INFO] Upgrading pip to latest version...
python -m pip install --upgrade pip --quiet
if %errorLevel% neq 0 (
    echo [WARNING] Failed to upgrade pip. Continuing with current version...
) else (
    echo [OK] pip upgraded successfully
)

for /f "tokens=2" %%i in ('python -m pip --version 2^>^&1') do set PIP_VERSION=%%i
echo [INFO] pip version: %PIP_VERSION%
echo pip upgrade completed >> "%LOG_FILE%"

REM ================================================================
REM STEP 4: Create Virtual Environment (Optional but Recommended)
REM ================================================================
echo.
echo [STEP 4] Setting up virtual environment...

set VENV_DIR=%~dp0desktop_assistant_env
if exist "%VENV_DIR%" (
    echo [INFO] Virtual environment already exists.
    choice /c YN /m "Do you want to recreate it? (Y/N)"
    if !errorlevel! equ 1 (
        echo [INFO] Removing existing virtual environment...
        rmdir /s /q "%VENV_DIR%"
    )
)

if not exist "%VENV_DIR%" (
    echo [INFO] Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if !errorLevel! neq 0 (
        echo [WARNING] Failed to create virtual environment.
        echo Continuing with global Python installation...
        set USE_VENV=0
    ) else (
        echo [OK] Virtual environment created successfully
        set USE_VENV=1
    )
) else (
    set USE_VENV=1
)

if %USE_VENV% equ 1 (
    echo [INFO] Activating virtual environment...
    call "%VENV_DIR%\Scripts\activate.bat"
    echo [OK] Virtual environment activated
    echo Virtual environment setup completed >> "%LOG_FILE%"
)

REM ================================================================
REM STEP 5: Install Core Dependencies
REM ================================================================
echo.
echo [STEP 5] Installing core dependencies...

echo [INFO] Installing requests (HTTP library)...
python -m pip install requests --quiet
if %errorLevel% neq 0 (
    echo [ERROR] Failed to install requests
    echo Failed to install requests >> "%LOG_FILE%"
    goto :installation_error
)
echo [OK] requests installed

echo [INFO] Installing OpenAI SDK...
python -m pip install "openai>=1.0.0" --quiet
if %errorLevel% neq 0 (
    echo [ERROR] Failed to install OpenAI SDK
    echo Failed to install OpenAI SDK >> "%LOG_FILE%"
    goto :installation_error
)
echo [OK] OpenAI SDK installed

REM ================================================================
REM STEP 6: Install Audio Dependencies
REM ================================================================
echo.
echo [STEP 6] Installing audio dependencies...

echo [INFO] Installing gTTS (Google Text-to-Speech)...
python -m pip install gtts --quiet
if %errorLevel% neq 0 (
    echo [WARNING] Failed to install gTTS (audio features will be disabled)
    echo Failed to install gTTS >> "%LOG_FILE%"
) else (
    echo [OK] gTTS installed
)

echo [INFO] Installing pygame (audio playback)...
python -m pip install pygame --quiet
if %errorLevel% neq 0 (
    echo [WARNING] Failed to install pygame (audio playback may not work)
    echo Failed to install pygame >> "%LOG_FILE%"
) else (
    echo [OK] pygame installed
)

REM ================================================================
REM STEP 7: Install PDF Dependencies
REM ================================================================
echo.
echo [STEP 7] Installing PDF dependencies...

echo [INFO] Installing fpdf2 (PDF generation)...
python -m pip install fpdf2 --quiet
if %errorLevel% neq 0 (
    echo [WARNING] Failed to install fpdf2 (PDF export will be disabled)
    echo Failed to install fpdf2 >> "%LOG_FILE%"
) else (
    echo [OK] fpdf2 installed
)

REM ================================================================
REM STEP 8: Install Image Dependencies
REM ================================================================
echo.
echo [STEP 8] Installing image dependencies...

echo [INFO] Installing Pillow (image processing)...
python -m pip install Pillow --quiet
if %errorLevel% neq 0 (
    echo [WARNING] Failed to install Pillow (image features will be disabled)
    echo Failed to install Pillow >> "%LOG_FILE%"
) else (
    echo [OK] Pillow installed
)

REM ================================================================
REM STEP 9: Install Additional Utilities
REM ================================================================
echo.
echo [STEP 9] Installing additional utilities...

echo [INFO] Installing packaging utilities...
python -m pip install wheel setuptools --quiet --upgrade
if %errorLevel% neq 0 (
    echo [WARNING] Failed to upgrade packaging utilities
) else (
    echo [OK] Packaging utilities updated
)

echo [INFO] Installing PyInstaller (for executable creation)...
python -m pip install pyinstaller --quiet
if %errorLevel% neq 0 (
    echo [WARNING] Failed to install PyInstaller (executable creation unavailable)
    echo Failed to install PyInstaller >> "%LOG_FILE%"
) else (
    echo [OK] PyInstaller installed
)

REM ================================================================
REM STEP 10: Verify Installations
REM ================================================================
echo.
echo [STEP 10] Verifying installations...

echo [INFO] Testing imports...
python -c "import openai; print('OpenAI: OK')" 2>nul || echo [WARNING] OpenAI import failed
python -c "import requests; print('Requests: OK')" 2>nul || echo [WARNING] Requests import failed
python -c "import tkinter; print('Tkinter: OK')" 2>nul || echo [ERROR] Tkinter import failed
python -c "import json, os, subprocess; print('Standard libraries: OK')" 2>nul || echo [ERROR] Standard libraries failed

echo [INFO] Testing optional imports...
python -c "import gtts; print('gTTS: OK')" 2>nul || echo [INFO] gTTS not available (audio disabled)
python -c "import pygame; print('Pygame: OK')" 2>nul || echo [INFO] Pygame not available (audio playback limited)
python -c "from fpdf import FPDF; print('FPDF: OK')" 2>nul || echo [INFO] FPDF not available (PDF export disabled)
python -c "from PIL import Image; print('PIL: OK')" 2>nul || echo [INFO] PIL not available (image features disabled)

echo Import verification completed >> "%LOG_FILE%"

REM ================================================================
REM STEP 11: Create Configuration Files
REM ================================================================
echo.
echo [STEP 11] Creating configuration files...

REM Create OpenAI config template
set CONFIG_FILE=%~dp0openai_config.json
if not exist "%CONFIG_FILE%" (
    echo [INFO] Creating OpenAI configuration template...
    (
        echo {
        echo   "openai_api_key": "sk-your-openai-api-key-here",
        echo   "model": "gpt-4",
        echo   "max_tokens": 1500,
        echo   "temperature": 0.7
        echo }
    ) > "%CONFIG_FILE%"
    echo [OK] Configuration template created: openai_config.json
    echo [IMPORTANT] Edit openai_config.json with your actual OpenAI API key
) else (
    echo [INFO] Configuration file already exists: openai_config.json
)

REM Create batch launcher
set LAUNCHER_FILE=%~dp0run_desktop_assistant.bat
echo [INFO] Creating launcher script...
(
    echo @echo off
    echo title Desktop Assistant Pro
    echo color 0A
    if %USE_VENV% equ 1 (
        echo echo Activating virtual environment...
        echo call "%VENV_DIR%\Scripts\activate.bat"
    )
    echo echo Starting Desktop Assistant Pro...
    echo echo.
    echo python "%~dp0desktop_assistant.py"
    echo if %%errorLevel%% neq 0 (
    echo     echo.
    echo     echo [ERROR] Failed to start Desktop Assistant Pro
    echo     pause
    echo ^)
) > "%LAUNCHER_FILE%"
echo [OK] Launcher created: run_desktop_assistant.bat

REM Create requirements.txt for future reference
set REQ_FILE=%~dp0requirements.txt
echo [INFO] Creating requirements.txt...
(
    echo # Desktop Assistant Pro Dependencies
    echo openai^>=1.0.0
    echo requests
    echo gtts
    echo pygame
    echo fpdf2
    echo Pillow
    echo pyinstaller
) > "%REQ_FILE%"
echo [OK] Requirements file created: requirements.txt

echo Configuration files created >> "%LOG_FILE%"

REM ================================================================
REM STEP 12: Create Desktop Shortcut (Optional)
REM ================================================================
echo.
echo [STEP 12] Creating desktop shortcut...

choice /c YN /m "Do you want to create a desktop shortcut? (Y/N)"
if %errorlevel% equ 1 (
    set SHORTCUT_PATH=%USERPROFILE%\Desktop\Desktop Assistant Pro.lnk
    set TARGET_PATH=%~dp0run_desktop_assistant.bat
    set ICON_PATH=%SystemRoot%\system32\shell32.dll,21
    
    REM Create VBS script to generate shortcut
    set VBS_FILE=%TEMP%\create_shortcut.vbs
    (
        echo Set WshShell = WScript.CreateObject("WScript.Shell"^)
        echo Set Shortcut = WshShell.CreateShortcut("!SHORTCUT_PATH!"^)
        echo Shortcut.TargetPath = "!TARGET_PATH!"
        echo Shortcut.WorkingDirectory = "%~dp0"
        echo Shortcut.IconLocation = "!ICON_PATH!"
        echo Shortcut.Description = "Desktop Assistant Pro - AI-Powered Automation Tool"
        echo Shortcut.Save
    ) > "!VBS_FILE!"
    
    cscript //nologo "!VBS_FILE!" >nul 2>&1
    del "!VBS_FILE!" >nul 2>&1
    
    if exist "!SHORTCUT_PATH!" (
        echo [OK] Desktop shortcut created
    ) else (
        echo [WARNING] Failed to create desktop shortcut
    )
)

REM ================================================================
REM STEP 13: Final System Test
REM ================================================================
echo.
echo [STEP 13] Running final system test...

echo [INFO] Testing Desktop Assistant Pro import...
python -c "
import sys, os
sys.path.insert(0, os.getcwd())

# Test basic functionality
try:
    import tkinter as tk
    import json
    import requests
    print('✓ Core functionality test passed')
except Exception as e:
    print(f'✗ Core functionality test failed: {e}')
    sys.exit(1)

# Test OpenAI
try:
    import openai
    print('✓ OpenAI integration available')
except:
    print('⚠ OpenAI integration unavailable')

# Test optional features
optional_features = []
try:
    import gtts
    optional_features.append('Audio generation')
except:
    pass

try:
    from fpdf import FPDF
    optional_features.append('PDF export')
except:
    pass

try:
    from PIL import Image
    optional_features.append('Image processing')
except:
    pass

if optional_features:
    print('✓ Optional features available:', ', '.join(optional_features))
else:
    print('⚠ No optional features available')

print('✓ System test completed successfully')
" 2>nul

if %errorLevel% neq 0 (
    echo [ERROR] System test failed
    echo System test failed >> "%LOG_FILE%"
    goto :installation_error
)

echo System test passed >> "%LOG_FILE%"

REM ================================================================
REM INSTALLATION COMPLETE
REM ================================================================
echo.
echo ===============================================
echo    INSTALLATION COMPLETED SUCCESSFULLY!
echo ===============================================
echo.
echo [SUCCESS] Desktop Assistant Pro is ready to use!
echo.
echo NEXT STEPS:
echo 1. Edit 'openai_config.json' with your OpenAI API key
echo 2. Run 'run_desktop_assistant.bat' to start the application
echo 3. Or double-click 'desktop_assistant.py' if you have Python file associations
echo.
echo FILES CREATED:
echo • openai_config.json (edit with your API key)
echo • run_desktop_assistant.bat (launcher script)
echo • requirements.txt (dependency list)
echo • installation_log.txt (installation log)
if %USE_VENV% equ 1 echo • desktop_assistant_env\ (virtual environment)
echo.
echo FEATURES AVAILABLE:
echo ✓ OpenAI GPT-4 integration (requires API key)
echo ✓ File reading and processing
echo ✓ Command execution
echo ✓ API testing
echo ✓ Multi-format export (PDF, HTML, Audio, Images)
echo ✓ Auto eBook generation
echo ✓ Modern GUI interface
echo.

if %USE_VENV% equ 1 (
    echo [INFO] Virtual environment is activated.
    echo To use Desktop Assistant Pro later:
    echo   1. Run 'run_desktop_assistant.bat', or
    echo   2. Activate environment manually: desktop_assistant_env\Scripts\activate.bat
    echo   3. Then run: python desktop_assistant.py
) else (
    echo [INFO] Using global Python installation.
    echo To use Desktop Assistant Pro: python desktop_assistant.py
)

echo.
echo Installation completed successfully at %date% %time% >> "%LOG_FILE%"
echo Press any key to exit installer...
pause >nul
goto :end

REM ================================================================
REM ERROR HANDLING
REM ================================================================
:installation_error
echo.
echo ===============================================
echo    INSTALLATION ERROR OCCURRED
echo ===============================================
echo.
echo [ERROR] Installation failed. Check the details above.
echo.
echo TROUBLESHOOTING TIPS:
echo 1. Run this installer as Administrator
echo 2. Check your internet connection
echo 3. Ensure Python 3.9+ is properly installed
echo 4. Try installing dependencies manually:
echo    pip install openai requests gtts pygame fpdf2 Pillow
echo.
echo Check 'installation_log.txt' for detailed error information.
echo.
echo Installation failed at %date% %time% >> "%LOG_FILE%"
pause
exit /b 1

:end
endlocal
exit /b 0
