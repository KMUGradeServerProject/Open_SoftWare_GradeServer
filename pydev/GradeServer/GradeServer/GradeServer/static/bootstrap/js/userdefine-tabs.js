$(function(){
	var window_width = $(window).width();
	var first_tab_left = getFirstTabLeft();
	var last_tab_left = getLastTabLeft();
	var tab_length = last_tab_left+Number($("#board-tabs").children().last().width());
	var move = window_width*2/3;

	function decideVisibility(tab_length, window_width){
		if(tab_length < $(".tabbable").width()){
			$(".tab-left").css("display", "None");
			$(".tab-right").css("display", "None");
			$("#board-tabs").css("left", 0);
		}
		else{
			$(".tab-left").css("display", "inline-block");
			$(".tab-right").css("display", "inline-block");	
		}
	}

	decideVisibility(tab_length, window_width);

	function getFirstTabLeft(){
		return Number($("#board-tabs").first().position().left);
	}
	function getLastTabLeft(){
		return Number($("#board-tabs").children().last().position().left);
	}

	$(".tab-left").css("left", $(".tabbable").position().left+"px");
	$(".tab-right").css("left", $(".tabbable").width()+"px");
	$(".tab-left").css("opacity", 0.5);
	$(".tab-right").css("opacity", 0.5);

	$(window).resize(function(){
		window_width = $(window).width();
		move = window_width*2/3;
		decideVisibility(tab_length, window_width);
		$(".tab-left").css("left", $(".tabbable").position().left+"px");
		$(".tab-right").css("left", $(".tabbable").width()+"px");
	});

	$(".tab-right").click(function(){
		if(tab_length+first_tab_left+Number($("#board-tabs").children().last().width()) > $(".tab-right").position().left){
			if(getLastTabLeft()+getFirstTabLeft()-move*2 > $(".tab-right").css("left").split("px")[0]){
				$("#board-tabs").animate({"left": $("#board-tabs").css("left").split("px")[0]-move+"px"}, "slow"); 
				//$("#board-tabs").css("left", $("#board-tabs").css("left").split("px")[0]-move+"px");
			}
			else{ 
				$("#board-tabs").animate({"left": -(tab_length-$(".tabbable").width())}, "slow");
				//$("#board-tabs").css("left", -(tab_length-$(".tabbable").width())-$(".tabbable").position().left);
			}
		}
	});

	$(".tab-left").click(function(){
		if(Number($("#board-tabs").css("left").split("px")[0])+Number(move) < 0){
			$("#board-tabs").animate({"left": Number($("#board-tabs").css("left").split("px")[0])+Number(move)+"px"}, "slow"); 
			//$("#board-tabs").css("left", Number($("#board-tabs").css("left").split("px")[0])+Number(move)+"px");
		}
		else{
			$("#board-tabs").animate({"left": "0px"}, "slow");
			//$("#board-tabs").css("left", "0px");
		}
	});

});