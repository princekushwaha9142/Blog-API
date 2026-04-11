# Blog API (FastAPI + PostgreSQL)

This is a backend API designed to power modern blogging platforms. Built with FastAPI, it’s high-performance, easy to scale, and comes packed with features like JWT authentication, nested commenting, and even an AI-driven recommendation engine.

---

## Features

### 🔐 Authentication

* User Register & Login (JWT)
* Password hashing (bcrypt)
* Protected routes

### 📝 Blog System

* Create / Read / Update / Delete posts
* User-based authorization

### 💬 Comments

* Add comments on posts
* Nested replies
* Delete own comments

### ❤️ Engagement

* Like / Unlike posts
* Bookmark posts

### 🔎 Search & Filter

* Search posts by title
* Filter by user

### 📊 Analytics

* Total posts count

### 📁 File Upload

* Upload blog images

### 🤖 AI Recommendation

* Recommend similar posts using TF-IDF + cosine similarity

---

## 🛠️ Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT Authentication
* Scikit-learn (AI feature)

---

## ⚙️ Installation

```bash
cd blog-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create `.env` file:

```
DATABASE_URL=postgresql://blog_user:1234@localhost/blog_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## ▶️ Run Server

```bash
uvicorn app.main:app --reload
```

---

## 📌 API Docs

Swagger UI:
http://127.0.0.1:8000/docs

---

## 📂 Project Structure

```
app/
 ├── models/    # Database tables (SQLAlchemy)
 ├── schemas/   # Data validation (Pydantic)
 ├── routes/    # API Endpoints (Auth, Posts, Comments)
 ├── core/      # Security & Config settings
 ├── db/        # Database connection & session
```

---

## 🎯 Future Improvements

* Redis caching
* Docker support
* AWS S3 file upload
* Advanced analytics dashboard