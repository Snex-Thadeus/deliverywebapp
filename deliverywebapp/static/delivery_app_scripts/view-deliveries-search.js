$('#hoverTable').DataTable({
    responsive: true,
    language: {
        searchPlaceholder: 'Search...',
        sSearch: ''
    }
});

$(document).ready(function () {
    //SEARCH

    fetchdata()
    $("#livebox").on("input", function (e) {
        $("table tbody").empty();
        $("table tbody").hide();
        fetchdata()
    });
});

//Modal Dropdowns
function btn_click(ID) {

    const zeroPad = (num, places) => String(num).padStart(places, '0')
    var OrderNo = "OD-" + zeroPad(ID, 4);
    let exampleModalScrollableTitle = document.getElementById("exampleModalScrollableTitle");
    exampleModalScrollableTitle.innerText = "Update Order Deliveries: " + OrderNo


    let chooseInvoiceReceipt = document.getElementById("chooseInvoiceReceipt");
    chooseInvoiceReceipt.innerHTML = null
    chooseInvoiceReceipt.innerHTML += '<option value="' + -1 + '">Choose Invoice/Receipt</option>';
    chooseInvoiceReceipt.innerHTML += '<option value="Invoice">Invoice</option>';
    chooseInvoiceReceipt.innerHTML += '<option value="Receipt">Receipt</option>';

    let invoiceNo_receiptNo = document.getElementById("invoiceNo_receiptNo");
    var invoiceReceiptSelect;
    chooseInvoiceReceipt.onchange = function () {
        invoiceReceiptSelect = chooseInvoiceReceipt.value
        if (chooseInvoiceReceipt.value == "Invoice") {
            invoiceNo_receiptNo.placeholder = "Capture Invoice No."
        } else if (chooseInvoiceReceipt.value == "Receipt") {
            invoiceNo_receiptNo.placeholder = "Capture Receipt No."
        }
    }

    //let btnUpdateDeliveries = document.getElementById("btnUpdateDeliveries");
    // var url_for = "/delivery_app/view-deliveries-edit/" + ID
    // btnUpdateDeliveries.href = url_for;


    let choosePaymentMode = document.getElementById("choosePaymentMode");
    choosePaymentMode.innerText = null
    choosePaymentMode.innerHTML += '<option value="' + -1 + '">Choose Payment Mode</option>';
    choosePaymentMode.innerHTML += '<option value="MPESA">MPESA</option>';
    choosePaymentMode.innerHTML += '<option value="Cheque">Cheque</option>';
    choosePaymentMode.innerHTML += '<option value="Cash">Cash</option>';
    var paymentModeSelect;
    choosePaymentMode.onchange = function () {
        paymentModeSelect = choosePaymentMode.value
    }

    $(document).on('click', '#btnUpdateDeliveries', function () {
        var payload = {
            "ID": ID,
            "Invoice_Receipt": invoiceReceiptSelect,
            "InvoiceNo_ReceiptNo": $('#invoiceNo_receiptNo').val(),
            "DeliveredDate": $('#bday').val(),
            "PaymentMode": paymentModeSelect,
            "ReferenceNo": $('#referenceNo').val(),
            "AmountPaid": $('#amountPaid').val().replace("Ksh ", '').replace(",", '').trim()
        }
        console.log("DATA")
        console.log(JSON.stringify(payload))
        $.ajax({
            type: 'POST',
            url: "/delivery_app/view-deliveries-edit",
            data: JSON.stringify(payload),
            dataType: "json",
            contentType: 'application/json;charset=UTF-8',//never lack this
            statusCode: {
                500: function (data) {
                    var category = 'danger'

                    var html = ['<div class="alert alert-' + category + ' alert-dismissible fade show" role="alert">',
                        '<button type="button" class="close" data-dismiss="alert" aria-label="Close"> ' +
                        '<span aria-hidden="true">×</span> ' +
                        '</button>' +
                        '</div>'].join(data.responseText)
                    console.log(data)

                    //generaing a Nan
                    // $('#error-info').html('<div class="alert alert-' + category + ' alert-dismissible fade show" role="alert">' +
                    //     + data.statusText +
                    //     '<button type="button" class="close" data-dismiss="alert" aria-label="Close"> ' +
                    //     '<span aria-hidden="true">×</span> ' +
                    //     '</button>' +
                    //     '</div>')

                    $('#error-info').html(html)
                    $("#error-info").show();

                },
                200: function (data) {
                    //console.log(data)
                }
            }
        }).done(function (data) {
            console.log(data)
            var category;
            var message;
            if (data == '1') {
                $("table tbody").empty();
                $("table tbody").hide();
                fetchdata()
                category = 'success'
                message = 'Order Delivery "' + OrderNo + '" successfully edited';

            } else {
                category = 'danger'
                message = data;
            }

            var html = ['<div class="alert alert-' + category + ' alert-dismissible fade show" role="alert">',
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close"> ' +
                '<span aria-hidden="true">×</span> ' +
                '</button>' +
                '</div>'].join(message)
            $('#error-info').html(html)
            $("#error-info").show();

        });
    });

    $("#error-info").hide();
    $("#error-info").empty();
    //clear data
    //$("#chooseInvoiceReceipt").val('');
    $("#bday").val('');
    $("#referenceNo").val('');
    $("#amountPaid").val('');
    $("#invoiceNo_receiptNo").val('');
    // $("#choosePaymentMode").val('');


    $("#exampleModalScrollable").modal();


}

