```
░▒█▀▀▀░░▀░░█░░█▀▀░░░▒█▀▀▀░░▀░░█▀▀░█░░░░█▀▀░█▀▀▄
░▒█▀▀░░░█▀░█░░█▀▀░░░▒█▀▀░░░█▀░▀▀▄░█▀▀█░█▀▀░█▄▄▀
░▒█░░░░▀▀▀░▀▀░▀▀▀░░░▒█░░░░▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░▀▀
```

# Platform-Specific Notes

## ✅ Fully Cross-Platform

This scraper works on **Windows**, **macOS**, and **Linux** with no code changes needed.

## Python Path Objects

The scraper uses Python's `pathlib.Path` which automatically handles:
- Forward slashes on Linux/Mac (`/`)
- Backslashes on Windows (`\`)
- Home directory expansion (`~`)
- Drive letters on Windows (`C:\`)

## Default Download Locations

| OS | Default Path |
|----|--------------|
| **Linux** | `/home/username/Documents/Epstein/` |
| **macOS** | `/Users/username/Documents/Epstein/` |
| **Windows** | `C:\Users\username\Documents\Epstein\` |

## Custom Output Directory

You can override the default location on any platform:

**Linux/Mac:**
```bash
python scraper.py --output-dir /mnt/external/Epstein
python scraper.py --output-dir ~/Desktop/Epstein
```

**Windows:**
```cmd
python scraper.py --output-dir D:\Data\Epstein
python scraper.py --output-dir %USERPROFILE%\Desktop\Epstein
```

## Virtual Environment Activation

| OS | Command |
|----|---------|
| **Linux/Mac** | `source venv/bin/activate` |
| **Windows (CMD)** | `venv\Scripts\activate` |
| **Windows (PowerShell)** | `venv\Scripts\Activate.ps1` |

**Note:** On Windows PowerShell, you may need to enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## File Path Differences

The scraper handles these automatically, but for reference:

**Linux/Mac:**
```
~/Documents/Epstein/data_set_1/documents/EFTA00000001.pdf
```

**Windows:**
```
C:\Users\YourName\Documents\Epstein\data_set_1\documents\EFTA00000001.pdf
```

## Disk Space Requirements

Estimated space needed for all 12 data sets:
- **Conservative estimate**: 50-100 GB
- **Safe estimate**: 150 GB free space recommended

Check available space before starting:

**Linux/Mac:**
```bash
df -h ~/Documents
```

**Windows:**
```cmd
wmic logicaldisk get size,freespace,caption
```

## Performance Considerations

### Network Speed
- **Slow connection**: Use `--data-sets 1` to test first
- **Fast connection**: Full scrape should complete in 2-6 hours

### Rate Limiting
The scraper includes 1-second delays between requests to be respectful to DOJ servers. This is intentional and should not be changed.

## Troubleshooting

### Windows: "python not recognized"
Try `py` instead of `python`:
```cmd
py -m venv venv
py scraper.py
```

### Windows: Permission Denied
Run Command Prompt or PowerShell as Administrator

### All: SSL Certificate Errors
Update your Python's SSL certificates:
```bash
pip install --upgrade certifi
```

### All: Out of Disk Space
Use `--data-sets` to download only specific sets:
```bash
python scraper.py --data-sets 1 2 3
```

## Testing

Test the scraper on any platform with:
```bash
# Quick test (downloads only Data Set 1)
python scraper.py --data-sets 1

# Metadata-only test (no downloads)
python scraper.py --no-download
```

## Cloud Storage

If using cloud storage (Dropbox, OneDrive, Google Drive):

**Recommended:**
```bash
# Download to cloud-synced folder
python scraper.py --output-dir ~/Dropbox/Epstein
python scraper.py --output-dir "C:\Users\YourName\OneDrive\Epstein"
```

**Note:** Large files may take time to sync. Consider using `--data-sets` to download in batches.
