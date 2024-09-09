from flask import Flask, send_file, render_template, request, redirect, url_for
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import os
from num2words import num2words
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

template_dir = 'templates'
env = Environment(loader=FileSystemLoader(template_dir))

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html', items=[])

def compute_amounts(items, place_of_supply, place_of_delivery):
    total_net_amount = 0
    total_tax_amount = 0
    for item in items:
        item['net_amount'] = item['unit_price'] * item['quantity'] - item['discount']
        if place_of_supply == place_of_delivery:
            item['tax_type'] = 'CGST & SGST'
            item['cgst_amount'] = round(item['net_amount'] * 0.09, 2)
            item['sgst_amount'] = round(item['net_amount'] * 0.09, 2)
            item['tax_amount'] = item['cgst_amount'] + item['sgst_amount']
            item['tax_rate'] = 9
        else:
            item['tax_type'] = 'IGST'
            item['igst_amount'] = round(item['net_amount'] * 0.18, 2)
            item['tax_amount'] = item['igst_amount']
            item['tax_rate'] = 18
        item['total_amount'] = item['net_amount'] + item['tax_amount']
        total_net_amount += item['net_amount']
        total_tax_amount += item['tax_amount']
    total_amount = round(total_net_amount + total_tax_amount, 2)
    return total_net_amount, total_tax_amount, total_amount

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    if request.method == 'POST':
        logo = request.files['logo']
        signature = request.files['signature']
        logo_filename = secure_filename(logo.filename)
        signature_filename = secure_filename(signature.filename)
        logo.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))
        signature.save(os.path.join(app.config['UPLOAD_FOLDER'], signature_filename))
        logo_url = '/uploads/' + logo_filename
        signature_url = '/uploads/' + signature_filename

        items = []
        i = 1
        while f'description_{i}' in request.form:
            items.append({
                'description': request.form[f'description_{i}'],
                'unit_price': float(request.form[f'unit_price_{i}']),
                'quantity': int(request.form[f'quantity_{i}']),
                'discount': float(request.form[f'discount_{i}'])
            })
            i += 1

        data = {
            'logo_url': logo_url,
            'seller_name': request.form['seller_name'],
            'seller_address': request.form['seller_address'],
            'seller_pan': request.form['seller_pan'],
            'seller_gst': request.form['seller_gst'],
            'billing_name': request.form['billing_name'],
            'billing_address': request.form['billing_address'],
            'billing_state': request.form['billing_state'],
            'shipping_name': request.form['shipping_name'],
            'shipping_address': request.form['shipping_address'],
            'shipping_state': request.form['shipping_state'],
            'order_no': request.form['order_no'],
            'order_date': request.form['order_date'],
            'invoice_no': request.form['invoice_no'],
            'invoice_date': request.form['invoice_date'],
            'place_of_supply': request.form['place_of_supply'],
            'place_of_delivery': request.form['place_of_delivery'],
            'reverse_charge': request.form['reverse_charge'],
            'items': items,
            'signature_url': signature_url
        }

        total_net_amount, total_tax_amount, total_amount = compute_amounts(
            data['items'],
            data['place_of_supply'],
            data['place_of_delivery']
        )
        data['amount_in_words'] = num2words(total_amount, lang='en').replace(',', '')

        template = env.get_template('invoice.html')
        html_content = template.render(
            logo_url=data['logo_url'],
            seller_name=data['seller_name'],
            seller_address=data['seller_address'],
            seller_pan=data['seller_pan'],
            seller_gst=data['seller_gst'],
            billing_name=data['billing_name'],
            billing_address=data['billing_address'],
            billing_state=data['billing_state'],
            shipping_name=data['shipping_name'],
            shipping_address=data['shipping_address'],
            shipping_state=data['shipping_state'],
            order_no=data['order_no'],
            order_date=data['order_date'],
            invoice_no=data['invoice_no'],
            invoice_date=data['invoice_date'],
            place_of_supply=data['place_of_supply'],
            place_of_delivery=data['place_of_delivery'],
            reverse_charge=data['reverse_charge'],
            items=data['items'],
            total_net_amount=total_net_amount,
            total_tax_amount=total_tax_amount,
            total_amount=total_amount,
            amount_in_words=data['amount_in_words'],
            signature_url=data['signature_url']
        )

        pdf_path = 'static/invoice.pdf'
        HTML(string=html_content).write_pdf(pdf_path)

        return send_file(pdf_path, as_attachment=True, download_name='invoice.pdf')

if __name__ == '__main__':
    app.run(debug=True)
