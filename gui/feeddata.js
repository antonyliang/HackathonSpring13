var dat  = new Array();


$(document).ready(function () {
    
    dat = [ [0, 0], [1,14], [2, 8], [3, 6]];
    update_data(1, [[0,0], [1,16], [2, 16], [3, 16]]);
    update_data(2, dat);
    update_data(3, dat);
    update_data(4, dat);
    update_data(5, dat);
    update_data(6, dat);
    update_data(7, dat);
    update_data(8, dat);
    update_data(9, dat);
    update_data(10, dat);
    update_data(11, dat);
    update_data(12, dat);
    draw_graph();

    alert("the graph will now set 0 and 1 to invisible");
    set_visible(0, false);
    set_visible(1, false);
}
                 );
