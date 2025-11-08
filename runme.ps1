# Powershell Script: runme.ps1

# Path to your project root (adjust as needed)
$projectSrcRoot = "D:\git\powercost"
$projecExectRoot = "D:\u\apps\powercost"

# Full path to the venv pythonw.exe
$venvPython = Join-Path $projectSrcRoot "venv\Scripts\pythonw.exe"

# Runtime parameters
$project = "-m powercost_project"
$iniFile = Join-Path $projectSrcRoot "ponderosa_electricity_usage.ini"
$logDir  = Join-Path $projecExectRoot "logs"

# Startup Log (Running output is in a different log)
if (!(Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$log_start_stdout = Join-Path $logDir "powercost_stdout.txt"
$log_start_stderr = Join-Path $logDir "powercost_stderr.txt"

# Build process options
$processOptions = @{
    FilePath = $venvPython
    ArgumentList = "$project --ini `"$iniFile`""
    WorkingDirectory = $projectSrcRoot
    NoNewWindow = $true
    PassThru = $true
    RedirectStandardOutput = $log_start_stdout
    RedirectStandardError = $log_start_stderr
}

# Launch the process
$process = Start-Process @processOptions
$mypid = $process.Id

Write-Output "Process started with PID = $mypid"
Write-Output "==> Press Enter to continue..."
Read-Host
