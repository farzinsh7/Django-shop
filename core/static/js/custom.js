$(document).ready(function(){
    let current_url_params = new URLSearchParams(window.location.search)
    $("#page-size-filter").val(current_url_params.get("page_size") || "")
    $("#search-query-filter").val(current_url_params.get("q") || "")
    $("#order-by-filter").val(current_url_params.get("order_by") || "")
    $("#category-id-filter").val(current_url_params.get("category_id") || "")
    $("#min-price-filter").val(current_url_params.get("min_price") || "")
    $("#max-price-filter").val(current_url_params.get("max_price") || "")
})
$("#page-size-filter").change(function(){
    let current_url_params = new URLSearchParams(window.location.search)
    var selectedOption = $(this).val();
    current_url_params.set("page_size", selectedOption)
    let new_url = window.location.pathname + "?" + current_url_params.toString()
    window.location.href = new_url
})
$("#order-by-filter").change(function(){
    let current_url_params = new URLSearchParams(window.location.search)
    var selectedOption = $(this).val();
    current_url_params.set("order_by", selectedOption)
    let new_url = window.location.pathname + "?" + current_url_params.toString()
    window.location.href = new_url
})
function changePage(page_number){
    let current_url_params = new URLSearchParams(window.location.search)
    current_url_params.set("page", page_number)
    let new_url = window.location.pathname + "?" + current_url_params.toString()
    window.location.href = new_url
}