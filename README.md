# web_cwk1
Project Name
Book Management API (Book Management Interface Service)
Project Purpose / What It Does
This is a lightweight Web API for managing book data (title, author, year).
It can serve as the backend data interface for any front-end application, management console, or data analysis process, supporting standard CRUD operations and is a typical prototype of a data-driven service.
Core Functions Currently Implemented (Basic Version)
Health Check GET /health
Used for confirming service online
Book CRUD (Database-driven)
POST /books: Create a book
GET /books: Query all books
GET /books/{id}: Query a book by ID
PUT /books/{id}: Update a book
DELETE /books/{id}: Delete a book
Input validation
title and author are required
year must be an integer (if provided)
Standard HTTP status codes and JSON responses
Success: 200/201/204
Error: 400/404
Persistent storage
Use SQLite (app.db)
Data remains after service restart
