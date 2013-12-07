$(document).ready(function() {
	var hoverWidth = $(".logo-image-hover").css("width");
	$(".logo-image-hover").css("width",0);

	$("#logo").hover(
	    function() {
	        $(".logo-image-hover").stop();
	        $(".logo-image-hover").clearQueue();
	        $(".logo-image-hover").animate({width: hoverWidth, opacity: 1.0}, 600);

	        $(".logo-image > div").stop();
	        $(".logo-image > div").clearQueue();
	        $(".logo-image .green-logo").animate({opacity: 1.0}, 300, "swing", function() {
	            $(".logo-image .blue-logo").animate({opacity: 0.0}, 120, "linear");
	        });
	    },
	    function() {
	        $(".logo-image-hover").stop();
	        $(".logo-image-hover").clearQueue();
	        $(".logo-image-hover").animate({width: 0, opacity: 0.0}, 600);

	        $(".logo-image > div").stop();
	        $(".logo-image > div").clearQueue();
	        $(".logo-image .blue-logo").css("opacity", "1.0");
	        $(".logo-image .green-logo").animate({opacity: 0.0}, 300, "swing");
	    }
	);

});