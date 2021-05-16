const form = document.querySelector(".top-banner form");
const input = document.querySelector(".top-banner input");
const msg = document.querySelector(".top-banner .msg");
const list = document.querySelector(".ajax-section .cities");
var input_v;
//var intervalID = setInterval(function(){start(input_v)},5000)

function start(inputVal){
  console.log(input_v)
  const url = `http://127.0.0.1:5000/current/${inputVal}`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      const { humidity,location, moisture, status, temperature } = data;
      if (location != undefined){const li = document.createElement("li");
      li.classList.add("city");
      const markup = `
        <h1 class="city-name" data-name="${location}">
          <span>${location}</span>
        </h1><br><br>
        <h4>Status: ${status}<sup></sup></h4>
        <h4>Moisture: ${moisture}<sup>%</sup></h4>
        <h4>Humidity: ${humidity}<sup>%</sup></h4>
        <h4>Temperature: ${temperature}<sup>°C</sup></h4>
        
      `;
      li.innerHTML = markup;
      list.appendChild(li);
    }
    else{
      throw 'error';
    }
    })
    .catch(() => {
      msg.textContent = "Please search for a valid phase";
    });

  msg.textContent = "";
  //form.reset();
  input.focus();
}

form.addEventListener("submit", e => {
  e.preventDefault();
  let inputVal = input.value;
  input_v = inputVal
  //check if there's already a city
  const listItems = list.querySelectorAll(".ajax-section .city");
  const listItemsArray = Array.from(listItems);

  if (listItemsArray.length > 0) {
    const filteredArray = listItemsArray.filter(el => {
      let content = "";
      //athens,gr
      if (inputVal.includes(",")) {
        //athens,grrrrrr->invalid country code, so we keep only the first part of inputVal
        if (inputVal.split(",")[1].length > 2) {
          inputVal = inputVal.split(",")[0];
          content = el
            .querySelector(".city-name span")
            .textContent.toLowerCase();
        } else {
          content = el.querySelector(".city-name").dataset.name.toLowerCase();
        }
      } else {
        //athens
        content = el.querySelector(".city-name span").textContent.toLowerCase();
      }
      return content == inputVal.toLowerCase();
    });

    if (filteredArray.length > 0) {
      msg.textContent = `You already know the info for ${
        filteredArray[0].querySelector(".city-name span").textContent
      }`;
      form.reset();
      input.focus();
      return;
    }
  }
  start(input_v)
});

