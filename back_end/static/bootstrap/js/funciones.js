/////////////////////////////////////////////////////////////////////////////////////////////////////////
/// UTIL ////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
function ScrollTo(id,ajuste){
	if(!ajuste)
		ajuste = 85;
  $('html, body').animate({
      scrollTop: $(id).offset().top-ajuste
  }, 1000);
}

function incrementers(actual,id){
	actual = $(actual);
	var valorAnterior = $(id).val();
	if(valorAnterior==""){valorAnterior=1;}

	if (actual.val() == "+") {
		var valorActual = parseFloat(valorAnterior) + 1;
	} else {
		if (valorAnterior > 0) {
			var valorActual = parseFloat(valorAnterior) - 1;
		} else {
			valorActual = 0;
		}
	}
	$(id).val(valorActual);
}

$(function(){
    // SCROLL SUAVE
    var platform = window.navigator.platform;
    if ((platform === 'MacIntel' || platform === 'MacPPC')) {
    }else{
        $.srSmoothscroll({step: 150});
    }

    // FIJAR MENU
    $(window).scroll(function () {
    	$('#menu').toggleClass("solid", ($(window).scrollTop() > 100));
    });

    /* SLIDERS */
    $('.slider').slick({
    	slidesToShow: 4,
    	slidesToScroll: 4,
    	autoplay: true,
    	arrows: true,
    	dots: true,
    	responsive: [
    	{
    		breakpoint: 1024,
    		settings: {
    			slidesToShow: 3,
    			slidesToScroll: 3,
    			infinite: true,
    			dots: true
    		}
    	},
    	{
    		breakpoint: 800,
    		settings: {
    			arrows: false,
    			slidesToShow: 3,
    			slidesToScroll: 3,
    			infinite: true,
    			dots: true
    		}
    	},
    	{
    		breakpoint: 600,
    		settings: {
    			arrows: false,
    			slidesToShow: 2,
    			slidesToScroll: 2
    		}
    	},
    	{
    		breakpoint: 480,
    		settings: {
    			arrows: false,
    			slidesToShow: 1,
    			slidesToScroll: 1
    		}
    	}]
    });
});