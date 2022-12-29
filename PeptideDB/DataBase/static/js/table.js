var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

if (temp_acc != 'undefined' && temp_des == 'undefined'){
    var link = `http://127.0.0.1:8000/PepView/?acc=${temp_acc}`
} else if (temp_acc == 'undefined' && temp_des != 'undefined'){
   var link = `http://127.0.0.1:8000/PepView/?des=${temp_des}`
} else if (temp_acc != 'undefined' && temp_des != 'undefined'){
   var link = `http://127.0.0.1:8000/PepView/?acc=${temp_acc}&des=${temp_des}`
}

getJSON(link,
function(err, data) {
    if (err !== null) {
        alert('Something went wrong: ' + err);
    } else {   
        console.log("OKKK1")
        table_content(JSON.parse(data))
        ExportData(JSON.parse(data))

        $(document).ready(function () {
            $('#example').DataTable({
                // data:data,
            });
        });
    }
});

function table_content(data){
    var table_body = document.querySelector('tbody')
    removeAllChildNodes(table_body)

    for (var i =0; i < data.length; i++){
        var row = document.createElement('tr')
    if (i % 2 == 0) {
        row.className = 'even'
    } else{
        row.className = 'odd'
    }

    row.innerHTML  =   `<td>${data[i].fields.db_id}</td>
                        <td>${data[i].fields.peptide_sequence}</td>
                        <td>${data[i].fields.accession}</td>
                        <td>${data[i].fields.gene_symbol}</td>
                        <td>${data[i].fields.protein_name}</td>
                        <td>${data[i].fields.cleavage_site}</td>
                        <td>${data[i].fields.annotated_sequence}</td>
                        <td>${data[i].fields.cellular_compartment}</td>
                        <td>${data[i].fields.species}</td>
                        <td>${data[i].fields.database_identified}</td>
                        <td>${data[i].fields.description}</td>
                        <td><a href=${data[i].fields.reference_link} target="_blank" >${data[i].fields.reference_number}</a></td>`

    table_body.append(row)
    }             
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}


function ExportData(data){
    document.querySelector('.form-control.dt-tb').addEventListener('change', (e)=>{

        if (e.target.value == 'all'){
            JSONToCSVConvertor(data, 'test', true)
        } else{
        }    
    })
}

function JSONToCSVConvertor(JSONData, ReportTitle) {
    var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;
    var arrData = JSONData
    var CSV = '';
    CSV += `ID\tPeptide Sequence\tAccession\tGene symbol\tProtein name\tCleavage side\tAbundance sequence\tCellular compartment\tSpecies\tDatabase identified\tDescription\tReference\tLink\r\n`

    for (var i = 0; i < arrData.length; i++) {
        var row = "";
        var headers = ['db_id','accession','gene_symbol','protein_name','cleavage_site','peptide_sequence','annotated_sequence','cellular_compartment','species','database_identified','description','reference_number','reference_link']
        for (var index in headers) {
            row += `${arrData[i].fields[headers[index]]}\t`;
        }

        row.slice(0, row.length - 1);
        //add a line break after each row
        CSV += row + '\r\n';
    }

    if (CSV == '') {
        alert("Invalid data");
        return;
    }

    //this trick will generate a temp "a" tag
    var link = document.createElement("a");
    link.id = "lnkDwnldLnk";

    //this part will append the anchor tag and remove it after automatic click
    document.body.appendChild(link);

    var csv = CSV;
    blob = new Blob([tsv], { type: 'text/tsv' });
    var csvUrl = window.webkitURL.createObjectURL(blob);
    var filename =  (ReportTitle || 'UserExport') + '.tsv';
    $("#lnkDwnldLnk")
        .attr({
            'download': filename,
            'href': csvUrl
        });

    $('#lnkDwnldLnk')[0].click();
    document.body.removeChild(link);
}