//jquery ajax call to open data file
function read_file() {
$.ajax({url: "data.txt", success: function(data) {
    return data;
}});
}
