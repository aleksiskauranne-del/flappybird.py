from docx import Document

# Path to the DOCX file
docx_path = r"c:\Users\ADMIN\OneDrive - Business College Helsinki\Pictures\opinnäytetyö ideoita\Cybersecurity internship.docx"

# Load the document
doc = Document(docx_path)

# Extract text from all paragraphs
full_text = ""
for para in doc.paragraphs:
    full_text += para.text + "\n"

# Print the full text
print(full_text)