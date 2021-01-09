let itemCount = 0;

function addQuestion()
{
    let input = document.createElement("input");
    input.setAttribute('type', 'text');
    input.setAttribute('class', 'form-control mb-8');
    input.setAttribute('placeholder', 'item name');
    input.setAttribute('name', itemCount);

    let parent = document.getElementById("items");
    parent.appendChild(input);

    itemCount = itemCount + 1;
    console.log(itemCount);
}

function sleeper()
{
    console.log("Hello");
    setTimeout(() => {  console.log("World!"); }, 2000);
}