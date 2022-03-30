function change_transaction_value(){
    let items = document.getElementsByName("item_value")
    let transaction_value = document.getElementsByName("value")
    let sum = 0
    for(var i=0;i < items.length;i++ ){
        sum += parseFloat(items[i].value)
    }
    transaction_value[0].value = sum
}

function add_item(){
    let elem = document.getElementById('item_template');

    clone_div = elem.content.cloneNode(true);
    document.getElementById('items').appendChild(clone_div)
}

function delete_item(element){
    $(element).parent().remove()
    change_transaction_value()
}

function getSubcategories(element){
    var category = $(element).val()
    $.ajax({
        type:'get',
        url:subcategories,
        data:{'category':category},
        success: function(response,status,jqXHR){
            if(jqXHR.status=="200"){
                $(element).nextAll('select').first().empty()                                  
            data = JSON.parse(response['subcategories'])                 
            $.each(data, function(i, item){
                var optionText = item['fields']['name']
                var optionValue = item['pk']
                $(element).nextAll('select').first().append($('<option>').val(optionValue).text(optionText))
                }                                               
            ) 
            }else{
                $(element).nextAll('select').first().empty() 
                $(element).nextAll('select').first().append($('<option>').val(-1).text("brak"))
            }                       
        }
    })
}
