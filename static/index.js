/**
 * Probably should have used alert()...
 */

function getHistoricalDataBySymbolName()
{
    let inputNode = document.getElementById("symbol");
    let symbol = inputNode.value;
    $.ajax({
        url: "/api/get-historical-data/",
        dataType: "json",
        type: "POST",
        data: {"symbol": symbol},
    }).done(function (res) {
        if (res.success > 0) {
            changeElementsValue(res.data, "keys");
            changeElementsValue(res.usage, "usage");
        } else {
            changeElementsValue(res.usage, "usage");
        }
        checkForErrorMessageBox(res.success, res.reason);
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
                makeListVisible();
                changeElementsValue(res.ebitdaMarginRaw, "ebitdaMarginRaw");
                changeElementsValue(res.symbol, "stockSymbol");
                changeElementsValue(res.keys, "keys");
                changeElementsValue(res.exchange, "exchange");
                changeElementsValue(res.usage, "usage");
                changeElementsValue(res.longName, "longName");
                changeElementsValue(res.grossMargin, "grossMargin");
                changeElementsValue(res.debtToEquity, "debtToEquity");
                changeElementsValue(res.returnOnAssets, "returnOnAssets");
                changeElementsValue(res.freeCashFlow, "freeCashFlow");
            }else {
                changeElementsValue(res.usage, "usage");
            }

            checkForErrorMessageBox(res.success, res.reason);
    });
}

function checkForErrorMessageBox(success, error) {
    let element = document.getElementById("alerter");
    if (success === false) {
        element.innerHTML = "<b>" + error + "</b>";
        element.style.visibility = "visible";
        return;
    }

    element.innerHTML = "";
    element.style.visibility = "hidden";
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