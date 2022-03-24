Set WshShell = WScript.CreateObject("WScript.Shell")
WshShell.AppActivate("SumatraPDF")
WScript.Sleep(100)
WshShell.AppActivate("Iterates.tex")