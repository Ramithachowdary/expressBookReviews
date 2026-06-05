const {
  getBooksListAxios,
  getBookDetailsByIsbnAxios,
  getBooksByAuthorAxios,
  getBooksByTitleAxios
} = require('./router/general.js');

async function testAll() {
  console.log("=== Task 10: Get all books (Async/Await) ===");
  const allBooks = await getBooksListAxios();
  console.log(JSON.stringify(allBooks, null, 2));

  console.log("\n=== Task 11: Search by ISBN (Promises) ===");
  const isbnBook = await getBookDetailsByIsbnAxios(1);
  console.log(JSON.stringify(isbnBook, null, 2));

  console.log("\n=== Task 12: Search by Author (Async/Await) ===");
  const booksByAuthor = await getBooksByAuthorAxios("Chinua Achebe");
  console.log(JSON.stringify(booksByAuthor, null, 2));

  console.log("\n=== Task 13: Search by Title (Promises) ===");
  const booksByTitle = await getBooksByTitleAxios("Things Fall Apart");
  console.log(JSON.stringify(booksByTitle, null, 2));
}

testAll();
