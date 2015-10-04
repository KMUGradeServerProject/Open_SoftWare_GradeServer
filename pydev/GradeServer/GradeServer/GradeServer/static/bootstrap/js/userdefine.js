		/* 
		fill every "here" sign using jinja2 template

		when you click 'Title', link to its information
		*/

// load function after all window's loaded
$(window).load(function(){
	window.onload = function(){
		setLegend();
	}
	function setLegend(){
		// solved, wrong answer, time over, compile error, runtime error
		var colors = new Array("#0c274c", "#18709c", "#19bdc4", "#fff6ee", "#ef4089");
		var errors = new Array("Solved", "Wrong Answer", "Time Over", "Compile Error", "Runtime Error");
		var target = document.getElementById("legend-box");
		for(var i=0;i<colors.length;i++){
			if(i==3) target.innerHTML += "<span class='label' style='color:black;background-color:"+colors[i]+"'>"+errors[i]+"</span>"+"<br>";
			else target.innerHTML += "<span class='label' style='background-color:"+colors[i]+"'>"+errors[i]+"</span>"+"<br>";
		}
	}
});

// re-position function
function placeModalCenter(id){
	$("#"+id).css("left", (window.innerWidth-$("#"+id).width())/2+"px");	
}

var textarea = $('#getCode');

// language change
function selectLanguage(selectObj) {
	var mode;
	var theme;
	if(selectObj.value == "C" || selectObj.value == "C++"){ mode = "c_cpp"; }
	if(selectObj.value == "JAVA"){ mode = "java"; }
	if(selectObj.value == "PYTHON2" || selectObj.value == "PYTHON3"){ mode = "python"; }
	if(selectObj.value == 6){ theme = "chrome"; }
	if(selectObj.value == 7){ theme = "clouds"; }
	if(selectObj.value == 8){ theme = "eclipse"; }
	if(selectObj.value == 9){ theme = "github"; }
	if(selectObj.value == 10){ theme = "monokai"; }
	if(selectObj.value == 11){ theme = "textmate"; }
	if(selectObj.value == 12){ theme = "tomorrow"; }

	editor.session.setMode("ace/mode/" + mode);
	editor.setTheme("ace/theme/" + theme);
}

function selectFiles(selectObj) {
	var tag = "";
	for(var i=20; i<selectObj.value; i++) {
		tag += '<input type="file" name="file[]"><br>';
	}
	document.getElementById("multipleFiles").innerHTML = tag;
}

$("#myCarousel").carousel({
	interval: 5000
});

$('.carousel .item').each(function(){
	var next = $(this).next();
	if (!next.length) {
		next = $(this).siblings(':first');
	}
	next.children(':first-child').clone().appendTo($(this));

	if (next.next().length>0) {
		next.next().children(':first-child').clone().appendTo($(this));
	}
	else {
		$(this).siblings(':first').children(':first-child').clone().appendTo($(this));
	}
});

$('#myTabs a').click(function (e) {
	e.preventDefault()
	$(this).tab('show')
});

jQuery(document).ready(function ($) {
		$('#language').tab();
});

$(document).on('click','.dropdown ul a',function(){
	var className = $(this).attr('class');
	if (!className) {
		var text = $(this).text();
		$(this).closest('.dropdown').children('a.dropdown-toggle').text(text);
		}
	else {
		if (className.substr(className.length-12, 12) != "main-checker") {
			var text = $(this).text();
			$(this).closest('.dropdown').children('a.dropdown-toggle').text(text);
			}
 	}
}); 	

// @@ Show deletion modal
// It shows different contents with modal up to 'target'
function showingDeleteModal(target){
	var items, checkboxes;

	// If target is 'undefined' then, 'toUpperCase' doesn't work.
	// So 'undefinedTab' variable needs.
	var undefinedTab = true; 
	
	if(target == 'college' || target == 'department'){
		items = $('.'+target+'-box-check').length;
		checkboxes = $('.'+target+'-box-check');
		undefinedTab = false;
	}
	else{
		items = $('.box-check').length;
		checkboxes = $('.box-check');
	}

	var cnt = 0;
	for(var i = 0; i < items; i++){
		if(checkboxes[i].checked == true){
			cnt++;
			break;
		}
	}
	
	if(!undefinedTab){
		target = target.charAt(0).toUpperCase()+target.slice(1);
	}

	if(cnt == 0){ 
		if(undefinedTab){
			$('#deleteNoItem').modal();
		}
		else{
			$('#deleteNo'+target+'Item').modal();
		}
	}

	else{ 
		if(undefinedTab){
			$('#deleteModal').modal();
		}
		else{
			$('#delete'+target+'Modal').modal();
		}
	}
}

