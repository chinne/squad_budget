# Budget Project

This project automates the extraction and processing of billing information from invoice files, simplifying the process
of handling financial data. The script reads `.pdf` invoices from a compressed `.zip` file, extracts key financial
details, and outputs a structured CSV for further analysis.

## Requirements

- **Invoices Folder**: Download the invoices from your SharePoint into the root directory of this project as a `.zip`
  file named `INVOICES.zip`. This is usually the default format if downloaded directly from SharePoint.
- **Python 3.7+**
- **Dependencies**: Install the required Python packages by running the command:

  ```sh
  pip install -r requirements.txt
  ```

  The `requirements.txt` file should include:
    - `pandas`
    - `PyPDF2`
    - `openpyxl` (for reading Excel files)

## How to Run the Code

To extract and process billing information from the invoices, run the `extract_billing_infos.py` script as follows:

```sh
python extract_billing_infos.py
```

This script performs the following:

1. Unzips the `INVOICES.zip` folder into a local `invoices/` directory.
2. Reads all invoice PDFs within the folder.
3. Extracts relevant information such as cost center, contract text, bill number, billing date, order number, and total
   amount.
4. Saves the extracted data into a CSV file named `vk_total_billings.csv`.

## Project Structure

- **`INVOICES.zip`**: The compressed folder containing all invoice files. This must be placed in the root directory.
- **`extract_billing_infos.py`**: The main Python script for extracting invoice data.
- **`requirements.txt`**: List of Python dependencies.
- **`vk_total_billings.csv`**: The resulting CSV file after processing the invoices.

## Example Workflow

1. **Download** the `INVOICES` folder from SharePoint and ensure it is saved as `INVOICES.zip` in the root directory of
   this project.
2. **Run** the `extract_billing_infos.py` script to extract relevant billing details from the invoices.
3. **Review** the `extracted_details.csv` for all gathered data.

## Contact

For questions or issues, feel free to open an issue on the repository or contact the project maintainer.

