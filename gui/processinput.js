//stores actual file processing stuff

var input = function () {
    this.file=read_file();//stores the file with the information
    this.line = 0; //stores the position in the file
    this.dat = this.file.split("\n");  //the array of elements split by newline
};
