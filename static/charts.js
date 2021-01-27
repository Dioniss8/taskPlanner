function getAdjustedCloseArray() {
	let adjCloseSeries = [];
	let openSeries = [];
	let symbol = document.getElementById("symbol").value;
	$.ajax({
		url: "/api/get-historical-data/",
		dataType: "json",
		type: "POST",
		data: {"symbol": symbol},
	}).done(function (res) {
		for(let i = 0; i<res.timePoints; i++) {
			adjCloseSeries.push({x: i, y: res.data[res.timePoints - (i+1)]["adjclose"]});
			openSeries.push({x: i, y: res.data[res.timePoints - (i+1)]["open"]});
		}
		changeElementsValue(res.usage, "usage");
		renderChart(adjCloseSeries, openSeries);
	})
}

function renderChart(adjCloseList, openSeries) {

var chart = new CanvasJS.Chart("chartContainer", {
	animationEnabled: true,
	title:{
		text: "Price graph",
	},
	axisX: {
		title: "Time",
	},
	axisY: {
		title: "Price",
	},
	legend:{
		cursor: "pointer",
		fontSize: 16,
		itemclick: toggleDataSeries
	},
	toolTip:{
		shared: true
	},
	data: [{
		name: "Adjusted Close",
		type: "spline",
		showInLegend: true,
		dataPoints: adjCloseList,
	},
	{
		name: "Open",
		type: "spline",
		showInLegend: true,
		dataPoints: openSeries,
	}],
});
chart.render();

function toggleDataSeries(e){
	if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
		e.dataSeries.visible = false;
	}
	else{
		e.dataSeries.visible = true;
	}
	chart.render();
}

}

function changeElementsValue(innerValue, elementId)
{
    let element = document.getElementById(elementId)
    element.innerHTML = innerValue
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
                changeElementsValue(res.longName, "longName");
                changeElementsValue(res.grossMargin, "grossMargin");
                changeElementsValue(res.operatingMargin, "operatingMargin");
                changeElementsValue(res.debtToEquity, "debtToEquity");
                changeElementsValue(res.returnOnAssets, "returnOnAssets");
                changeElementsValue(res.freeCashFlow, "freeCashFlow");
            }

            changeElementsValue(res.usage, "usage");
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