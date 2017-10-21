base = '''
<!doctype html>
<html lang=en>
<head>
<meta charset=utf-8>
<title>blah</title>
</head>
<body>
{}
'''

landing_view = base.format('''
<p>Crewdolfos</p>
<p id="quote"></p>
<button id="getq">New quote?</button>
<script src="/static/jquery.js"></script>
<script>
function rq() {
	$.get( "/quote?file=quote" + Math.floor((Math.random() * 3) + 1) + ".txt", function( data ) {
  		$( "#quote" ).html( data.result );
	});
};
$( document ).ready(function() {
	$( "#getq" ).click(function( event ) {
		rq();
	});
	rq();
});
</script>
''')

index_view = base.format('''
<p>index</p>
<form action="/login" method="post">
  <label for="login">User:</label>
  <input id="login" type="text" name="login">
  <label for="password">Password:</label>
  <input id="password" type="text" name="password">
  <input type="submit" value="Login">
</form>
<p>{}</p>
''')

board_view = base.format('''
<p>board</p>
<a href='/logout'>Logout</a>
{}
<form action="/send" method="post">
  <label for="user">User:</label>
  <input id="user" type="text" name="user">
  <label for="message">MSG:</label>
  <input id="message" type="text" name="message">
  <input type="submit" value="Sned!">
</form>
<p>{}</p>
''')
