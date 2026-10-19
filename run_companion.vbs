Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
scriptDir = FSO.GetParentFolderName(WScript.ScriptFullName)

localAppData = WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%")
pythonw = localAppData & "\Programs\Python\Python313\pythonw.exe"

If Not FSO.FileExists(pythonw) Then
    pythonw = scriptDir & "\.venv\Scripts\pythonw.exe"
End If

script = scriptDir & "\companion.py"

WshShell.CurrentDirectory = scriptDir
WshShell.Run """" & pythonw & """ """ & script & """", 0, False
