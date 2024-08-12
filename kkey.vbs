Set objShell = CreateObject("WScript.Shell")

Public Sub Sub1()
	objShell.SendKeys "{k}"
	msg1 = msgbox("close this box", o, "abhay")
End Sub 

window.setInterval( Sub1 , 10000 )