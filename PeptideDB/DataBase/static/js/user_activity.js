
if(document.querySelector('#upload-type') != null){
    document.querySelector('#upload-type').addEventListener('change', (e)=>{

        if (e.target.value == 'newfile'){
            window.location = 'data_upload'
        }else{
            window.location = '/upload_page';
        }
    })

}

