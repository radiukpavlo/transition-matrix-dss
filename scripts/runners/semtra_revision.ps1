[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("setup", "setup-vision", "run-v1", "run-v2", "run-v3", "latex", "latex-v3", "qc", "qc-v3", "all", "all-v3")]
    [string]$Command = "all",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
$VenvPip = Join-Path $Root ".venv\Scripts\pip.exe"
$LatexPluginRoot = "C:\Users\radiu\.codex\plugins\cache\openai-bundled\latex\0.2.2"
$LatexPluginScript = Join-Path $LatexPluginRoot "scripts\compile_latex.py"
$V2Root = Join-Path $Root "outputs\revision_v2"
$V3Root = Join-Path $Root "outputs\revision_v3"
$LatexOut = Join-Path $V2Root "latex"

function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Get-Python {
    if (Test-Path -LiteralPath $VenvPython) {
        return $VenvPython
    }
    return "python"
}

function Invoke-Logged {
    param(
        [string]$Exe,
        [string[]]$Arguments,
        [string]$LogPath,
        [switch]$AllowFailure,
        [string]$WorkingDirectory = $Root
    )
    Ensure-Directory -Path (Split-Path -Parent $LogPath)
    Push-Location $WorkingDirectory
    try {
        & $Exe @Arguments 2>&1 | Tee-Object -FilePath $LogPath
        $exitCode = $LASTEXITCODE
        if (($exitCode -ne 0) -and (-not $AllowFailure)) {
            throw "Command failed with exit code ${exitCode}: $Exe $($Arguments -join ' ')"
        }
        return $exitCode
    }
    finally {
        Pop-Location
    }
}

function Stop-ProcessTree {
    param([int]$ProcessId)
    $children = Get-CimInstance Win32_Process | Where-Object { $_.ParentProcessId -eq $ProcessId }
    foreach ($child in $children) {
        Stop-ProcessTree -ProcessId $child.ProcessId
    }
    $proc = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
    if ($null -ne $proc) {
        Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
    }
}

function Invoke-LoggedProcess {
    param(
        [string]$Exe,
        [string[]]$Arguments,
        [string]$LogPath,
        [switch]$AllowFailure,
        [string]$WorkingDirectory = $Root,
        [int]$TimeoutSeconds = 180
    )
    Ensure-Directory -Path (Split-Path -Parent $LogPath)
    $stdout = "${LogPath}.stdout"
    $stderr = "${LogPath}.stderr"
    Remove-Item -LiteralPath $stdout, $stderr -Force -ErrorAction SilentlyContinue
    $proc = Start-Process -FilePath $Exe -ArgumentList $Arguments -WorkingDirectory $WorkingDirectory -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru -WindowStyle Hidden
    if (-not $proc.WaitForExit($TimeoutSeconds * 1000)) {
        Stop-ProcessTree -ProcessId $proc.Id
        "Command timed out after ${TimeoutSeconds}s: $Exe $($Arguments -join ' ')" | Out-File -FilePath $LogPath -Encoding utf8
        if (Test-Path -LiteralPath $stdout) { Get-Content -LiteralPath $stdout | Out-File -FilePath $LogPath -Append -Encoding utf8 }
        if (Test-Path -LiteralPath $stderr) { Get-Content -LiteralPath $stderr | Out-File -FilePath $LogPath -Append -Encoding utf8 }
        if (-not $AllowFailure) {
            throw "Command timed out after ${TimeoutSeconds}s: $Exe $($Arguments -join ' ')"
        }
        return 124
    }
    $content = @()
    if (Test-Path -LiteralPath $stdout) { $content += Get-Content -LiteralPath $stdout }
    if (Test-Path -LiteralPath $stderr) { $content += Get-Content -LiteralPath $stderr }
    $content | Out-File -FilePath $LogPath -Encoding utf8
    $exitCode = $proc.ExitCode
    if ($null -eq $exitCode) {
        $exitCode = 0
    }
    if (($exitCode -ne 0) -and (-not $AllowFailure)) {
        throw "Command failed with exit code ${exitCode}: $Exe $($Arguments -join ' ')"
    }
    return $exitCode
}

