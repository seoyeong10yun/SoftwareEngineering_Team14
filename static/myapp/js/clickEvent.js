document.addEventListener('DOMContentLoaded', function () {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('로그인되지 않았습니다.');
    return;
  }

  const menuItems = document.querySelectorAll('.menu-bar__menu-box-1 a');

  menuItems.forEach(item => {
    item.addEventListener('click', function (event) {
      event.preventDefault();
      const category = item.getAttribute('data-category');
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
      loadGenreContent(token);
      const pagination = document.getElementById('pagination');
      pagination.style.display = 'none';
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
        }

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
      searchContent.innerHTML = '';
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
    const rcmds = {
      'liked-genre': data.liked_genre,
      'liked-cast': data.liked_cast,
      'liked-director': data.liked_director,
      'watched-genre': data.watched_genre,
      'watched-cast': data.watched_cast,
      'watched-director': data.watched_director
    };

    hideAllContent();
    const rcmdContent = document.getElementById('recommendations');
    if (rcmdContent) {
      rcmdContent.style.display = 'block';
      rcmdContent.innerHTML = '';

      console.log('Received data:', data);

      for (const [rcmd, items] of Object.entries(rcmds)) {
        console.log(`Processing ${rcmd} with data:`, items);

        const rcmdSection = document.createElement('div');
        rcmdSection.className = 'rcmd-section';
        rcmdSection.innerHTML = `<h3>${rcmd}</h3>`;
        const rcmdList = document.createElement('ul');
        rcmdList.className = 'rcmd-list';

        items.forEach(item => {
          const li = document.createElement('li');
          li.className = 'content-item';
          li.innerHTML = `
                    <h3>${item.title}</h3>
                    <p>${item.description}</p>
                `;
          li.onclick = () => window.location.href = `/content/${item.id}/`;
          rcmdList.appendChild(li);
        });

        rcmdSection.appendChild(rcmdList);
        rcmdContent.appendChild(rcmdSection);
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

  function loadGenreContent(token) {
    const genres = ['Dramas', 'Comedies', 'Movies', 'Anime Series', 'Kids'];

    Promise.all(
      genres.map(genre =>
        fetch(`/api/genre/${genre}/`, {
          headers: {
            'Authorization': `Token ${token}`,
          }
        }).then(response => response.json())
      )
    ).then(allData => {
      hideAllContent();
      const genreContent = document.getElementById('genre-content');
      if (genreContent) {
        genreContent.style.display = 'block';
        genreContent.innerHTML = '';

        genres.forEach((genre, index) => {
          const data = allData[index];
          const genreSection = document.createElement('div');
          genreSection.className = 'genre-section';
          genreSection.innerHTML = `<h3>${genre}</h3>`;
          const genreList = document.createElement('ul');
          genreList.className = 'genre-list';

          const shuffled = data.results.sort(() => 0.5 - Math.random());
          const selected = shuffled.slice(0, 4);

          selected.forEach(content => {
            const li = document.createElement('li');
            li.className = 'content-item';
            li.textContent = content.title;
            li.onclick = () => window.location.href = `/content/${content.id}/`;
            genreList.appendChild(li);
          });

          genreSection.appendChild(genreList);
          genreContent.appendChild(genreSection);
        });
      }
    }).catch(error => {
      console.error('Error loading genre content:', error);
    });
  }

  const searchButton = document.getElementById('search-button');
  searchButton.addEventListener('click', function () {
    searchContent(token);
  });

  function searchContent(token) {
    console.log("searchContent 함수 호출됨");
    const tag = document.getElementById('search-tag').value;
    const query = document.getElementById('search-query').value;

    fetch(`/api/search/?tag=${tag}&query=${query}`, {
      headers: {
        'Authorization': `Token ${token}`,
      }
    })
      .then(response => response.json())
      .then(data => {
        console.log("검색 결과:", data);
        hideAllContent();
        const contentList = document.getElementById('content-list');
        contentList.style.display = 'block';
        contentList.innerHTML = '';

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