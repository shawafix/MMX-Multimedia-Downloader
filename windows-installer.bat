@echo off
echo Welcome to the MMX Multimedia Downloader setup!
echo.

where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed! Great job!
    goto INSTALL_DEPS
)

echo Downloading Python...
curl -o python_installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe
if not exist python_installer.exe (
    echo Failed to download Python installer.
    pause
    exit /b 1
)

echo Installing Python... This might take a few minutes.
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 DisablePathLengthLimit=1
if %errorlevel% neq 0 (
    echo Failed to install Python.
    pause
    exit /b 1
)

del python_installer.exe

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python installation failed. Please restart your computer and try again.
    pause
    exit /b 1
)

:INSTALL_DEPS
echo Installing yt-dlp...
python -m pip install yt-dlp
if %errorlevel% neq 0 (
    echo Failed to install yt-dlp.
    pause
    exit /b 1
)

echo Downloading ffmpeg...
curl -o ffmpeg.zip https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
if not exist ffmpeg.zip (
    echo Failed to download ffmpeg.
    pause
    exit /b 1
)

mkdir ffmpeg
tar -xf ffmpeg.zip -C ffmpeg
if %errorlevel% neq 0 (
    echo Failed to extract ffmpeg.
    pause
    exit /b 1
)

del ffmpeg.zip
setx PATH "%PATH%;%cd%\ffmpeg"

echo Installing pyfiglet...
python -m pip install pyfiglet
if %errorlevel% neq 0 (
    echo Failed to install pyfiglet.
    pause
    exit /b 1
)

python -c "from pyfiglet import Figlet; print(Figlet(font='slant').renderText('All Set!'))"
echo Installation complete! Launching the MMX Multimedia Downloader...
python main.py
if %errorlevel% neq 0 (
    echo Failed to launch main.py. Please run it manually.
    pause
    exit /b 1
)

pause
