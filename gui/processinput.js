//stores actual file processing stuff

var Input = function (input) {
    this.file=input;//stores the file with the information
    //    alert(this.file);
    this.line = 0; //stores the position in the file
    this.stats = this.file.split(",");  //the array of elements split by newline
    this.xaxisv = 0;
    this.toString = function () {
        return "File: " + this.file + " current line position: " + this.line
        + " split array: " + this.stats;
    };
};
