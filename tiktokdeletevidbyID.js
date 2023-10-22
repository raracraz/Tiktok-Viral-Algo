// A videoId variable is introduced, which should be set to the ID of the video you want to delete.
// The querySelectorAll and forEach loop have been removed, as they are used to iterate through all videos on the page.
// A single fetch call is made to send a POST request to the TikTok API to delete the specified video.

function delbyID(videoId) {
    const options = {
        method: 'POST',
        credentials: 'include'
    };
    const url = "beginning of the URL" + "6&aweme_id=" + videoId + "&target=" + videoId + "end of the URL";
    fetch(url, options)
        .then(response => {
            if (response.ok) {
                console.log('Video deleted successfully');
            } else {
                console.error('Failed to delete video:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
};

module.exports = delbyID;