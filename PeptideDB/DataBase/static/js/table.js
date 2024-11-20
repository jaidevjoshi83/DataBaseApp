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

var hostname = document.getElementById('hostname').getAttribute('data-hostname');
var query_acc = document.getElementById('hostname').getAttribute('data-acc');
var query_des = document.getElementById('hostname').getAttribute('data-des');
var query_pep = document.getElementById('hostname').getAttribute('data-pep');

let link = `https://${hostname}/PepView/?`;

const params = [];


if (query_acc !== 'undefined') {
    params.push(`acc=${query_acc}`);
}
if (query_des !== 'undefined') {
    params.push(`des=${query_des}`);
}
if (query_pep !== 'undefined') {
    params.push(`pep=${query_pep}`);
}


console.log(params)
// Combine parameters with '&' and append to the link
link += params.join('&');


console.log(link)

getJSON(link,
function(err, data) {
    if (err !== null) {
        alert('Something went wrong: ' + err);
    } else {   

        ExportData(data)
        table_content(data)

    }
});

function table_content(data){

    var table_body = document.querySelector('tbody')
    removeAllChildNodes(table_body)

    for (var i = 0; i < data.length; i++){
        var row = document.createElement('tr')
        if (i % 2 == 0) {
            row.className = 'even'
        } else{
            row.className = 'odd'
        }

        var ref_list = []

        for (var j = 0; j < data[i].reference_link.length;  j++) {
            ref_list.push(`<a href=http://doi.org/${data[i].reference_link[j]} target="_blank" rel="noopener noreferrer" >${data[i].reference_link[j]}</a>`)
        }
       
        row.innerHTML  =   `<td>${i+1}</td>
                            <td>${data[i].peptide_sequence}</td>
                            <td>${data[i].accession}</td>
                            <td>${data[i].gene_symbol}</td>
                            <td>${data[i].protein_name}</td>
                            <td>${data[i].cleavage_site}</td>
                            <td>${data[i].annotated_sequence}</td>
                            <td>${data[i].cellular_compartment}</td>
                            <td>${data[i].species}</td>
                            <td>${data[i].database_identified}</td>
                            <td>${data[i].description}</td>
                            <td>${ref_list.join(', ')}</td>`

        table_body.append(row)

        $(document).ready(function() {
            $('#sampleTable').DataTable();
        });
    }             
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function ExportData(data){
    document.querySelector('#export_data').addEventListener('click', (e)=>{

        console.log("OK")
        // if (e.target.value == 'all'){
        JSONToCSVConvertor(data, 'diced', true)
        // } else{
        // }    
    })
}

function JSONToCSVConvertor(JSONData, ReportTitle) {
    var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;
    var arrData = JSONData

    var CSV = '';
    CSV += `ID\tAccession\tGene symbol\tProtein name\tCleavage side P1 residue\tPeptide sequence\tAnnotated Sequence\tCellular compartment\tSpecies\tDatabase identified\tDescription\tReference\r\n`

    for (var i = 0; i < arrData.length; i++) {
        var row = "";
        var headers = ['db_id','accession','gene_symbol','protein_name','cleavage_site','peptide_sequence','annotated_sequence','cellular_compartment','species','database_identified','description','reference_link']
        for (var index in headers) {
            row += `${arrData[i][headers[index]]}\t`;
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

    var tsv = CSV;
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

//#######################################################################

function return_data_dict(table_data){

    var pgs = {}
    var total_rows = 20

    for (var i = 0; i < Math.floor(table_data.length/total_rows ); i++){
        pgs[i] = table_data.slice(i*total_rows, (i+1)*total_rows)
    }
    pgs[Math.floor(table_data.length/total_rows )] = table_data.slice(Math.floor(table_data.length/total_rows)*total_rows, )

    return pgs
}
