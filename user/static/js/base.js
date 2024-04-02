function toggleText() {
    var content = document.getElementById("postContent");
    var btn = document.getElementById("seeMoreBtn");

    if (content.style.maxHeight === "100px") {
        content.style.maxHeight = "none"; // Show full content
        btn.innerText = "See Less";
    } else {
        content.style.maxHeight = "100px"; // Truncate content
        btn.innerText = "See More";
    }
}

// Show "See More" button if content is truncated
document.addEventListener("DOMContentLoaded", function() {
    let content = document.getElementById("postContent");
    let btn = document.getElementById("seeMoreBtn");

    if (content !== null){
        if (content.scrollHeight > content.clientHeight) {
            btn.style.display = "block";
        }
    }
});

function goBack() {
            window.history.back();
        }

// document.addEventListener('DOMContentLoaded', function() {
//     document.getElementById('like-btn').addEventListener('click', function() {
//         var post_id = this.dataset.postId;
//         console.log(`${post_id}/like/`);
//         fetch(`/post/${post_id}/like/`)
//         .then(response => response.json())
//         .then(data => {
//             document.getElementById('like-count').innerText = data.likes;
//             console.log('So, I know you like this post.');
//             });
//     });
// });
document.addEventListener('DOMContentLoaded', function() {
    // Get all elements with the class 'like-btn'
    var likeButtons = document.querySelectorAll('.like-btn');
    
    // Iterate over each like button
    likeButtons.forEach(function(button) {
        
        // Add click event listener to each like button
        button.addEventListener('click', function() {
            var post_id = this.dataset.postId;
            var likeCountElement = this.querySelector('.like-count');
            
            fetch(`/post/${post_id}/like/`)
            .then(response => response.json())
            .then(data => {
                likeCountElement.innerText = data.likes; // Update like count for this post
            });
        });
    });
});

// comment
$(document).ready(function() {
    $('#comment-content').on('input', function() {
        this.style.height = 'auto'; // Reset textarea height
        this.style.height = (this.scrollHeight) + 'px'; // Set textarea height to its scroll height
    });
});




//##################

// const videoElement = document.getElementById('videoElement');
//     const canvas = document.createElement('canvas');
//     const context = canvas.getContext('2d');

// function updateBackgroundColor() {
//     // Ensure the canvas dimensions match the video
//     canvas.width = videoElement.videoWidth;
//     canvas.height = videoElement.videoHeight;

//     // Draw the current video frame onto the canvas
//     context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

//     // Get the image data from the canvas
//     const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
//     const pixels = imageData.data;

//     // Variables to hold the sum of all colors
//     let r = 0, g = 0, b = 0;

//     for (let i = 0; i < pixels.length; i += 4) {
//         r += pixels[i];     // Red
//         g += pixels[i + 1]; // Green
//         b += pixels[i + 2]; // Blue
//     }

//     // Compute the average color
//     const pixelCount = pixels.length / 4;
//     r = Math.floor(r / pixelCount);
//     g = Math.floor(g / pixelCount);
//     b = Math.floor(b / pixelCount);

//     // Update the background color of the page
//     document.body.style.backgroundColor = `rgb(${r},${g},${b})`;
// }

// // Continuously sample and update the background color
// setInterval(updateBackgroundColor, 1000); // every second
