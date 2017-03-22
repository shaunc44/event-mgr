$(document).ready(function() {
    $('#login-register').on(function(event){

        event.preventDefault(); // tells html to stop loading
        // data = $('#login-register').serialize()

        $.ajax({
            url: '/signUp',
            data: $('#login-register').serialize(),
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