// server.js
// Главный серверный файл: Fastify + Pug + REST API

const path = require('path');
const fastify = require('fastify')({ logger: true });

// Регистрация шаблонизатора Pug
fastify.register(require('@fastify/view'), {
  engine: { pug: require('pug') },
  root: path.join(__dirname, 'views')
});

// Раздача статики из папки views/
fastify.register(require('@fastify/static'), {
  root: path.join(__dirname, 'views'),
  prefix: '/static/' // ссылки вида /static/index.css
});

// In-memory хранилище задач
let todos = [];
let nextId = 1;

/**
 * GET /
 * Рендеринг главной страницы
 */
fastify.get('/', async (request, reply) => {
  return reply.view('index.pug', { todos });
});

/**
 * POST /todos
 * Создание новой задачи
 */
fastify.post('/todos', async (request, reply) => {
  const { title } = request.body || {};
  if (!title || typeof title !== 'string') {
    return reply.code(400).send({ error: 'Поле "title" обязательно и должно быть строкой' });
  }

  const newTodo = { id: nextId++, title: title.trim(), completed: false };
  todos.push(newTodo);

  return reply.code(201).send(newTodo);
});

/**
 * GET /todos
 * Получение всех задач
 */
fastify.get('/todos', async (request, reply) => {
  return reply.code(200).send(todos);
});

/**
 * PUT /todos/:id
 * Обновление задачи
 */
fastify.put('/todos/:id', async (request, reply) => {
  const id = Number(request.params.id);
  const todo = todos.find(t => t.id === id);

  if (!todo) {
    return reply.code(404).send({ error: 'Задача не найдена' });
  }

  const { title, completed } = request.body || {};

  if (typeof title === 'string') todo.title = title.trim();
  if (typeof completed === 'boolean') todo.completed = completed;

  return reply.code(200).send(todo);
});

/**
 * DELETE /todos/:id
 * Удаление задачи
 */
fastify.delete('/todos/:id', async (request, reply) => {
  const id = Number(request.params.id);
  const index = todos.findIndex(t => t.id === id);

  if (index === -1) {
    return reply.code(404).send({ error: 'Задача не найдена' });
  }

  todos.splice(index, 1);
  return reply.code(200).send({ message: 'Задача удалена' });
});

// Запуск сервера
const PORT = process.env.PORT || 3000;

fastify.listen({ port: PORT, host: '0.0.0.0' }, (err, address) => {
  if (err) {
    fastify.log.error(err);
    process.exit(1);
  }
  fastify.log.info(`Server running at ${address}`);
});