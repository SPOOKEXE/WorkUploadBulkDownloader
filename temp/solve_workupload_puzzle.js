let solvePuzzle = function(){
	$.ajax({
		url: "/puzzle",
		type: 'GET',
		dataType: 'json',
		success: function(res) {
			let found = 0;
			let i = 0;
			while (i < res.data.range) {
				sha256(res.data.puzzle + i, res.data.find, i).then(function(s){
					if(typeof s !== "undefined"){
						$('#captcha_55785').val($('#captcha_55785').val() + s + ' ');
						found++;
						if(found == res.data.find.length){
							$.ajax({
								url: "/captcha",
								type: 'POST',
								dataType: "json",
								data: {
									captcha: $('#captcha_55785').val()
								}
							}).always(function(data, textStatus, xhr){
								$('#captcha_55785').val('');
								if(typeof window.captchaCallback !== "undefined"){
									window.captchaCallback();
								}
							});
						}
					}
				});
				i++;
			}
		}
	});
};
solvePuzzle();
setInterval(solvePuzzle, 20000);
