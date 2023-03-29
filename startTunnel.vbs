Dim WshShell 
Set WshShell=WScript.CreateObject("WScript.Shell") 
WshShell.Run "cmd.exe"
WScript.Sleep 1500
Call ENmode()
Sub ENmode()
    If IMEStatus = vbIMEModeOn Then
        WshShell.SendKeys "+", True
    End If
End Sub
WshShell.SendKeys "ssh -CNg -L 6006:127.0.0.1:6006 root@region-102.seetacloud.com -p 32371"
WshShell.SendKeys "{ENTER}"
WScript.Sleep 3000
WshShell.SendKeys "Z3oAUhJ{+}Dn"
WshShell.SendKeys "{ENTER}"