function changePage(page_number){
    let current_url_params = new URLSearchParams(window.location.search)
    current_url_params.set("page", page_number)
    let new_url = window.location.pathname + "?" + current_url_params.toString()
    window.location.href = new_url
}

function formatPriceInToman(element) {
    let rawPrice = parseFloat(element.innerText);

    if (rawPrice > 0) {
        let formatter = new Intl.NumberFormat('fa-IR');
        let formattedPrice = formatter.format(rawPrice);
        element.innerText = `${formattedPrice} تومان`;
    } else {
        element.innerText = `رایگان`; 
    }
}