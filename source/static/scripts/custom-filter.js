
var includePage = false;

// Changes page
function changePage(page) {
	if (page > 1) includePage = true;
	$("[name=p]", "#filter").val(page.toString());
	$("#filter").submit();
}

$(function(){
	$("[name]", "#filter").change(function(){ 
		//$("[name]", "#filter").each(function(){ this.disabled = true; })
		$("#filter").submit();
	});
});