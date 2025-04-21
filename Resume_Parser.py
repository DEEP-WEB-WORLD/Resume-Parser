import pdfplumber
import spacy
import re
import json

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Define skill keywords
SKILLS = ['python', 'java', 'c++', 'html', 'css', 'sql', 'javascript', 'machine learning',
          'data science', 'deep learning', 'nlp', 'excel', 'power bi', 'flask', 'django']

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

# Extract name
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return None

# Extract email
def extract_email(text):
    match = re.findall(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
    return match[0] if match else None

# Extract phone number
def extract_phone(text):
    match = re.findall(r'\+?\d[\d -]{8,12}\d', text)
    return match[0] if match else None

# Extract skills
def extract_skills(text):
    text = text.lower()
    extracted_skills = [skill for skill in SKILLS if skill in text]
    return extracted_skills

# Extract education (basic)
def extract_education(text):
    education_keywords = ['bca', 'b.tech', 'mca', 'm.tech', 'bsc', 'msc', 'bcom', 'mba']
    edu_found = []
    for keyword in education_keywords:
        if keyword.lower() in text.lower():
            edu_found.append(keyword.upper())
    return list(set(edu_found))

# Extract all info
def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    parsed = {
        'Name': extract_name(text),
        'Email': extract_email(text),
        'Phone': extract_phone(text),
        'Skills': extract_skills(text),
        'Education': extract_education(text)
    }
    return parsed

# Example usage
if __name__ == "__main__":
    file_path = "sample_resume.pdf"  # Replace with your PDF path
    result = parse_resume(file_path)
    
    # Save to JSON
    with open("parsed_resume.json", "w") as f:
        json.dump(result, f, indent=4)
    
    print("Resume Parsed Successfully:")
    print(json.dumps(result, indent=4))
