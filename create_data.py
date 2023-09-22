import PyPDF2
import json
from tqdm import tqdm 

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        # Initialize the PDF reader
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text page-by-page
        text_data = {}
        for page_num in tqdm(range(len(pdf_reader.pages))):
            page = pdf_reader.pages[page_num]
            text_data[f"Page{page_num + 1}"] = page.extract_text()

    return text_data

def sanitize_string(input_str):
    """Sanitize string to ensure it's valid UTF-8."""
    return input_str.encode('utf-8', errors='replace').decode('utf-8')

def main():
    pdf_path = "/Users/abhishekmamdapure/AbhishekPersonal/Resources Books/AAAMLP/AAAMLP.pdf"
    extracted_data = extract_text_from_pdf(pdf_path)

    sanitized_data = {key: sanitize_string(value) for key, value in extracted_data.items()}


    # Save the extracted data to a JSON file
    with open("extracted_data.json", "w", encoding="utf-8") as json_file:
        json.dump(sanitized_data, json_file, indent=4, ensure_ascii=False)

    print("Text has been extracted and saved to 'extracted_data.json'.")

if __name__ == "__main__":
    main()
