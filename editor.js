document.addEventListener("DOMContentLoaded",function ()
{
    const content = document.getElementById('editor');
    content.addEventListener('keypress',(KeyboardEvent) => reference());
});
function execCmd(command, value = null) {
    document.execCommand(command, false, value);
}

function saveDoc() {
   content = document.getElementById('editor').innerHTML;
   const text = content.innerText;

   // Create a Blob object with the text
   const blob = new Blob([text], { type: 'text/plain' });

   // Create a URL for the Blob
   const url = URL.createObjectURL(blob);

   // Create a temporary link element
   const a = document.createElement('a');
   a.href = url;
   a.download = 'textfile.txt'; // Set the default file name

   // Programmatically click the link to trigger the download
   a.click();

   // Clean up the URL object
   URL.revokeObjectURL(url);
}

async function loadDoc() {
    input = document.getElementById('fileInput');
    input.click();
   
 }

function openDocs() {
    location.assign('files.html');
}


function unhighlightEntries(){   
    choices = document.getElementsByTagName('p');
    for (ele of choices){
        if (ele.classList.contains('highlight')){
            ele.classList.remove('highlight');
        } 
    }
}

function showPopup(text){
    popup = document.getElementsByClassName('popuptext')[0];
    popup.innerText = text;
    popup.classList.toggle("show");
}

function removePopup(){
    popup = document.getElementsByClassName('popuptext')[0];
    if (popup.classList.contains('show')){
        popup.classList.toggle('show');
    }
}

function updateAside(results, search,len){
    const asidetop = document.getElementById('search');
    const aside = document.getElementById('list');
    editor = document.getElementById('editor');
    child = editor.firstChild;
    if (child.innerText == undefined){
        const sp1 = document.createElement("span");
        sp1.textContent = child.nodeValue;
        editor.replaceChild(sp1,child);
    }
    children = editor.children;
    choices = []
    for (child of children){
        if (child.innerText!='\n'){
            choices.push(child);
        }
    }
    total = results.pop();
    asidetop.innerText = search.slice(0,60) + '...';
    for (let r of results){
         element = document.createElement("li");
         r0 = r.split(':');
         first = r0[0].split(' ');
         num = first.pop();
         if (first[0] =='Current' & first[1]=='Document'){
            index = num-1;
            para = choices[index].innerText;
            console.log(index);
            r1 = r0[1].split('(');
            r3 = '(' + r1[1] + ': ' + r0[2].slice(0,8) + '])';
            if (para.length>100){
                para = para.slice(0,100) + '...';
            }
            r2 = r0[0]+': '+ para + ' '+ r3;
            choices[index].classList.add("highlight");
            element.textContent = r2;
            
         }
         else{
            link = document.createElement("a");
            link.href = "#";
            link.onclick = ()=>{showPopup(r.toString())};
            link.innerText = first.slice(0,first.length-1)+ ' ' + num+ ': Refer to document (Score: ' + r0[r0.length-1];
            element.appendChild(link);
         }
        aside.appendChild(element);
         
    }
}

async function reference(){
    if (event.key == 'Enter'){
        unhighlightEntries();
        removePopup();
        let asidetop = document.getElementById('search');
        let aside = document.getElementById('list');
        asidetop.innerHTML = '';
        aside.innerHTML = '';
        content = document.getElementById('editor');
        text = content.innerText;
        format = content.innerHTML;
        lines = text.split('\n');
        lines = lines.filter((x)=> x!='');
        sentence = lines.length;
        if (sentence>0){
            paper = lines.slice(0,sentence-1);
            paper = paper.join('\n');
            search = lines[sentence-1];
            json = JSON.stringify({doc:paper,term:search});
            result = await postData(json);
            updateAside(result,search,sentence-1);
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

  async function sendDoc() {
    input = document.getElementById('fileInput');
    const [file] = input.files;
    const formData = new FormData();

    formData.append('files', file);

    try {
        const response = await fetch('http://localhost:8080/v1/read', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const result = await response.json();
        let content = document.getElementById('editor');
        text = result['text'].filter((x)=> x!='');
        lines = '';
        for (t of text){
            lines += '<p>';
            lines += t;
            lines += '</p>';
        }
        content.innerHTML = lines;
    } catch (error) {
        console.log(error);
    }
}







