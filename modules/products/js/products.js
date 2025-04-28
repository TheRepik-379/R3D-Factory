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
    let template = '<div class="col-md card m-3" style="max-width: 400px;">'
        + '<div class="row g-0">'
        + '<div class="col-md-4">'
        + '<img src="{КАРТИНКА}" class="img-fluid rounded-start" alt="...">'
        + '</div>'
        + '<div class="col-md-8">'
        + '<div class="card-body d-flex flex-column">'
        + '<h5 class="card-title">{НАЗВАНИЕ}</h5>'
        + '<p class="card-text">{ОПИСАНИЕ}</p>'
        + '<p class="card-text text-end">{ЦЕНА} Р</p>'
        + '<a class="btn btn-warning">Купить</a>'
        + '</div>'
        + '</div>'
        + '</div>'
        + '</div>'
    let products = await get_products()
    let container = document.getElementById("products")
    products.forEach(element => {
        product = template
        product = product.replace("{НАЗВАНИЕ}", element.name)
        product = product.replace("{ОПИСАНИЕ}", element.description)
        product = product.replace("{ЦЕНА}", element.price)
        product = product.replace("{КАРТИНКА}", element.photo)
        container.innerHTML += product
    })
}
render_products()