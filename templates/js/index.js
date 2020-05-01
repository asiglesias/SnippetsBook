
var hidden = false;
$(document).ready(function(){

    $('#hamburger').click(function(){
        if(hidden)
        {
            showSidebar();
        }
        else{
            hideSidebar();
        }
        hidden = !hidden;
    });
});

function hideSidebar()
{
    $('#content').css("left", '0');
}

function showSidebar()
{
    $('#content').css("left", '350px');
}