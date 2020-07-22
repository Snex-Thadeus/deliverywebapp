$(document).ready(function(){
      fetchdata()
        $("#livebox").on("input",function(e){
            $("table tbody").empty();
            $("table tbody").hide();
            fetchdata()
        });
    });

    function fetchdata(){
         $.ajax({
                method:"post",
                url:"/search_view_product",
                data:{text:$("#livebox").val()},
                success:function(res){
                     $.each(JSON.parse(res),function(index,product){

                        var url_for = "/delivery_app/define-product-edit/"+product.ID
                        var data = "<tr>";

                         data += "<td>"+ product.SKUNumber  +"</td>";
                         data += "<td>"+ product.Description +"</td>";
                         data += "<td class='text-right table-actions'>" +
                                 "<a class='table-action  mg-r-10' href='"+url_for+"'><i class='fa fa-pencil'></i></a>" +

                             "</td>";
                         data += "</tr>";
                         $('table tbody').show().append(data);


                     });

                      if ( JSON.parse(res).length <= 0){

                        $('table tbody').show().append("<tr><td style='text-align: center' colspan='3'><p  style='color: #0e90d2'>No products to show</p></td></tr>");
                    }



                }
            });
    }