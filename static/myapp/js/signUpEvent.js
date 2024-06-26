document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var username = document.getElementById('username').value;
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;

    fetch('/api/signup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({username: username, password1: password1, password2: password2}),
    })
    .then(response => response.json())
    .then(data => {
        if (!data.username) {
            // 서버에서 반환된 오류 메시지를 표시
            let errorMessage = '';
            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                    errorMessage += `${key}: ${data[key].join(' ')}\n`;
                }
            }
            alert('Registration failed: ' + errorMessage);
        } else {
            alert('Registration successful!');
            window.location.href = '/login/';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});