###############################################################################
# runme.ps1 – Startup launcher for powercost_project (Python, pythonw.exe)
# Supports credentials passed from Task Scheduler using: -DbUser "x" -DbPass "y"
###############################################################################

param(
    [Parameter(Mandatory=$false)]
        [string]$POWERCOST_USER,
    [Parameter(Mandatory=$false)]
        [string]$POWERCOST_PASS
)

$now = Get-Date -Format "yyyyMMdd_HHmmss"

Write-Output "`n`nrunme.ps1: Script started at $now"

# Project paths
$projectSrcRoot  = "D:\git\powercost"
$projectExecRoot = "D:\u\apps\powercost"
$logDir          = Join-Path $projectExecRoot "logs"

# Ensure log directory exists
if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

# Transcript log (captures everything printed to screen)
$transcriptFile = Join-Path $logDir ("runme_" + $now + "_startup.txt")
Start-Transcript -Path $transcriptFile


###############################################################################
# 1. ENVIRONMENT VARIABLE HANDLING
###############################################################################
Write-Output "Checking DB environment variables..."

# Check for DB userid and password for MySQL database

if (-not $env:DPOWERCOST_USER -and $POWERCOST_USER) {
    Write-Output "Setting DB_USER from Task Scheduler arguments."
    $env:DPOWERCOST_USER = $POWERCOST_USER
}
elseif ($env:DPOWERCOST_USER) {
    Write-Output "DB_USER already set in environment."
}
else {
    Write-Error "WARNING: POWERCOST_USER is not set (and no argument provided)."
    exit 1
}

if (-not $env:POWERCOST_PASS -and $POWERCOST_PASS) {
    Write-Output "Setting POWERCOST_PASS from Task Scheduler arguments."
    $env:POWERCOST_PASS = $POWERCOST_PASS
}
elseif ($env:POWERCOST_PASS) {
    Write-Output "POWERCOST_PASS already set in environment."
}
else {
    Write-Error "WARNING: POWERCOST_PASS is not set (and no argument provided)."
    exit 1
}

###############################################################################
# 2. Python Setup
###############################################################################
$venvPython = Join-Path $projectSrcRoot "venv\Scripts\pythonw.exe"
$project = "-m powercost_project"
$iniFile = Join-Path $projectSrcRoot "ponderosa_electricity_usage.ini"

# Startup logs for Python process
$stdout = Join-Path $logDir ("runme_" + $now + "_stdout.txt")
$stderr = Join-Path $logDir ("runme_" + $now + "_stderr.txt")

Write-Output "Launching Python..."
Write-Output "projectSrcRoot   = $projectSrcRoot"
Write-Output "projectExecRoot  = $projectExecRoot"
Write-Output "venvPython       = $venvPython"
Write-Output "Project          = $project"
Write-Output "iniFile          = $iniFile"
Write-Output "stdout log       = $stdout"
Write-Output "stderr log       = $stderr"
Write-Output " "

###############################################################################
# 3. Build Start-Process options
###############################################################################

$processOptions = @{
    FilePath               = $venvPython
    ArgumentList           = "$project --ini `"$iniFile`""
    WorkingDirectory       = $projectSrcRoot
    NoNewWindow            = $true
    PassThru               = $true
    RedirectStandardOutput = $stdout
    RedirectStandardError  = $stderr
}

###############################################################################
# 4. Launch Python process
###############################################################################

try {
    Write-Output "Starting Python process..."
    $process = Start-Process @processOptions
    Write-Output "Process started with PID = $($process.Id)"
}
catch {
    Write-Error "FATAL: Could not start pythonw.exe. $_"
}

###############################################################################
# End Transcript
###############################################################################

Stop-Transcript
