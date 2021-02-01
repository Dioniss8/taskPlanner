function getAdjustedCloseArray(longName) {
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
		renderChart(longName, adjCloseSeries, openSeries);
	})
}

function renderChart(longName, adjCloseList, openSeries) {

var chart = new CanvasJS.Chart("chartContainer", {
	animationEnabled: true,
	title:{
		text: longName,
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

                let financialStats = document.getElementById("financialStatistics");
                financialStats.innerHTML = "";
                const financialStatistics = res.financialStatistics;
				Object.keys(financialStatistics).forEach(function (key) {
					if (financialStatistics[key].fmt) {
						let inputString = "<b>" + key + "</b> " + financialStatistics[key].fmt;
						let element = document.createElement("li");
						element.innerHTML = inputString;
						element.className = "list-group-item";
						financialStats.appendChild(element);
					}
				});

				let defaultKeyStats = document.getElementById("defaultKeyStatistics");
				defaultKeyStats.innerHTML = "";
				const defaultKeyStatistics = res.defaultKeyStatistics;
				Object.keys(defaultKeyStatistics).forEach(function (key) {
					if (defaultKeyStatistics[key] && defaultKeyStatistics[key].fmt !== undefined) {
						let inputString = "<b>" + key + "</b> " + defaultKeyStatistics[key].fmt;
						let element = document.createElement("li");
						element.innerHTML = inputString;
						element.className = "list-group-item";
						defaultKeyStats.appendChild(element);
					}
				});

				let summaryDetailStats = document.getElementById("summaryDetail");
				summaryDetailStats.innerHTML = "";
				const summaryDetail = res.summaryDetail;
				Object.keys(summaryDetail).forEach(function (key) {
					if (summaryDetail[key] && summaryDetail[key].fmt) {
						let inputString =  "<b>" + key + "</b> " + summaryDetail[key].fmt;
						let element = document.createElement("li");
						element.innerHTML = inputString;
						element.className = "list-group-item";
						summaryDetailStats.appendChild(element);
					}
				});
            }

            changeElementsValue(res.usage, "usage");
            checkForErrorMessageBox(res.success, res.reason);

            if (res.success > 0) {
	            getAdjustedCloseArray(res.longName);
			}
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
