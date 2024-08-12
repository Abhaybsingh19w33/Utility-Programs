Clear-Host
Echo "Keep-alive with Scroll Lock.."

$WShell = New-Object -ComObject "Wscript.Shell"

for (; ; ) {
    $WShell.sendkeys("{a}")
    Start-Sleep -Milliseconds 2000
    Echo "First key pressed after 1000 mls"
    $Wshell.sendkeys("{b}")
    Start-Sleep -Milliseconds 2000
    Echo "Second key pressed after 2000 mls"
}