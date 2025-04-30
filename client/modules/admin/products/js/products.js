async function get_products() {
    let response = await fetch("http://localhost:8000/api/product/all")

    if (response.ok) {
        let json = await response.json()
        return json
    } else {
        alert("Ошибка HTTP: " + response.status)
    }
}

async function render_products() {
    let template = '<tr>'
        + '<th scope="row">{ИД}</th>'
        + '<td><img src="{КАРТИНКА}" width="50px" class="img-fluid rounded-start" alt="..."></td>'
        + '<td>{НАЗВАНИЕ}</td>'
        + '<td>{ОПИСАНИЕ}</td>'
        + '<td>{ЦЕНА} Р</td>'
        + '<td>'
        + '<button class="btn btn-danger me-2" onclick="delete_product({ИД})">🗑️</button>'
        + '<a class="btn btn-warning" href="form.html?id={ИД}">✏️</a>'
        + '</td>'
        + '</tr>'
    let products = await get_products()
    let container = document.getElementById("products")
    products.forEach(element => {
        product = template
        product = product.replaceAll("{ИД}", element.id)
        product = product.replace("{НАЗВАНИЕ}", element.name)
        product = product.replace("{ОПИСАНИЕ}", element.description)
        product = product.replace("{ЦЕНА}", element.price)
        product = product.replace("{КАРТИНКА}", element.image)
        container.innerHTML += product
    })
}
render_products()

async function delete_product(id) {
    let response = await fetch("http://localhost:8000/api/product/" + id, {"method": "DELETE"})

    if (response.ok) {
        window.location.reload();
    } else {
        alert("Ошибка HTTP: " + response.status)
    }
}