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
		text: "Stocks values"
	},
	axisX: {
		valueFormatString: "DD MMM,YY"
	},
	axisY: {
		title: "Temperature (in °C)",
		suffix: " °C"
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
		name: "Myrtle Beach",
		type: "spline",
		showInLegend: true,
		dataPoints: adjCloseList,
	},
	{
		name: "Myrtle Beach",
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