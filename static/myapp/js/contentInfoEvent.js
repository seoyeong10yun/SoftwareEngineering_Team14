const token = localStorage.getItem('token');
        const contentId = window.location.pathname.split('/').slice(-2, -1)[0];

        fetch(`/api/content_list/${contentId}/`, {
            headers: {
                'Authorization': `Token ${token}`,
            }
        })
        .then(response => response.json())
        .then(data => {
            const contentInfo = document.getElementById('content-info');
            contentInfo.innerHTML = `
                <h1>${data.title}</h1>
                <p><strong>Genre:</strong> ${data.genre}</p>
                <p><strong>Release Date:</strong> ${data.release_date}</p>
                <p><strong>Rating:</strong> ${data.rating}</p>
                <p><strong>Description:</strong> ${data.description}</p>
                <p><strong>Director:</strong> ${data.director}</p>
                <p><strong>Cast:</strong> ${data.cast}</p>
                <p><strong>Country:</strong> ${data.country}</p>
                <p><strong>Duration:</strong> ${data.duration}</p>
            `;
        });

        document.getElementById('like-button').onclick = () => {
            fetch('/api/like_content/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                },
                body: JSON.stringify({content_id: contentId}),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message || 'Liked!');
            });
        };

        document.getElementById('dislike-button').onclick = () => {
            fetch('/api/dislike_content/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                },
                body: JSON.stringify({content_id: contentId}),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message || 'Disliked!');
            });
        };

        document.getElementById('watch-button').onclick = () => {
            fetch('/api/add_watch_history/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                },
                body: JSON.stringify({content_id: contentId}),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    alert('Watch history added!');
                }
            })
            .catch(error => {
                console.error('Error adding to watch history:', error);
            });
        };