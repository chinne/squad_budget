import csv
import os
import re
import zipfile
from datetime import datetime
from typing import Optional

from PyPDF2 import PdfReader, errors

# Example usage
ZIP_FILE_PATH = "INVOICES.zip"
EXTRACT_FOLDER = "invoices"
CSV_OUTPUT_PATH = "vk_total_billings.csv"


def extract_details_from_text(input_string: str) -> dict:
    def get_match(pattern: str, text: str) -> Optional[str]:
        match = re.search(pattern, text)
        return match.group(1) if match else None

    # regex patterns for relevant information
    cost_center_pattern = r"Kundenkostenstelle:\s*(\d+)"
    contract_text_pattern = r"Vertragstext:\s*([A-Za-z0-9_]+)(?=Rechnung)"
    bill_number_pattern = r"Rechnung\s+(\d+)"
    billing_date_pattern = r"vom\s+(\d{2}\.\d{2}\.\d{4})"
    order_number_pattern = r"Bestellnummer:\s*(\d+)"
    total_amount_pattern = r"Endbetrag\s+([0-9.,]+)"

    # extract details
    cost_center = get_match(cost_center_pattern, input_string)
    contract_text = get_match(contract_text_pattern, input_string)
    bill_number = get_match(bill_number_pattern, input_string)
    order_number = get_match(order_number_pattern, input_string)

    # extract and convert total amount
    total_amount = get_match(total_amount_pattern, input_string)
    if total_amount:
        total_amount = float(total_amount.replace(".", "").replace(",", "."))

    # extract and parse billing date
    billing_date_str = get_match(billing_date_pattern, input_string)
    billing_date = None
    if billing_date_str:
        try:
            billing_date = datetime.strptime(billing_date_str, "%d.%m.%Y").date()
        except ValueError:
            print(
                f"Error parsing date from string '{billing_date_str}', setting billing date to None."
            )
            billing_date = None

    result = {
        "cost_center": cost_center,
        "contract_text": contract_text,
        "bill_number": bill_number,
        "billing_date": billing_date,
        "order_number": order_number,
        "total_amount": total_amount,
    }

    return result


def unzip_files(zip_path: str, extract_to: str) -> None:
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
    except zipfile.BadZipFile:
        print(f"Error: The zip file '{zip_path}' is corrupt or not a zip file.")
    except FileNotFoundError:
        print(f"Error: The zip file '{zip_path}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred while extracting '{zip_path}': {e}")


def process_extracted_pdfs(extract_folder: str, csv_path: str) -> None:
    with open(csv_path, mode="w", newline="") as csv_file:
        fieldnames = [
            "path",
            "page_number",
            "cost_center",
            "contract_text",
            "bill_number",
            "billing_date",
            "order_number",
            "total_amount",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate through all files in the extracted folder
        for root, _, files in os.walk(extract_folder):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    process_pdf(pdf_path, writer)


def process_pdf(pdf_path: str, writer: csv.DictWriter) -> None:
    try:
        reader = PdfReader(pdf_path)
        number_of_pages = len(reader.pages)

        # Extract text from each page and get details
        for page_num in range(number_of_pages):
            page = reader.pages[page_num]
            text = extract_text_from_page(page, pdf_path, page_num)
            if text:
                details = extract_details_from_text(text)
                details.update({"path": pdf_path, "page_number": page_num + 1})
                writer.writerow(details)
            else:
                print(
                    f"Warning: No text extracted from {pdf_path}, page {page_num + 1}."
                )

    except errors.PdfReadError:
        print(f"Error: Could not read PDF file '{pdf_path}'. It might be corrupt.")
    except FileNotFoundError:
        print(f"Error: The PDF file '{pdf_path}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred while processing '{pdf_path}': {e}")


def extract_text_from_page(page, pdf_path: str, page_num: int) -> Optional[str]:
    try:
        return page.extract_text()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}, page {page_num + 1}: {e}")
        return None


if __name__ == "__main__":
    unzip_files(ZIP_FILE_PATH, EXTRACT_FOLDER)
    process_extracted_pdfs(EXTRACT_FOLDER, CSV_OUTPUT_PATH)
