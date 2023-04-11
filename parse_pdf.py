import pdfplumber

# Open the PDF file
with pdfplumber.open("../pdf/<name>.pdf") as pdf:
    # Create an empty string to store the text
    text = ""
    # Loop through each page of the PDF
    for page in pdf.pages:
        # Extract the text from the page and add it to the string
        text += page.extract_text()

# Save the text to a file
with open("../pdf/<name>.txt", "w") as file:
    file.write(text)

# The above code uses pdfplumber to open the PDF file located at "../pdf/Audio.pdf", extracts the text from each page of the PDF, and saves the text to a file located at "../pdf/Audio_new.txt".