function Invoke-Setup {
    if (-not (Test-Path -LiteralPath $VenvPython)) {
        & python -m venv (Join-Path $Root ".venv")
    }
    & $VenvPython -m pip install --upgrade pip
    if (Test-Path -LiteralPath (Join-Path $Root "requirements.txt")) {
        & $VenvPip install -r (Join-Path $Root "requirements.txt")
    }
    $importCheck = @'
import importlib
mods = ['numpy', 'pandas', 'scipy', 'sklearn', 'matplotlib', 'pyarrow', 'h5py', 'PIL']
optional = ['torch', 'torchvision']
missing = []
for mod in mods:
    try:
        importlib.import_module(mod)
    except Exception as exc:
        missing.append('{}: {}'.format(mod, exc))
for mod in optional:
    try:
        importlib.import_module(mod)
        print('optional {}: present'.format(mod))
    except Exception as exc:
        print('optional {}: unavailable ({})'.format(mod, exc))
if missing:
    raise SystemExit('Missing required imports: ' + '; '.join(missing))
print('required scientific imports: ok')
'@
    & $VenvPython -c $importCheck
}

function Invoke-SetupVision {
    Invoke-Setup
    $py = Get-Python
    $visionCheck = @'
import importlib
missing = []
for mod in ['torch', 'torchvision']:
    try:
        importlib.import_module(mod)
    except Exception as exc:
        missing.append('{}: {}'.format(mod, exc))
if missing:
    raise SystemExit('; '.join(missing))
import torch, torchvision
print('torch={}'.format(torch.__version__))
print('torchvision={}'.format(torchvision.__version__))
'@
    & $py -c $visionCheck
    if ($LASTEXITCODE -ne 0) {
        & $py -m pip install torch torchvision
        if ($LASTEXITCODE -ne 0) {
            $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
            if ($null -ne $pyLauncher) {
                & py -3.12 -m venv (Join-Path $Root ".venv-vision")
                if ($LASTEXITCODE -eq 0) {
                    $visionPython = Join-Path $Root ".venv-vision\Scripts\python.exe"
                    & $visionPython -m pip install --upgrade pip
                    & $visionPython -m pip install -r (Join-Path $Root "requirements.txt")
                    & $visionPython -m pip install torch torchvision
                    if ($LASTEXITCODE -eq 0) {
                        & $visionPython -c $visionCheck
                        return
                    }
                }
            }
            throw "Unable to install torch/torchvision in .venv or fallback .venv-vision."
        }
    }
    & $py -c $visionCheck
}

function Invoke-RunV1 {
    $py = Get-Python
    $v1Manifest = Join-Path $Root "outputs\revision_v1\manifest_revision_v1.json"
    if ((Test-Path -LiteralPath $v1Manifest) -and (-not $Force)) {
        Write-Host "revision_v1 already present; preserving existing v1 artifacts."
        return
    }
    $args = @((Join-Path $Root "scripts\runners\run_revision_v1.py"))
    if ($Force) {
        $args += "--force-rebuild"
    }
    & $py @args
    if ($LASTEXITCODE -ne 0) {
        throw "run_revision_v1.py failed with exit code $LASTEXITCODE"
    }
}

function Invoke-RunV2 {
    $py = Get-Python
    $args = @((Join-Path $Root "scripts\runners\run_revision_v2.py"))
    if ($Force) {
        $args += "--force-rebuild"
    }
    & $py @args
    if ($LASTEXITCODE -ne 0) {
        throw "run_revision_v2.py failed with exit code $LASTEXITCODE"
    }
}

function Get-VisionPython {
    $py = Get-Python
    $visionPython = Join-Path $Root ".venv-vision\Scripts\python.exe"
    if (Test-Path -LiteralPath $visionPython) {
        & $py -c "import torch, torchvision" 2>$null
        if ($LASTEXITCODE -ne 0) {
            return $visionPython
        }
    }
    return $py
}

function Invoke-RunV3 {
    $py = Get-VisionPython
    $args = @((Join-Path $Root "scripts\runners\run_revision_v3.py"))
    if ($Force) {
        $args += "--force-rebuild"
    }
    & $py @args
    if ($LASTEXITCODE -ne 0) {
        throw "run_revision_v3.py failed with exit code $LASTEXITCODE"
    }
}

