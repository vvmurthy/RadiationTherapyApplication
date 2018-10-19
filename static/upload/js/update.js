function update_ct(){
    $.ajax(
        {
            url : 'users/patients/data/cts',
            type = 'POST'
        ,
        success : function(json){
            $('#mstatus').html(json.matchstatus);
            $("#ct").attr('src', json.imgsrc)
        }
        });
};