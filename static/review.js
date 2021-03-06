function make_editable() {
	update_stars();
	document.getElementById("review_title_textbox").value = rating_title;
	
	document.getElementById("edit_btn").classList.add("hidden");
	document.getElementById("cancel_btn").classList.remove("hidden");
	document.getElementById("submit_btn").classList.remove("hidden");
	document.getElementById("review_title_whole_thing").classList.remove("hidden");
	document.getElementById("star_widget").classList.remove("hidden");
	document.getElementById("ratingtextarea").removeAttribute("readonly");
}

function submit_rating() {
	// we get these from a <script> tag in rating.html
	// they are inserted into variables by the template
	// of course the user_id is checked in views.py before writing to the DB
	document.getElementById("id_username").value = user_id;
	document.getElementById("id_ISBN").value = book_id;
	document.getElementById("id_title").value = document.getElementById("review_title_textbox").value;
	document.getElementById("id_review").value = document.getElementById("ratingtextarea").value;
	document.getElementById("id_stars").value = num_stars;
	
	if (document.getElementById("review_title_textbox").value == "") {
		alert("You need to enter a title for your review first.");
	} else if (document.getElementById("ratingtextarea").value == "") {
		alert("You haven't entered your review.");
	} else {
		document.getElementById("rating_form").submit();
	}
}


var STARS = [
	"☆☆☆☆☆",
	"★☆☆☆☆",
	"★★☆☆☆",
	"★★★☆☆",
	"★★★★☆",
	"★★★★★"
]
function add_star() {
	num_stars = Math.min(num_stars + 1, 5);
	update_stars();
}
function remove_star() {
	num_stars = Math.max(num_stars - 1, 1);
	update_stars();
}
function update_stars() {
	document.getElementById("star_widget_stars").innerText = STARS[num_stars];
	document.getElementById("big_star_span").innerText = STARS[num_stars];
}
function update_title() {
	document.getElementById("big_title").innerText = document.getElementById("review_title_textbox").value;
}