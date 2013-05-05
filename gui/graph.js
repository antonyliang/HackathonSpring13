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
var linegraph = null;
var profitgraph = null;
var servergraph = null;
var xaxis_val = 1;
var linepos = 0;
var linevals = [];
 for(var i = 0; i < 10; i = i + 1) {
     lines[i] = new Array();
  }
 for(var i = 0; i < 13; i = i + 1) {

     lines[i] = {show: true};
     plots[i] = {show: true};
     data[i] = new Array();

 }

 function update_plot() {
     linegraph.setData([data[0], data[1], data[2]]);
     linegraph.setupGrid();
     linegraph.draw();
     profitgraph.setData([data[12]]);
     profitgraph.setupGrid();
     profitgraph.draw();
     servergraph.setData([data[3], data[4], data [5], data[6],
                         data[7], data[8], data[9], data[10], data[11]]);
     servergraph.setupGrid();
     servergraph.draw();
 }

 function update_fromline (line) {
//     alert("Here's your line: " + line);
     var input = line.split(",");
  //   alert("Your split: " + input);
     for(var n = 0; n < input.length; n = n +1) {
         data[n].push([xaxis_val, input[n]]);
     }
     update_plot();
 }


function set_visible(index, isVisible) {
    if(!isVisible) {
        lines[index] = {show: false};
        plots[index] = {show: false};
    }
    else {
        lines[index] = {show: true};
        plots[index] = {show: true};
    }

}
//alert("Now instantiating graph");
//alert("value of file:" + file);
//alert("This is control " + control);

function parse_file () {

    alert("parsing");
    var fi = null;
    fi = read_file();
    while(fi !== null && fi !== "") {
        fi = read_file();
        linevals = fi.split("\n");
        while(linepos < linevals.length) {
            console.log(linepos);
            console.log(linevals.length);
            update_fromline(linevals[linepos]);
            linepos = linepos + 1;
            xaxis_val = xaxis_val + 1;
            update_plot();
        }
        alert("done");
    }
}
   $(document).ready(function () {
      linegraph = $.plot (
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

            }
            
        ]
    );
//       alert("starting the process");
       profitgraph = $.plot (
           $("#profitgraph"),
           [
               {
                   label: "Profit",
                   data: data[12],
                   lines: lines[12],
                   points: plots[12]
                   
               }

           ]
       );
       servergraph = $.plot (
           $("#servergraph"),
           [
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

               }
           ]
       );
       parse_file();
   }
                    );
