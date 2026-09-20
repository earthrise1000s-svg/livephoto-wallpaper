# LivePhoto-Wallpaper 📸✨

> **Convert Videos into iPhone Dynamic Live Wallpapers**  
> 100% compatible authentic Live Photos for iOS 17+ dynamic lock screen wallpapers.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![iOS Tested](https://img.shields.io/badge/iOS-27%20Tested-success.svg)](https://apple.com/ios)
[![Zero External Assets](https://img.shields.io/badge/Assets-Zero%20Dependency%20(Pure%20Capsule)-brightgreen.svg)](#)

[English Documentation](README_EN.md) | [中文说明](README.md)

---

## 🌟 The Core Problem & Architectural Breakthrough

### Why do some iPhone Live Photos work as dynamic wallpapers while others fail?

Many iPhone users encounter this confusing issue: Native Live Photos shot on iPhone play fine in the Photos app, but when set as a lock screen wallpaper, some animate smoothly while others prompt "This Live Photo cannot be used"!

There are three main reasons:

- **Camera Shake Ban (Anti-Motion Sickness)**: Apple disables motion if the capture is shaky; only exceptionally smooth and steady Live Photos are permitted on the lock screen.
- **Cover and Video Start Desynchronization (Preventing Flicker)**: If the cover image deviates even slightly from timestamp 0, Apple outright disables the dynamic effect.
- **Missing Gyroscope Stabilization Metadata**: Standard conversion tools leave out the hardware motion vectors recorded by the iPhone camera.

---

### 💡 What Does This Tool Do?

Whatever video you bring (personal clips, anime scenes, movie edits):  
This tool **seamlessly injects 3-second, ultra-stable, smooth native iPhone camera profile and parameters into a Live Photo**, making Apple's lock screen engine 100% convinced that **"this is a pristine, ultra-stable Apple native Live Photo"**, smoothly activating the dynamic press-to-play wallpaper effect!

---

## 📊 Feature Comparison

| Feature | Conventional Converters / Apps | Typical Open Source Scripts | **LivePhoto-Wallpaper (Ours)** |
| :--- | :---: | :---: | :---: |
| **iOS 17+ Lock Screen Support** | ❌ Frequently fails or static | ⚠️ Inconsistent / stretching | **✅ 100% Genuine Apple Recognition** |
| **External Asset Dependency** | Requires heavy template files | Requires manual iPhone live photo | **✅ Zero dependency (25KB data capsule)** |
| **Video Compression Loss** | ⚠️ Re-encodes with quality loss | ⚠️ Re-encoding required | **✅ Passthrough stream copy (lossless)** |
| **Orientation & Aspect Ratio** | ❌ Distorts or adds black bars | ⚠️ Manual tweaking required | **✅ Normalized Orientation=1, auto-fit** |
| **1-Click Camera Roll Import** | Clunky manual saving in app | Requires AirDrop / split saving | **✅ iOS Shortcuts Magic Link import** |
| **AI Agent & CLI Ready** | ❌ GUI only | ⚠️ Fragmented scripts | **✅ Standard CLI + SKILL.md specification** |

---

## 🚀 Two Ways to Use

### Path A: 📱 Mobile AI Agent Chat (Recommended for everyday users!)

If you are using this tool via AI Agent chat clients, **you do not need to install anything or run any commands**. The synthesis is executed automatically by the backend AI:

1. **Add Companion Shortcut (Once only)**:  
   Tap to download and add the officially signed shortcut: 👉 **[【Live Photo Importer】Shortcut](https://github.com/earthrise1000s-svg/livephoto-wallpaper/raw/main/shortcuts/实况壁纸入库.shortcut)** (used for seamless, 1-click camera roll saving);
2. **Send Target Video**:  
   Directly send the video you want as your lock screen wallpaper in chat (if it's an existing Live Photo in your library, tap `...` and select **"Save as Video"** first);
3. **1-Click Save**:  
   Once generated, click the provided link to automatically invoke the Shortcut and instantly save the paired Live Photo into your camera roll!

---

### Path B: 💻 Developers / Local CLI (Batch Processing & Integration)

If you are a developer or want to batch-process videos locally on macOS/Linux:

1. **System Requirements (Developers only)**:
   ```bash
   # On macOS
   brew install exiftool
   ```

2. **Clone & Install**:
   ```bash
   git clone https://github.com/earthrise1000s-svg/livephoto-wallpaper.git
   cd livephoto-wallpaper
   pip install .
   ```

---

## ❓ FAQ

### Q1: Can I upload an existing Live Photo directly?
**Answer: Please export it as a video first!**  
When you select a Live Photo from your iPhone camera roll in web chats or messaging apps, iOS usually strips the video track and only transmits a static `.jpg`.  
**How to export**: In the iPhone Photos app, open the Live Photo, tap `...` in the top right, and choose **"Save as Video"**. Send that video to this tool to synthesize a brand-new, genuine Live Photo wallpaper!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
