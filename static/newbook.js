function submit_form() {
	document.getElementById("invisible_submit_button").click();
}
function load_from_google_books() {
	var isbn_field = document.getElementById("id_ISBN");
	if (!isbn_field.checkValidity()) {
		// if the isbn is blank we show one of those 'please fill in this field' popups
		isbn_field.reportValidity();
	} else {
		// generate the url to get from google books
		var url = "https://www.googleapis.com/books/v1/volumes/?q=" + isbn_field.value + "&callback=receive_from_google_books";
		// we're using JSON-P here because it's a bit simpler
		// in general JSON-P is less secure than other methods but we can reasonably trust google not to XSS us
		var scr = document.createElement("script");
		scr.src = url;
		document.body.appendChild(scr);
	}
}
function receive_from_google_books(response) {
	var details = get_details(response);
	document.getElementById("id_title").value = details.title;
	document.getElementById("id_author").value = details.author;
	document.getElementById("id_description").value = details.description;
	
	
}
function get_details(response) {
	// google books doesn't fully index by ISBN the way we'd like them to
	// so when we search by ISBN, we might get more than one response
	// so we have to just pick the first one that has the ISBN we want.
	
	var correct_isbn = document.getElementById("id_ISBN").value;
	
	var books = response["items"];
	for (var i = 0; i < books.length; i++) {
		var book = books[i];
		var volumeInfo = book["volumeInfo"];
		
		// it's also possible for a book to have two ISBNs in here, so
		// we have to iterate through them.
		var isbns = volumeInfo["industryIdentifiers"];
		for (var j = 0; j < isbns.length; j++) {
			var isbn = isbns[j];
			if (isbn["identifier"] == correct_isbn) {
				// we've got the right book here, so return it's information
				// we can only get title, author and description, not genre (since we've made up a set list of valid genres)
				
				// here we use this || "" thing to eliminate 'undefined' values
				// if a field is missing, we want to leave it blank on the form, not fill it in with the word 'undefined'.
				var title = volumeInfo["title"] || "";
				var author = volumeInfo["authors"] || "";
				var description = volumeInfo["description"] || "";
				
				return {"title"      : title,
				        "author"     : author,
				        "description": description };
			}
		}
	}
}