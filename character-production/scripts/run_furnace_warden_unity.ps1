param([ValidateSet('Build','Review','Play','Avatar')] [string]$Stage='Review')
$ErrorActionPreference='Stop'
$characterRoot=Split-Path -Parent $PSScriptRoot
$project=Join-Path $characterRoot 'unity-validation'
$folder=Join-Path $characterRoot 'evidence/diagnostics/furnace-warden-unity'
New-Item -ItemType Directory -Force -Path $folder | Out-Null
$version=(Select-String -Path "$project/ProjectSettings/ProjectVersion.txt" -Pattern '^m_EditorVersion: (.+)$').Matches[0].Groups[1].Value
$editor=Join-Path $env:ProgramFiles "Unity/Hub/Editor/$version/Editor/Unity.exe"
$method=@{Build='FurnaceWardenBuild.Run';Review='FurnaceWardenReview.Run';Play='FurnaceWardenReview.TestPlay';Avatar='FurnaceWardenAvatar.Inspect'}[$Stage]
$log=Join-Path $folder ("unity-"+$Stage.ToLowerInvariant()+".log")
$arguments=@('-batchmode','-force-d3d11','-projectPath',('"'+$project+'"'),'-executeMethod',$method,'-logFile',('"'+$log+'"'))
if($Stage -ne 'Play'){$arguments+='-quit'}
$proc=Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle Hidden -PassThru
if(-not $proc.WaitForExit(420000)){
    if(-not $proc.HasExited){Stop-Process -Id $proc.Id -Force}
    throw "The owned Unity $Stage process timed out. See $log"
}
if($proc.ExitCode -ne 0){Get-Content $log -Tail 18;throw "Unity $Stage exited $($proc.ExitCode). See $log"}
Write-Output "Unity $Stage completed."

