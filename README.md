# 🧠 AI File Chat

A smart application for **full document extraction**, **reorganization**, and **Q&A interaction** — powered by OpenAI and Streamlit.

## 🚀 Features

- **Upload Files**: Supports `.pdf`, `.txt`, `.jpg`, `.png`.
- **Smart Extraction**:
  - Attempts structured extraction via **MarkItDown**.
  - Falls back to **OCR (Tesseract)** if necessary.
- **Content Reorganization**:
  - Reorganizes messy extracted text into clean Markdown via OpenAI model (`gpt-4.1-mini`).
- **Interactive Q&A**:
  - Ask direct questions about the uploaded content.
  - Receives precise and concise answers instantly.
- **Download Reorganized Files**:
  - Save the cleaned-up Markdown as a `.txt` file.
- **User-Friendly Interface**:
  - Built with **Streamlit** for ease of use and beautiful layout.
  - Sidebar contains author links and branding.

## 📂 Supported File Types

- PDF documents (`.pdf`)
- Text files (`.txt`)
- Image files (`.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`)

## 🛠️ How It Works

1. Upload a file.
2. Start extraction and display the extracted text.
3. Reorganize the text into structured Markdown.
4. Ask questions about the content.
5. Download the reorganized content.

## 📎 Requirements

Install the dependencies:

```bash
pip install streamlit openai tiktoken markitdown pytesseract pymupdf pillow
```

**Note**:  
Ensure `Tesseract OCR` is installed in your system for OCR extraction to work:
- [Tesseract Installation Guide](https://github.com/tesseract-ocr/tesseract)

## 👨‍💻 Developed By

**Ahmed Zeyad Tareq**  
- 🎓 Master's in Artificial Intelligence Engineering  
- 📌 Data Scientist, AI Developer  
- [GitHub](https://github.com/AhmedZeyadTareq) | [LinkedIn](https://www.linkedin.com/in/ahmed-zeyad-tareq) | [Kaggle](https://www.kaggle.com/ahmedzeyadtareq)

---

✨ **Enjoy smart document interaction!**
