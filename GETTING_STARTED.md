```
░▒█▀▀▀░░▀░░█░░█▀▀░░░▒█▀▀▀░░▀░░█▀▀░█░░░░█▀▀░█▀▀▄
░▒█▀▀░░░█▀░█░░█▀▀░░░▒█▀▀░░░█▀░▀▀▄░█▀▀█░█▀▀░█▄▄▀
░▒█░░░░▀▀▀░▀▀░▀▀▀░░░▒█░░░░▀▀▀░▀▀▀░▀░░▀░▀▀▀░▀░▀▀
```

# 🔰 Complete Beginner's Guide - Start Here!

**Never used GitHub or command line before? No problem! This guide explains EVERYTHING step-by-step.**

---

## What Does This Program Do?

This program automatically downloads public government documents from the DOJ website about the Epstein case. Instead of clicking and saving thousands of files one by one, this does it all for you!

**You'll see a menu like this:**

![Interactive Menu](docs/images/interactive-menu.png)

---

## Step 1: Download This Program from GitHub

1. **Go to**: https://github.com/KowaiAI/Epstein_File_fisher
2. **Look at the top-right** - You'll see a green button that says **"<> Code"**
3. **Click that green button**
4. **Click "Download ZIP"** at the bottom of the menu
5. **Wait for the download** - It's a small file, about 100 KB
6. **Find the downloaded file** - It's probably in your "Downloads" folder
   - The file is named: `Epstein_File_fisher-main.zip`

---

## Step 2: Put the Files Somewhere Safe

1. **Open your "Documents" folder**
   - **Windows**: Click the folder icon on your taskbar, then click "Documents"
   - **Mac**: Open Finder, click "Documents" on the left
   - **Linux**: Open your file manager, go to Documents

2. **Move the ZIP file to Documents**
   - Drag `Epstein_File_fisher-main.zip` from Downloads to Documents

3. **Right-click on the ZIP file**
4. **Click "Extract All" or "Extract Here"** (the exact wording depends on your computer)
5. **You'll see a new folder** called `Epstein_File_fisher-main`
6. **Optional**: Rename it to just `Epstein_File_fisher` (remove the `-main` part) to make it simpler

---

## Step 3: Open the Command Line (Terminal)

**This is the black/white window where you type commands. Don't worry, we'll tell you exactly what to type!**

### Windows Users:
1. Press the **Windows key** (bottom left of keyboard, looks like ⊞)
2. Type: `cmd`
3. Press **Enter**
4. A black window will open - this is **Command Prompt** ✅

### Mac Users:
1. Press **Command + Space** (at the same time)
2. Type: `terminal`
3. Press **Enter**
4. A window will open - this is **Terminal** ✅

### Linux Users:
1. Press **Ctrl + Alt + T** (all at the same time)
2. A window will open - this is **Terminal** ✅

---

## Step 4: Go to the Folder You Just Extracted

**Now we need to "move" into the folder using the command line:**

**Type these commands EXACTLY as shown and press Enter after each line:**

### Windows:
```cmd
cd Documents\Epstein_File_fisher-main
```

### Mac/Linux:
```bash
cd Documents/Epstein_File_fisher-main
```

**If you renamed the folder** (removed `-main`), use this instead:

### Windows:
```cmd
cd Documents\Epstein_File_fisher
```

### Mac/Linux:
```bash
cd Documents/Epstein_File_fisher
```

💡 **Tip**: If you see an error like "cannot find the path", make sure:
- You extracted the ZIP file
- You moved it to Documents folder
- The folder name matches exactly what you type

---

## Step 5: Install Python (If You Don't Have It)

**Python is the language this program is written in. You need it installed on your computer.**

### Check if you already have Python:

**Windows - Type this:**
```cmd
python --version
```

**Mac/Linux - Type this:**
```bash
python3 --version
```

**If you see something like "Python 3.12.1" or "Python 3.8.10"** - Great! ✅ Skip to Step 6.

**If you see an error like "command not found"**, you need to install Python:

### How to Install Python:

