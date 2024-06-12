document.addEventListener("DOMContentLoaded",function ()
{
    const query = document.getElementById('searchQuery');
    query.addEventListener('keypress',(KeyboardEvent) => {
        if (event.key == 'Enter'){
            performSearch();
        }
    });
});

async function performSearch() {
    const query = document.getElementById('searchQuery').value.toLowerCase();
    const results = document.getElementById('results');
    results.innerHTML = ''; // Clear previous results

    if (query) {
        term = {'doc':'','term':query};
        json = JSON.stringify(term);
        let result = await postData(json);
        total = result.pop();
        if (result.length>0){
            list = document.createElement('ul');
            for (r of result){
                element = document.createElement("li");
                element.textContent = r;
                list.appendChild(element);
            }
            results.appendChild(list);
        }else{
            results.innerText = 'No result found';
        }
        
    }
}


async function postData(json) {
    url = 'http://localhost:8080/v1/references';
    const response = await fetch(url, {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json'
      },
      body: json
    });
    return response.json();
  }