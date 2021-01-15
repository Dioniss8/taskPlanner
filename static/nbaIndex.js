

function getAllUsersFromDb()
{
    let name = "get-all-users";
    console.log("SMTh");
    $.ajax({
        url: "/api/" + name
    }).done(function (res) {
        for (let i = 0; i<res.data.length; i++) {
            let text = res.data[i].username + " " + res.data[i].id + "\n";
            console.log(res.data[i]);
            appendChildElementToTarget(text);
        }
        console.log(res.data.length);
    })
}

function appendChildElementToTarget(text)
{
    let base = document.createElement("div");
    base.innerHTML = text;
    let parent = document.getElementById("target");
    parent.appendChild(base);
}