function Invoke-Latex {
    Ensure-Directory -Path $LatexOut
    $py = Get-Python
    $statusRecords = @()
    foreach ($stem in @("main", "supply")) {
        $tex = Join-Path $Root "manuscript\${stem}.tex"
        $pluginLog = Join-Path $LatexOut "plugin_${stem}_compile.log"
        $pluginExit = $null
        if (Test-Path -LiteralPath $LatexPluginScript) {
            $pluginExit = Invoke-LoggedProcess -Exe $py -Arguments @($LatexPluginScript, $tex) -LogPath $pluginLog -AllowFailure -WorkingDirectory $LatexPluginRoot -TimeoutSeconds 90
        }
        else {
            "LaTeX plugin compiler script not found: $LatexPluginScript" | Out-File -FilePath $pluginLog -Encoding utf8
            $pluginExit = 127
        }

        $work = Join-Path $Root "manuscript"
        $fallbackStatus = "pass"
        $fallbackError = ""
        try {
            Invoke-LoggedProcess -Exe "pdflatex" -Arguments @("-interaction=nonstopmode", "-halt-on-error", "${stem}.tex") -LogPath (Join-Path $LatexOut "${stem}_pdflatex_pass1.log") -WorkingDirectory $work -TimeoutSeconds 120 | Out-Null
            Invoke-LoggedProcess -Exe "bibtex" -Arguments @($stem) -LogPath (Join-Path $LatexOut "${stem}_bibtex.log") -WorkingDirectory $work -TimeoutSeconds 120 | Out-Null
            Invoke-LoggedProcess -Exe "pdflatex" -Arguments @("-interaction=nonstopmode", "-halt-on-error", "${stem}.tex") -LogPath (Join-Path $LatexOut "${stem}_pdflatex_pass2.log") -WorkingDirectory $work -TimeoutSeconds 120 | Out-Null
            Invoke-LoggedProcess -Exe "pdflatex" -Arguments @("-interaction=nonstopmode", "-halt-on-error", "${stem}.tex") -LogPath (Join-Path $LatexOut "${stem}_pdflatex_pass3.log") -WorkingDirectory $work -TimeoutSeconds 120 | Out-Null
        }
        catch {
            $fallbackStatus = "degraded_existing_archive_reused"
            $fallbackError = $_.Exception.Message
        }

        foreach ($ext in @(".pdf", ".log", ".aux", ".bbl", ".blg", ".out", ".toc")) {
            $src = Join-Path $work "${stem}${ext}"
            $useSrc = $src
            if ((-not (Test-Path -LiteralPath $useSrc)) -or ((Get-Item -LiteralPath $useSrc).Length -eq 0)) {
                $archive = Join-Path $Root "outputs\revision_v1\latex\${stem}${ext}"
                if (Test-Path -LiteralPath $archive) {
                    $useSrc = $archive
                }
            }
            if (Test-Path -LiteralPath $useSrc) {
                Copy-Item -LiteralPath $useSrc -Destination (Join-Path $LatexOut "${stem}${ext}") -Force
            }
        }
        $statusRecords += [pscustomobject]@{
            stem = $stem
            plugin_exit_code = $pluginExit
            fallback_status = $fallbackStatus
            fallback_error = $fallbackError
        }
    }
    $status = [pscustomobject]@{
        generated_at = (Get-Date).ToUniversalTime().ToString("o")
        plugin_attempted_first = $true
        fallback_attempted = $true
        note = "If local fallback times out, existing successful revision LaTeX PDFs/logs are reused for the active archive."
        records = $statusRecords
    }
    $status | ConvertTo-Json -Depth 5 | Out-File -FilePath (Join-Path $LatexOut "latex_status.json") -Encoding utf8
}

function Invoke-LatexV3 {
    $oldLatexOut = $script:LatexOut
    $script:LatexOut = Join-Path $V3Root "latex"
    try {
        Invoke-Latex
    }
    finally {
        $script:LatexOut = $oldLatexOut
    }
}

function Invoke-QC {
    $py = Get-Python
    & $py (Join-Path $Root "scripts\runners\run_revision_v2.py") --validate-only --require-v2
    if ($LASTEXITCODE -ne 0) {
        throw "revision_v2 validation failed with exit code $LASTEXITCODE"
    }
}

function Invoke-QCV3 {
    $py = Get-VisionPython
    & $py (Join-Path $Root "scripts\runners\run_revision_v3.py") --validate-only
    if ($LASTEXITCODE -ne 0) {
        throw "revision_v3 validation failed with exit code $LASTEXITCODE"
    }
}

switch ($Command) {
    "setup" {
        Invoke-Setup
    }
    "setup-vision" {
        Invoke-SetupVision
    }
    "run-v1" {
        Invoke-RunV1
    }
    "run-v2" {
        Invoke-RunV2
    }
    "run-v3" {
        Invoke-RunV3
    }
    "latex" {
        Invoke-Latex
    }
    "latex-v3" {
        Invoke-LatexV3
    }
    "qc" {
        Invoke-QC
    }
    "qc-v3" {
        Invoke-QCV3
    }
    "all" {
        Invoke-Setup
        Invoke-RunV1
        Invoke-Latex
        Invoke-RunV2
        Invoke-QC
    }
    "all-v3" {
        Invoke-SetupVision
        Invoke-RunV3
        Invoke-LatexV3
        Invoke-RunV3
        Invoke-QCV3
    }
}
