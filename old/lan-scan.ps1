$network = "192.168.1"
1..254 | ForEach-Object {
    $ip = "$network.$_"
    if (Test-Connection -Count 1 -Quiet $ip) {
        Write-Host "Online: $ip" -ForegroundColor Green
    }
}
