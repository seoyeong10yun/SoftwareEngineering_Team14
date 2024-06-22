// 버튼 및 콘텐츠 리스트 요소 선택
const menuButtons = document.querySelectorAll('.menu-buttons button');
const contentLists = document.querySelectorAll('.content-list');

// 버튼 클릭 이벤트 핸들러 설정
menuButtons.forEach(button => {
  button.addEventListener('click', () => handleButtonClick(button));
});

// 버튼 클릭 핸들러 함수
function handleButtonClick(button) {
  const targetId = button.getAttribute('data-target');

  // 기존에 활성화된 버튼과 콘텐츠 리스트 비활성화
  deactivateAllButtons();
  hideAllContentLists();

  // 클릭된 버튼과 해당 콘텐츠 리스트 활성화
  activateButton(button);
  showContentList(targetId);

  // 콘텐츠 리스트 로딩
  loadContentList(targetId);
}

// 모든 버튼 비활성화 함수
function deactivateAllButtons() {
  menuButtons.forEach(btn => btn.classList.remove('active'));
}

// 모든 콘텐츠 리스트 숨기기 함수
function hideAllContentLists() {
  contentLists.forEach(list => list.style.display = 'none');
}

// 특정 버튼 활성화 함수
function activateButton(button) {
  button.classList.add('active');
}

// 특정 콘텐츠 리스트 표시 함수
function showContentList(targetId) {
  document.getElementById(targetId).style.display = 'block';
}

// 콘텐츠 리스트 로딩 함수
async function loadContentList(listId) {
  try {
    const response = await fetch(`/api/${listId}/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    renderContentList(listId, data);
  } catch (error) {
    handleError(error);
  }
}

// 콘텐츠 리스트 렌더링 함수
function renderContentList(listId, data) {
  const scrollContainer = document.querySelector(`#${listId} .scroll-container`);
  scrollContainer.innerHTML = '';

  data.forEach(item => {
    const contentItem = document.createElement('div');
    contentItem.classList.add('content-item');
    contentItem.innerHTML = `
      <img src="${item.image}" alt="${item.title}">
      <h3>${item.title}</h3>
      <p>${item.description}</p>
    `;
    contentItem.addEventListener('click', () => {
      window.location.href = `/content/${item.id}/`;
    });
    scrollContainer.appendChild(contentItem);
  });
}

// 에러 처리 함수
function handleError(error) {
  console.error('Error fetching content list:', error);
}
