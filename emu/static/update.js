function sendEntry() {
    let form = document.getElementById("textBox");
    let input = form.value;
    form.value = ''

    // update input
    let newInputLine = document.createElement("p");
    newInputLine.textContent = "$ " + input;
    document.getElementById("output").appendChild(newInputLine);

    // TODO POST to server, get response
    // let formData = new FormData(form);

    let formData = new FormData();
    formData.append("text", input)

    let request = new XMLHttpRequest();
    request.open("POST", "/entry", false);
    request.onreadystatechange = function() {
        if (request.readyState === XMLHttpRequest.DONE) {
            let status = request.status;
            if (status === 0 || (status >= 200 && status < 400)) {
                // TODO render element
                console.log(request.responseText);
            } else {
                // TODO handle error
                console.log("error");
            }
        }
    }
    request.send(formData);


    form.scrollIntoView();
}

function it_worked() {
    console.log("it worked!");
}
