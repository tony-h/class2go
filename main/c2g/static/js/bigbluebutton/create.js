/*
	The main BigBlueButton JS file that performs AJAX to:
		* Create new meetings
		* Join existing meetings
		* Get a list of recordings
		* Get a single recording

	Tony Hetrick - 2012
	Build for jQuery JavaScript Library 1.8.2
*/

// Globals
var MISSING_DATA_CLASS_NAME = "required-field";
var BASE_AJAX_URL = "/courses/webinar/";
var BASE_IMG_URL = "/static/graphics/";

	// Initialize the page and tie into any events necessary.
	window.onload = function(){
	
		$("input[name='meetingName']").keyup(meetingNameInputKeyUp);
		$("#start-meeting-button").click(startMeeting);
	};
	
	// On keyup from input box, adjust the size of the button and dynamically
	// add the name of the meeting
	function meetingNameInputKeyUp() {
		var element = $(this);
		
		element.removeClass(MISSING_DATA_CLASS_NAME);
		var button = $("#start-meeting-button")[0];
		
		// Display the user entered text on the button.
		if (this.value == "") {
			button.setAttribute('value',"Create meeting" );
		} else {

			button.setAttribute('value',"Create meeting: " + this.value);
			
			// Dynamically adjust the size of the button to fit the characters being typed

			// By default, element value is empty.  We just need to set the .width to 
			// something close to what the CSS is (or the width + the increment below)
			if (button.style.width == "") {
				button.style.width = "107pt";
			} else  {
				button.style.width = parseInt(button.value.length * 7) + "pt";
			}
		}
	}
	
//********************* Create Meetings Section ***********************//
	
	// Initiate a meeting and receive the generated web page
	function startMeeting () {
	
		var meetingInput = $("input[name='meetingName']");
		var messageTextArea = $("textarea[name='welcome-message']");
		var meetingInfo = $("#meeting-info");
		
		// If no meeting, prompt user for information
		if (meetingInput.val() == "") {
			meetingInput.addClass(MISSING_DATA_CLASS_NAME);
			meetingInfo.html("Please fill in the required information");
			return;
		}
		
		// Show the loading object so the users don't panic
		// Show the loading object so the users don't panic
		displayLoadingImage(meetingInfo);
		
		// The GET request that we will call to initiate a meeting
		// 	name: The name of the meeting
		$.ajax({
			type: "POST",
			url: BASE_AJAX_URL + "start_meeting",
			async: false, 
			data: {
				meetingName: meetingInput.val(), 
				message: messageTextArea.val(),
				csrfmiddlewaretoken: getCsrToken()
			}
		})
		.done(displayMeetingInfo)
		.fail(startMeetingAjaxFailure);
	}
	
	// Displays the resulting HTML from the web-service to our page
	function displayMeetingInfo(ajax) {
	
		// Display the HTML on the page
		$("#meeting-info").html(ajax);
	}

	// If a failure, display error
	// other args to use:  status, exception
	function startMeetingAjaxFailure(ajax) {
		$("#meeting-info").html(ajax.responseText);
	}	

//********************* Misc Functions, etc Section ***********************//

	// Builds our Ajax loading image
	function displayLoadingImage(element) {
		// clear any other HTML before displaying it
		element.html("");

		element.prepend($("<img>", {
		  "src": BASE_IMG_URL + "bigbluebutton/ajax-loader.gif",
		  "id": "ajax-loader"
		}));
	}

		// Since the {{ csrf_token }} variable is not available here, getting it
	// from an element stored on the page
	function getCsrToken() {
		return $("input[name='csrfmiddlewaretoken']")[0].value;		
	}