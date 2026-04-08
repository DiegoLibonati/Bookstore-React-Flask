import { useEffect, useState } from "react";

import type { JSX } from "react";
import type { Book as BookT } from "@/types/app";

import Book from "@/components/Book/Book";
import Pagination from "@/components/Pagination/Pagination";
import FilterMenu from "@/components/FilterMenu/FilterMenu";
import AddBook from "@/components/AddBook/AddBook";

import { useHide } from "@/hooks/useHide";

import bookService from "@/services/bookService";
import genreService from "@/services/genreService";

import "@/styles/Filters.css";
import "@/styles/Books.css";
import "@/styles/Pagination.css";

import "@/pages/BooksPage/BooksPage.css";

const BooksPage = (): JSX.Element => {
  const [books, setBooks] = useState<BookT[]>([]);
  const [genres, setGenres] = useState<BookT["genre"][]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [booksPerPage] = useState<number>(7);

  const { hide, handleHide } = useHide();

  const indexOfLastBook: number = currentPage * booksPerPage;
  const indexOfFirstBook: number = indexOfLastBook - booksPerPage;
  const currentBooks: BookT[] = books.slice(indexOfFirstBook, indexOfLastBook);

  const handleGetBooks = async (): Promise<void> => {
    if (!loading) setLoading(true);

    const responseBooks = await bookService.getAll();
    const books = responseBooks.data;

    setBooks(books);
    setLoading(false);
  };

  const handleGetGenres = async (): Promise<void> => {
    if (!loading) setLoading(true);

    const response = await genreService.getAll();
    const genres = response.data;

    setGenres(genres);
    setLoading(false);
  };

  useEffect(() => {
    void handleGetBooks();
    void handleGetGenres();
  }, []);

  if (loading) {
    return <h2>Loading</h2>;
  }

  return (
    <main className="main-app">
      <section className="filters-wrapper">
        <article className="filters">
          <button
            onClick={() => {
              handleHide();
            }}
            aria-label="filters"
            className="filters__btn"
          >
            Filters
          </button>

          {hide ? (
            <ul className="filters__menus">
              <li
                onClick={() => {
                  void handleGetBooks();
                }}
                className="filters__show-all"
              >
                Show All
              </li>
              {genres.length > 0 && (
                <FilterMenu genres={genres} filterName="Genres" setBooks={setBooks}></FilterMenu>
              )}
            </ul>
          ) : null}
        </article>
      </section>

      <section className="books">
        {currentBooks.map((book) => (
          <Book key={book._id} {...book}></Book>
        ))}

        <AddBook books={books} genres={genres} setBooks={setBooks} setGenres={setGenres}></AddBook>
      </section>

      <section className="pagination">
        <Pagination
          booksPerPage={booksPerPage}
          totalBooks={books.length}
          setCurrentPage={setCurrentPage}
        ></Pagination>
      </section>
    </main>
  );
};

export default BooksPage;
