pip install weasyprint
pip install pdfkit
Go to the wkhtmltopdf downloads page.
Download the Windows installer (choose the latest stable version).
Install the downloaded .exe file.
then change path as below---line 645(inside download_report route) for
path_to_wkhtmltopdf = r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"

Now Run app.py
