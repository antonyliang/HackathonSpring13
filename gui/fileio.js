//jquery ajax call to open data file
var file = null;
function read_file() {
$.ajax({url: "data.txt", success: function(data) {
    alert("THIS IS THE DATA MAN " + data);
    file = data;
}});
alert("FILE MAN FILE " + file);
return file;}
