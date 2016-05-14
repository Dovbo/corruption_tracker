//  start of w2ui config
var layout = {
        name: 'layout',
        padding: 0,
        panels: [
            { type: 'main', minSize: 400, resizable: true, }
        ]
    };

var grid = { 
        name: 'grid',
        show: {          
            toolbar : true,
            footer : true,
            lineNumbers : true
        },
        columns: [
            { field: 'complainer', caption: 'complainer', size: '15%', sortable: true, searchable: true },
            { field: 'servant', caption: 'servant', size: '15%', sortable: true, searchable: true },
            { field: 'claim_type', caption: 'claim_type', size: '20%', sortable: true, searchable: true},
            { field: 'text', caption: 'text', size: '35%', searchable: true},
            { field: 'bribe', caption: 'bribe', size: '15%', sortable: true},
            { field: 'created', caption: 'created', size: '15%', sortable: true},
        ],};

$(function () { 
    $().w2layout(layout);
    $().w2grid(grid);
});
// end of w2ui config

function w2ui_popup() {
    w2popup.open({
        title: 'Claims',
        body: '<div id="main_w2ui" style="position: absolute; left: 0px; top: 0px; right: 0px; bottom: 0px; width: 100%;"></div>',
        width : 1000,
        onOpen  : function (event) {
            event.onComplete = function () {
                $('#w2ui-popup #main_w2ui').w2render('layout');
                w2ui.layout.content('main', w2ui.grid);
            }
        },
    });
}


function update_dropdown (org_type_id){
    // console.log(org_type_id)
    var $dropdown = $("#claim_type");
    $dropdown.empty();

    if (claim_types[org_type_id]){
        // console.log(claim_types[org_type_id])
    $.each(claim_types[org_type_id], function(key, value) {
      $dropdown.append($("<option></option>")
         .attr("value", value.id).text(value.value));
    });    
    }
}

function fill_claim_form(org_id){
    $('#organization').val(org_id);
    for (var i = places.length - 1; i >= 0; i--) {
        if (places[i].data === parseInt(org_id)){
            update_dropdown(places[i].org_type_id)
            $('#organization_name').val(places[i].value);
            break
        }
    }  
}    

function clear_claim_form(){
    var $dropdown = $("#claim_type");
    $dropdown.empty();
    $('#organization').val(null);
    $('#organization_name').val(null);    
}


function select_building (org_id, coordinates) {
    fill_claim_form(org_id);
    window.location.hash = "organization=" + org_id + "&zoom_to=" + coordinates; 

        $.ajax({
            type: "GET",
            url: api_url + 'claim/' + org_id + "/",
            success: function(data){
                var messages = "";
                var template, message, template_button;

                template = document.getElementById('claim_template_global').innerHTML;
                template_button = document.getElementById('show_all_button_template').innerHTML;

                var records = [];
                var record;
                var count = 0
                data = data['results']
                for (var i = data.length - 1; i >= 0; i--) {

                    if (count < 3) {
                        if (data[i]['bribe']) { message = template.replace('%bribe%', data[i]['bribe']);}
                        else { message = template.replace('%bribe%', '0');};

                        if (data[i]['complainer']) { message = message.replace('%complainer%', '<a id="%complainer_id%" href="#"" class="claims_of_user">' + data[i]['complainer_name'] + '</a>');}
                        else { message = message.replace('%complainer%', 'Anon');};

                        message = message.replace('%servant%', data[i]['servant']);
                        message = message.replace('%claim_type%', data[i]['claim_type']);
                        message = message.replace('%text%', data[i]['text']);
                        message = message.replace('%created%', data[i]['created']);

                        if (data[i]['claim_icon']) {
                            message = message.replace('<div class="claim_icon"></div>',  
                                '<div class="claim_icon"><img src="' + data[i]['claim_icon'] + '"></div>');
                        }
                        messages += message;
                        count += 1
                    } 
                    record = {recid: i+1, complainer: data[i]['complainer'], servant: data[i]['servant'], claim_type: data[i]['claim_type'],
                                text: data[i]['text'], bribe: data[i]['bribe'], created: data[i]['created']};
                    records.push(record);
                }

                w2ui.grid.records = records;

                // template_button = template_button.replace('%org_id%', org_id);
                if (messages == "") {
                    messages = '<h3>Claims</h3>No claims for this polygon';
                    template_button= '';} else {
                    messages = '<h3>Claims</h3>' + messages
                    };            
                $("#claims_list").html('<div class="claims_list_styles">'+messages + template_button+'</div>');

            },
            error: function(data){
                console.log(data.responseText)
            }                
        });
}


function add_claim(event){
    $('#processing').show();
    event.preventDefault();
    $.ajax({
        type: "POST",
        url: api_url + 'claim/',
        data: $('#claim_form').serialize(),
        statusCode: {
            200: function (response) {
                //
            },
            201: function (response) {
                //
            },
            400: function (response) {
                //
            },
            403: function (response) {
                alert("Too much claims. Please wait an hour and try again.");
            }
        },
        success: function(data){                 
            $('#processing').hide();
            $('#message').html('Thank you for your message');
            window.location.reload();

            // $('#claim_text').val('');
            // $('#servant').val('');
            // if (grecaptcha_reset){
            //     grecaptcha.reset();
            // };
        },
        error: function(data){
            console.log(data.responseText)
        }                
    });
    return false;

}


function add_organization(event){
    $('#processing').show();
    event.preventDefault();
    post_data = $('#org_form').serialize();

    $.ajax({
        type: "POST",
        url: api_url + 'organization/',
        data: post_data,

        success: function(data){                 
            $('#processing').hide();
            var splitted_cntr = $('#centroid').val().split(',')
            window.location.hash = "organization=" + data.id + "&zoom_to=" + splitted_cntr[1]+','+splitted_cntr[0];                        
            window.location.reload();

        },
        error: function(data){
            console.log(data.responseText)
        }                
    });
    return false;

}






