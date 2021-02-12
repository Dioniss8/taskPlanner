function onButtonClicked() {
    let ids = [];
    let element = document.getElementById("groups-chosen");
    for (let option of element.options) {
        if (option.selected) {
            ids.push(option.value);
        }
    }

    $.ajax({
        url: "/api/multiples/get-data/",
        dataType: "json",
        type: "POST",
        data: {"groups-chosen": ids},
    }).done(function (res) {
        if (res.success > 0) {
            Object.keys(res.data).forEach(function (key) {
                console.log(res.data[key]);
                console.log(key);
            })
        }
    })

    console.log(ids);
}