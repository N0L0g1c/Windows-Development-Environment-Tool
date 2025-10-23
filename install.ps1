# One-liner installation script
# Downloads and runs the main setup script

param(
    [string]$Stack = "",
    [string]$Tools = "",
    [switch]$NonInteractive = $false,
    [switch]$Debug = $false,
    [switch]$DryRun = $false
)

# Script URL (replace with actual repository URL)
$ScriptUrl = "https://raw.githubusercontent.com/N0L0g1c/Windows-Development-Environment-Tool/main/setup.ps1"

# Download and execute the main script
try {
    Write-Host "Downloading Windows Dev Environment Setup..." -ForegroundColor Cyan
    
    # Download the script
    $ScriptContent = Invoke-WebRequest -Uri $ScriptUrl -UseBasicParsing
    $ScriptPath = "$env:TEMP\setup.ps1"
    $ScriptContent.Content | Out-File -FilePath $ScriptPath -Encoding UTF8
    
    # Execute with parameters
    $Arguments = @()
    if ($Stack) { $Arguments += "--Stack", $Stack }
    if ($Tools) { $Arguments += "--Tools", $Tools }
    if ($NonInteractive) { $Arguments += "--NonInteractive" }
    if ($Debug) { $Arguments += "--Debug" }
    if ($DryRun) { $Arguments += "--DryRun" }
    
    Write-Host "Running setup script..." -ForegroundColor Green
    & $ScriptPath @Arguments
    
    # Clean up
    Remove-Item $ScriptPath -Force
}
catch {
    Write-Error "Failed to download or run setup script: $($_.Exception.Message)"
    Write-Host "You can download the script manually from: $ScriptUrl" -ForegroundColor Yellow
}
