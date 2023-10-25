/*
 * A script to delete all videos from a Tittok account
 * 
 * Before running:
 *   1. Log into your Tiktok account in a browser (tested with Firefox)
 *   2. Navigate to the View Profile
 *   3. Open the developer tools in the browser to inspect the URLs of the requests (Network tab in Firefox)
 *   4. Click on one of the videos and delete it
 *   5. In the developer tools, find the last POST request with a URL that starts with https://m.tiktok.com/api/aweme/delete
 *   6. Copy the URL into the script below into the line that starts with 'const url'. Replace the value of aweme_id and target with:  " + id + "
 *   7. Navigate back to the VIew Profile page
 *   8. Open developer tools and copy the script below into the Javascript console
 *   9. Run the script several times until all the videos are deleted 
 *      (each time you run it, it will only delete the videos showed on the page and reload the page)
 */

(() => {
    let es =
        document.querySelectorAll(".video-feed-item-wrapper");
    console.log("es length: " + es.length);
    let promises = [];
    es.forEach(
        e => {
            const parts = e.href.split("/");
            const id = parts[parts.length - 1]
            const options = {
                method: 'POST',
                credentials: 'include'
            }
            const url = "begining of the URL" + "6&aweme_id=" + id + "&target=" + id + "end of the URL";
            //     console.log(url);
            promises.push(fetch(url, options));
        }
    );
    Promise.all(promises)
        .then(vs => {
            console.log("All done, reloading the page!");
        });
})()