@echo off
echo .....
echo check if pyinstaller is installed:
python -m pip install configparser
echo removing old stuff, build and dist folder
rmdir /s /q dist
rmdir /s /q build
del NoRScript_ClientV2.4.spec 
del NoRScript_OverlayV2.4.spec
echo -------------- success removed old Shit ---------------------------
echo building executables
pyinstaller --onefile -n NoRScript_ClientV2.4  execute.py
pyinstaller --onefile -n NoRScript_OverlayV2.4  overlay.py
echo -------------- success created executable ---------------------------
pause