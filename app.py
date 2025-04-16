import streamlit as st
import tempfile
import os
import pdfkit
import fitz
from mistralai.client import MistralClient

# Initialize Mistral client
api_key = st.secrets["MISTRAL_API_KEY"]
client = MistralClient(api_key=api_key)

st.title("CV to HTML")
st.write("Upload a CV (PDF), and we'll generate a structured HTML version you can edit and export.")

uploaded_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully!")
    original_filename = uploaded_file.name
    base_filename = os.path.splitext(original_filename)[0]  # Extract filename without extension
    output_filename_prefix = base_filename + " Go&Dev"

    # Save the file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    # Extract text from PDF
    text_content = ""
    try:
        pdf_document = fitz.open(temp_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text_content += page.get_text()
        pdf_document.close()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        text_content = "Failed to extract text from PDF."
    if "html_content" not in st.session_state:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file.getbuffer())
            temp_pdf_path = temp_pdf.name

        st.success("File uploaded successfully!")

        messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": """
From the provided CV, extract and format the following in clean, valid HTML (no markdown, no extra explanation or metadata, and **no ```html at the top or ``` at the bottom**):

- get rid of the ```html at the top and the ``` at the bottom.
-**First name only** (assumed to be the second word in a typical French full name), displayed at the top, centered, font-size: 20px. if the first name is not found put "not found" instead.
- **Candidate's job title or function**, immediately under the first name, centered, font-size: 16px.
- Leave vertical space before the next sections.

### Sections to extract and format into separate boxes:
1. **Domaines de Compétences** (box 1)
   - Compétences Techniques (e.g., languages, tools) (all the technical skills you can find)
   - Fonctionnel (e.g., domain expertise) (make it concise and straight to the point)
   - Langues (spoken/written languages)

2. **Formation** (box 2)
   - Academic qualifications with institutions and years.

3. **Expériences Professionnelles** (box 3)
   - Jobs listed in reverse chronological order: title, company, dates, responsibilities.

### Formatting Rules:
- do not show the anotation html at the top and the bottom.
- **Separate Boxes**: Each of the three sections ("Domaines de Compétences", "Formation", "Expériences Professionnelles") should be enclosed in their own **box** with a border and padding for clarity.
- Center all section titles ("Domaines de Compétences", "Formation", "Expériences Professionnelles") using font-size: 24px.
- Each box should have a small margin between the sections for clear separation.
- Do **not** include any identifying details (full name, phone, LinkedIn, GitHub, etc.) other than the first name.
"""
            },
            {
                "type": "text",
                "text": str(text_content),
            },
        ],
    }]

    # Call Mistral API
    with st.spinner("Processing CV..."):
        chat_response = client.chat(
            model="mistral-small-latest",
            messages=messages,
            response_format={"type": "text"},
        )
    # Define an HTML template with a logo at the top
    html_output = f"""
    <html lang="fr">
    <head>
        <title>Generated CV</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .header {{ position: relative; margin-bottom: 20px; }}
        .logo {{ position: absolute; top: 0; right: 0; }}
        .logo img {{ width: 100px; height: auto; }}
        .content {{ border: 1px solid #ddd; padding: 20px; border-radius: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">
            <img src="https://www.goandev.net/wp-content/uploads/2023/10/cropped-Design-sans-titre-1.png" alt="Company Logo">
        </div>
    </div>
        {chat_response.choices[0].message.content}
    
</body>
</html>
"""


# Display HTML in Streamlit
if 'html_output' in locals():
    st.subheader("Generated HTML")
    st.components.v1.html(html_output, height=500, scrolling=True)
    # Download HTML file
    html_filename = f"{output_filename_prefix}.html"
    with open(html_filename, "w", encoding="utf-8") as file:
        file.write(html_output)
    st.download_button(
    label="Download HTML",
    data=html_output,
    file_name=html_filename,
    mime="text/html",
)
    # Convert HTML to PDF and provide download option
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdf_filename = f"{output_filename_prefix}.pdf"
    options = { 'encoding': 'UTF-8' }
    pdfkit.from_string(html_output, pdf_filename, configuration=config, options=options)
    with open(pdf_filename, "rb") as pdf_file:
        st.download_button(
        label="Download PDF",
        data=pdf_file,
        file_name=pdf_filename,
        mime="application/pdf",
    )
    # Convert HTML to .doc and provide download option
    doc_filename = "generated_cv.doc"
    with open(doc_filename, "w", encoding="utf-8") as doc_file:
        # Word opens HTML nicely if content is well-formed
        doc_file.write(html_output)
    with open(doc_filename, "rb") as doc_file:
        st.download_button(
            label="Download DOC (Word)",
            data=doc_file,
            file_name=doc_filename,
            mime="application/msword",
        )

