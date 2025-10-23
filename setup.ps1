# Windows Dev Environment Setup Script
# Sets up your Windows dev environment without the usual headaches

param(
    [string]$Stack = "",
    [string]$Tools = "",
    [string]$CustomFile = "",
    [switch]$NonInteractive = $false,
    [switch]$Debug = $false,
    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [string]$PackageManager = "auto",
    [switch]$Choco = $false,
    [switch]$Scoop = $false,
    [switch]$Winget = $false,
    [switch]$Help = $false
)

# Script version and metadata
$ScriptVersion = "1.0.0"
$ScriptName = "Windows Dev Environment Setup"
$LogFile = "$env:TEMP\dev-setup.log"
$ConfigFile = "$env:USERPROFILE\.dev-setup\config.json"

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    Cyan = "Cyan"
    Magenta = "Magenta"
    White = "White"
}

# Enhanced logging functions
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Write-Host $LogEntry
    Add-Content -Path $LogFile -Value $LogEntry
}

function Write-Success {
    param([string]$Message)
    Write-Host $Message -ForegroundColor $Colors.Green
    Write-Log $Message "SUCCESS"
}

function Write-Warning {
    param([string]$Message)
    Write-Host $Message -ForegroundColor $Colors.Yellow
    Write-Log $Message "WARNING"
}

function Write-Error {
    param([string]$Message)
    Write-Host $Message -ForegroundColor $Colors.Red
    Write-Log $Message "ERROR"
}

function Write-Info {
    param([string]$Message)
    Write-Host $Message -ForegroundColor $Colors.Blue
    Write-Log $Message "INFO"
}

function Write-Debug {
    param([string]$Message)
    if ($Debug) {
        Write-Host $Message -ForegroundColor $Colors.Cyan
        Write-Log $Message "DEBUG"
    }
}

# Enhanced utility functions
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Get-PackageManager {
    if ($Choco) { return "choco" }
    if ($Scoop) { return "scoop" }
    if ($Winget) { return "winget" }
    
    # Auto-detect
    if (Test-Command "choco") { return "choco" }
    if (Test-Command "scoop") { return "scoop" }
    if (Test-Command "winget") { return "winget" }
    
    # Default to winget (built into Windows 10/11)
    return "winget"
}

