
function deleteItem(item_id) {
    fetch(`/delete_item/${item_id}`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const messageElement = document.createElement('div');
        messageElement.className = "alert alert-success shadow";
        messageElement.id = "message";
        document.querySelector('#display-items').prepend(messageElement);
        document.querySelector('#message').innerHTML = data.message;

        setTimeout(() => {
            document.querySelector('#message').innerHTML = "";
            window.location.replace(window.location.href);
        }, 3000)  
    })
    .catch(error => {
        console.log('Error:', error)
    })
}


function displayItem(shop_id) {
    document.querySelector(`#add-item-input-${shop_id}`).classList.remove("d-none");
}


function addItem(shop_id) {

    const item_name = document.querySelector(`#item-name-${shop_id}`).value; 
    const item_note = document.querySelector(`#item-note-${shop_id}`).value;
    
    fetch("/add_item", {
        method: "POST",
        body: JSON.stringify({
            item_name: item_name,
            item_note: item_note,
            shop_id: shop_id
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const messageElement = document.createElement('div');
        messageElement.className = "alert alert-success shadow";
        messageElement.id = "message";
        document.querySelector('#display-items').prepend(messageElement);
        document.querySelector('#message').innerHTML = data.message;

        setTimeout(() => {
            document.querySelector('#message').innerHTML = "";
            window.location.replace(window.location.href);
        }, 3000)
    })
    .catch(error => {
        console.log('Error:', error)
    })
    document.querySelector(`#add-item-input-${shop_id}`).classList.add("d-none");
}