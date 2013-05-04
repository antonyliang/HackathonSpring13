/* This is the code for the graph that plots the ten game server
** integer outputs, which are server info plus profit. */

//written by Andrew Spano, uses flot.js and jquery.js

/*whole function must be wrapped in a jquery document.ready
 *to avoid loading before the html */


//trying to establish dynamic graph, making parameters into vars themselves
var file;
var control;
var lines = new Array();
var plots = new Array();
var data = new Array();
for(var i = 0; i < 10; i = i + 1) {
    lines[i] = new Array();
 }
for(var i = 0; i < 13; i = i + 1) {

    lines[i] = {show: true};
    plots[i] = {show: true};
    data[i] = new Array();

}

// draw_graph();
file = read_file();
//alert("this should work" + file);
if(file != null) {
    control = new Input(file);
}

function update_data (index, dat) {
    data[index] = dat;
}

function update_fromfile () {
    alert("updating from file");
    var splitdata;
    var isRunning = true;
    while(control.linepos < control.lines.length) {
        splitdata = control.lines[control.linepos].split(","); //splits current line into comma split array of ints
        if(splitdata[0] === "STOP") {
            return false;
        }
        for(var i in data) {
            //alert(splitdata[i]);
            data[i].push([control.xaxisv, splitdata[i]]);
        }
        control.xaxisv += 30;
        control.linepos += 1;
    }
    return isRunning;
}


function set_visible(index, yesorno) {
    if(!yesorno) {
        lines[index] = {show: false};
        plots[index] = {show: false};
    }
    else {
        lines[index] = {show: true};
        plots[index] = {show: true};
    }

    draw_graph();
}
//alert("Now instantiating graph");
//alert("value of file:" + file);
//alert("This is control " + control);
function draw_graph() {
    $.plot (
        $("#placeholder"),
        [
            {
                label: "Demand in the United States",
                data: data[0],
                lines: lines[0],
                points: plots[0]


            },
            {
                label: "Demand in the European Union",
                data: data[1],
                lines: lines[1],
                points: plots[1]
            },

            {

                label: "Demand in the Asian Pacific",
                data: data[2],
                lines: lines[2],
                points: plots[2]

            },


            {
                label: "Number of Web Servers in North America",
                data: data[3],
                lines: lines[3],
                points: plots[3]
            },

            {
                label: "Number of Web Servers in the European Union",
                data: data[4],
                lines: lines[4],
                points: plots[4]

            },

            {
                label: "Number of Web Servers in the Asian Pacific",
                data: data[5],
                lines: lines[5],
                points: lines[5]

            },

            {
                label: "Number of Java Servers in the United States",
                data: data[6],
                lines: lines[6],
                points: plots[6]

            },
            {
                label: "Number of Java Servers in the European Union",
                data: data[7],
                lines: lines[7],
                points: plots[7]

            },
            {
                label: "Number of Java Servers in the Asian Pacific",
                data: data[8],
                lines: lines[8],
                points: plots[8]

            },
            {
                label: "Number of Database Servers in the United States",
                data: data[9],
                lines: lines[9],
                points: plots[9]

            },
            {
                label: "Number of Database Servers in the European Union",
                data: data[10],
                lines: lines[10],
                points: plots[10]

            },
            {
                label: "Number of Database Servers in the Asian Pacific",
                data: data[11],
                lines: lines[11],
                points: plots[11]

            },

            {
                label: "Profit",
                data: data[12],
                lines: lines[12],
                points: plots[12]

            }
            
        ]
    );


}
