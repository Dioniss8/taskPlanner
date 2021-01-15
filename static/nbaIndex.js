

function getAllUsersFromDb()
{
    let data = null;
    let name = "get-all-users";
    console.log("SMTh");
    $.ajax({
        url: "/api/" + name
    }).done(function (res) {
        data = res.name
        console.log("Also");
    })

    Object.keys(data).forEach(function(key){
        console.log("key" + key);
        console.log("\n" + data[key]);
    });
    let input = document.createElement("div");
    input.innerHTML = "Yeesh";
    let parent = document.getElementById("target");
    parent.appendChild(input);
}