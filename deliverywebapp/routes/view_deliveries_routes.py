import json
from flask import request, flash, render_template
from deliverywebapp import app
from deliverywebapp.forms.forms import UpdateDeliveriesForm
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_deliveries', methods=['GET', 'POST'])
def search_view_deliveries_route():
    searchbox = request.form.get('text')
    try:
        if searchbox:
            deliveries = db.session.execute(
                'SELECT o.OrderNo,o.CustomerName,o.Telephoneno, o.DeliveryMethod, o.Location,o.OrderDate,p.Description AS Product,o.Quantity,o.TotalAmount,'
                'CASE WHEN  d.Invoice_Receipt IS NULL THEN " " ELSE d.Invoice_Receipt END Invoice_Receipt,'
                'CASE WHEN d.InvoiceNo_ReceiptNo IS NULL THEN " " ELSE d.InvoiceNo_ReceiptNo END InvoiceNo_ReceiptNo,'
                'CASE WHEN d.DeliveredDate IS NULL THEN " " ELSE d.DeliveredDate END DeliveredDate,'
                'CASE WHEN d.PaymentMode IS NULL THEN " " ELSE d.PaymentMode END PaymentMode,'
                'CASE WHEN d.ReferenceNo IS NULL THEN " " ELSE d.ReferenceNo END ReferenceNo,'
                'CASE WHEN AmountPaid IS NULL THEN " " ELSE d.AmountPaid END AmountPaid '
                ' FROM order_tb o LEFT OUTER JOIN deliveries_tb d ON o.OrderNo = d.OrderNo '
                'INNER JOIN product_tb p ON o.ProductID = p.ID WHERE o.CustomerName LIKE "%' + searchbox + '%" OR o.Telephoneno LIKE "%' + searchbox + '%" ORDER BY o.OrderDate DESC')

            deliveries_rows = [dict(row) for row in deliveries]

            return json.dumps(deliveries_rows, cls=AlchemyEncoder)
        else:
            # products = ProductPriceTb.query.all()
            deliveries = db.session.execute(
                'SELECT o.OrderNo,o.CustomerName,o.Telephoneno, o.DeliveryMethod, o.Location,o.OrderDate,p.Description AS Product,o.Quantity,o.TotalAmount, '
                'CASE WHEN  d.Invoice_Receipt IS NULL THEN " " ELSE d.Invoice_Receipt END Invoice_Receipt,'
                'CASE WHEN d.InvoiceNo_ReceiptNo IS NULL THEN " " ELSE d.InvoiceNo_ReceiptNo END InvoiceNo_ReceiptNo,'
                'CASE WHEN d.DeliveredDate IS NULL THEN " " ELSE d.DeliveredDate END DeliveredDate,'
                'CASE WHEN d.PaymentMode IS NULL THEN " " ELSE d.PaymentMode END PaymentMode,'
                'CASE WHEN d.ReferenceNo IS NULL THEN " " ELSE d.ReferenceNo END ReferenceNo,'
                'CASE WHEN AmountPaid IS NULL THEN " " ELSE d.AmountPaid END AmountPaid '
                ' FROM order_tb o LEFT OUTER JOIN deliveries_tb d ON o.OrderNo = d.OrderNo '
                'INNER JOIN product_tb p ON o.ProductID = p.ID ORDER BY o.OrderDate DESC')

            deliveries_rows = [dict(row) for row in deliveries]
            return json.dumps(deliveries_rows, cls=AlchemyEncoder)

    except Exception as ex:
        flash(ex, 'danger')


# RECEIPT_INVOICE = [('-1', 'Choose Invoice/Receipt'), ('Invoice', 'Invoice'), ('Receipt', 'Receipt')]
# PAYMENT_MODE = [('-1', 'Choose Payment Mode'), ('MPESA', 'MPESA'), ('Cheque', 'Cheque'), ('Cash', 'Cash')]


@app.route('/delivery_app/view-deliveries-edit', methods=['GET', 'POST'])
def view_deliveries_edit():
    try:
        # existDelivery = db.session.query(DeliveriesTb).filter(DeliveriesTb.OrderNo == request.json['ID']).one()
        # if existDelivery:
        #     if len(existDelivery) > 0:
        #         existDelivery.OrderNo = str(request.json['ID'])
        #         existDelivery.Invoice_Receipt = str(request.json['Invoice_Receipt'])
        #         existDelivery.InvoiceNo_ReceiptNo = str(request.json['InvoiceNo_ReceiptNo'])
        #         existDelivery.DeliveredDate = str(request.json['DeliveredDate'])
        #         existDelivery.PaymentMode = str(request.json['PaymentMode'])
        #         existDelivery.ReferenceNo = str(request.json['ReferenceNo'])
        #         existDelivery.AmountPaid = str(request.json['AmountPaid'])
        #         db.session.commit()
        #     else:
        delivery = DeliveriesTb(
            str(request.json['ID']),
            str(request.json['Invoice_Receipt']),
            str(request.json['InvoiceNo_ReceiptNo']),
            str(request.json['DeliveredDate']),
            str(request.json['PaymentMode']),
            str(request.json['ReferenceNo']),
            str(request.json['AmountPaid'])
        )
        db.session.add(delivery)
        db.session.commit()

        return "1"
    except Exception as ex:
        return ex


@app.route('/deliveries/<int:page_num>')
def delivery(page_num):
    deliveries = DeliveriesTb.query.paginate(per_page=50, page=page_num, error_out=True)
    return render_template('paginate.html', deliveries=deliveries)


@app.route('/delivery_app/view-deliveries', methods=['GET', 'POST'])
def view_deliveries():
    form = UpdateDeliveriesForm()

    return render_template('/delivery_app/view-deliveries.html', form=form)

