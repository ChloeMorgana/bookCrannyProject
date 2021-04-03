function make_editable() {
	document.getElementById("edit_btn").classList.add("hidden");
	document.getElementById("cancel_btn").classList.remove("hidden");
	document.getElementById("submit_btn").classList.remove("hidden");
	document.getElementById("ratingtextarea").removeAttribute("readonly");
}