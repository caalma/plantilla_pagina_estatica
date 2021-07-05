/* global variable */
var G = {};

/* initialization */
$(window).on({
	load: function(){
		yml_load('cfg/general.yml', function(v){
			G.cfg = v;
			$('title').text(G.cfg['title']);
			$('#title').html(G.cfg['title']);
			$('#content').html(marked.parse(G.cfg['content']));
			
			$('#exit').on({
				click: function(ev){
					server_shutdown();
				}
			});
		});
	},
});

window.addEventListener('beforeunload', on_before_unload);