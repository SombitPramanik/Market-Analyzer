const ServerAddress = "http://127.0.0.1:5000/GetPossibleStockList";
const GetGraphAddress = "http://127.0.0.1:5000/FetchGraph";
let optionData = {};
const DropDowns = document.querySelectorAll(".DropDown");
let GetRuleGetTime = [];
DropDowns.forEach(DropDown => {
    const select = DropDown.querySelector(".select");
    const caret = DropDown.querySelector(".caret");
    const DropDownMenu = DropDown.querySelector(".DropDownMenu");
    const options = DropDown.querySelector(".DropDownMenu");
    const selected = DropDown.querySelector(".selected");

    select.addEventListener('click', () => {
        select.classList.toggle("selectClicked");
        caret.classList.toggle("caretRotate");
        DropDownMenu.classList.toggle("DropDownMenuOpen");
    });

    options.addEventListener('click', (event) => {
        if (event.target.tagName === 'LI') {
            selected.innerHTML = event.target.innerHTML;
            select.classList.remove("selectClicked");
            caret.classList.remove("caretRotate");
            DropDownMenu.classList.remove("DropDownMenuOpen");

            const selectedOption = event.target;
            const allOptions = options.querySelectorAll("li");

            allOptions.forEach(opt => {
                opt.classList.remove("active");
            });
            selectedOption.classList.add("active");

            if ((selectedOption.getAttribute("value") !== null) && selectedOption.getAttribute("WhoAreYOU") !== "iamStockValue") {
                // When the Stock name and the time is selected
                console.log(selectedOption.getAttribute("value"));
                GetRuleGetTime.push(selectedOption.getAttribute("value"));
                console.log(GetRuleGetTime);
                if (GetRuleGetTime.length === 2) {
                    let SendingData = {
                        RuleName: GetRuleGetTime[0],
                        TimeDelta: GetRuleGetTime[1]
                    };
                    let MethodConstructor = {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(SendingData)
                    };
                    fetch(ServerAddress, MethodConstructor).then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    }).then(ReceivedData => {
                        let ul = document.getElementById("SelectStockList");
                        ul.innerHTML = '<li WhoAreYOU="iamStockValue" value="Default" class="active">chose stock</li>';

                        ReceivedData.forEach(StockName => {
                            const li = document.createElement("li");
                            li.setAttribute("WhoAreYOU", "iamStockValue");
                            li.setAttribute("value", `${StockName}`);
                            li.textContent = StockName;
                            ul.appendChild(li);
                        });

                    }).catch(error => {
                        console.log("Some Problem with Fetch Function", error);
                    });
                    //Reset the Variable after completing all operation
                    GetRuleGetTime.length = 0;
                }

            }
            else {
                // when the stock list is selected
                // all the Stock list available hear
                let TimeDelta = document.getElementsByClassName("active")[1].getAttribute("value");
                if(TimeDelta !== null){
                    let SendingData ={
                        "TimeDelta": TimeDelta,
                        "StockName": selectedOption.getAttribute("value")
                    };
                    let MethodConstructor = {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(SendingData)
                    };
                    fetch(GetGraphAddress, MethodConstructor).then(response => response.blob())
                    .then(blob => {
                        // Create a URL for the blob
                        const url = URL.createObjectURL(blob);
                        // Set the src attribute of the img tag to the URL
                        document.getElementById('plotGraph').src = url;
                    })
                    .catch(error => {
                        console.log("Some Problem with Fetch Function", error);
                    });
                }
            }
        }
    });
});