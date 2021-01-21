let isErrorVisible = false;

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
                makeListVisible();
                changeElementsValue(res.ebitdaMarginRaw, "ebitdaMarginRaw");
                changeElementsValue(res.symbol, "stockSymbol");
                changeElementsValue(res.keys, "keys");
                changeElementsValue(res.exchange, "exchange");
                changeElementsValue(res.usage, "usage");
                changeElementsValue(res.longName, "longName");
                changeElementsValue(res.grossMargin, "grossMargin");
                changeElementsValue(res.debtToEquity, "debtToEquity");
            }else {
                changeElementsValue(res.reason, "usage");
            }
    });
}

function checkForErrorMessageBox() {
    //TODO
}

function makeListVisible()
{
    let element = document.getElementById("list");
    element.style.visibility = "visible";
}

function changeElementsValue(innerValue, elementId)
{
    let element = document.getElementById(elementId)
    element.innerHTML = innerValue
}