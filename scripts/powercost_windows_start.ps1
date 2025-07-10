# =============================================================================
# Script ponderosa_electricity_usage.ps1
# =============================================================================
# Filename: ponderosa_electricity_usage.ps1
# Author: James Buck
# Created: 2025-06-264
# Last Modified: 2025-06-26
# Description: This script uses Start-Process to spawn a Python script via
#              pythonw.exe into the background in Windows.
# =============================================================================


# -------------------------
# Get INI file as parameter
# -------------------------
param (
    [Parameter(Mandatory=$true, HelpMessage="Specify the name of the INI file")]
    [string]$iniFile
)


# -------------
# Read INI File
# -------------
function Read-Ini ($filePath) {
    $ini = @{}
    $section = "NoSection" # Default section for keys before any explicit section
    switch -regex -file $filePath {
        "^\[(.+)\]$" { # Matches section headers like [SectionName]
            $section = $matches[1]
            $ini[$section] = @{}
        }
        "^(;.*)$" {} #Ignore Comments
        "(.+?)\s*=\s*(.*)" { # Matches key-value pairs like Key = Value
            $name,$value = $matches[1..2]
            if (!($ini.ContainsKey($section))) { $ini[$section] = @{} } # Ensure section exists
            $ini[$section][$name] = $value.Trim() # Trim whitespace from value
        }
    }
    return $ini
}


# Read INI settings
# -----------------
$iniSettings  = Read-Ini $iniFile

$run_dir = $iniSettings["powershell"]["run_dir"]
Set-Location -Path $run_dir

$python_script = $iniSettings["powershell"]["python_script"]

# Usually = pythonw.exe to rRun without DOS terminal window on Windows
$python_exec = $iniSettings["powershell"]["python_exec"]

# Set timestamp to be used in the log file.
$ts   = Get-Date -Format "yyyyMMdd-HHmm"
$log = $run_dir + "\logs\PEU_$ts" + "_Startup.txt"
$log_start_stdout = $run_dir + "\logs\PEU_$ts" + "_stdout.txt"
$log_start_stderr = $run_dir + "\logs\PEU_$ts" + "_stderr.txt"

$now   = Get-Date -Format "MM/dd/yyyy HH:mm:ss"

# Run Python Script
# -----------------
$Stream = [System.IO.StreamWriter]::new($log)
$Stream.WriteLine("ponderosa_electricty_usage.ps1: Script entered.")
$Stream.WriteLine("   TIME           = $now")
$Stream.WriteLine("   run_dir        = $run_dir")
$Stream.WriteLine("   python_exec    = $python_exec")
$Stream.WriteLine("   python_script  = $python_script")
$Stream.WriteLine("   log            = $log")
$Stream.WriteLine("   iniFile        = $iniFile")

# Redirect standard output to the StreamWriter
[System.Console]::SetOut($Stream)

$processOptions = @{
    FilePath = $python_exec
    ArgumentList = "$python_script --ini $iniFile"
    WorkingDirectory = $run_dir
    NoNewWindow = $true
    PassThru = $true
    RedirectStandardOutput = $log_start_stdout
    RedirectStandardError = $log_start_stderr
}
$process = Start-Process @processOptions

$Stream.WriteLine("   PID            = " + $process.Id)
$Stream.WriteLine("   Name           = " + $process.Name)
$Stream.Close()

exit
