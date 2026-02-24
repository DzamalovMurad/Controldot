// views/index.js
// Клиентский JS: работа с REST API через fetch

const form = document.getElementById('todo-form');
const input = document.getElementById('todo-title');
const list = document.getElementById('todo-list');
const errorMessage = document.getElementById('error-message');

let todos = window.__INITIAL_TODOS__ || [];

// API функции
async function apiGetTodos() {
  const res = await fetch('/todos');
  return res.json();
}

async function apiCreateTodo(title) {
  const res = await fetch('/todos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title })
  });
  return res.json();
}

async function apiUpdateTodo(id, data) {
  const res = await fetch(`/todos/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}

async function apiDeleteTodo(id) {
  const res = await fetch(`/todos/${id}`, { method: 'DELETE' });
  return res.json();
}

// Отрисовка
function renderTodos() {
  list.innerHTML = '';
  todos.forEach(todo => {
    const li = document.createElement('li');
    li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
    li.dataset.id = todo.id;

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = todo.completed;
    checkbox.className = 'todo-checkbox';
    checkbox.addEventListener('change', async () => {
      const updated = await apiUpdateTodo(todo.id, { completed: checkbox.checked });
      todo.completed = updated.completed;
      renderTodos();
    });

    const title = document.createElement('span');
    title.textContent = todo.title;
    title.className = 'todo-title';

    const editBtn = document.createElement('button');
    editBtn.textContent = 'Редактировать';
    editBtn.className = 'todo-edit';
    editBtn.addEventListener('click', async () => {
      const newTitle = prompt('Новое название:', todo.title);
      if (newTitle) {
        const updated = await apiUpdateTodo(todo.id, { title: newTitle });
        todo.title = updated.title;
        renderTodos();
      }
    });

    const delBtn = document.createElement('button');
    delBtn.textContent = 'Удалить';
    delBtn.className = 'todo-delete';
    delBtn.addEventListener('click', async () => {
      await apiDeleteTodo(todo.id);
      todos = todos.filter(t => t.id !== todo.id);
      renderTodos();
    });

    li.appendChild(checkbox);
    li.appendChild(title);
    li.appendChild(editBtn);
    li.appendChild(delBtn);

    list.appendChild(li);
  });
}

// Добавление
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const title = input.value.trim();
  if (!title) return;

  const newTodo = await apiCreateTodo(title);
  if (newTodo.error) {
    errorMessage.textContent = newTodo.error;
    return;
  }

  errorMessage.textContent = '';
  todos.push(newTodo);
  input.value = '';
  renderTodos();
});

// Инициализация
renderTodos();