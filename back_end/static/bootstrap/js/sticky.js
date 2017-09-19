// fijar(pocicionTopInicial, elemento, clase, ajusteDeAltura);
function fijar(limite,target,clase,ajuste,resp,limiteInf){
	if (typeof(ajuste) === "undefined") {
		ajuste = 0;
	}
	if (typeof(limiteInf) === "undefined") {
		limiteInf = 0;
	}
				alert(limite);
	if (!!$(limite).offset()) {
				alert(limite);
		var stickyTop = $(limite).offset().top+ajuste;
		$(window).scroll(function(){
			if( $(window).width() > resp){
				if (limiteInf == 0) {
					var windowTop = $(window).scrollTop();
					if (stickyTop < windowTop ){
						$(target).addClass(clase);
					}
					else {
						$(target).removeClass(clase);
					}
				}else {
					var windowTop = $(window).scrollTop();
					if (stickyTop < windowTop && limiteInf > windowTop){
						$(target).addClass(clase);
						$(target).css("margin-top",0);
					}
					else {
						$(target).removeClass(clase);
						if (windowTop > stickyTop){
							$(target).css("margin-top",limiteInf);
						}else{
							$(target).removeClass(clase);
							$(target).css("margin-top",0);
						}
					}
				}
			}else{
				$(target).removeClass(clase);
				$(target).css("margin-top",0);
			}
		});
	}
}