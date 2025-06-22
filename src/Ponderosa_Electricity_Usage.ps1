# =============================================================================
# Script Ponderosa_Electricity_Usage.ps1
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
# "D:\u\apps\powercost\Ponderosa_Electricity_Usage.ini"

$rundir = $iniSettings["powershell"]["rundir"]
Set-Location -Path $rundir

$python_script = $rundir + "\" + $iniSettings["powershell"]["python_script"]

# Usually = pythonw.exe to rRun without DOS terminal window on Windows
$python_exec = $iniSettings["powershell"]["python_exec"]

# Set timestamp to be used in the log file.
$ts   = Get-Date -Format "yyyyMMdd-HHmm"
$log = $rundir + "\logs\PEU_$ts" + "_Startup.txt"

# Run Python Script
# -----------------
$Stream = [System.IO.StreamWriter]::new($log)
$Stream.WriteLine("Ponderosa_Electricty_Usage.ps1: Script entered.")
$Stream.WriteLine("   rundir         = $rundir")
$Stream.WriteLine("   python_exec    = $python_exec")
$Stream.WriteLine("   python_script  = $python_script")
$Stream.WriteLine("   log            = $log")
$Stream.WriteLine("   iniFile        = $iniFile")

# Redirect standard output to the StreamWriter
[System.Console]::SetOut($Stream)

$processOptions = @{
    FilePath = $python_exec
    ArgumentList = "$python_script --ini $iniFile"
    WorkingDirectory = $rundir
    NoNewWindow = $true
    PassThru = $true
}
$process = Start-Process @processOptions

$Stream.WriteLine("   PID            = " + $process.Id)
$Stream.WriteLine("   Name           = " + $process.Name)
$Stream.Close()

exit
