document.addEventListener('DOMContentLoaded', function () {
  const menuItems = document.querySelectorAll('.menu-bar__menu-box-1 ul li a');
  const sections = document.querySelectorAll('.content-list');

  menuItems.forEach(item => {
    item.addEventListener('click', function (event) {
      event.preventDefault();
      const category = this.textContent;
      loadContent(category);
    });
  });
});

function loadContent(category) {
  fetch('/api/${category}', {
    headers: {
      'Authorization': `Token ${token}`,
    }
  })
    .then(response => response.json())
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

  data.forEach(item => {
    const contentItem = document.createElement('div');
    contentItem.className = 'content-item';
    contentItem.innerHTML = `
          <img class="poster" src="poster.img" alt="포스터">
          <h3>${item.title}</h3>
          <p>${item.description}</p>
      `;
    content.onclick = () => window.location.href = `/content/${item.id}/`;
    contentList.appendChild(contentItem);
  });
}