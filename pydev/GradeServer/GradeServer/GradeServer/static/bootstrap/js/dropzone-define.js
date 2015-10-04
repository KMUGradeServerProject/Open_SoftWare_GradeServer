//dropzone

Dropzone.options.myDropzoneC = { // The camelized version of the ID of the form element
	
	// The configuration we've talked about above
	autoProcessQueue: false, // auto false
	uploadMultiple: true,	// 
	parallelUploads: 5,	// 
	maxFiles: 5,			// 
	maxFilesize: 0.1, 
	addRemoveLinks: true,	// Remove 
	acceptedFiles: ".c, .h",		// 

		// The setting up of the dropzone
		// submit-all 
		//	processQueue()
	init: function() {
		var myDropzone = this;
		$("#submit-all").click(function (e) {
			myDropzone.processQueue();
				});
				
		this.on("successmultiple", function(files, response) {
		// Gets triggered when the files have successfully been sent.
		// Redirect user or notify of success
			location.href = parent.document.referrer;
	 	});
	}
}

Dropzone.options.myDropzoneCpp = { // The camelized version of the ID of the form element
	
	// The configuration we've talked about above
		autoProcessQueue: false, // auto false
		uploadMultiple: true,	// 
		parallelUploads: 5,	// 
		maxFiles: 5,			//
		maxFilesize: 0.1, 
		addRemoveLinks: true,	// Remove 
		acceptedFiles: ".cpp, .h",		// 

		// The setting up of the dropzone
		// submit-all 
		//	processQueue()
		init: function() {
		var myDropzone = this;
		$("#submit-all").click(function (e) {
			myDropzone.processQueue();
				});
				
		this.on("successmultiple", function(files, response) {
		// Gets triggered when the files have successfully been sent.
		// Redirect user or notify of success
			address = "http://localhost/problemList/" + response;
			location.href = parent.document.referrer;
	 	});
	}
}

Dropzone.options.myDropzoneJAVA = { // The camelized version of the ID of the form element
	
	// The configuration we've talked about above
		autoProcessQueue: false, // auto false
		uploadMultiple: true,	// 
		parallelUploads: 5,	// 
		maxFiles: 5,			// 
		maxFilesize: 0.1,
		addRemoveLinks: true,	// Remove 
		acceptedFiles: ".java, .class, .jar",		// 

		// The setting up of the dropzone
		// submit-all 
		//	processQueue()
		init: function() {
		var myDropzone = this;
		$("#submit-all").click(function (e) {
			myDropzone.processQueue();
				});
				
		this.on("successmultiple", function(files, response) {
		// Gets triggered when the files have successfully been sent.
		// Redirect user or notify of success
			location.href = parent.document.referrer;
	 	});
	}
}

Dropzone.options.myDropzonePYTHON2 = { // The camelized version of the ID of the form element
	
	// The configuration we've talked about above
		autoProcessQueue: false, // auto false
		uploadMultiple: true,	// 
		parallelUploads: 5,	// 
		maxFiles: 5,			// 
		maxFilesize: 0.1,
		addRemoveLinks: true,	// Remove 
		acceptedFiles: ".py",		// 

		// The setting up of the dropzone
		// submit-all 
		//	processQueue()
		init: function() {
		var myDropzone = this;
		$("#submit-all").click(function (e) {
			myDropzone.processQueue();
				});
				
		this.on("successmultiple", function(files, response) {
		// Gets triggered when the files have successfully been sent.
		// Redirect user or notify of success
			location.href = parent.document.referrer;
	 	});
	}
}

Dropzone.options.myDropzonePYTHON3 = { // The camelized version of the ID of the form element
	
	// The configuration we've talked about above
		autoProcessQueue: false, // auto false
		uploadMultiple: true,	// 
		parallelUploads: 5,	// 
		maxFiles: 5,			// 
		maxFilesize: 0.1,
		addRemoveLinks: true,	// Remove 
		acceptedFiles: ".py",		// 

		// The setting up of the dropzone
		// submit-all 
		//	processQueue()
		init: function() {
		var myDropzone = this;
		$("#submit-all").click(function (e) {
			myDropzone.processQueue();
				});
				
		this.on("successmultiple", function(files, response) {
		// Gets triggered when the files have successfully been sent.
		// Redirect user or notify of success
			location.href = parent.document.referrer;
	 	});
	}
}

Dropzone.options.myDropzoneUser = { // The camelized version of the ID of the form element
	
	// The configuration we've talked about above
	autoProcessQueue: false, // auto false
	uploadMultiple: true,	// 
	maxFiles: 5,			// 
	maxFilesize: 0.1, 
	addRemoveLinks: true,	// Remove 
	acceptedFiles: ".csv",		// 

		// The setting up of the dropzone
		// submit-all 
		//	processQueue()
	init: function() {
		var myDropzone = this;
		$("#submit-all").click(function (e) {
			myDropzone.processQueue();
				});
				
		this.on("successmultiple", function(files, response) {
		// Gets triggered when the files have successfully been sent.
		// Redirect user or notify of success
			location.href = parent.document.referrer;
	 	});
	}
}