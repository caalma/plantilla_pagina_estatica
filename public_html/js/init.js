/* underscore custom settings */
_.templateSettings = {
  interpolate:/\{\{=([\s\S]+?)\}\}/g,
  evaluate:/\{\{([\s\S]+?)\}\}/g,
  escape:/\{\{--([\s\S]+?)\}--\}/g
};


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

		});
	},
});

window.addEventListener('beforeunload', on_before_unload);