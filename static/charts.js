function getAdjustedCloseArray() {
	let counter = 0;
	let adjCloseSeries = [];
	let symbol = document.getElementById("symbol").value;
	$.ajax({
		url: "/api/get-historical-data/",
		dataType: "json",
		type: "POST",
		data: {"symbol": symbol},
	}).done(function (res) {
		for(let i = 0; i<res.timePoints; i++) {
			adjCloseSeries.push({x: counter, y: res.data[counter]["adjclose"]});
			counter++;
		}
		changeElementsValue(res.usage, "usage");
		renderChart(adjCloseSeries);
	})
}

function renderChart(dataPoints) {

var chart = new CanvasJS.Chart("chartContainer", {
	animationEnabled: true,
	title:{
		text: "Daily High Temperature at Different Beaches"
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
		dataPoints: dataPoints,
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