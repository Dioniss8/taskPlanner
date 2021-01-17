function getAllUsersFromDb()
{
    let name = "get-all-users";
    $.ajax({
        url: "/api/" + name,
    }).done(function (res) {
        let element = document.getElementById("target");
        element.innerHTML = res.data[0].username;
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
                changeElementsValue(res.data, "target");
                changeElementsValue(res.usage, "usage");
            }else {
                changeElementsValue("Missing symbol", "usage");
            }
    });
}

function changeElementsValue(innerValue, elementId)
{
    let element = document.getElementById(elementId)
    element.innerHTML = innerValue
}