1. **Open your web browser** (Chrome, Firefox, Safari, Edge)
2. **Go to**: https://www.python.org/downloads/
3. **Click the big yellow button** that says **"Download Python"**
4. **Run the downloaded file** (usually in Downloads folder)
5. **⚠️ SUPER IMPORTANT**: Check the box that says **"Add Python to PATH"**
   - This is at the BOTTOM of the first screen
   - If you miss this, Python won't work!
6. **Click "Install Now"**
7. **Wait 2-3 minutes** for installation
8. **Click "Close"** when done
9. **Close and reopen your command line window** (close the black window and open it again)
10. **Try the version command again** to make sure it worked

---

## Step 6: Set Up the Program (Only Do This Once)

**This downloads the helper tools the program needs. You only do this ONCE!**

### Windows:
Type this and press Enter:
```cmd
scripts\setup.bat
```

### Mac/Linux:
Type these commands one at a time, pressing Enter after each:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**What's happening?**
- Creating a "virtual environment" (safe space for the program)
- Downloading helper libraries (requests, beautifulsoup, etc.)
- Takes about 1-2 minutes
- You'll see text scrolling - this is normal!
- When it says "Setup complete!" you're ready ✅

---

## Step 7: Run the Program!

**Now the fun part - actually running it!**

### Windows:
```cmd
run.bat
```

### Mac/Linux:
```bash
chmod +x run.sh
./run.sh
```

**You should see the FILE FISHER menu appear!** 🎉

---

## Step 8: Choose What to Download

You'll see a menu with options 1-12 (each data set) plus 99 (all) and 0 (exit).

### To Test First (RECOMMENDED):
1. Type: `1`
2. Press Enter
3. Type: `n` (for "no more data sets")
4. Press Enter

This downloads only Data Set 1 (about 50 files, 5-10 minutes). Good for testing!

### To Download Everything:
1. Type: `99`
2. Press Enter

This downloads ALL 12 data sets (thousands of files, several HOURS!)

### To Pick Specific Sets:
1. Type the number (like `8`)
2. Press Enter
3. It asks: "Add another data set? (yes/no)"
4. Type `yes` to add more, or `no` when you're done

**The program will show you:**
```
Download Configuration:
  Data Sets: [8]
  Output Directory: /home/YourName/Documents/Epstein
  Download Files: True
```

Press Enter to start!

---

## Step 9: Wait for Download

**You'll see progress bars like this:**
```
Data Set 8: 45%|████▌     | 29/64 [02:30<02:50, 4.87s/it]
```

**What this means:**
- 45% = Almost halfway done
- 29/64 = Downloaded 29 files out of 64 total
- 02:30 = 2 minutes 30 seconds so far
- 02:50 = About 2 minutes 50 seconds remaining

**IMPORTANT:**
- **DO NOT close the window!**
- You can minimize it and do other things
- Don't shut down your computer
- Keep internet connected

**How long will it take?**
- 1 data set: 15-30 minutes
- All 12 sets: 2-6 hours (depends on your internet speed)

---

## Step 10: Find Your Downloaded Files

1. **Open your file manager**
   - Windows: Click folder icon on taskbar
   - Mac: Open Finder
   - Linux: Open Files

2. **Go to your Documents folder**

3. **Open the "Epstein" folder**

4. **You'll see folders like:**
   ```
   Documents/Epstein/
   ├── data_set_1/
   ├── data_set_2/
   ├── data_set_8/
   └── ...
   ```

5. **Inside each data set folder:**
   ```
   data_set_8/
   ├── documents/    ← PDF files here
   ├── videos/       ← MP4, MOV files here
   ├── audio/        ← MP3 files here
   ├── images/       ← JPG, PNG files here
   └── archives/     ← ZIP files here
   ```

---

## ❓ Common Problems and Solutions

### Problem: "python is not recognized" (Windows)

**What happened**: You didn't check "Add Python to PATH" during installation.

**How to fix**:
1. Go to Control Panel → Programs → Uninstall a program
2. Find Python and uninstall it
3. Download Python again from python.org
4. This time, CHECK THE BOX that says "Add Python to PATH" (bottom of first screen)
5. Install again
6. Restart your command prompt

