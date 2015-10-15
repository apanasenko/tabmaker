function remove_team(url, id){
    $.post(url, {id: id},
        function(data, status){
            $('#message').text(data.message);
        }
    );
}
