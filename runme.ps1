# runme.ps1

$project = "-m powercost_project"

$iniFile = "D:\u\apps\powercost\ponderosa_electricity_usage.ini"

$log_start_stdout = "logs/powercost_stdout.txt"
$log_start_stderr = "logs/powercost_stderr.txt"

$PSScriptRoot = "D:\git\powercost"
$venvPython = "$PSScriptRoot\venv\Scripts\pythonw.exe" &
    & $venvPython -m powercost_project

$processOptions = @{
    FilePath = "pythonw.exe"
    ArgumentList = "$project --ini $iniFile"
    WorkingDirectory = "."
    NoNewWindow = $true
    PassThru = $true
    RedirectStandardOutput = $log_start_stdout
    RedirectStandardError = $log_start_stderr
}
$process = Start-Process @processOptions
$mypid = $process.Id

Write-Output "Code sumitted, PID = $mypid"
Write-Output "==> Press Enter to continue..."

Read-Host # Waits for the user to press Enter

#Cannot overwrite variable PID because it is read-only or constant.
#At D:\u\apps\powercost\runme.ps1:18 char:1
#+ $pid = $process.Id
#+ ~~~~~~~~~~~~~~~~~~
#    + CategoryInfo          : WriteError: (PID:String) [], SessionStateUnauthorizedAccessException
#    + FullyQualifiedErrorId : VariableNotWritable
#
#Code sumitted, PID = 25280
#==> Press Enter to continue...
