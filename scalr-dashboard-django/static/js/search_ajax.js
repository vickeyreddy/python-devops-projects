$(document).ready(function() {
	$('#searchSubmit').click(function() {
		q = $('#search').val();
		$('#results').html('&nbsp;').load('{% url demo_user_search %}?search=' + q);
	});
});

$(document).ajaxStart(function() {
	$('#spinner').show();
}).ajaxStop(function() {
	$('#spinner').hide();
});

