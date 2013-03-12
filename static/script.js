$(document).ready(function(){
	f1=true;
	f2=true;
	f3=true;
	f4=true;
	$('#div1').click(function(){
		if (f1) {
			$('#div1').animate({height: '+=320'},'slow');
			$('#div1').animate({width: '+=600'},'slow');
			$('#div2').fadeOut('slow');
			$('#div3').fadeOut('slow');
			$('#div4').fadeOut('slow');
			$('.res').fadeOut('slow');
			$('#reset1').animate({top: '+=280'},'fast');
			$('#reset1').animate({left: '+=600'},'fast');
			$('#reset1').fadeTo(1,'slow');
			f1=false;
		}
	});
	$('#div2').click(function(){
		if (f2) {
			$('#div2').animate({height: '+=320'},'slow');
			$('#div2').animate({width: '+=600'},'slow');
			$('#div2').animate({left: '-=160'},'slow');
			$('#div1').fadeOut('slow');
			$('#div3').fadeOut('slow');
			$('#div4').fadeOut('slow');
			$('.res').fadeOut('slow');
			$('#reset2').animate({top: '+=280'},'fast');
			$('#reset2').animate({left: '+=440'},'fast');
			$('#reset2').fadeTo(1,'slow');
			f2=false;
		}
	});
	$('#div3').click(function(){
		if (f3) {
			$('#div3').animate({height: '+=320'},'slow');
			$('#div3').animate({width: '+=600'},'slow');
			$('#div3').animate({left: '-=380'},'slow');
			$('#div1').fadeOut('slow');
			$('#div2').fadeOut('slow');
			$('#div4').fadeOut('slow');
			$('.res').fadeOut('slow');
			$('#reset3').animate({top: '+=280'},'fast');
			$('#reset3').animate({left: '+=220'},'fast');
			$('#reset3').fadeTo(1,'slow');
			f3=false;
		}
	});
	$('#div4').click(function(){
		if (f4) {
			$('#div4').animate({height: '+=320'},'slow');
			$('#div4').animate({width: '+=600'},'slow');
			$('#div4').animate({left: '-=600'},'slow');
			$('#div1').fadeOut('slow');
			$('#div2').fadeOut('slow');
			$('#div3').fadeOut('slow');
			$('.res').fadeOut('slow');
			$('#reset4').animate({top: '+=280'},'fast');
			$('#reset4').animate({left: '+=0'},'fast');
			$('#reset4').fadeTo(1,'slow');
			f4=false;
		}
	});
});