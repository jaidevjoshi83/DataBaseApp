function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
  }

document.querySelectorAll('button')[2].addEventListener('click', ()=>{
    var data = { }
    var Inps = document.querySelector('#bugs-form').querySelectorAll('input')

    for (var i = 0; Inps.length > i; i++ ){

        if (Inps[i].value == '' && (Inps[i].name != 'email' && Inps[i].name != 'name' && Inps[i].name != 'institution')){
            Inps[i].style.background  = 'pink'
            return 

        } else{
            Inps[i].style.background  = ''
            data[Inps[i].name] =  Inps[i].value
            Inps[i].value =  ''
        }
    }

    if (document.querySelector('#bugs-form').querySelectorAll('textarea')[0].value == ''){
        document.querySelector('#bugs-form').querySelectorAll('textarea')[0].style.background  = 'pink' 
    } else {
        data[document.querySelector('#bugs-form').querySelectorAll('textarea')[0].name] = document.querySelector('#bugs-form').querySelectorAll('textarea')[0].value
        document.querySelector('#bugs-form').querySelectorAll('textarea')[0].value = ''
    }

    data[document.querySelector('#bugs-form').querySelectorAll('select')[0].name] = document.querySelector('#bugs-form').querySelectorAll('select')[0].value
    // document.querySelector('#bugs-form').querySelectorAll('select')[0].value = ''
    
    const url = `/bugs?data=${JSON.stringify(data)}`;

    fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'), // Fetch and include the CSRF token
    },

    // body: JSON.stringify({ jai: 'hi' })

    })
    .then(response => {
        if (response.ok) {
            document.querySelector('#post-error').innerHTML =  'Posted Successfuly...'
        return response.json();
        }
        throw new Error('Error:' + response.status);
    })
    .then(responseData => {
        console.log('Response:', responseData);
    })
    .catch(error => {
        console.error('Error:', error);
        console.log("error")
    });
})

document.querySelector('#bug-title').addEventListener('click', ()=>{
    document.querySelector('#post-error').innerHTML =  ''
})