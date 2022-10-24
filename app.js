var ipp = require('ipp');
var fs = require('fs');

fs.readFile('2022-10-19 12_47_07.535848.pdf', function (err, data) {
    if (err)
        throw err;

    var printer = ipp.Printer("http://192.168.168.50/ipp");
    var msg = {
        "operation-attributes-tag": {
            "requesting-user-name": "user",
            "job-name": "scripted job",
            "document-format": "application/pdf"
        },
        data: data
    };
    printer.execute("Print-Job", msg, function (err, res) {
        console.log(res);
    });
});