function fetchdata() {
    $.ajax({
        method: "post",
        url: "/search_view_deliveries",
        data: {text: $("#livebox").val()},
        success: function (res) {
            $.each(JSON.parse(res), function (index, delivery) {

                const zeroPad = (num, places) => String(num).padStart(places, '0')

                var url_for = "/delivery_app/define-order-edit/" + delivery.ID
                var ID = delivery.OrderNo;
                var data = "<tr>";

                data += "<td class='text-right table-actions'>" +
                    // "<a class='table-action  mg-r-10' href='"+url_for+"'><i class='fa fa-pencil'></i></a>" +
                    // "<a class='btn btn-primary' href='"+url_for+"'>Update Order</a>" +
                    "<button type='button' id='updateOrder' onclick='javascript:btn_click(" + ID + ")' class='btn btn-primary waves-effect' >Update Order</button>" +//data-toggle='modal' data-target='#exampleModalScrollable'
                    "</td>";
                data += "<td>OD-" + zeroPad(delivery.OrderNo, 4) + "</td>";
                data += "<td>" + delivery.CustomerName + "</td>";
                data += "<td>" + delivery.Telephoneno + "</td>";
                data += "<td>" + delivery.DeliveryMethod + "</td>";
                data += "<td>" + delivery.Location + "</td>";
                data += "<td>" + delivery.OrderDate + "</td>";
                data += "<td>" + delivery.Product + "</td>";
                data += "<td>" + delivery.Quantity + "</td>";
                data += "<td>" + delivery.TotalAmount + "</td>";
                data += "<td>" + delivery.Invoice_Receipt + "</td>";
                data += "<td>" + delivery.InvoiceNo_ReceiptNo + "</td>";
                data += "<td>" + delivery.DeliveredDate + "</td>";
                data += "<td>" + delivery.PaymentMode + "</td>";
                data += "<td>" + delivery.ReferenceNo + "</td>";
                data += "<td>" + delivery.AmountPaid + "</td>";
                data += "</tr>";
                $('table tbody').show().append(data);
            });

            if (JSON.parse(res).length <= 0) {
                $('table tbody').show().append("<tr><td style='text-align: center' colspan='3'><p  style='color: #0e90d2'>No order deliveries to show</p></td></tr>");
            }
        }
    });


}





