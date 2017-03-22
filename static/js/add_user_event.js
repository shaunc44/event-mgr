$(document).ready(function() {
    $('#singlebutton').click(function(){
        $.ajax({
            url: '/addUserEvent',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

