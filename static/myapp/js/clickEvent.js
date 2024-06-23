document.addEventListener('DOMContentLoaded', function () {
  let currentPage = 1;
  let currentGenrePage = 1;
  let currentGenre = '';
  const tokenInput = document.getElementById('token_input');
  const token = localStorage.getItem('token');
  if (!token) {
    alert('로그인되지 않았습니다.');
    return;
  }
  if (tokenInput) {
    tokenInput.value = token;
  }
  const menuItems = document.querySelectorAll('.menu-bar__menu-box-1 a');
  const sections = document.querySelectorAll('.content-list');
  console.log('token: ', tokenInput);

  //initialize
  loadContentList(currentPage);
  loadRecommendedContent();

  menuItems.forEach(item => {
    item.addEventListener('click', function (event) {
      event.preventDefault();
      const category = item.getAttribute('data-category');
      console.log('category: ', category);
      if (category === 'recommend') {
        loadRecommendedContent();
      } else if (category === 'watch_history') {
        loadWatchHistory();
      } else if (category === 'genre') {
        loadGenreContent(currentPage);
      }
    });
  });

  function loadRecommendedContent() {
    fetch('/api/recommend/', {
      headers: {
        'Authorization': `Token ${token}`,
      }
    })
      .then(response => response.json())
      .then(data => {
        const likedGenre = document.getElementById('liked-genre');
        const likedCast = document.getElementById('liked-cast');
        const likedDirector = document.getElementById('liked-director');
        const watchedGenre = document.getElementById('watched-genre');
        const watchedCast = document.getElementById('watched-cast');
        const watchedDirector = document.getElementById('watched-director');

        likedGenre.innerHTML = ''; // Clear existing content
        likedCast.innerHTML = ''; // Clear existing content
        likedDirector.innerHTML = ''; // Clear existing content
        watchedGenre.innerHTML = ''; // Clear existing content
        watchedCast.innerHTML = ''; // Clear existing content
        watchedDirector.innerHTML = ''; // Clear existing content

        if (!data.liked_content_exists) {
          likedGenre.innerHTML = '<li>No liked content available</li>';
          likedCast.innerHTML = '<li>No liked content available</li>';
          likedDirector.innerHTML = '<li>No liked content available</li>';
        } else {
          data.liked_genre.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item.title;
            li.onclick = () => window.location.href = `/content/${item.id}/`;
            likedGenre.appendChild(li);
          });

          data.liked_cast.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item.title;
            li.onclick = () => window.location.href = `/content/${item.id}/`;
            likedCast.appendChild(li);
          });

          data.liked_director.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item.title;
            li.onclick = () => window.location.href = `/content/${item.id}/`;
            likedDirector.appendChild(li);
          });
        }

        if (!data.watch_history_exists) {
          watchedGenre.innerHTML = '<li>No watch history available</li>';
          watchedCast.innerHTML = '<li>No watch history available</li>';
          watchedDirector.innerHTML = '<li>No watch history available</li>';
        } else {
          data.watched_genre.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item.title;
            li.onclick = () => window.location.href = `/content/${item.id}/`;
            watchedGenre.appendChild(li);
          });
          data.watched_cast.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item.title;
            li.onclick = () => window.location.href = `/content/${item.id}/`;
            watchedCast.appendChild(li);
          });

          data.watched_director.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item.title;
            li.onclick = () => window.location.href = `/content/${item.id}/`;
            watchedDirector.appendChild(li);
          });
        }
      })
      .catch(error => {
        console.error('Error loading recommended content:', error);
      });
  }

  function loadContentList(page) {
    const contentList = document.querySelector('.content-list');
    contentList.innerHTML = '';

    fetch(`/api/content_list/?page=${page}`, {
      headers: {
        'Authorization': `Token ${token}`,
      }
    })
      .then(response => response.json())
      .then(data => {
        const itemsToDisplay = data.results.slice(0, 9); // 최대 9개의 아이템만 처리
        itemsToDisplay.forEach((item, index) => {
          if (index % 3 === 0) {
            const row = document.createElement('div');
            row.className = 'content-row';
            contentList.appendChild(row);
          }
          const contentItem = document.createElement('div');
          contentItem.className = 'content-item';
          contentItem.innerHTML = `
        <img class="poster" src="${item.poster}" alt="포스터">
        <h3>${item.title}</h3>
        <p>${item.description}</p>
      `;
          contentItem.onclick = () => window.location.href = `/content/${item.id}/`;
          contentList.lastChild.appendChild(contentItem);
        });
      })
      .catch(error => console.error('Error fetching content list:', error));
  }

  document.getElementById("logout").addEventListener("click", function () {
    const token = localStorage.getItem('token');
    if (!token) {
      alert('로그인되지 않았습니다.');
      return;
    }
    fetch('/api/logout/', {
      method: 'POST',
      headers: {
        'Authorization': 'Token ' + token,
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')  // CSRF 토큰 설정
      }
    })
      .then(response => {
        if (response.ok) {
          localStorage.removeItem('token');
          window.location.href = '/login/';
        } else {
          alert('로그아웃에 실패했습니다. 다시 시도해주세요.');
        }
      })
      .catch(error => {
        console.error('로그아웃 요청 중 에러 발생:', error);
        alert('로그아웃에 실패했습니다. 다시 시도해주세요.');
      });
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

});

