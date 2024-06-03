// Check if MediaRecorder is available in the user's browser
if (!window.MediaRecorder) {

    // If not available, alert the user
    alert('MediaRecorder is not supported by this browser.');

} else {

    // Initialize an array to store audio data chunks
    let chunks = [];

    // Declare a variable to reference the MediaRecorder instance
    let mediaRecorder;

    // Request access to user's media devices for audio only
    navigator.mediaDevices.getUserMedia({audio: true})
        .then(stream => {

            // If access granted, initialize the mediaRecorder with the received audio stream
            mediaRecorder = new MediaRecorder(stream);

            // Set an event handler for when audio data becomes available
            mediaRecorder.ondataavailable = (event) => {
                // Add the data to the chunks array
                chunks.push(event.data);
            };

            // Set an event handler for when recording stops
            mediaRecorder.onstop = () => {
                // Create a new Blob object from the data chunks
                let blob = new Blob(chunks, {'type': 'audio/wav'});
                // Reset the chunks array
                chunks = [];
                // Call the uploadAudio function to send the audio data to server
                uploadAudio(blob);
            };
        });

    // Define function to start recording
    function startRecording() {
        // Start the mediaRecorder instance, if it exists
        if (mediaRecorder) {
            mediaRecorder.start();
            // Show the "recording" text
            document.getElementById('recording-indicator').style.display = 'block';
        }
    }

    // Define function to stop recording
    function stopRecording() {
        // Stop the mediaRecorder instance, if it exists
        if (mediaRecorder) {
            mediaRecorder.stop();
            // Hide the "recording" text
            document.getElementById('recording-indicator').style.display = 'none';
        }
    }

    // Define function to send the audio data to server
    function uploadAudio(audioBlob) {
        // Create a new FormData object
        let formData = new FormData();
        // Append the audio data to formData
        formData.append("audio", audioBlob, "sample.wav");
        // Send the formData to the server using fetch
        fetch('/talk', {
            method: 'POST',
            body: formData
        })
            // Handle the promise returned by fetch
            .then(
                response => {
                    response.blob().then((audioBlob) => {
                        // now checkout the Blob we received:
                        console.log(audioBlob);

                        // create ObjectURL from Blob
                        let url = URL.createObjectURL(audioBlob);

                        // create an HTMLAudioElement, set its source to the ObjectURL, and play it
                        let audio = new Audio();
                        audio.src = url;
                        audio.play();
                    });
                }
            ).catch(
            error => console.error('Error:', error)
        );
    }
}