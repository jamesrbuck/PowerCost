# Powershell Script: runme.ps1

# Path to your project root (adjust as needed)
$projectSrcRoot = "D:\git\powercost"
$projectExecRoot = "D:\u\apps\powercost"
$logDir  = Join-Path $projectExecRoot "logs"

$runme_log = Join-Path $logDir "runme.txt"
Start-Transcript -Path $runme_log -Append

$venvPython = Join-Path $projectSrcRoot "venv\Scripts\pythonw.exe"
$project = "-m powercost_project"
$iniFile = Join-Path $projectSrcRoot "ponderosa_electricity_usage.ini"

# Startup Log (Running output is in a different log)
if (!(Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$log_start_stdout = Join-Path $logDir "runme_stdout.txt"
$log_start_stderr = Join-Path $logDir "runme_stderr.txt"

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

Write-Output "projectSrcRoot   = $projectSrcRoot"
Write-Output "projectExecRoot  = $projectExecRoot"
Write-Output "venvPython       = $venvPython"
Write-Output "Project          = $project"
Write-Output "iniFile          = $iniFile"
Write-Output "logDir           = $logDir"
Write-Output "log_start_stdout = $log_start_stdout"
Write-Output "log_start_stderr = $log_start_stderr"
Write-Output " "

# Launch the process
$process = Start-Process @processOptions
$mypid = $process.Id

Write-Output "Process Options = $processOptions\n"
Write-Output "Process started with PID = $mypid"
