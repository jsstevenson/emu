function sendEntry() {
    let form = document.getElementById("textBox");
    let input = form.value;
    form.value = ''

    // update input
    let newInputLine = document.createElement("p");
    newInputLine.textContent = "$ " + input;
    document.getElementById("output").appendChild(newInputLine);

    let formData = new FormData();
    formData.append("text", input)

    let request = new XMLHttpRequest();
    request.open("POST", "/entry");
    request.onreadystatechange = function() {
        if (request.readyState === XMLHttpRequest.DONE) {
            let status = request.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                let response = JSON.parse(request.response);
                response.lines.forEach(line => {
                    let newLine = document.createElement("p");
                    newLine.textContent = line
                    document.getElementById("output").appendChild(newLine);
                })
            } else {
                let errLine = document.createElement("p");
                errLine.classList.add("error");
                document.getElementById("output").appendChild(errLine);
                console.log("error");
            }
            form.scrollIntoView();
        }
    }

    request.send(formData);
}

var input = document.getElementById('textBox');
input.focus();
input.select();
