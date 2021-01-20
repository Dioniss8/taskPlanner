function getAllUsersFromDb()
{
    let name = "get-all-users";
    $.ajax({
        url: "/api/" + name,
    }).done(function (res) {
        let element = document.getElementById("stockSymbol");
        element.innerHTML = res.data[0].username;
        console.log(res.data.length);
    })
}

function getStatisticsBySymbolName()
{
    let name = "get-statistics/";
    let inputNode = document.getElementById("symbol");
    let symbol = inputNode.value;
    $.ajax({
        url: "/api/" + name,
        dataType: "json",
        type: "POST",
        data: {'symbol': symbol},
    }).done(function (res) {
            if(res.success > 0){
                changeElementsValue(res.ebitdaMarginRaw, "ebitdaMarginRaw");
                changeElementsValue(res.symbol, "stockSymbol");
                changeElementsValue(res.keys, "keys");
                changeElementsValue(res.exchange, "exchange");
                changeElementsValue(res.usage, "usage");
                changeElementsValue(res.longName, "longName");
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