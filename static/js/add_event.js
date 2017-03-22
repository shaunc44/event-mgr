$(document).ready(function() {
    $('#singlebutton').on(function(event){

        event.preventDefault(); // tells html to stop loading
        // data = $('#login-register').serialize()

        $.ajax({
            url: '/addEvent',
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

