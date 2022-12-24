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
        table_content(JSON.parse(data))
        ExportData(JSON.parse(data))
    }
});


function table_content(data){

   var table_body = document.querySelector('tbody')
   var table_head = document.querySelector('thead')

   removeAllChildNodes(table_body)

   for (var i =0; i < 10; i++){

    console.log(i)

    var row = document.createElement('tr')

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
    CSV += `"ID","Sequence","Master Protein Accession","Master Protein Description","Cleavage Side","Annotated Sequence","Abundance"\r\n`

    for (var i = 0; i < arrData.length; i++) {
        var row = "";
        //2nd loop will extract each column and convert it in string comma-seprated
        //FixMe: sequence spelling 
        for (var index in Object.keys(arrData[i].fields)) {
            console.log(index)
            row += '"' + arrData[i].fields[Object.keys(arrData[i].fields)[index]] + '",';
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
    blob = new Blob([csv], { type: 'text/csv' });
    var csvUrl = window.webkitURL.createObjectURL(blob);
    var filename =  (ReportTitle || 'UserExport') + '.csv';
    $("#lnkDwnldLnk")
        .attr({
            'download': filename,
            'href': csvUrl
        });

    $('#lnkDwnldLnk')[0].click();
    document.body.removeChild(link);
}