// showing add user modal
function addUserModal(){
	$('#addUserModal').modal();
}

// showing add gruop modal
function addGroupModal(){
	$('#addGroupModal').modal();
}

// @@ Show summary button
// It shows summary button on 'User submission' menu.
// When course administrator clicks on some course, then it shows the button.
// If course administrator stays 'all' tab, then it doesn't show up.
function visibleButton(parent){ 
	var displayOption;
	if(parent.id == "link-all"){
		displayOption = "none";
	}
	else{
		displayOption = "";
	}
	document.getElementById('summary').style.display = displayOption;
}

// @@ Check All checkbox function
// works up to 'Check All' checkbox's checked option
// 'range' means the position of checkboxes.
// it doesn't search in all page range.
function selectAllCheckboxes(range){
	var checkboxes = document.getElementById(range).getElementsByTagName("input");
	// @@ TODO
	// ID doesn't support !!
	var checkAllBox = document.getElementById(range).getElementsByClassName('checkAll')[0];
	// when 'Check All' is unchecked, other checkboxes are being unchecked
	for(var i=0;i<checkboxes.length;i++){
		if(checkboxes[i].type == "checkbox"){
			checkboxes[i].checked = checkAllBox.checked;
		}
	}
}

$(".shortdate").each(function(){
	for(var i=0;i<2;i++){
		$(this).text($(this)[0].innerHTML.split(' ')[0]);
	}
});

$(".shortdate-time").each(function(){
	$(this).text($(this)[0].innerHTML.trim().substring(2,16));
});


// Date and Time Picker
$(".dateTimePicker").appendDtpicker({
	// AutoDate On : false
	"autodateOnStart" : false,
	
	// Minute Interval
	"minuteInterval" : 15,
	
	// Select on close
	"closeOnSelected" : true,
	
	// Animation False
	"animation" : false
}) ;

// Only Date Picker
$(".datePicker").appendDtpicker({
	// AutoDate On : false
	"autodateOnStart" : false,
	
	// only Date
	"dateOnly": true,
	
	// Select on close
	"closeOnSelected" : true,
	
	// Animation False
	"animation" : false
}) ;
var opts = {
	  lines: 13 // The number of lines to draw
	, length: 28 // The length of each line
	, width: 14 // The line thickness
	, radius: 42 // The radius of the inner circle
	, scale: 1 // Scales overall size of the spinner
	, corners: 1 // Corner roundness (0..1)
	, color: '#000' // #rgb or #rrggbb or array of colors
	, opacity: 0.25 // Opacity of the lines
	, rotate: 0 // The rotation offset
	, direction: 1 // 1: clockwise, -1: counterclockwise
	, speed: 1 // Rounds per second
	, trail: 60 // Afterglow percentage
	, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
	, zIndex: 2e9 // The z-index (defaults to 2000000000)
	, className: 'spinner' // The CSS class to assign to the spinner
	, top: '30%' // Top position relative to parent
	, left: '50%' // Left position relative to parent
	, shadow: false // Whether to render a shadow
	, hwaccel: false // Whether to use hardware acceleration
	, position: 'absolute' // Element positioning
	}
	var target = document.getElementById('spin');
	var spinner = new Spinner(opts)


$('.btn').click(function(){

	if($(this).attr('id') != 'memberInsert' && $(this).attr('id')!='modifyProblem'){
		
		spinner.spin(target);
		$.ajax({

			success: function(res){
				spinner.stop();
			},
			error: function(res){
				spinner.stop();
			}
		});
	}

});

$(".modal-body").css("max-height", $(".fluid-footer").position().top-$(".body").position().top*5);
$(window).resize(function(){
	$(".modal-body").css("max-height", $(".fluid-footer").position().top-$(".body").position().top*5);
});

// Auto Size
function autoSize(obj, basicHeight, maxRow) {
	var height = obj.style.height.split("px")[0];
	if (obj.scrollHeight > 70 && maxRow > height){
		obj.style.height = basicHeight + "px" ;
		obj.style.height = obj.scrollHeight + "px";
	}
	/*
	if ({{ OtherResources().const.MAX_ROW }} > height) {
		obj.style.height = basicHeight + "px" ;
		obj.style.height = (16 + obj.scrollHeight) + "px" ;
	}
	*/
}