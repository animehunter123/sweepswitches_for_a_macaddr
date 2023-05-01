$aggSwitches = @("192.168.1.1", "192.168.1.2", "192.168.1.3")
$macRegex = [regex]::new("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})")
$workstationList = @{}

foreach ($switch in $aggSwitches) {
    $output = ssh admin@$switch "show mac-address"
    $matches_res = $macRegex.Matches($output)
    $workstationList[$switch] = $matches_res.Value
}

foreach ($switch in $workstationList.Keys) {
    Write-Host "Workstations connected to switch $switch:"
    foreach ($workstation in $workstationList[$switch]) {
        $hostname = nslookup $workstation
        Write-Host "`t$workstation ($hostname)"
    }
}
