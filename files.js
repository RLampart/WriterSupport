document.addEventListener("DOMContentLoaded",function ()
{
    addFiles();
});

function home(){
    location.assign('home.html');
}

function editor(){
    location.assign('editor.html');
}

function search(){
    location.assign('search.html');
}

async function addFiles(){
    const content = document.getElementById('files');
    content.innerHTML = "";
    files = await getData();
    content.innerHTML += "<ul>";
    if (files.length>1){
        for (file of files){
            content.innerHTML += "<li>";
            content.innerHTML += `<img src='x icon.png' alt='close icon' class='icon' onclick='removeDoc("${file}")' />`;
            content.innerHTML += "<span>"+file+"</span>";
            content.innerHTML += "</li>";
        }
    }else if (files.length==1){
        content.innerHTML += "<li>";
        content.innerHTML += `<img src='x icon.png'  alt='close icon' class='icon' onclick='removeDoc("${files}")' />`;
        content.innerHTML += "<span>"+files+"</span>";
        content.innerHTML += "</li>";
    }
    
    content.innerHTML += "</ul>";
}

async function removeDoc(filename){
    choice = confirm(`Remove ${filename}?`);
    if (choice){
        url = 'http://localhost:8080/v1/removeDoc';
        const response = await fetch(url, {
        method: 'POST', 
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({"file":filename})
      });
        const result = await response.json();
        alert(result['msg']);
        addFiles();
  }
    
}

async function sendDoc() {
        input = document.getElementById('fileInput');
        const [file] = input.files;
        const formData = new FormData();

        formData.append('files', file);

        try {
            const response = await fetch('http://localhost:8080/v1/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            const result = await response.json();
            alert(result['msg']);
            addFiles();
        } catch (error) {
            console.log(error);
        }
    }


async function getData() {
    url = 'http://localhost:8080/v1/files';
    const response = await fetch(url, {
      method: 'GET', 
    });
    return response.json();
  }






