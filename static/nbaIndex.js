function getAllUsersFromDb()
{
    let name = "get-all-users";
    $.ajax({
        url: "/api/" + name,
    }).done(function (res) {
        for (let i = 0; i<res.data.length; i++) {
            let text = res.data[i].username + " " + res.data[i].id + "\n";
            console.log(res.data[i]);
            appendChildElementToTarget(text);
        }
        console.log(res.data.length);
    })
}

function getStatisticsBySymbolName()
{
    let name = "get-statistics/";
    let inputNode = document.getElementById("player_key");
    let symbol = inputNode.value;
    $.ajax({
        url: "/api/" + name,
        dataType: "json",
        type: "POST",
        data: {'symbol': symbol},
    }).done(function (res) {
            if(res.success > 0){
                appendChildElementToTarget(res.data);
                changeElementsValue(res.usage);
            }else {
                changeElementsValue("Missing symbol");
            }
    });
}

function changeElementsValue(innerValue)
{
    let element = document.getElementById("usage")
    element.innerHTML = innerValue
}


function appendChildElementToTarget(text)
{
    let base = document.createElement("div");
    base.innerHTML = text;
    let parent = document.getElementById("target");
    parent.appendChild(base);
}