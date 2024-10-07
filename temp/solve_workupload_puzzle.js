<input id="captcha_85274" type="hidden"  disabled="disabled" />
<script>
	async function sha256(message, find, i) {
		const msgBuffer = new TextEncoder().encode(message);
		const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
		const hashArray = Array.from(new Uint8Array(hashBuffer));
		const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

		if(find.includes(hashHex)){
			return i;
		}
	}

	$(document).ready(function () {
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
								$('#captcha_85274').val($('#captcha_85274').val() + s + ' ');
								found++;
								if(found == res.data.find.length){
									$.ajax({
										url: "/captcha",
										type: 'POST',
										dataType: "json",
										data: {
											captcha: $('#captcha_85274').val()
										}
									}).always(function(data, textStatus, xhr){
										$('#captcha_85274').val('');
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
	});

</script>
