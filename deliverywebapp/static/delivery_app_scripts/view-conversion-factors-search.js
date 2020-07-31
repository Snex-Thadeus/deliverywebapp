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
                url:"/search-view-conversion-factors",
                data:{text:$("#livebox").val()},
                success:function(res){
                     $.each(JSON.parse(res),function(index,conversionfactors){

                        var url_for = "/delivery_app/define-view-conversion-factors-edit/"+conversionfactors.ID
                        var data = "<tr>";

                         data += "<td>"+ conversionfactors.MaterialItem  +"</td>";
                         data += "<td>"+ conversionfactors.ItemUom  +"</td>";
                         data += "<td>"+ conversionfactors.MeasurementDescription  +"</td>";
                         data += "<td>"+ conversionfactors.DescribeQuantity  +"</td>";

                         data += "<td class='text-right table-actions'>" +
                                 "<a class='table-action  mg-r-10' href='"+url_for+"'><i class='fa fa-pencil'></i></a>" +
                             "</td>";
                         data += "</tr>";
                         $('table tbody').show().append(data);


                     });

                      if ( JSON.parse(res).length <= 0){

                        $('table tbody').show().append("<tr><td style='text-align: center' colspan='3'><p  style='color: #0e90d2'>No conversion factors to show</p></td></tr>");
                    }



                }
            });
    }