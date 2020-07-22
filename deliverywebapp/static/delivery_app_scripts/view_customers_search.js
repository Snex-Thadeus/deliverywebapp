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
                url:"/search_view_customers",
                data:{text:$("#livebox").val()},
                success:function(res){
                     $.each(JSON.parse(res),function(index,customer){

                        var url_for = "/delivery_app/define-customer-edit/"+customer.ID
                        var data = "<tr>";

                         data += "<td>"+ customer.FirstName  +"</td>";
                         data += "<td>"+ customer.LastName  +"</td>";
                         data += "<td>"+ customer.ContactPerson  +"</td>";
                         data += "<td>"+ customer.Type  +"</td>";
                         data += "<td>"+ customer.Email  +"</td>";
                         data += "<td>"+ customer.PhoneNumber  +"</td>";
                         data += "<td>"+ customer.PhoneNumber2  +"</td>";
                         data += "<td>"+ customer.PhoneNumber3  +"</td>";
                         data += "<td>"+ customer.Name  +"</td>";
                         data += "<td>"+ customer.Location  +"</td>";
                         data += "<td class='text-right table-actions'>" +
                                 "<a class='table-action  mg-r-10' href='"+url_for+"'><i class='fa fa-pencil'></i></a>" +
                             "</td>";
                         data += "</tr>";
                         $('table tbody').show().append(data);

                     });

                      if ( JSON.parse(res).length <= 0){

                        $('table tbody').show().append("<tr><td style='text-align: center' colspan='11'><p  style='color: #0e90d2'>No Customers to show</p></td></tr>");
                    }



                }
            });
    }