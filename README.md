# Spotify Ad Skipper 
A very light macOS tool that automatically skips Spotify ads by detecting when one plays, instantly quitting and relaunching Spotify, then playign your music.

---
### 
Do NOT use Spotify in Split Screen for this program to work

## How it works
Spotify's ad track IDs always start with `spotify:ad:`. The script polls Spotify every ~0.8 seconds via AppleScript. The moment an ad is detected, it:
1. Force-quits Spotify
2. Relaunches it
3. Resumes playback

**Typical skip time: ~Less than 0.8 seconds**

---

## Requirements
- macOS
- Python 3
- Spotify (free tier)

---

## Setup

**1. Download `spotify_ad_skipper.py` and place it in your Downloads folder**

**2. Create a double-clickable launcher on your Desktop:**
```bash
echo '#!/bin/bash
python3 ~/Downloads/spotify_ad_skipper.py' > ~/Desktop/Spotify_ad_skipper.command && chmod +x ~/Desktop/Spotify_ad_skipper.command
```

**3. Double-click `Spotify_ad_skipper` on your Desktop**

That's it. It will open Spotify and start skipping ads automatically.

> On first run, macOS may ask for permission to control Spotify — click Allow.

---

## Usage
- **Start:** Double-click `Spotify_ad_skipper` on your Desktop
- **Stop:** Close the Terminal window that opens

---

## Notes
- This tool automates what you'd do manually (quitting and reopening Spotify to skip ads)
- It does not modify any Spotify files
- Consider supporting artists by upgrading to Spotify Premium
Do NOT use Spotify in Split Screen for this program to work

---

*Made by nedathar*
