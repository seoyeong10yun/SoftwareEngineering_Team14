// Get the URL parameters
const urlParams = new URLSearchParams(window.location.search);
const slug = urlParams.get('slug');

// Add event listeners to the like and dislike buttons
document.getElementById('like-btn').addEventListener('click', () => {
    // Handle the like button click
    console.log('Like button clicked');
});

document.getElementById('dislike-btn').addEventListener('click', () => {
    // Handle the dislike button click
    console.log('Dislike button clicked');
});