function Install-PackageManager {
    param([string]$Manager)
    
    Write-Info "Installing package manager: $Manager"
    
    switch ($Manager) {
        "choco" {
            if (-not (Test-Command "choco")) {
                Write-Info "Installing Chocolatey..."
                Set-ExecutionPolicy Bypass -Scope Process -Force
                [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
                iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
                Write-Success "Chocolatey installed successfully"
            }
        }
        "scoop" {
            if (-not (Test-Command "scoop")) {
                Write-Info "Installing Scoop..."
                Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
                irm get.scoop.sh | iex
                Write-Success "Scoop installed successfully"
            }
        }
        "winget" {
            if (-not (Test-Command "winget")) {
                Write-Error "Winget is not available. Please install Windows 10 version 1709 or later, or Windows 11"
                return $false
            }
        }
    }
    return $true
}

function Install-Package {
    param(
        [string]$Package,
        [string]$Manager,
        [string]$Arguments = ""
    )
    
    Write-Info "Installing package: $Package"
    
    if ($DryRun) {
        Write-Info "DRY RUN: Would install $Package using $Manager"
        return $true
    }
    
    try {
        switch ($Manager) {
            "choco" {
                if ($Arguments) {
                    choco install $Package $Arguments -y
                } else {
                    choco install $Package -y
                }
            }
            "scoop" {
                scoop install $Package
            }
            "winget" {
                if ($Arguments) {
                    winget install $Package $Arguments
                } else {
                    winget install $Package
                }
            }
        }
        Write-Success "Successfully installed $Package"
        return $true
    }
    catch {
        Write-Error "Failed to install $Package: $($_.Exception.Message)"
        return $false
    }
}

function Install-WebDevStack {
    Write-Info "Installing web development stack..."
    
    $packages = @(
        "git",
        "nodejs",
        "vscode",
        "googlechrome",
        "firefox",
        "postman",
        "docker-desktop"
    )
    
    # Check if user wants Cursor instead of VS Code
    if (-not $NonInteractive) {
        $editorChoice = Read-Host "Choose your code editor: (1) VS Code (2) Cursor (3) Both"
        switch ($editorChoice) {
            "2" { 
                $packages = $packages | Where-Object { $_ -ne "vscode" }
                $packages += "cursor"
            }
            "3" { 
                $packages += "cursor"
            }
        }
    }
    
    $manager = Get-PackageManager
    Install-PackageManager $manager
    
    foreach ($package in $packages) {
        Install-Package $package $manager
    }
    
    # Install VS Code extensions
    if (Test-Command "code") {
        Write-Info "Installing VS Code extensions..."
        $extensions = @(
            "ms-python.python",
            "ms-vscode.vscode-typescript-next",
            "bradlc.vscode-tailwindcss",
            "esbenp.prettier-vscode",
            "ms-vscode.vscode-json"
        )
        
        foreach ($extension in $extensions) {
            code --install-extension $extension
        }
    }
    
    # Install Cursor extensions (if Cursor is installed)
    if (Test-Command "cursor") {
        Write-Info "Installing Cursor extensions..."
        $extensions = @(
            "ms-python.python",
            "ms-vscode.vscode-typescript-next",
            "bradlc.vscode-tailwindcss",
            "esbenp.prettier-vscode",
            "ms-vscode.vscode-json"
        )
        
        foreach ($extension in $extensions) {
            cursor --install-extension $extension
        }
    }
    
    Write-Success "Web development stack installed successfully"
}

function Install-DataScienceStack {
    Write-Info "Installing data science stack..."
    
    $packages = @(
        "git",
        "python",
        "vscode",
        "jupyter",
        "anaconda3"
    )
    
    # Check if user wants Cursor instead of VS Code
    if (-not $NonInteractive) {
        $editorChoice = Read-Host "Choose your code editor: (1) VS Code (2) Cursor (3) Both"
        switch ($editorChoice) {
            "2" { 
                $packages = $packages | Where-Object { $_ -ne "vscode" }
                $packages += "cursor"
            }
            "3" { 
                $packages += "cursor"
            }
        }
    }
    
    $manager = Get-PackageManager
    Install-PackageManager $manager
    
    foreach ($package in $packages) {
        Install-Package $package $manager
    }
    
    # Install Python packages
    if (Test-Command "pip") {
        Write-Info "Installing Python data science packages..."
        $pythonPackages = @(
            "numpy",
            "pandas",
            "matplotlib",
            "seaborn",
            "scikit-learn",
            "jupyter"
        )
        
        foreach ($package in $pythonPackages) {
            pip install $package
        }
    }
    
    Write-Success "Data science stack installed successfully"
}

function Install-DotNetStack {
    Write-Info "Installing .NET development stack..."
    
    $packages = @(
        "git",
        "dotnet-sdk",
        "visualstudio2022community",
        "vscode",
        "sql-server-management-studio"
    )
    
    # Check if user wants Cursor instead of VS Code
    if (-not $NonInteractive) {
        $editorChoice = Read-Host "Choose your code editor: (1) VS Code (2) Cursor (3) Both"
        switch ($editorChoice) {
            "2" { 
                $packages = $packages | Where-Object { $_ -ne "vscode" }
                $packages += "cursor"
            }
            "3" { 
                $packages += "cursor"
            }
        }
    }
    
    $manager = Get-PackageManager
    Install-PackageManager $manager
    
    foreach ($package in $packages) {
        Install-Package $package $manager
    }
    
    Write-Success ".NET development stack installed successfully"
}

function Install-MobileDevStack {
    Write-Info "Installing mobile development stack..."
    
    $packages = @(
        "git",
        "nodejs",
        "vscode",
        "android-studio",
        "flutter"
    )
    
    # Check if user wants Cursor instead of VS Code
    if (-not $NonInteractive) {
        $editorChoice = Read-Host "Choose your code editor: (1) VS Code (2) Cursor (3) Both"
        switch ($editorChoice) {
            "2" { 
                $packages = $packages | Where-Object { $_ -ne "vscode" }
                $packages += "cursor"
            }
            "3" { 
                $packages += "cursor"
            }
        }
    }
    
    $manager = Get-PackageManager
    Install-PackageManager $manager
    
    foreach ($package in $packages) {
        Install-Package $package $manager
    }
    
    Write-Success "Mobile development stack installed successfully"
}

function Install-DevOpsStack {
    Write-Info "Installing DevOps stack..."
    
    $packages = @(
        "git",
        "docker-desktop",
        "kubernetes-cli",
        "terraform",
        "azure-cli",
        "vscode"
    )
    
    # Check if user wants Cursor instead of VS Code
    if (-not $NonInteractive) {
        $editorChoice = Read-Host "Choose your code editor: (1) VS Code (2) Cursor (3) Both"
        switch ($editorChoice) {
            "2" { 
                $packages = $packages | Where-Object { $_ -ne "vscode" }
                $packages += "cursor"
            }
            "3" { 
                $packages += "cursor"
            }
        }
    }
    
    $manager = Get-PackageManager
    Install-PackageManager $manager
    
    foreach ($package in $packages) {
        Install-Package $package $manager
    }
    
    Write-Success "DevOps stack installed successfully"
}

function Install-CustomPackages {
    param([string]$PackageList)
    
    Write-Info "Installing custom packages: $PackageList"
    
    $packages = $PackageList -split ","
    $manager = Get-PackageManager
    Install-PackageManager $manager
    
    foreach ($package in $packages) {
        $package = $package.Trim()
        if ($package) {
            Install-Package $package $manager
        }
    }
    
    Write-Success "Custom packages installed successfully"
}

function Install-FromFile {
    param([string]$FilePath)
    
    if (-not (Test-Path $FilePath)) {
        Write-Error "Package file not found: $FilePath"
        return
    }
    
    Write-Info "Installing packages from file: $FilePath"
    
    $packages = Get-Content $FilePath | Where-Object { $_ -and -not $_.StartsWith("#") }
    $manager = Get-PackageManager
    Install-PackageManager $manager
    
    foreach ($package in $packages) {
        $package = $package.Trim()
        if ($package) {
            Install-Package $package $manager
        }
    }
    
    Write-Success "Packages from file installed successfully"
}

function Show-Help {
    Write-Host @"
Windows Dev Environment Setup v$ScriptVersion

USAGE:
    .\setup.ps1 [OPTIONS]

OPTIONS:
    Development Stacks:
        --web-dev              Install web development stack
        --data-science         Install data science stack
        --dotnet               Install .NET development stack
        --mobile-dev           Install mobile development stack
        --devops               Install DevOps stack

    Execution Modes:
        --non-interactive      Run without prompts
        --debug                Enable debug mode
        --dry-run              Show what would be installed
        --force                Force installation without confirmation

    Package Managers:
        --choco                Use Chocolatey
        --scoop                Use Scoop
        --winget               Use Winget
        --auto                 Auto-detect (default)

    Custom Installation:
        --tools PACKAGES       Install specific packages (comma-separated)
        --custom FILE          Install packages from file

    Utilities:
        --help                 Show this help

EXAMPLES:
    .\setup.ps1 --web-dev
    .\setup.ps1 --data-science --non-interactive
    .\setup.ps1 --tools git,nodejs,python,vscode
    .\setup.ps1 --custom packages.txt
    .\setup.ps1 --web-dev --dry-run

"@
}

function Show-Status {
    Write-Info "Windows Dev Environment Status"
    Write-Host "=============================="
    Write-Host "Script Version: $ScriptVersion"
    Write-Host "Log File: $LogFile"
    Write-Host "Config File: $ConfigFile"
    Write-Host ""
    
    # Check installed tools
    $tools = @("git", "node", "python", "code", "docker")
    foreach ($tool in $tools) {
        if (Test-Command $tool) {
            Write-Success "$tool is installed"
        } else {
            Write-Warning "$tool is not installed"
        }
    }
}

function Initialize-Environment {
    # Create config directory
    $configDir = Split-Path $ConfigFile -Parent
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }
    
    # Set up environment variables
    Write-Info "Setting up environment variables..."
    
    # Add common paths
    $env:PATH += ";$env:USERPROFILE\AppData\Local\Programs\Microsoft VS Code\bin"
    $env:PATH += ";$env:USERPROFILE\AppData\Local\Programs\Python\Python39\Scripts"
    
    # Set Git editor
    if (Test-Command "code") {
        $env:GIT_EDITOR = "code --wait"
    }
    
    Write-Success "Environment initialized"
}

