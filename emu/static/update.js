/* command history */
let cmdHistory = [];
let currentIndex = 0;

/* Updates text box from command input history */
function getHistory() {
  if (currentIndex > 0 && cmdHistory.length > currentIndex + 1) {
    let textBox = document.getElementById("textBox");
    currentIndex++;
    textBox.value = cmdHistory[currentIndex];
  } else if (currentIndex == 0 && cmdHistory.length > currentIndex) {
    let textBox = document.getElementById("textBox");
    cmdHistory.unshift(textBox.value);
    currentIndex++;
    textBox.value = cmdHistory[currentIndex];
  }
}

/* Updates textBox with 'future' commands */
function getFuture() {
  if (currentIndex > 0) {
    let textBox = document.getElementById("textBox");
    currentIndex--;
    textBox.value = cmdHistory[currentIndex];
    if (currentIndex == 0) {
      cmdHistory.shift();
    }
  }
}

/* Checks for up/down key input and calls history functions
 * Args:
 *  e: event
 */
function traverseHistory(e) {
  e = e || window.event;
  if (e.keyCode == "38") {
    console.log("up");
    getHistory();
  } else if (e.keyCode == "40") {
    console.log("down");
    getFuture();
  }
}
let textBox = document.getElementById("textBox");
textBox.onkeydown = traverseHistory;

/* Gets user text entry from form, sends request, updates DOM */
function sendEntry() {
  let form = document.getElementById("textBox");
  let input = form.value;
  if (input != "") {
    cmdHistory.unshift(input);
  } else {
      let newInputLine = document.createElement("p");
      newInputLine.textContent = "$";
      document.getElementById("output").appendChild(newInputLine);
      form.scrollIntoView();
      return;
  }
  form.value = "";
  currentIndex = 0;
  cmdHistory = cmdHistory.filter((cmd) => {
    return cmd != "";
  });

  // update input
  let newInputLine = document.createElement("p");
  newInputLine.textContent = "$ " + input;
  document.getElementById("output").appendChild(newInputLine);

  let formData = new FormData();
  formData.append("text", input);

  let request = new XMLHttpRequest();
  request.open("POST", "/entry");
  request.onreadystatechange = function () {
    if (request.readyState === XMLHttpRequest.DONE) {
      let status = request.status;
      if (status === 0 || (status >= 200 && status < 400)) {
        let response = JSON.parse(request.response);
        response.lines.forEach((line) => {
          let newLine = document.createElement("p");
          newLine.textContent = line;
          document.getElementById("output").appendChild(newLine);
        });
      } else {
        let errLine = document.createElement("p");
        errLine.classList.add("error");
        document.getElementById("output").appendChild(errLine);
        console.log("error");
      }
      form.scrollIntoView();
    }
  };

  request.send(formData);
}

/* Input form is selected on page load and any click in 'window'*/
textBox.focus();
textBox.select();
document.getElementsByClassName("window")[0]
    .addEventListener('click', function(event) {
        textBox.focus();
    });
