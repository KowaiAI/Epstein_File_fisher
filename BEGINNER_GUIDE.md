```
░▒█▀▀▀░░▀░░█░░█▀▀░░░▒█▀▀▀░░▀░░█▀▀░█░░░░█▀▀░█▀▀▄
░▒█▀▀░░░█▀░█░░█▀▀░░░▒█▀▀░░░█▀░▀▀▄░█▀▀█░█▀▀░█▄▄▀
░▒█░░░░▀▀▀░▀▀░▀▀▀░░░▒█░░░░▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░▀▀
```

# 🔰 Complete Beginner's Guide to DOJ Epstein Files Scraper

**This guide is written for people who are not familiar with computers or technical terms. Follow each step exactly as written.**

---

## 📋 Table of Contents

1. [What Does This Program Do?](#what-does-this-program-do)
2. [What You Need Before Starting](#what-you-need-before-starting)
3. [Step-by-Step Instructions](#step-by-step-instructions)
   - [Windows Users](#for-windows-users)
   - [Mac Users](#for-mac-users)
   - [Linux Users](#for-linux-users)
4. [What to Expect](#what-to-expect)
5. [Troubleshooting Problems](#troubleshooting-problems)
6. [Frequently Asked Questions](#frequently-asked-questions)

---

## What Does This Program Do?

This program automatically downloads public documents from the U.S. Department of Justice website about the Jeffrey Epstein case. Instead of clicking and saving thousands of files one by one, this program does it all for you automatically.

**Important:** These are public government documents that anyone can access. This program simply makes it easier to download them all at once.

---

## What You Need Before Starting

### 1. **A Computer**
   - Windows, Mac, or Linux computer
   - At least **150 GB of free space** on your hard drive
   - Internet connection (faster is better)

### 2. **Python** (This is free software that runs the program)
   - Don't worry if you don't have it yet - we'll help you install it below

### 3. **Time**
   - Setup: 10-15 minutes
   - Downloading all files: 2-6 hours (you can leave it running)

### 4. **Patience**
   - This guide explains everything step-by-step
   - If something doesn't work, check the "Troubleshooting" section at the end

---

## Step-by-Step Instructions

## For Windows Users

### Step 1: Install Python

1. **Open your web browser** (Internet Explorer, Edge, Chrome, or Firefox)

2. **Go to this website:** `https://www.python.org/downloads/`

3. **Click the big yellow button** that says **"Download Python"**
   - This will download a file (about 25 MB)

4. **Find the downloaded file** (usually in your Downloads folder)
   - It will be named something like `python-3.12.1-amd64.exe`

5. **Double-click the file** to start installation

6. **IMPORTANT:** On the first screen, check the box that says **"Add Python to PATH"**
   - This is a small checkbox at the bottom
   - If you miss this, Python won't work!

7. **Click "Install Now"**
   - Wait for installation to complete (2-3 minutes)

8. **Click "Close"** when done

### Step 2: Download the Scraper Program

1. **Open File Explorer** (the folder icon on your taskbar)

2. **Go to your Documents folder**
   - You can click "Documents" on the left side

3. **Create a new folder called "Epstein-Scraper"**
   - Right-click → New → Folder
   - Type the name: `Epstein-Scraper`
   - Press Enter

4. **Download the scraper files:**
   - Option A: If you received a ZIP file, extract it into the `Epstein-Scraper` folder
   - Option B: If you received individual files, copy them all into the `Epstein-Scraper` folder

### Step 3: Open Command Prompt

1. **Click the Windows Start button** (bottom-left corner)

2. **Type:** `cmd`

3. **Press Enter**
   - A black window will open - this is called "Command Prompt"
   - Don't be scared! This is where we'll type commands

### Step 4: Navigate to the Scraper Folder

In the black Command Prompt window, type these commands **exactly** and press Enter after each one:

```cmd
cd Documents
cd Epstein-Scraper
```

**What this does:** Moves you into the folder where the scraper program is located.

### Step 5: Set Up the Program Environment

Type this command and press Enter:

```cmd
python -m venv venv
```

**Wait:** This might take 30-60 seconds. You'll see text scrolling by.

**What this does:** Creates a safe space for the program to run without affecting other programs on your computer.

### Step 6: Activate the Environment

Type this command and press Enter:

```cmd
venv\Scripts\activate
```

**You'll know it worked when:** Your command prompt now starts with `(venv)`

Example: `(venv) C:\Users\YourName\Documents\Epstein-Scraper>`

### Step 7: Install Required Components

Type this command and press Enter:

```cmd
pip install -r requirements.txt
```

**Wait:** This will take 1-2 minutes. You'll see lots of text.

**What this does:** Downloads additional software pieces the program needs to work.

### Step 8: Run the Scraper

**IMPORTANT CHOICE:**

**Option A - Test First (Recommended for beginners):**
```cmd
python scraper.py --data-sets 1
```
This downloads only the first set of files (about 3,000 files) as a test.

**Option B - Download Everything:**
```cmd
python scraper.py
```
This downloads all 12 sets (about 38,000+ files). This takes several hours!

**After typing the command, press Enter and wait...**

---

## For Mac Users

### Step 1: Check if Python is Installed

1. **Open Spotlight** (press Command + Space)

2. **Type:** `terminal`

3. **Press Enter**
   - A window with text will open

4. **Type this and press Enter:**
```bash
python3 --version
```

5. **If you see something like "Python 3.12.1":**
   - Python is already installed! Skip to Step 2.

6. **If you see "command not found":**
   - You need to install Python

**To install Python:**
1. Open Safari (your web browser)
2. Go to: `https://www.python.org/downloads/`
3. Click "Download Python"
4. Open the downloaded file
5. Follow the installation wizard

### Step 2: Download the Scraper Program

1. **Open Finder**

2. **Go to Documents**

3. **Create a new folder called "Epstein-Scraper"**

4. **Copy all the scraper files into this folder**

### Step 3: Open Terminal

1. **Open Spotlight** (Command + Space)

2. **Type:** `terminal`

3. **Press Enter**

### Step 4: Navigate to the Scraper Folder

Type these commands **exactly** and press Enter after each one:

```bash
cd Documents
cd Epstein-Scraper
```

### Step 5: Set Up the Program Environment

```bash
python3 -m venv venv
```

**Wait:** 30-60 seconds

### Step 6: Activate the Environment

```bash
source venv/bin/activate
```

**You'll know it worked when:** Your terminal prompt starts with `(venv)`

### Step 7: Install Required Components

```bash
pip install -r requirements.txt
```

**Wait:** 1-2 minutes

### Step 8: Run the Scraper

**Test first (recommended):**
```bash
python scraper.py --data-sets 1
```

**Or download everything:**
```bash
python scraper.py
```

---

## For Linux Users

### Step 1: Open Terminal

- **Ubuntu/Debian:** Press Ctrl + Alt + T
- **Or:** Search for "Terminal" in your applications

### Step 2: Install Python (if needed)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

Enter your password when asked.

### Step 3: Navigate to Documents

```bash
cd ~/Documents
mkdir Epstein-Scraper
cd Epstein-Scraper
```

### Step 4: Download Scraper Files

Copy all scraper files into the `~/Documents/Epstein-Scraper/` folder

### Step 5: Set Up Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 6: Run the Scraper

**Test first:**
```bash
python scraper.py --data-sets 1
```

**Or download everything:**
```bash
python scraper.py
```

---

## What to Expect

### When the Program Starts:

1. **You'll see text appearing** in the window
   - This is normal! The program is telling you what it's doing

2. **You'll see progress bars** that look like this:
   ```
   Data Set 1: 45%|████▌     | 29/64 [02:30<02:50, 4.87s/it]
   ```
   - The percentage shows how much is done
   - Don't close the window!

3. **The program will create folders** automatically:
   - Windows: `C:\Users\YourName\Documents\Epstein\`
   - Mac: `/Users/YourName/Documents/Epstein/`
   - Linux: `/home/YourName/Documents/Epstein/`

### What Gets Downloaded:

Files are organized like this:
```
Documents/
└── Epstein/
    ├── data_set_1/
    │   ├── documents/    (PDF files)
    │   ├── videos/       (MP4, MOV files)
    │   ├── audio/        (MP3 files)
    │   ├── images/       (JPG, PNG files)
    │   └── archives/     (ZIP files)
    ├── data_set_2/
    └── ... (up to data_set_12)
```

### How Long Will It Take?

- **Test (1 data set):** 15-30 minutes
- **Full download (all 12 sets):** 2-6 hours depending on your internet speed

**Can I leave it running?**
- YES! You can minimize the window and do other things
- The program will keep working in the background
- Don't shut down your computer or close the window

### How Will I Know It's Done?

When finished, you'll see:
```
2026-02-06 15:30:45,123 [INFO] Scraping complete!
2026-02-06 15:30:45,124 [INFO] Total documents found: 38,247
```

---

## Troubleshooting Problems

### Problem: "Python is not recognized" (Windows)

**Solution:**
1. Uninstall Python
2. Reinstall Python
3. **Make sure** to check "Add Python to PATH" during installation

### Problem: "Permission denied"

**Solution:**
- Windows: Right-click Command Prompt and "Run as Administrator"
- Mac/Linux: Add `sudo` before commands and enter your password

### Problem: "No space left on device"

**Solution:**
- You need at least 150 GB of free space
- Check your hard drive space
- Delete other files or use an external hard drive

### Problem: Program stops with errors

**Solution:**
1. Close the program (press Ctrl+C)
2. Run it again with the same command
3. The program will skip already-downloaded files and continue

### Problem: "403 Forbidden" errors

**Explanation:** The DOJ website may be detecting automated downloads and blocking them.

**Solutions:**
1. **Wait and try again later** (maybe in a few hours or tomorrow)
2. **Use slower settings:** The program already waits 2 seconds between requests, but you can increase this
3. **Download one set at a time:**
   ```bash
   python scraper.py --data-sets 1
   python scraper.py --data-sets 2
   # ... etc
   ```
   Wait a day between each set

### Problem: Downloaded files won't open

**Solution:**
- Make sure you have a PDF reader installed
- Try a different PDF reader (Adobe Reader, Foxit, etc.)
- Some files might be corrupted - try downloading that specific set again

---

## Frequently Asked Questions

### Is this legal?
**Yes!** These are public documents released by the U.S. government. Anyone can access them.

### Will this harm my computer?
**No.** This program only downloads files from a government website. It doesn't install anything harmful.

### Can I stop and restart?
**Yes!** If you close the program, you can run it again later. It will skip files you already downloaded.

### How much internet data will this use?
Downloading all files will use **50-150 GB** of internet data. If you have a data cap, be aware of this.

### Can I use the computer while it's downloading?
**Yes!** Just don't close the black window (Command Prompt/Terminal). You can use other programs.

### What if I only want specific files?
You can download one data set at a time:
```bash
python scraper.py --data-sets 3
```
Replace `3` with any number 1-12.

### Where exactly are my files?

**Windows:**
1. Open File Explorer
2. Go to "This PC" → "Documents" → "Epstein"

**Mac:**
1. Open Finder
2. Go to your home folder → "Documents" → "Epstein"

**Linux:**
1. Open Files
2. Go to Home → "Documents" → "Epstein"

### Can I change where files are saved?

**Yes!** Add `--output-dir` to the command:

**Windows:**
```cmd
python scraper.py --output-dir D:\MyFolder\Epstein
```

**Mac/Linux:**
```bash
python scraper.py --output-dir /path/to/folder
```

### The program seems stuck. What do I do?

**Wait:** Some files are very large (videos especially) and may take several minutes each.

**Check:** Look for the progress percentage. If it's moving (even slowly), it's working.

**If truly stuck:**
1. Press Ctrl+C to stop
2. Run the command again

---

## Getting Help

If you're still having trouble:

1. **Read the error message carefully**
   - Copy the last few lines of text
   - Search Google for that error message

2. **Check your internet connection**
   - Make sure you can access other websites

3. **Try the test command first**
   - `python scraper.py --data-sets 1`
   - This downloads less and helps identify problems faster

4. **Ask for help**
   - Have a tech-savvy friend or family member look at this guide
   - Bring your computer to a local library (they often have tech help)

---

## Summary Cheat Sheet

### Windows Quick Start
```cmd
cd Documents\Epstein-Scraper
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scraper.py --data-sets 1
```

### Mac/Linux Quick Start
```bash
cd Documents/Epstein-Scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scraper.py --data-sets 1
```

---

**You're ready to start! Take your time, follow each step carefully, and don't worry if you need to read through the instructions multiple times. Good luck!** 🍀
