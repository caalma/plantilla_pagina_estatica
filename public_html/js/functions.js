function yml_load(url, fn){
	$.get(url, function(r){
		fn(jsyaml.load(r));
	});
}

function ask_exit(){
	return false;
}

function on_before_unload(e){
    if (ask_exit()){
        e.preventDefault();
        e.returnValue = '';
    	server_shutdown();
        return;
    }
    delete e['returnValue'];
}