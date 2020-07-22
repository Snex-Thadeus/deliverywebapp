$(document).ready(function () {
    fetchdata()
    $("#livebox").on("input", function (e) {
        $("table tbody").empty();
        $("table tbody").hide();
        fetchdata()
    });
});

function fetchdata() {
    $.ajax({
        method: "post",
        url: "/search_view_orders",
        data: {text: $("#livebox").val()},
        success: function (res) {
            $.each(JSON.parse(res), function (index, order) {

                const zeroPad = (num, places) => String(num).padStart(places, '0')

                var url_for = "/delivery_app/define-order-edit/" + order.ID
                var data = "<tr>";


                data += "<td>OD-" + zeroPad(order.OrderNo, 4) + "</td>";
                data += "<td>" + order.CustomerName + "</td>";
                data += "<td>" + order.TelephoneNo + "</td>";
                data += "<td>" + order.DelvieryMethod + "</td>";
                data += "<td>" + order.Location + "</td>";
                data += "<td>" + order.OrderDate + "</td>";
                data += "<td>" + order.LPONo + "</td>";
                data += "<td>" + order.Product + "</td>";
                data += "<td>" + order.Price + "</td>";
                data += "<td>" + order.Quantity + "</td>";
                data += "<td>" + order.TotalAmount + "</td>";
                data += "<td class='text-right table-actions'>" +
                    "<a class='table-action  mg-r-10' href='" + url_for + "'><i class='fa fa-pencil'></i></a>" +
                    "</td>";
                data += "</tr>";
                $('table tbody').show().append(data);

            });

            if (JSON.parse(res).length <= 0) {

                $('table tbody').show().append("<tr><td style='text-align: center' colspan='11'><p  style='color: #0e90d2'>No orders to show</p></td></tr>");
            }
        }
    });
}