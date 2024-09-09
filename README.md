Invoice Generator Application
=============================

This is a Flask-based web application that generates an invoice PDF based on user input from a form. The application handles file uploads for the logo and signature, computes the total amounts and tax rates, and uses the `weasyprint` library to generate a PDF from an HTML template.

Getting Started
---------------

### Prerequisites

* Python 3.x
* Flask
* WeasyPrint
* Jinja2
* Num2Words
* Werkzeug

### Installation

1. Clone the repository: `git clone https://github.com/your-username/invoice-generator.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Run the application: `python app.py`

### Usage

1. Access the application through a web browser at `http://localhost:5000`
2. Fill out the form with the required information
3. Upload the logo and signature files
4. Click the "Generate Invoice" button to download the invoice PDF

Documentation
-------------

### app.py

This is the main application file that defines the Flask routes and logic.

### templates/form.html

This is the HTML template for the user input form.

### templates/invoice.html

This is the HTML template for the invoice PDF.

### static/invoice.pdf

This is the generated invoice PDF file.

### uploads/

This is the directory where the uploaded logo and signature files are stored.

Configuration
-------------

### app.config['UPLOAD_FOLDER']

This is the directory where the uploaded files are stored. By default, it is set to `uploads`.

### template_dir

This is the directory where the HTML templates are stored. By default, it is set to `templates`.

License
-------

This application is licensed under the MIT License.

Author
------

Zulfa
