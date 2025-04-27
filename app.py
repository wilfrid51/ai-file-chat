import warnings

warnings.filterwarnings("ignore",
                        message="builtin type (SwigPyPacked|SwigPyObject|swigvarlink) has no __module__ attribute",
                        category=DeprecationWarning)

# ==== Imports ====
import os
import tempfile

import fitz  # PyMuPDF
import pytesseract
import tiktoken
from PIL import Image
from markitdown import MarkItDown
from openai import OpenAI

import streamlit as st

# ==== Config ====
OPENAI_API_KEY = "OPENAI_API_KEY"
LLM_MODEL = "gpt-4.1-mini"

# ==== Streamlit UI ====
st.set_page_config(page_title="🧠 AI File Chat", layout="centered")
st.title("🧠 Content Extraction")

# Sidebar
logo_link = "formal image.jpg"
with st.sidebar:
    if os.path.exists(logo_link):
        logo_image = Image.open(logo_link)
        st.image(logo_image, width=150)
    else:
        st.warning("Logo not found. Please check the logo path.")

    st.write("## 🔗 👨‍💻 Developed By:")
    st.write("    **Eng.Ahmed Zeyad Tareq**")
    st.write("🎓 Master's in Artificial Intelligence Engineering.")
    st.write("📌 Data Scientist, AI Developer.")
    st.write("[GitHub](https://github.com/AhmedZeyadTareq) | [LinkedIn](https://www.linkedin.com/in/ahmed-zeyad-tareq) | [Kaggle](https://www.kaggle.com/ahmedzeyadtareq)")

uploaded_file = st.file_uploader("📂 Choose File:", type=["pdf", "txt", "jpg", "png"])


# ==== Functions ====

def pdf_to_images(file_obj, dpi: int = 300) -> list[Image.Image]:
    """Convert PDF to images"""
    if isinstance(file_obj, str):
        doc = fitz.open(file_obj)
    else:
        doc = fitz.open(stream=file_obj.read(), filetype="pdf")

    pages = []
    for page in doc:
        pix = page.get_pixmap(dpi=dpi, colorspace="rgb")
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pages.append(img)
    doc.close()
    return pages


def convert_file(path: str) -> str:
    """Convert file to text (prefer structured, fallback to OCR)"""
    ext = os.path.splitext(path)[1].lower()
    try:
        print("[🔍] Trying structured text extraction via MarkItDown...")
        md = MarkItDown(enable_plugins=False)
        result = md.convert(path)
        if result.text_content.strip():
            print(f"[✔] Markdown extracted. Saving...")
            # with open('data.md', 'a', encoding='utf-8') as f:
            #     f.write(result.text_content)
            return result.text_content
        else:
            print("[⚠️] No structured text found. Fallback to OCR...")
    except Exception:
        print(f"[❌] MarkItDown failed. Fallback to OCR...")

    print("[🔍] OCR Started...")
    try:
        _ = fitz.open(path)
        is_pdf = True
    except Exception:
        is_pdf = False

    if is_pdf:
        pages = pdf_to_images(path)
    elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        pages = [Image.open(path)]
    else:
        raise Exception(f"Unsupported file format: {ext or 'unknown'}")

    full_text = ""
    for img in pages:
        page_text = pytesseract.image_to_string(img, lang='eng')
        full_text += "\n" + page_text

    return full_text


def reorganize_markdown(raw: str) -> str:
    """Reorganize markdown via OpenAI"""
    client = OpenAI()
    completion = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": f"reorganize the following content:\n {raw}"},
            {"role": "system", "content": (
                "You are a reorganizer. Return the content in Markdown, keeping it identical. "
                "Do not delete or replace anything—only reorganize for better structure. your response the content direct without (``` ```)."
            )}
        ]
    )
    # with open('data.md', 'a', encoding='utf-8') as f:
    #     f.write(completion.choices[0].message.content)
    print("===Reorganized Done===")
    return completion.choices[0].message.content


def rag(con: str, question: str) -> str:
    """Answer questions from provided content"""
    client = OpenAI()
    completion = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": question},
            {"role": "system", "content": f"You are an assistant. Answer concisely from the following content:\n {con}"}
        ]
    )
    return completion.choices[0].message.content


def count_tokens(content: str, model="gpt-4-turbo"):
    """Count tokens in the content"""
    enc = tiktoken.encoding_for_model(model)
    print(f"The Size of the Content_Tokens: {len(enc.encode(content))}")


# ==== Main Process ====

if uploaded_file:
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

        if st.button("Start 🔁"):
            raw_text = convert_file(file_path)
            st.text_area("📄 Content:", raw_text, height=200)
            st.session_state["raw_text"] = raw_text

        if "raw_text" in st.session_state:
            if st.button("🧹 Reorganize to Content"):
                organized = reorganize_markdown(st.session_state["raw_text"])
                st.session_state["organized_text"] = organized
                st.markdown(organized)
                st.download_button(
                    label="⬇️ Download as TXT",
                    data=organized,
                    file_name="reorganized_content.txt",
                    mime="text/plain",
                    key="download_txt"
                )
            if "organized_text" in st.session_state:
                question = st.text_input("Ask Anything about Content..❓")
                if st.button("💬 Send"):
                    answer = rag(st.session_state["organized_text"], question)
                    st.markdown(f"**Question❓:**\n{question}")
                    st.markdown(f"**Answer💡:**\n{answer}")
