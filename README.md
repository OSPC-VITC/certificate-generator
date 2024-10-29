# Certificate Generator 

This project is a certificate generator app built with Streamlit. It allows users to create personalized certificates using a custom template and export them as PDFs, with options for different certificate types, signatory details, and prize assignments. The generated certificates are zipped for easy download.

## Features
- **Customizable Certificate Types**: Choose from Excellence, Participation, and Appreciation.
- **Dynamic Event Details**: Specify event name and date for personalized certificates.
- **Multiple Signatories**: Add up to three signatories with name, designation, and signature image.
- **CSV/XLSX File Support**: Upload a file with names and automatically assign certificates.
- **Prize Allocation**: For Excellence certificates, assign prize ranks (First, Second, Third) to selected names.
- **Batch PDF Export**: Generate a ZIP file of certificates for easy download.

## How It Works
1. **Customize Certificate Details**: Select the certificate type, input event name and date, and add signatory details.
2. **Upload Names File**: Provide a CSV or XLSX file with participant names.
3. **Prize Allocation**: For Excellence certificates, assign prize categories to selected participants.
4. **Generate and Download**: Click the **Generate Certificates** button to create PDFs for each name and download them in a ZIP file.

## Installation
To run the app locally, you need to have Python 3.x installed. Follow these steps to set up the project:

```bash
# Clone the repository
git clone https://github.com/OSPC-VITC/certificate-generator.git
cd certificate-generator

# Install dependencies
pip install -r requirements.txt
```
## Running the App
Once the dependencies are installed, start the Streamlit app with the following command:

```bash
streamlit run main.py
```
The app should open in your web browser at http://localhost:8501.
## Dependencies
The project relies on the following Python libraries:
- **Streamlit**: For creating the web application interface.
- **Pandas**: For handling CSV/XLSX file uploads and data processing.
- **Pillow**: For image manipulation and text rendering on the certificates.

## Directory Structure
```plaintext
.
├── main.py                    # Main Streamlit app
├── requirements.txt           # Dependencies
├── Latinia.ttf                # Font
├── certificate_template.png   # template
└── README.md                  # Project documentation
```