function Main {
    # Show banner
    Write-Host "Windows Dev Environment Setup v$ScriptVersion" -ForegroundColor $Colors.Cyan
    Write-Host "=============================================" -ForegroundColor $Colors.Cyan
    Write-Host ""
    
    # Initialize logging
    Write-Log "Starting Windows Dev Environment Setup"
    
    # Check if running as administrator
    if (-not (Test-Administrator)) {
        Write-Warning "Some installations may require administrator privileges"
        Write-Warning "Consider running PowerShell as Administrator for best results"
    }
    
    # Initialize environment
    Initialize-Environment
    
    # Handle help
    if ($Help) {
        Show-Help
        return
    }
    
    # Handle status
    if ($Stack -eq "status") {
        Show-Status
        return
    }
    
    # Determine what to install
    if ($Stack) {
        switch ($Stack.ToLower()) {
            "web-dev" { Install-WebDevStack }
            "data-science" { Install-DataScienceStack }
            "dotnet" { Install-DotNetStack }
            "mobile-dev" { Install-MobileDevStack }
            "devops" { Install-DevOpsStack }
            default {
                Write-Error "Unknown stack: $Stack"
                Write-Info "Available stacks: web-dev, data-science, dotnet, mobile-dev, devops"
                return
            }
        }
    }
    elseif ($Tools) {
        Install-CustomPackages $Tools
    }
    elseif ($CustomFile) {
        Install-FromFile $CustomFile
    }
    else {
        # Interactive mode
        Write-Info "No specific stack or tools specified. Starting interactive mode..."
        Write-Host ""
        Write-Host "Available development stacks:" -ForegroundColor $Colors.Yellow
        Write-Host "1. Web Development (Node.js, VS Code, browsers, Docker)"
        Write-Host "2. Data Science (Python, Jupyter, Anaconda)"
        Write-Host "3. .NET Development (Visual Studio, .NET SDK)"
        Write-Host "4. Mobile Development (Android Studio, Flutter)"
        Write-Host "5. DevOps (Docker, Kubernetes, Terraform)"
        Write-Host "6. Custom (Choose your own packages)"
        Write-Host ""
        
        $choice = Read-Host "Select a stack (1-6)"
        
        switch ($choice) {
            "1" { Install-WebDevStack }
            "2" { Install-DataScienceStack }
            "3" { Install-DotNetStack }
            "4" { Install-MobileDevStack }
            "5" { Install-DevOpsStack }
            "6" {
                $customTools = Read-Host "Enter packages (comma-separated)"
                Install-CustomPackages $customTools
            }
            default {
                Write-Error "Invalid choice"
                return
            }
        }
    }
    
    Write-Success "Setup completed successfully!"
    Write-Info "Check the log file for details: $LogFile"
}

# Run main function
Main