---

### Problem: "Permission denied" (Mac/Linux)

**What happened**: The script doesn't have permission to run.

**How to fix**:
```bash
chmod +x scripts/setup.sh
chmod +x run.sh
```

Then try running again.

---

### Problem: "No such file or directory"

**What happened**: You're not in the right folder.

**How to fix**:
1. **Check where you are:**
   - Windows: Type `cd` and press Enter
   - Mac/Linux: Type `pwd` and press Enter
2. **You should see**: `C:\Users\YourName\Documents\Epstein_File_fisher-main` (or similar)
3. **If not**, type the `cd Documents\Epstein_File_fisher-main` command again
4. **Make sure the folder name matches** (with or without `-main`)

---

### Problem: Program stops or shows errors

**What happened**: Network hiccup, server busy, or temporary issue.

**How to fix**:
1. Press **Ctrl+C** to stop the program
2. Run it again: `run.bat` (Windows) or `./run.sh` (Mac/Linux)
3. Choose the same data sets
4. **The program is smart!** It will skip files you already downloaded and continue where it left off

---

### Problem: "Not enough space on device"

**What happened**: You need about 150 GB of free space for ALL data sets.

**How to check your space:**
- Windows: Right-click C: drive → Properties
- Mac: Click Apple menu → About This Mac → Storage
- Linux: Open Disks application

**Solutions**:
- **Download one data set at a time** instead of all
- **Buy an external hard drive** (USB drive with lots of space)
- **Delete other large files** (old videos, games, etc.)
- **Choose which data sets you actually need** instead of downloading all

---

### Problem: Internet keeps disconnecting

**How to fix**:
1. Connect to a stable Wi-Fi network
2. If using mobile hotspot, make sure you have enough data
3. Plug in ethernet cable if possible (faster and more stable)
4. If it stops, just run again - program will continue where it left off

---

### Problem: Program seems "stuck"

**What's probably happening**:
- Large video files take several minutes EACH
- The program is still working, just slowly

**How to tell if it's still working:**
- Look at the progress bar - is the percentage slowly increasing?
- Look at your Epstein folder - are new files appearing?

**If truly frozen:**
1. Wait 5 minutes first (some files are huge!)
2. If still nothing, press Ctrl+C
3. Run again

---

## 🔄 How to Run It Again Later

**You don't need to set up again! The setup was a one-time thing.**

**Just do this:**

1. **Open command line** (same as Step 3)
2. **Go to the folder:**
   - Windows: `cd Documents\Epstein_File_fisher-main`
   - Mac/Linux: `cd Documents/Epstein_File_fisher-main`
3. **Run it:**
   - Windows: `run.bat`
   - Mac/Linux: `./run.sh`

That's it! The menu will appear and you can download more data sets.

---

## 📊 Understanding Data Sets

**What are data sets?**
Each data set is a batch of files released by the DOJ at different times.

**Which ones should I download?**
- If you're a researcher: Probably all of them
- If you're curious: Start with Data Set 1 to see what's there
- If you have limited space: Pick specific sets based on dates or content

**Can I download more later?**
Yes! You can run the program again anytime and pick different sets. Already-downloaded files will be skipped.

---

## 🆘 Still Need Help?

1. **Read the error message carefully** - It usually tells you what's wrong
2. **Check you followed every step exactly** - Even small typos matter
3. **Try Google** - Copy the error message and search for it
4. **Ask a tech-savvy friend or family member** - Show them this guide
5. **Visit your local library** - Many have free tech help

---

## 📚 Additional Resources

- **[Full Documentation](docs/)** - More detailed guides
- **[CSV Method Guide](docs/CSV_METHOD.txt)** - Alternative download method
- **[Interactive Menu Guide](docs/INTERACTIVE_MENU.txt)** - Menu details

---

**You've got this! Take your time, read carefully, and don't be afraid to try. The program won't break your computer - worst case, you just have to run it again.** 🚀

---

**Repository**: https://github.com/KowaiAI/Epstein_File_fisher

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
