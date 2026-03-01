# Quick Start: Template Customizer

## What's New?

The Template Customizer lets you change how text looks **without editing JSON files**. You can now:
- ✅ Change font (including Japanese fonts)
- ✅ Change font size
- ✅ Change text color
- ✅ Change text alignment
- ✅ See changes instantly in preview

---

## 5-Minute Tutorial

### 1. Launch the App
```bash
# macOS
open dist/ATEM\ Media\ Generator.app

# Windows
ATEM-Media-Generator.exe
```

### 2. Select a Template
Click on any template in the left panel:
- For English: "Simple Title" or "Lower Third - Name Only"
- For Japanese: "タイトル - 日本語" or "ロワーサード - 日本語"

### 3. Enter Parameters
In the middle panel, enter text for required fields (marked with *):
- For title templates: Enter your title text
- For lower-third templates: Enter name and optional title

**You should see the preview update on the right!**

### 4. Customize (NEW!)
Scroll down in the middle panel to see "Template Customizer"

For each text layer, you can change:

**Font** → Click dropdown, select new font
- Try: "ヒラギノ角ゴシック" (Japanese) or "Helvetica" (English)

**Size** → Adjust the slider or spin box
- Try: 48, 72, 96 (larger numbers = bigger text)

**Alignment** → Select left/center/right
- Try: "center" for centered titles

**Color** → Click color button, pick a new color
- Try: White [255, 255, 255], Gold [255, 200, 0], etc.

### 5. Preview Changes
As you adjust each setting, the preview on the right updates **instantly**!

### 6. Save Your Image
Once happy with the preview:
1. Click **Save PNG** button in toolbar
2. Choose where to save
3. Click Save

Done! Your customized image is saved. ✨

---

## Real-World Examples

### Example 1: Golden Title (English)

```
Template: "Simple Title"
Parameter: "Welcome to ATEM Media"

Customizer:
  Font: Helvetica
  Size: 80
  Color: Gold (255, 200, 0)
  Alignment: center
```

**Result**: Large golden title, centered

---

### Example 2: Japanese Lower Third

```
Template: "ロワーサード - 日本語"
Parameters:
  - name: 山田太郎
  - title: ニュースキャスター

Customizer (Name Layer):
  Font: ヒラギノ角ゴシック
  Size: 48
  Color: White (255, 255, 255)
  Alignment: left

Customizer (Title Layer):
  Font: ヒラギノゴシック
  Size: 32
  Color: Light Gray (220, 220, 220)
  Alignment: left
```

**Result**: Professional Japanese lower-third graphic

---

### Example 3: Red Alert (English)

```
Template: "Simple Title"
Parameter: "BREAKING NEWS"

Customizer:
  Font: Arial
  Size: 100
  Color: Red (255, 0, 0)
  Alignment: center
```

**Result**: Large red alert text

---

## Japanese Font Guide

### Available Japanese Fonts

**macOS** (built-in):
- ヒラギノ角ゴシック (Modern, clean)
- ヒラギノゴシック (Standard, readable)

**Windows**:
- Meiryo (日本語フォント - standard)
- MS 明朝 (日本語明朝 - serif style)

**Linux**:
- Use: "Noto Sans CJK" if installed

### How to Use Japanese Fonts

1. Select a template (English or Japanese)
2. Enter Japanese text in parameters
3. In Template Customizer, click Font dropdown
4. Select "ヒラギノ角ゴシック" or "ヒラギノゴシック"
5. Preview shows Japanese text with proper font

---

## Tips & Tricks

### Tip 1: Font Size for Text Fit
- Very large text (72+px): Good for titles
- Medium text (48px): Good for names
- Small text (32px): Good for subtitles/attributions

### Tip 2: Color Combinations
**Good Contrast**:
- White text on dark background
- Light gray on black
- Gold/orange on dark blue

**Avoid**:
- Light text on light background
- Similar brightness values

### Tip 3: Professional Look
- Use one main font per template
- Limit to 2-3 font sizes
- Use consistent colors
- Leave adequate spacing

### Tip 4: Multiple Variations Quickly
1. Generate image 1 with Font A
2. Save it
3. Change to Font B
4. Save as different filename
5. Compare both

### Tip 5: Batch Processing
If you need the SAME customizations for many images:
1. Create a custom template with your preferred settings
2. Save it as new `.json` file in `templates/`
3. Use that template for batch processing

---

## Common Questions

### Q: Do changes save to the template file?
**A**: No. Changes are temporary (per session).
- To save permanently: Edit the `.json` template file
- Or: Export the template by copying values to JSON

### Q: Can I use other fonts?
**A**: Yes, if installed on your system.
- Add font name to dropdown (by editing `ui/template_customizer.py`)
- Or: Edit template `.json` file directly

### Q: How do I change font weight?
**A**: Font weight (bold/regular) must be in the `.json` template.
- Not yet adjustable in Customizer
- Future version will add this

### Q: Why is my Japanese text showing as boxes?
**A**: Font not installed on your system.
- macOS: Check Font Book for Hiragino fonts
- Windows: Ensure Meiryo is in Fonts folder
- Linux: Install Noto Sans CJK fonts

### Q: Can I save customized templates?
**A**: Not yet through the UI.
- Workaround: Manually edit the `.json` template file
- Future version will add this feature

---

## Keyboard Shortcuts (Coming Soon!)

Currently not implemented, but planned:
- `Cmd/Ctrl + S`: Save image
- `Cmd/Ctrl + R`: Reset customizer to original
- `Cmd/Ctrl + Z`: Undo changes

---

## Troubleshooting

### Problem: Customizer doesn't appear
**Solution**:
1. Make sure a template is selected (left panel)
2. Scroll down in middle panel to find it
3. Restart application

### Problem: Font changes don't show
**Solution**:
1. Make sure text parameter is filled in
2. Check preview updates when you change size
3. Try different font to verify it's working

### Problem: Japanese text appears as boxes
**Solution**:
1. Select template that uses Japanese fonts
2. Select ヒラギノ角ゴシック or ヒラギノゴシック from dropdown
3. If still boxes, font may not be installed

### Problem: Color picker doesn't open
**Solution**:
1. Click directly on color button (not the label)
2. Button should change when clicked
3. Restart app if color dialog doesn't appear

---

## What's Next?

## Version 1.2 Planned Features
- Save customized templates as new templates
- Layer visibility toggle
- More Japanese font options
- Batch apply settings to all layers
- X/Y position adjustment

---

## Questions or Issues?

1. Check [TEMPLATE_CUSTOMIZER_GUIDE.md](TEMPLATE_CUSTOMIZER_GUIDE.md) for detailed info
2. Review [README.md](README.md) for general usage
3. Create a GitHub issue with your question

---

**Happy Customizing! 🎨**

[Back to Main Guide](README.md)
