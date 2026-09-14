while ($true) {

    Write-Host "Checking GitHub..."

    git fetch origin

    $local = git rev-parse HEAD
    $remote = git rev-parse origin/main

    if ($local -ne $remote) {

        Write-Host "New code detected!"
        git pull origin main

        Write-Host "Running updated program..."
        python hello.py

    }
    else {
        Write-Host "No update."
    }

    Start-Sleep -Seconds 10
}
