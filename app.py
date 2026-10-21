
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

todos = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Todo App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            padding: 40px 15px;
        }
        .container {
            max-width: 500px;
            margin: auto;
            padding: 25px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 5px 20px #0001;
        }
        h1 { text-align: center; color: #2563eb; }
        form {
            display: flex;
            gap: 8px;
        }
        input {
            flex: 1;
            min-width: 0;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
        }
        button, .btn {
            padding: 10px 12px;
            border: none;
            border-radius: 6px;
            color: white;
            cursor: pointer;
            text-decoration: none;
            font-size: 14px;
        }
        .add { background: #2563eb; }
        .done { background: #16a34a; }
        .delete { background: #dc2626; }
        .todo {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            padding: 14px 0;
            border-bottom: 1px solid #e2e8f0;
        }
        .task { overflow-wrap: anywhere; }
        .completed {
            text-decoration: line-through;
            color: #94a3b8;
        }
        .actions { display: flex; gap: 5px; }
        .empty { text-align: center; color: #64748b; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 My Todo List</h1>

        <form action="/add" method="POST">
            <input name="task" placeholder="Enter a task..."
                   maxlength="200" required>
            <button class="add">Add</button>
        </form>

        <br>

        {% for todo in todos %}
        <div class="todo">
            <span class="task {% if todo.done %}completed{% endif %}">
                {{ todo.task }}
            </span>
            <div class="actions">
                <a class="btn done"
                   href="/toggle/{{ todo.id }}">
                   {{ "Undo" if todo.done else "Done" }}
                </a>
                <a class="btn delete" href="/delete/{{ todo.id }}">
                    Delete
                </a>
            </div>
        </div>
        {% else %}
        <p class="empty">No tasks yet. Add your first task!</p>
        {% endfor %}
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML, todos=todos)


@app.route("/add", methods=["POST"])
def add():
    global next_id

    task = request.form.get("task", "").strip()

    if task:
        todos.append({
            "id": next_id,
            "task": task,
            "done": False
        })
        next_id += 1

    return redirect("/")


@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    for todo in todos:
        if todo["id"] == task_id:
            todo["done"] = not todo["done"]
            break

    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete(task_id):
    global todos
    todos = [todo for todo in todos if todo["id"] != task_id]
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
