//DateTimer picker
$('#datepicker').datepicker();

//validate drop downs


//Price Input
$('.price-input').on({
    keyup: function () {
        formatCurrency($(this));
    },
    blur: function () {
        formatCurrency($(this), "blur");
    }
});

function formatNumber(n) {
    // format number 1000000 to 1,234,567
    return n.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}


function formatCurrency(input, blur) {
    // appends $ to value, validates decimal side
    // and puts cursor back in right position.

    // get input value
    var input_val = input.val();

    // don't validate empty input
    if (input_val === "") {
        return;
    }

    // original length
    var original_len = input_val.length;

    // initial caret position
    var caret_pos = input.prop("selectionStart");

    // check for decimal
    if (input_val.indexOf(".") >= 0) {

        // get position of first decimal
        // this prevents multiple decimals from
        // being entered
        var decimal_pos = input_val.indexOf(".");

        // split number by decimal point
        var left_side = input_val.substring(0, decimal_pos);
        var right_side = input_val.substring(decimal_pos);

        // add commas to left side of number
        left_side = formatNumber(left_side);

        // validate right side
        right_side = formatNumber(right_side);

        // On blur make sure 2 numbers after decimal
        if (blur === "blur") {
            right_side += "00";
        }

        // Limit decimal to only 2 digits
        right_side = right_side.substring(0, 2);

        // join number by .
        input_val = "Ksh " + left_side + "." + right_side;

    } else {
        // no decimal entered
        // add commas to number
        // remove all non-digits
        input_val = formatNumber(input_val);
        input_val = "Ksh " + input_val;

        // final formatting
        if (blur === "blur") {
            input_val += ".00";
        }
    }

    // send updated string to input
    input.val(input_val);

    // put caret back in the right position
    var updated_len = input_val.length;
    caret_pos = updated_len - original_len + caret_pos;
    input[0].setSelectionRange(caret_pos, caret_pos);
}


// Basic DataTable
$('#basicDataTable').DataTable({
    responsive: true,
    language: {
        searchPlaceholder: 'Search...',
        sSearch: ''
    }
});

// No Style DataTable
$('#noStyleedTable').DataTable({
    responsive: true,
    language: {
        searchPlaceholder: 'Search...',
        sSearch: ''
    }
});

// Compact DataTable
$('#compactTable').DataTable({
    responsive: true,
    language: {
        searchPlaceholder: 'Search...',
        sSearch: ''
    }
});

// // Hoverable DataTable
// $('#hoverTable').DataTable({
//     responsive: true,
//     language: {
//         searchPlaceholder: 'Search...',
//         sSearch: ''
//     }
// });

// Scrollable Table DataTable
$('#scrollableTable').DataTable({
    responsive: true,
    language: {
        searchPlaceholder: 'Search...',
        sSearch: ''
    },
    "order": [[1, "desc"]],
    "scrollY": "250px",
    "scrollCollapse": true,
    "paging": false
});


// File Uploader
var readURL = function (input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('.profile-pic').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$(".file-upload").on('change', function () {
    readURL(this);
});

$(".upload-button").on('click', function () {
    $(".file-upload").click();
});

// Credit Card
var cleaveA = new Cleave('#inputCreditCard', {
    creditCard: true,
    onCreditCardTypeChanged: function (type) {
        console.log(type)
        var card = $('#creditCardType').find('.' + type);

        if (card.length) {
            card.addClass('tx-primary');
            card.siblings().removeClass('tx-primary');
        } else {
            $('#creditCardType span').removeClass('tx-primary');
        }
    }
});

// Date Formatting
var cleave = new Cleave('#inputDate2', {
    date: true,
    datePattern: ['m', 'Y']
});

// Blocks Formatting
var cleaveH = new Cleave('#inputBlocks', {
    blocks: [3],
});
