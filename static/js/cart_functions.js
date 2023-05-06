
const deleteBtns = document.querySelectorAll('.delete-one-btn');
const aumentBtns = document.querySelectorAll('.add-one-btn');
const deleteAllBtns = document.querySelectorAll('.delete-all-btn');
const userInfo = document.getElementById('user-info');
const userId = userInfo.getAttribute('data-user-id');
const precio_total = document.getElementById("carrito-precio-total")
const url = "https://flask-production-c95b.up.railway.app"
console.log(`ID del usuario actual: ${userId}`);

deleteBtns.forEach(deleteBtn => {
    deleteBtn.addEventListener('click', () => {
        const id = deleteBtn.id.split('_')[1]; // Obtenemos el valor de ID del botón
        const url = `${url}/carrito/disminuirproducto?id=${userId}&product_id=${id}`; // URL del elemento a eliminar
        let precio = "$349"
        console.log(id)
        const precioEntero = parseInt(parseFloat(precio.replace(/[^0-9.-]+/g, "")));
        fetch(url, {
            method: 'DELETE',
        })
            .then(response => {
                if (response.ok) {
                    console.log(`Elemento ${id} eliminado`);
                    let cantidadInput = document.getElementById(`cantidad_de_${id}`);
                    cantidadInput.value = `${cantidadInput.value - 1}`
                    const product_counter = document.getElementById(`item_counter_${id}`)
                    product_counter.textContent = `$${parseInt(parseFloat(product_counter.textContent.replace(/[^0-9.-]+/g, ""))) - precioEntero}`
                    precio_total.textContent = `$${parseInt(parseFloat(precio_total.textContent.replace(/[^0-9.-]+/g, ""))) - precioEntero}`
                } else {
                    throw new Error(`Error al eliminar el elemento ${id}`);
                }
            })
            .catch(error => console.error(error));
    });
});

aumentBtns.forEach(aumentBtn => {
    aumentBtn.addEventListener('click', () => {
        const id = aumentBtn.id.split('_')[1]; // Obtenemos el valor de ID del botón
        const url = `${url}/carrito/aumentarproducto?id=${userId}&product_id=${id}`; // URL del elemento a eliminar
        let precio = "$349"
        console.log(id)
        const precioEntero = parseInt(parseFloat(precio.replace(/[^0-9.-]+/g, "")));
        fetch(url, {
            method: 'PUT',
        })
            .then(response => {
                if (response.ok) {
                    console.log(`Elemento ${id} ha sido aumentado en uno`);
                    let cantidadInput = document.getElementById(`cantidad_de_${id}`);
                    const product_counter = document.getElementById(`item_counter_${id}`)
                    cantidadInput.value = `${parseInt(cantidadInput.value) + 1}`
                    product_counter.textContent = `$${parseInt(parseFloat(product_counter.textContent.replace(/[^0-9.-]+/g, ""))) + precioEntero}`
                    precio_total.textContent = `$${parseInt(parseFloat(precio_total.textContent.replace(/[^0-9.-]+/g, ""))) + precioEntero}`

                } else {
                    throw new Error(`Error al agregar el elemento ${id}`);
                }
            })
            .catch(error => console.error(error));
    });
});

deleteAllBtns.forEach(deleteAllBtn => {
    deleteAllBtn.addEventListener('click', () => {
        const id = deleteAllBtn.id.split('_')[1]; // Obtenemos el valor de ID del botón
        console.log(id)
        let url = `${url}/carrito/eliminarproducto?id=${userId}&product_id=${id}`; // URL del elemento a eliminar
        fetch(url, {
            method: 'DELETE',
        })
            .then(response => {
                if (response.ok) {
                    console.log(`Elemento ${id} ha sido borrado`);
                    const item_borrado = document.getElementById(`item_${id}`);
                    const eliminado = document.getElementById(`item_counter_${id}`).textContent
                    const precio_eliminado = parseInt(parseFloat(eliminado.replace(/[^0-9.-]+/g, "")))
                    item_borrado.remove()
                    precio_total.textContent = `$${parseInt(parseFloat(precio_total.textContent.replace(/[^0-9.-]+/g, ""))) - precio_eliminado}`

                } else {
                    throw new Error(`Error al eliminar${id}`);
                }
            })
            .catch(error => console.error(error));
    });
});