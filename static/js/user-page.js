// Is this necessary anymore????
$(document).ready(function(){
    $('#fileupload').fileupload({
        url: 'upload',
        dataType: 'json',
        add: function (e, data) {
            data.submit();
        }
    });
})



// $(document).ready(function() {
//     $('#btnSignUp').click(function(){
//         $.ajax({
//             url: '/signUp',
//             data: $('form').serialize(),
//             type: 'POST',
//             success: function(response) {
//                 console.log(response);
//             },
//             error: function(error) {
//                 console.log(error);
//             }
//         });
//     });
// });

