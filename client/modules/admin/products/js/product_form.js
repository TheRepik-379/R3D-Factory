async function get_product(id) {
    let response = await fetch("http://localhost:8000/api/product/" + id)
    if (response.ok) {
        let json = await response.json()
        return json
    } else {
        alert("Ошибка HTTP: " + response.status)
    }
}

async function update_form(){
    let params = new URLSearchParams(document.location.search)
    let id = params.get("id")
    if (id == null){
        document.getElementById("_button").innerText = "Добавить"
        document.getElementById("_button").onclick = add_product
        return
    }
    document.getElementById("_button").innerText = "Редактировать"
    document.getElementById("_button").onclick = edit_product
    let product = await get_product(id)
    document.getElementById("name").value = product["name"]
    document.getElementById("description").value = product["description"]
    document.getElementById("image").value = product["image"]
    document.getElementById("price").value = product["price"]
}

async function edit_product() {
    let params = new URLSearchParams(document.location.search)
    let id = params.get("id")
    let response = await fetch("http://localhost:8000/api/product/" + id, {
        method: "PUT",
        body: new FormData(document.getElementById("product_form"))
    })
    if (response.ok) {
        window.location = "./"
    } else {
        alert("Ошибка HTTP: " + response.status)
    }
}

async function add_product() {
    let response = await fetch("http://localhost:8000/api/product", {
        method: "POST",
        body: new FormData(document.getElementById("product_form"))
    })
    if (response.ok) {
        window.location = "./"
    } else {
        alert("Ошибка HTTP: " + response.status)
    }
}

update_form()