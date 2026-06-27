import fitz

def extract_pdf(uploaded_file):
    text = ""

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    for page in pdf:
        text += page.get_text() + "\n"

    pdf.close()

    return text