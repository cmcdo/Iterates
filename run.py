import psutil
import os
from os import walk
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()
key = "f5"
FileName = ''
    
Files = next(walk('.'), (None, None, []))[2]    

for file in Files:
    if file[len(file) - 3:] == 'tex':
        FileName = file
        break
        
FirstRun = False
f = open('refresh.vbs','r')
for line in f:
    if 'First' in line:
        FirstRun  = True

f.close()
os.system('cmd /c "pdflatex "'+FileName)

if FirstRun:
    f = open('refresh.vbs', 'w')
    f.write('Set WshShell = WScript.CreateObject("WScript.Shell")'+"\n") 
    f.write('WshShell.AppActivate("SumatraPDF")'+"\n")
    f.write('WScript.Sleep(100)'+'\n')
    f.write('WshShell.AppActivate("'+FileName[:-4]+'.tex'+'")')
    f.close()

if not ("SumatraPDF" in (i.name() for i in psutil.process_iter())):
    os.startfile(FileName[:-4] + '.pdf')
    time.sleep(0.1)
    os.startfile("refresh.vbs")

else:
    os.startfile("refresh.vbs")
    time.sleep(0.1)
    
    keyboard.press(Key.ctrl)
    keyboard.press("1")
    
    keyboard.release(Key.ctrl)
    keyboard.release("1")

    time.sleep(0.1)
    keyboard.press(Key.f5)

    keyboard.release(Key.f5)
    time.sleep(0.1)
    if 1 == 2:
        keyboard.press(Key.f11)
        keyboard.release(Key.f11)
