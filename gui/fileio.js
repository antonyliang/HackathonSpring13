var file = null;
function read_file () {
    $.ajax({
        async: false,
        type: 'GET',
        url: 'data.txt',
        success: function(data) {
            //callback
            file = data;
        }
    })
    return file;};
