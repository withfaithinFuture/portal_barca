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

document.addEventListener("DOMContentLoaded", function() {
    // Обработка формы обратной связи
    const feedbackForm = document.getElementById("feedbackForm");
    if (feedbackForm) {
        feedbackForm.addEventListener("submit", function(event) {
            event.preventDefault();

            const name = document.getElementById("name").value.trim();
            const email = document.getElementById("email").value.trim();
            const message = document.getElementById("message").value.trim();

            // Валидация
            if (!name || !email || !message) {
                alert("Пожалуйста, заполните все поля");
                return;
            }

            // Отправка данных через Fetch API
            fetch('/feedback/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    message: message
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Сообщение отправлено!");
                    feedbackForm.reset();
                } else {
                    alert("Ошибка: " + (data.error || "Неизвестная ошибка"));
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Произошла ошибка при отправке");
            });
        });
    }

    // Обработка формы авторизации
    const authForm = document.getElementById("authForm");
    if (authForm) {
        authForm.addEventListener("submit", async function(e) {
            e.preventDefault();

            const formData = new FormData(authForm);
            const errorElement = document.querySelector(".error-message");
            errorElement.style.display = "none";

            try {
                const response = await fetch('/auth/', {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    window.location.href = "/";
                } else {
                    errorElement.textContent = data.error || "Ошибка авторизации";
                    errorElement.style.display = "block";
                }
            } catch (error) {
                console.error("Error:", error);
                errorElement.textContent = "Ошибка соединения с сервером";
                errorElement.style.display = "block";
            }
        });
    }


});

document.querySelectorAll('.like-container').forEach(container => {
    const contentType = container.dataset.contentType;
    const contentId = container.dataset.contentId;

    const wsScheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const wsPath = `${wsScheme}${window.location.host}/ws/likes/${contentType}/${contentId}/`;
    const socket = new WebSocket(wsPath);

    // Обработчики сообщений
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'like_data' || data.type === 'like_update') {
            updateLikeUI(container, data);
        }
    };

    socket.onerror = function(error) {
        console.error('WebSocket Error:', error);
    };

    socket.onclose = function(event) {
        if (event.code === 4001) {
            alert('Для голосования необходимо авторизоваться');
        }
    };

    // Обработчики кликов
    container.querySelectorAll('.like-btn, .dislike-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const vote = this.classList.contains('like-btn') ? 1 : -1;

            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({
                    type: 'like_action',
                    vote: vote
                }));
            }
        });
    });
});

function updateLikeUI(container, data) {
    container.querySelector('.like-count').textContent = data.likes;
    container.querySelector('.dislike-count').textContent = data.dislikes;

    // Обновляем активное состояние кнопок
    container.querySelectorAll('.like-btn, .dislike-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    if (data.user_vote === 1) {
        container.querySelector('.like-btn').classList.add('active');
    } else if (data.user_vote === -1) {
        container.querySelector('.dislike-btn').classList.add('active');
    }
}

const socket = new WebSocket(wsPath);

socket.onopen = function() {
    // CSRF-токен для аутентификации
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    socket.send(JSON.stringify({
        type: 'auth',
        token: csrfToken
    }));
};
