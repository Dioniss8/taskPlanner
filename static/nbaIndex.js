

function getAllUsersFromDb()
{
    let data = null;
    let name = "get-all-users";
    console.log("SMTh");
    $.ajax({
        url: "/api/" + name
    }).done(function (res) {
        appendToParent(res)
    })
}

function appendToParent(text)
{
    let input = document.createElement("p");
    input.innerHTML = text;
    let parent = document.getElementById("target");
    parent.appendChild(input);
}