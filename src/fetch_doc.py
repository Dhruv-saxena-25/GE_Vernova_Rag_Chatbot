from pdf2image import convert_from_path
from io import BytesIO
import base64



def extract_pdf_pages_as_images_base64(page_numbers):
    """
    Extracts specified pages from a PDF and returns them as base64-encoded images.
    """
    images_base64 = []
    pdf_path = "data/GE_Vernova_Sustainability_Report_2023.pdf"  # Specify the correct path to your PDF
    try:
        for page_number in page_numbers:
            # Convert the specified page to an image (1-based indexing)
            images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number, dpi=200)
            # Convert the image to a BytesIO object
            img_io = BytesIO()
            images[0].save(img_io, 'PNG')
            img_io.seek(0)

            # Encode the image as base64 and add it to the list
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            images_base64.append(img_base64)
            print(f'Page {page_number} converted to base64')
            
    except Exception as e:
        print(f"An error occurred: {e}")

    return images_base64