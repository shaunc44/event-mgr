$(document).ready(function(){
    // MUSTACHE.JS
    Mustache.tags = [ '<%', '%>' ];

    $.ajax({
        url : '/getEventsByUser',
        method : 'GET',
        dataType: 'json',
        success: function(data){
            // MUSTACHE.JS  -- Events diplay
            var eventsTemplate = $("#eventList").html();
            var eventsRender = Mustache.render(eventsTemplate, data);
            $(".list-group").html(eventsRender);
        },
        error: function(error){
            console.log(error);
        }
    });
});


    // $.ajax({
    //     url : '/getUsername',
    //     method : 'GET',
    //     dataType: 'json',
    //     success: function(data){
    //         // MUSTACHE.JS
    //         // Username display
    //         var usernameTemplate = $("#username-header-scrpt").html();
    //         var usernameRender = Mustache.render(usernameTemplate, data);
    //         $(".username-header-html").html(usernameRender);
    //     },
    //     error: function(error){
    //         console.log(error);
    //     }
    // });

