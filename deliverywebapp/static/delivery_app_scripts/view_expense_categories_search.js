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
                url:"/search_view_expense_categories",
                data:{text:$("#livebox").val()},
                success:function(res){
                     $.each(JSON.parse(res),function(index,expenseCategory){

                        var url_for = "/delivery_app/define-expense-category-edit/"+expenseCategory.ID
                        var data = "<tr>";

                         data += "<td>"+ expenseCategory.CategoryDescription  +"</td>";
                         data += "<td class='text-right table-actions'>" +
                                 "<a class='table-action  mg-r-10' href='"+url_for+"'><i class='fa fa-pencil'></i></a>" +
                             "</td>";
                         data += "</tr>";
                         $('table tbody').show().append(data);


                     });

                      if ( JSON.parse(res).length <= 0){

                        $('table tbody').show().append("<tr><td style='text-align: center' colspan='3'><p  style='color: #0e90d2'>No expense categories to show</p></td></tr>");
                    }



                }
            });
    }