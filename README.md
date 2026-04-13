# 🚀 CAPTCHA Recognition & Automated Tender Download System

## 📌 Project Overview

This project is an AI-powered automation system designed to bypass CAPTCHA-protected tender websites and automatically download tender documents. It integrates deep learning-based CAPTCHA recognition with browser automation to streamline data extraction.

---

## 🎯 Key Features

* 🔐 CAPTCHA recognition using deep learning (PyTorch)
* 🤖 Automated tender website navigation using browser automation
* 📥 Automatic PDF downloading and file management
* 🧠 Intelligent workflow for handling multi-page tender data
* 🗄️ Database integration for storing and managing records

---

## 🛠️ Tech Stack

* Python
* PyTorch
* OpenCV
* Selenium (Browser Automation)
* NumPy / Pandas
* SQL (Database)

---

## 📂 Project Structure

```
.
├── main.py                     # Main execution script
├── config.py                   # Configuration settings
├── requirements.txt            # Dependencies

├── captcha_model_files/        # Trained model & config
│   ├── captcha_model.pth
│   └── captcha_config.json

├── Captcha_solver/             # CAPTCHA prediction logic
│   └── captcha_predict.py

├── automation/                 # Automation scripts
│   ├── open_site.py
│   ├── click_detail.py
│   ├── download_pdf.py
│   ├── next_page.py
│   └── ...

├── browser/                    # Browser driver setup
│   └── chrome_driver.py

├── database/                   # Database operations
│   ├── db_connection.py
│   ├── save_to_db.py
│   └── db.sql
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR-USERNAME/Auto-download-system-captcha-recognize.git
cd Auto-download-system-captcha-recognize
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Setup Requirements

* Install **Google Chrome**
* Download **ChromeDriver** (matching your Chrome version)
* Update driver path in:

```python
browser/chrome_driver.py
```

---

## ▶️ How to Run

```bash
python main.py
```

👉 This will:

* Open the tender website
* Solve CAPTCHA automatically
* Navigate through pages
* Download tender PDFs
* Store results

---

## 🧠 How It Works

1. **CAPTCHA Solver**

   * Uses trained deep learning model to predict CAPTCHA text

2. **Automation Engine**

   * Selenium controls browser actions:

     * Open website
     * Fill CAPTCHA
     * Navigate pages

3. **Download System**

   * Automatically downloads tender documents (PDF)

4. **Database Handling**

   * Stores and manages downloaded data

---

## ⚠️ Notes

* Dataset is not included due to size
* Ensure stable internet connection
* CAPTCHA accuracy depends on training quality

---

## 🚀 Future Improvements

* Deploy using FastAPI for API-based usage
* Improve CAPTCHA accuracy with larger dataset
* Add dashboard for monitoring downloads
* Integrate cloud storage (AWS/GCP)

---

## 👨‍💻 Author

**Ayush Gaudani**
AI/ML Engineer

---

## ⭐ Use Case

This system is highly useful for:

* Tender data extraction companies
* MSMEs participating in bidding
* Automated document collection systems

---
