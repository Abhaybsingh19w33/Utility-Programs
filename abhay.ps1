Clear-Host
Echo "Keep-alive" 

$WShell = New-Object -ComObject "Wscript.Shell"

for(;;)
{
$WShell.sendkeys("{CAPSLOCK}")
Start-Sleep -Milliseconds 1000
Get-Date
}