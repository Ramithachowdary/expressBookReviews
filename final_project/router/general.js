const express = require('express');
let books = require("./booksdb.js");
let isValid = require("./auth_users.js").isValid;
let users = require("./auth_users.js").users;
const public_users = express.Router();
const axios = require('axios');

public_users.post("/register", (req,res) => {
  const username = req.body.username;
  const password = req.body.password;

  if (!username || !password) {
    return res.status(400).json({message: "Username and password are required"});
  }

  if (isValid(username)) {
    return res.status(409).json({message: "User already exists!"});
  }

  users.push({username, password});
  return res.status(200).json({message: "User successfully registered. Now you can login"});
});

// Helper functions resolving local database data with Promises (Tasks 10 - 13)
const getBooks = () => {
  return new Promise((resolve, reject) => {
    resolve(books);
  });
};

const getBookByIsbn = (isbn) => {
  return new Promise((resolve, reject) => {
    if (books[isbn]) {
      resolve(books[isbn]);
    } else {
      reject({ status: 404, message: `ISBN ${isbn} not found` });
    }
  });
};

const getBooksByAuthor = (author) => {
  return new Promise((resolve, reject) => {
    const filtered = Object.values(books).filter(b => b.author === author);
    if (filtered.length > 0) {
      resolve(filtered);
    } else {
      reject({ status: 404, message: `No books found for author ${author}` });
    }
  });
};

const getBooksByTitle = (title) => {
  return new Promise((resolve, reject) => {
    const filtered = Object.values(books).filter(b => b.title === title);
    if (filtered.length > 0) {
      resolve(filtered);
    } else {
      reject({ status: 404, message: `No books found with title ${title}` });
    }
  });
};

// Route Handlers (Tasks 10 - 13 implementations inside the router)

// Get the book list available in the shop (Task 10)
public_users.get('/', async function (req, res) {
  try {
    const bookList = await getBooks();
    return res.status(200).send(JSON.stringify(bookList, null, 4));
  } catch (error) {
    return res.status(500).json({message: "Error retrieving book list"});
  }
});

// Get book details based on ISBN (Task 11)
public_users.get('/isbn/:isbn', function (req, res) {
  const isbn = req.params.isbn;
  getBookByIsbn(isbn)
    .then(book => res.status(200).json(book))
    .catch(err => res.status(err.status || 500).json({message: err.message}));
});
  
// Get book details based on author (Task 12)
public_users.get('/author/:author', async function (req, res) {
  const author = req.params.author;
  try {
    const filtered_books = await getBooksByAuthor(author);
    return res.status(200).json(filtered_books);
  } catch (err) {
    return res.status(err.status || 500).json({message: err.message});
  }
});

// Get all books based on title (Task 13)
public_users.get('/title/:title', function (req, res) {
  const title = req.params.title;
  getBooksByTitle(title)
    .then(filtered_books => res.status(200).json(filtered_books))
    .catch(err => res.status(err.status || 500).json({message: err.message}));
});

// Get book review
public_users.get('/review/:isbn', function (req, res) {
  const isbn = req.params.isbn;
  if (books[isbn]) {
    return res.status(200).json(books[isbn].reviews);
  } else {
    return res.status(404).json({message: `ISBN ${isbn} not found`});
  }
});

// Axios asynchronous retrieval helper functions (to fulfill the requirements of Tasks 10-13 using Axios client)

// Task 10: Fetch list of all books using Axios and async/await
async function getBooksListAxios() {
  try {
    const response = await axios.get('http://localhost:5000/');
    return response.data;
  } catch (error) {
    console.error("Error fetching books list:", error.message);
  }
}

// Task 11: Fetch book details by ISBN using Axios and Promise callbacks
function getBookDetailsByIsbnAxios(isbn) {
  return axios.get(`http://localhost:5000/isbn/${isbn}`)
    .then(response => response.data)
    .catch(error => {
      console.error(`Error fetching book with ISBN ${isbn}:`, error.message);
    });
}

// Task 12: Fetch books by author using Axios and async/await
async function getBooksByAuthorAxios(author) {
  try {
    const response = await axios.get(`http://localhost:5000/author/${author}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching books by author ${author}:`, error.message);
  }
}

// Task 13: Fetch books by title using Axios and Promise callbacks
function getBooksByTitleAxios(title) {
  return axios.get(`http://localhost:5000/title/${title}`)
    .then(response => response.data)
    .catch(error => {
      console.error(`Error fetching books with title ${title}:`, error.message);
    });
}

module.exports.general = public_users;
module.exports.getBooksListAxios = getBooksListAxios;
module.exports.getBookDetailsByIsbnAxios = getBookDetailsByIsbnAxios;
module.exports.getBooksByAuthorAxios = getBooksByAuthorAxios;
module.exports.getBooksByTitleAxios = getBooksByTitleAxios;
