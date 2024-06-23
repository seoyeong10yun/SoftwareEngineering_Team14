document.addEventListener('DOMContentLoaded', function () {
  // const tokenInput = document.getElementById('token_input');
  const token = localStorage.getItem('token');
  if (!token) {
    alert('로그인되지 않았습니다.');
    return;
  }
  // if (tokenInput) {
  //   tokenInput.value = token;
  // }
  const menuItems = document.querySelectorAll('.menu-bar__menu-box-1 a');
  // const sections = document.querySelectorAll('.content-list');

  menuItems.forEach(item => {
    item.addEventListener('click', function (event) {
      event.preventDefault();
      const category = item.getAttribute('data-category');
      console.log('category: ', category);
      loadContentList(category, token);
    });
  });

  function loadContentList(category, token) {
    let url = '';
    if (category === 'recommend') {
      url = '/api/recommend/';
    } else if (category === 'watch_history') {
      url = '/api/watch_history/';
    } else if (category === 'genre') {
      // 장르를 선택한 경우, 추가 작업이 필요할 수 있습니다.
      return;
    }

    fetch(url, {
      headers: {
        'Authorization': `Token ${token}`,
      }
    })
      .then(response => response.json())
      .then(data => {
        clearContent();
        if (category === 'recommend') {
          updateRecommendationList(data);
        } else if (category === 'watch_history') {
          updateWatchHistoryList(data);
        } // 추가 카테고리 작업은 여기에 추가

        const pagination = document.getElementById('pagination');
        pagination.style.display = 'none';

      })
      .catch(error => {
        console.error('Error loading content:', error);
      });
  }

  function clearContent() {
    const recommendations = document.getElementById('recommendations');
    const watchHistory = document.getElementById('watch-history');
    const genreContent = document.getElementById('genre-content');
    const searchContent = document.getElementById('content-list');

    if (recommendations) {
      recommendations.innerHTML = '';
    }
    if (watchHistory) {
      watchHistory.innerHTML = '';
    }
    if (genreContent) {
      genreContent.innerHTML = '';
    }
    if (searchContent) {
      genreContent.innerHTML = '';      
    }
  }

  function hideAllContent() {
    const recommendations = document.getElementById('recommendations');
    const watchHistory = document.getElementById('watch-history');
    const genreContent = document.getElementById('genre-content');
    const searchContent = document.getElementById('content-list');

    if (recommendations) {
      recommendations.style.display = 'none';
    }
    if (watchHistory) {
      watchHistory.style.display = 'none';
    }
    if (genreContent) {
      genreContent.style.display = 'none';
    }
    if (searchContent) {
      searchContent.style.display = 'none';
    }
  }

  function updateRecommendationList(data) {
    hideAllContent();
    const recommendations = document.getElementById('recommendations');
    if (recommendations) {
      recommendations.style.display = 'block';
      recommendations.innerHTML = `
          <h3>Liked Genre</h3>
          <ul id="liked-genre"></ul>
          <h3>Liked Cast</h3>
          <ul id="liked-cast"></ul>
          <h3>Liked Director</h3>
          <ul id="liked-director"></ul>
          <h3>Watched Genre</h3>
          <ul id="watched-genre"></ul>
          <h3>Watched Cast</h3>
          <ul id="watched-cast"></ul>
          <h3>Watched Director</h3>
          <ul id="watched-director"></ul>
      `;

      const likedGenre = document.getElementById('liked-genre');
      const likedCast = document.getElementById('liked-cast');
      const likedDirector = document.getElementById('liked-director');
      const watchedGenre = document.getElementById('watched-genre');
      const watchedCast = document.getElementById('watched-cast');
      const watchedDirector = document.getElementById('watched-director');

      if (!data.liked_content_exists) {
        likedGenre.innerHTML = '<li>No liked content available</li>';
        likedCast.innerHTML = '<li>No liked content available</li>';
        likedDirector.innerHTML = '<li>No liked content available</li>';
      } else {
        data.liked_genre.forEach(item => {
          const li = document.createElement('li');
          li.className = 'content-item';
          li.textContent = item.title;
          li.onclick = () => window.location.href = `/content/${item.id}/`;
          likedGenre.appendChild(li);
        });

        data.liked_cast.forEach(item => {
          const li = document.createElement('li');
          li.className = 'content-item';
          li.textContent = item.title;
          li.onclick = () => window.location.href = `/content/${item.id}/`;
          likedCast.appendChild(li);
        });

        data.liked_director.forEach(item => {
          const li = document.createElement('li');
          li.className = 'content-item';
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
          li.className = 'content-item';
          li.textContent = item.title;
          li.onclick = () => window.location.href = `/content/${item.id}/`;
          watchedGenre.appendChild(li);
        });
        data.watched_cast.forEach(item => {
          const li = document.createElement('li');
          li.className = 'content-item';
          li.textContent = item.title;
          li.onclick = () => window.location.href = `/content/${item.id}/`;
          watchedCast.appendChild(li);
        });

        data.watched_director.forEach(item => {
          const li = document.createElement('li');
          li.className = 'content-item';
          li.textContent = item.title;
          li.onclick = () => window.location.href = `/content/${item.id}/`;
          watchedDirector.appendChild(li);
        });
      }
    }
  }

  function updateWatchHistoryList(data) {
    hideAllContent();
    const watchHistory = document.getElementById('watch-history');
    if (watchHistory) {
      watchHistory.style.display = 'block';
      watchHistory.innerHTML = '';
      data.forEach(item => {
        const contentItem = document.createElement('div');
        contentItem.className = 'content-item';
        contentItem.innerHTML = `
              <h3>${item.content.title}</h3>
              <p>Watched on: ${new Date(item.watch_date).toLocaleDateString()}</p>
          `;
        contentItem.onclick = () => window.location.href = `/content/${item.content.id}/`;
        watchHistory.appendChild(contentItem);
      });
    }
  }

  const searchButton = document.getElementById('search-button');
  searchButton.addEventListener('click', function () {
      searchContent(token);
  });

  function searchContent(token) {
    console.log("searchContent 함수 호출됨"); // 디버깅을 위해 추가
    const tag = document.getElementById('search-tag').value;
    const query = document.getElementById('search-query').value;

    fetch(`/api/search/?tag=${tag}&query=${query}`, {
        headers: {
            'Authorization': `Token ${token}`,
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("검색 결과:", data); // 디버깅을 위해 추가
        hideAllContent(); // 이전 내용을 숨깁니다
        const contentList = document.getElementById('content-list');
        contentList.style.display = 'block';
        contentList.innerHTML = ''; // 기존 내용을 지웁니다

        if (data.length === 0) {
            contentList.innerHTML = '<p>검색 결과가 없습니다.</p>';
            return;
        }

        paginateResults(data, 1, 12); // 초기 페이지 로드를 위해 호출

        createPagination(data, 12); // 페이징 버튼 생성
    })
    .catch(error => {
        console.error('Error searching content:', error);
    });
}

function paginateResults(results, page, itemsPerPage) {
    const contentList = document.getElementById('content-list');
    contentList.innerHTML = ''; // 기존 내용을 지웁니다

    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedItems = results.slice(start, end);

    paginatedItems.forEach(content => {
        const contentItem = document.createElement('div');
        contentItem.className = 'content-item';
        contentItem.innerHTML = `
            <h3>${content.title}</h3>
            <p>${content.description}</p>
        `;
        contentItem.onclick = () => window.location.href = `/content/${content.id}/`;
        contentList.appendChild(contentItem);
    });
}

function createPagination(results, itemsPerPage) {
    const pagination = document.getElementById('pagination');
    pagination.style.display = 'block';
    pagination.innerHTML = '';

    let currentPage = 1;
    const totalPages = Math.ceil(results.length / itemsPerPage);

    const prevButton = document.createElement('button');
    prevButton.textContent = '이전';
    prevButton.disabled = currentPage === 1;
    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            paginateResults(results, currentPage, itemsPerPage);
            nextButton.disabled = currentPage === totalPages;
            prevButton.disabled = currentPage === 1;
        }
    });

    const nextButton = document.createElement('button');
    nextButton.textContent = '다음';
    nextButton.disabled = currentPage === totalPages;
    nextButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            paginateResults(results, currentPage, itemsPerPage);
            nextButton.disabled = currentPage === totalPages;
            prevButton.disabled = currentPage === 1;
        }
    });

    pagination.appendChild(prevButton);
    pagination.appendChild(nextButton);
}

  document.getElementById("logout").addEventListener("click", function () {
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

  // 초기 로드: 추천 콘텐츠를 로드
  loadContentList('recommend', token);
});