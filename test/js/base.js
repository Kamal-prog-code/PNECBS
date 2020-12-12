var negbtn = document.getElementsByClassName("neg_cls")

for (var i = 0 ; i < negbtn.length; i++) {
    negbtn[i].addEventListener('click',function(){
    var itemid = this.dataset.itemid
    datatrans(itemid)
  })
}

function datatrans(itemid){
  console.log('Sending data...')

  var url = '/get_content/'
  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'itemid':itemid})
  })

  .then((response) => {
    return response.json()
  })

  .then((data) => {
    console.log('data',data)
  })
}