/*
	The main BigBlueButton JS file that performs AJAX to:
		* Display (and join) an inprogress meeting
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
	
		// The <select /> change event
		$("#recording-select").change(getRecordingUrl);

		// Get the list of running meetings
		getRunningMeetings();
		
		// Get the list of recordings
		getRecordings();
	};

//********************* Get Running Meetings Section ***********************//
	
		// Gets the list of recordings
	function getRunningMeetings () {
	
		$.ajax({
			"url": BASE_AJAX_URL + "get_meetings",
			"type" : "GET",
			"data": {
				"action": "getRunningMeetings"
			},			
		})
		.done(displayMeetings)
		.fail(getRunningMeetingsAjaxFailure);
	}

	// Populate the control with the list of recordings
	function displayMeetings(xmlDom) {
	
		// the webservice gives us this meetings XML doc 
		//	<meeting>
			// <meetingID></meetingID>
			// <meetingName></meetingName>
			// <createTime></createTime>
			// <attendeePW></attendeePW>
			// <running>true</running>
		// </meeting>

		var meetingInfoTag = $("#meeting-info");
		meetingInfoTag.html("");
		var meetings = $(xmlDom).find("meeting");
		
		// Tracks running meetings (not instanced meeting, but only active)
		var runningMeetingsCounter = 0;

		// Get the meeting information and build the HTML object to prompt 
		// a user to join the meeting
		meetings.each(function(idx, e) {
			// extract data from XML
			var meetingId = $(e).find("meetingID").text();
			var meetingName = $(e).find("meetingName").text();
			var attendeePw = $(e).find("attendeePW").text();
			var running = $(e).find("running").text();
		
			// If meeting is not actively running. Don't show
			if (running == "true") {
			
				runningMeetingsCounter++;
			
				// Build the button so the information can be POSTed
				var button = $("<button>", {
				  "id": meetingId,
				  "value": attendeePw,
				  "text": "Join " + meetingName
				});
			
				meetingInfoTag.append(button);
				
				// Get the click event for the button to join the meetings
				button.click(joinMeeting);
			}
		});
		
		// If no active meetings, display message
		if (runningMeetingsCounter == 0) {
			meetingInfoTag.html("There are no active meetings");
		}
	}
	
	// Makes the calls so the user can join to meeting
	function joinMeeting() {
		
		// start the visible display and kill the button
		displayLoadingImage($("#meeting-info"));
		
		// Make our POST call to join the meeting
		$.ajax({
			type:"POST", 
			url: BASE_AJAX_URL + "join_meeting", 
			async:false, 
			data: {
				meetingId: this.id,
				attendeePw: this.value, 
				csrfmiddlewaretoken: getCsrToken()
			}
		})
		.done(joinMeetingResponse)
		.fail(getRunningMeetingsAjaxFailure);
	}
	
	// Respose to join meeting: Open meeting URL and display URL
	function joinMeetingResponse(ajax) {

		var meetingInfo = $("#meeting-info");
		
		var paraElem = $("<p>", {
		  text: "The webinar will open in a new window.  If not, "
		});
		
		// <a> element to the meeting returned from the POST request
		var anchorElem = $("<a>", {
		  href: ajax,
		  target: "_blank",
		  text: "view the webinar here."
		});
		
		// Display information about meeting if the window will not open
		paraElem.append(anchorElem);
		meetingInfo.html("");
		meetingInfo.append(paraElem);

		window.open(ajax,'BigBlueButton');
	}
		
	// If a failure, display error
	// other args to use:  status, exception
	function getRunningMeetingsAjaxFailure(ajax) {
		$("#meeting-info").html(ajax.responseText);
	}	

	
//********************* Get Recordings Section ***********************//

	// Gets the list of recordings
	function getRecordings () {
	
		$.ajax({
			"url": BASE_AJAX_URL + "get_recordings",
			"type" : "GET",
			"data": {
				"action": "getAll"
			},			
		})
		.done(displayRecordings)
		.fail(getRecordingsAjaxFailure);
}
	
	// Populate the control with the list of recordings
	function displayRecordings(ajax) {
	
		var selectTag = $("#recording-select");
	
		// Clear the list of previous entries
		selectTag.html("");
		
		// Build a new option that is the first element. This makes the
		// change event works when selecting the first meeting in the list
		// Also, it provides instructions to the user
		selectTag.prepend($("<option>", {
		  "text": "Select a Recording"
		}));

		// Insert the informative option, along with the returned list
		selectTag.html(selectTag[0].outerHTML + ajax);
	}
	
	// Gets the recording URL
	function getRecordingUrl () {

		// Show the loading object so the users don't panic
		displayLoadingImage($("#recording-info"));
			
		var recordingList = this.children;
		var selectedRecordId = "";
		
		// Loop through list searching for the selected id
		for (var i = 0; i < recordingList.length; i++) {
			if (recordingList[i].selected) {
				selectedRecordId = recordingList[i].id;
				break;
			}
		}

		// Get the url for this recording
		$.ajax({
			"url": BASE_AJAX_URL + "get_recordings",
			"type" : "GET",
			"data": {
				"action": "getUrl",
				"recordId": selectedRecordId
			},			
		})
		
		.done(displayRecordingUrl)
		.fail(getRecordingsAjaxFailure);
	}
	
	// Display the URL
	function displayRecordingUrl(ajax) {
		
		var recordingInfo = $("#recording-info");
		
		// Clear any previous data
		recordingInfo.html("");
		
		// build the <a /> tag and insert it in the document
		recordingInfo.prepend($("<a>", {
		  "href": ajax,
		  "target": "_blank",
		  "text": "View the recording"
		}));
	}
	
	// If a failure, display error
	// other args to use:  status, exception
	function getRecordingsAjaxFailure(ajax) {
		$("#recording-info").html(ajax.responseText);
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