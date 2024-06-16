// static/js/script.js
function setCurrentTime() {
  var now = new Date();
  var year = now.getFullYear();
  var month = ("0" + (now.getMonth() + 1)).slice(-2);
  var day = ("0" + now.getDate()).slice(-2);
  var hours = ("0" + now.getHours()).slice(-2);
  var minutes = ("0" + now.getMinutes()).slice(-2);
  var seconds = ("0" + now.getSeconds()).slice(-2);
  var formattedDateTime = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
  document.querySelector('input[type="datetime-local"]').value =
    formattedDateTime;
}

// script.js (assuming you have WebSocket or AJAX polling implemented for real-time updates)
function trackRide(rideId) {
    setInterval(() => {
        // AJAX request to fetch ride status or location updates
        $.ajax({
            url: `/rides/${rideId}/status`,
            success: function(response) {
                // Update UI with ride status or location information
                console.log(response);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    }, 5000);  // Poll every 5 seconds (adjust as needed)
}

