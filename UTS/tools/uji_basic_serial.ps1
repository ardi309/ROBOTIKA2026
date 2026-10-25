# Jalankan setelah operator siap, piringan bebas, dan Serial Monitor ditutup.
# Mode default hanya menguji parser saat OFF. Mode variasi-berjalan menyalakan motor.
param(
    [ValidateSet('perintah', 'variasi-berjalan')][string]$Mode = 'perintah',
    [string]$Port = 'COM5',
    [ValidateRange(10, 15)][int]$StepSeconds = 15
)
$ErrorActionPreference = 'Stop'
$taskModule = Join-Path (Split-Path -Parent $PSScriptRoot) '01_Basic_iMCLab'
$taskLog = Join-Path $taskModule ('data\basic_' + $Mode + '_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
$taskLines = [System.Collections.Generic.List[string]]::new()
$taskSerial = [System.IO.Ports.SerialPort]::new($Port, 115200, [System.IO.Ports.Parity]::None, 8, [System.IO.Ports.StopBits]::One)
$taskSerial.NewLine = "`n"
$taskSerial.ReadTimeout = 200
$taskSerial.WriteTimeout = 500
$taskSerial.DtrEnable = $false
$taskSerial.RtsEnable = $false
$taskStopConfirmed = $false
$taskInterrupted = $false
function Write-TaskLog([string]$Text) {
    $taskEntry = (Get-Date -Format 'o') + ' ' + $Text
    $taskLines.Add($taskEntry)
    Write-Host $taskEntry
}
function Read-TaskLine {
    try {
        $taskLine = $taskSerial.ReadLine().Trim()
        if ($taskLine) { Write-TaskLog ('RX ' + $taskLine) }
        return $taskLine
    } catch [System.TimeoutException] { return '' }
}
function Send-TaskCommand([string]$Command, [string]$Expected) {
    Write-TaskLog ('TX ' + $Command)
    $taskSerial.WriteLine($Command)
    $taskAckWatch = [System.Diagnostics.Stopwatch]::StartNew()
    while ($taskAckWatch.Elapsed.TotalSeconds -lt 2) {
        $taskReply = Read-TaskLine
        if ($taskReply -match $Expected) { return }
        if ($taskReply.StartsWith('ERR ')) { throw $taskReply }
    }
    throw "No matching acknowledgement for command $Command."
}
try {
    $taskSerial.Open()
    $taskSerial.DiscardInBuffer()
    Write-TaskLog "Basic serial experiment; mode=$Mode; $Port; 115200 baud; step=$StepSeconds seconds; no-pulse cutoff=3 seconds."
    Send-TaskCommand '0' '^ACK PWM=0 SET=\d+ '
    if ($Mode -eq 'perintah') {
        $taskChecks = @(
            @('PWM:200', '^ACK PWM=0 SET=200 '),
            @('-', '^ACK PWM=0 SET=190 '),
            @('+', '^ACK PWM=0 SET=200 '),
            @('PWM:0', '^ACK PWM=0 SET=0 '),
            @('PWM:255', '^ACK PWM=0 SET=255 '),
            @('PWM:256', '^ERR PWM must be 0\.\.255$'),
            @('R', '^STATUS PWM=0 SET=255 '),
            @('abc', '^ERR use 0, 1, \+, -, PWM:0\.\.255, R$'),
            @('PWM:200', '^ACK PWM=0 SET=200 '),
            @('R', '^STATUS PWM=0 SET=200 ')
        )
        foreach ($taskCheck in $taskChecks) {
            Send-TaskCommand $taskCheck[0] $taskCheck[1]
            Write-TaskLog ('CHECK PASS ' + $taskCheck[0])
        }
        Write-TaskLog 'RESULT all command checks passed with motor output OFF.'
    } else {
        # Mulai sekali dari OFF; setpoint berikutnya diubah tanpa mematikan motor.
        # Ini mengukur respons saat berjalan, bukan kemampuan start setiap PWM.
        Send-TaskCommand 'PWM:200' '^ACK PWM=0 SET=200 '
        $taskTotalWatch = [System.Diagnostics.Stopwatch]::StartNew()
        $taskLastPulseTime = 0.0
        Send-TaskCommand '1' '^ACK PWM=200 SET=200 '
        foreach ($taskPwm in @(200, 160, 120, 80)) {
            if ($taskPwm -ne 200) {
                Send-TaskCommand ('PWM:' + $taskPwm) ('^ACK PWM=' + $taskPwm + ' SET=' + $taskPwm + ' ')
            }
            Write-TaskLog "PHASE PWM=$taskPwm; requested duration=$StepSeconds seconds; motor stays enabled between phases."
            $taskPhaseWatch = [System.Diagnostics.Stopwatch]::StartNew()
            while ($taskPhaseWatch.Elapsed.TotalSeconds -lt $StepSeconds) {
                $taskData = Read-TaskLine
                if ($taskData -match '^DATA .* PULSES=(\d+) ' -and [int]$Matches[1] -gt 0) {
                    $taskLastPulseTime = $taskTotalWatch.Elapsed.TotalSeconds
                }
                if (($taskTotalWatch.Elapsed.TotalSeconds - $taskLastPulseTime) -ge 3) {
                    Write-TaskLog "EARLY STOP PWM=${taskPwm}: no detected pulses for 3 seconds; later phases skipped."
                    $taskInterrupted = $true
                    break
                }
            }
            if ($taskInterrupted) { break }
            Write-TaskLog "PHASE COMPLETE PWM=$taskPwm"
        }
        if (-not $taskInterrupted) { Write-TaskLog 'RESULT all four running-PWM phases completed.' }
    }
} catch {
    Write-TaskLog ('ERROR ' + $_.Exception.Message)
    throw
} finally {
    if ($taskSerial.IsOpen) {
        try {
            Send-TaskCommand '0' '^ACK PWM=0 SET=\d+ '
            $taskStopConfirmed = $true
            $taskCoastWatch = [System.Diagnostics.Stopwatch]::StartNew()
            while ($taskCoastWatch.Elapsed.TotalSeconds -lt 4) { $null = Read-TaskLine }
        } catch {
            Write-TaskLog 'STOP NOT CONFIRMED: operator must disconnect motor power.'
        } finally {
            $taskSerial.Close()
        }
    }
    $taskSerial.Dispose()
    $taskLines | Set-Content -LiteralPath $taskLog -Encoding utf8
    Write-Host "Saved: $taskLog"
}
if (-not $taskStopConfirmed) { throw 'Motor OFF was not confirmed.' }
