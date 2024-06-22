document.addEventListener('DOMContentLoaded', function () {
  const token = localStorage.getItem('token'); // loadContent 함수 내에서 토큰을 가져옴
  const menuItems = document.querySelectorAll('.menu-bar__menu-box-1 ul li a');
  const sections = document.querySelectorAll('.content-list');

  menuItems.forEach(item => {
    item.addEventListener('click', function (event) {
      event.preventDefault();
      const category = item.getAttribute('data-category');
      // console test
      console.log('Selected category:', category);
      loadContent(category,token);
    });
  });
  // Initial load
});

function loadContent(category,token) {
  if (!token) {
    console.error('토큰이 없습니다. 로그인해주세요.');
    return;
  }

  fetch(`/api/${category}/`, {
    headers: {
      'Authorization': `Token ${token}`,
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    updateContentList(data);
  })
  .catch(error => {
    console.error('Error fetching content:', error);
  });
}

function updateContentList(data) {
  const contentList = document.querySelector('.content-list');
  contentList.innerHTML = '';

  data.results.forEach(item => {
    const contentItem = document.createElement('div');
    contentItem.className = 'content-item';
    contentItem.innerHTML = `
      <img class="poster" src="${item.poster}" alt="포스터">
      <h3>${item.title}</h3>
      <p>${item.description}</p>
    `;
    contentItem.onclick = () => window.location.href = `/content/${item.id}/`;
    contentList.appendChild(contentItem);
  });
}

document.getElementById("logout").addEventListener("click", function() {
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

function searchContent() {
  const tag = document.getElementById('search-tag').value;
  const query = document.getElementById('search-query').value;

  fetch(`/api/search/?tag=${tag}&query=${query}`, {
      headers: {
          'Authorization': `Token ${token}`,
      }
  })
  .then(response => response.json())
  .then(data => {
      const contentList = document.getElementById('content-list');
      contentList.innerHTML = ''; // Clear existing content
      data.forEach(content => {
          const li = document.createElement('li');
          li.textContent = content.title;
          li.onclick = () => window.location.href = `/content/${content.id}/`;
          contentList.appendChild(li);
      });
  })
  .catch(error => {
      console.error('Error searching content:', error);
  });
}