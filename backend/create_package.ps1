# Define the package directory
$PackageDir = "package"

# Remove any existing package directory to start fresh
Remove-Item -Path $PackageDir -Recurse -Force -ErrorAction Ignore

# Create a new package directory
New-Item -ItemType Directory -Path $PackageDir

# Install Python dependencies from requirements.txt into the package directory
pip install -r requirements.txt --target $PackageDir

# Copy Python files to the package directory. Adjust the copy command as needed for your project structure.
Get-ChildItem -Path "." -Filter "*.py" | Copy-Item -Destination $PackageDir

# Optionally, remove compiled Python files (.pyc) and __pycache__ directories to clean up
Get-ChildItem -Path $PackageDir -Recurse -Filter "*.pyc" | Remove-Item
Get-ChildItem -Path $PackageDir -Recurse -Directory -Name "__pycache__" | ForEach-Object { Remove-Item -Path "$PackageDir\$_" -Recurse -Force }

# Change to the package directory
Push-Location -Path $PackageDir

# Zip the contents of the package directory
Compress-Archive -Path "*" -DestinationPath "../deployment-package.zip" -Force

# Move back to the original directory
Pop-Location

# Optionally, clean up by removing the package directory if no longer needed
# Remove-Item -Path $PackageDir -Recurse -Force

# Echo a message to indicate completion
Write-Output "Deployment package created: deployment-package.zip"
