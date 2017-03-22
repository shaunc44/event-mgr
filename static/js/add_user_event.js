$(document).ready(function() {
    $('#singlebutton').on(function(event){

        event.preventDefault(); // tells html to stop loading
        // data = $('#login-register').serialize()

        $.ajax({
            url: '/addUserEvent',
            data: $('#singlebutton').serialize(),
            method: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});



// $(document).ready(function() {
//     $('#singlebutton').click(function(){
//         $.ajax({
//             url: '/addUserEvent',
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