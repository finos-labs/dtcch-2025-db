# Installing pytesseract Correctly

## Overview
[`pytesseract`](https://github.com/madmaze/pytesseract) is a Python wrapper for [Tesseract OCR](https://github.com/tesseract-ocr/tesseract), which allows you to extract text from images. Before using `pytesseract`, you must install Tesseract OCR properly.

---

## 1️⃣ Install Tesseract OCR

### **🔹 macOS (Homebrew)**
```sh
brew install tesseract
```

### **🔹 Windows**
1. Download the latest Tesseract OCR installer from:
   👉 [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer and follow the setup instructions.
3. Add Tesseract to your system `PATH` (usually found at `C:\Program Files\Tesseract-OCR\`).
4. Verify installation:
   ```sh
   tesseract --version
   ```

### **🔹 Linux (Ubuntu/Debian)**
```sh
sudo apt update && sudo apt install -y tesseract-ocr
```

### **🔹 Linux (Arch Linux)**
```sh
sudo pacman -S tesseract-ocr
```

---

## 2️⃣ Install `pytesseract`
After installing Tesseract OCR, install `pytesseract` via pip:
```sh
pip install pytesseract
```

---

## 3️⃣ Set Tesseract Path (Windows Only)
If Tesseract is not found automatically, you must specify its path in Python:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```

---

## 4️⃣ Verify Installation
Run the following Python code to check if `pytesseract` is working correctly:

```python
import pytesseract
from PIL import Image

image = Image.open("sample.png")  # Replace with a valid image path
text = pytesseract.image_to_string(image)
print(text)
```

If everything is set up correctly, it should output extracted text from the image. 🎉

---

## 5️⃣ Troubleshooting
### **🔸 'TesseractNotFoundError' or 'OSError'**
- Ensure Tesseract is installed and added to `PATH` (Windows users).
- On Windows, manually set the Tesseract path as shown in Step 3.

### **🔸 'ModuleNotFoundError: No module named pytesseract'**
- Ensure `pytesseract` is installed:
  ```sh
  pip install pytesseract
  ```

### **🔸 Fontconfig Download Errors (macOS/Linux)**
- Try installing Fontconfig manually:
  ```sh
  brew install fontconfig  # macOS
  sudo apt install fontconfig  # Ubuntu/Debian
  ```

---

## 🎯 Summary
✅ Install **Tesseract OCR** for your OS  
✅ Install `pytesseract` via `pip install pytesseract`  
✅ Set the correct Tesseract path (Windows)  
✅ Run a test script to verify installation  

🚀 Now you're ready to extract text from images using Python!

