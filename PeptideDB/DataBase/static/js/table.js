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
    var link = `http://${host_name}/PepView/?acc=${temp_acc}`
} else if (temp_acc == 'undefined' && temp_des != 'undefined'){
   var link = `http://${host_name}/PepView/?des=${temp_des}`
} else if (temp_acc != 'undefined' && temp_des != 'undefined'){
   var link = `http://${host_name}/PepView/?acc=${temp_acc}&des=${temp_des}`
}

getJSON(link,
function(err, data) {
    if (err !== null) {
        alert('Something went wrong: ' + err);
    } else {   
        
        table_content(data)
        ExportData(data)

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

    var ref_list = []

    for (var j = 0; j < data[i].reference_link.length;  j++) {
        ref_list.push(`<a href=${data[i].reference_link[j]} target="_blank" >${data[i].reference_number[j]}</a>`)
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


$(document).ready(function(){

    console.log("ok")
    $('#data').after('<div id="nav"></div>');
    var rowsShown = 4;
    var rowsTotal = $('#data tbody tr').length;
    var numPages = rowsTotal/rowsShown;
    for(i = 0;i < numPages;i++) {
        var pageNum = i + 1;
        $('#nav').append('<a href="#" rel="'+i+'">'+pageNum+'</a> ');
    }
    $('#data tbody tr').hide();
    $('#data tbody tr').slice(0, rowsShown).show();
    $('#nav a:first').addClass('active');
    $('#nav a').bind('click', function(){

        $('#nav a').removeClass('active');
        $(this).addClass('active');
        var currPage = $(this).attr('rel');
        var startItem = currPage * rowsShown;
        var endItem = startItem + rowsShown;
        $('#data tbody tr').css('opacity','0.0').hide().slice(startItem, endItem).
        css('display','table-row').animate({opacity:1}, 300);
    });
});

