import { useEffect, useState } from "react";

import { Book as BookT } from "@src/entities/app";

import { Book } from "@src/components/Book/Book";
import { Pagination } from "@src/components/Pagination/Pagination";
import { FilterMenu } from "@src/components/FilterMenu/FilterMenu";
import { AddBook } from "@src/components/AddBook/AddBook";

import { useHide } from "@src/hooks/useHide";

import { getBooks } from "@src/api/get/getBooks";
import { getGenres } from "@src/api/get/getGenres";

import "@src/assets/css/Filters.css";
import "@src/assets/css/Books.css";
import "@src/assets/css/Pagination.css";

import "@src/pages/BooksPage/BooksPage.css";

export const BooksPage = (): JSX.Element => {
  const [books, setBooks] = useState<BookT[]>([]);
  const [genres, setGenres] = useState<BookT["genre"][]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [booksPerPage] = useState<number>(7);

  const { hide, handleHide } = useHide();

  const indexOfLastBook: number = currentPage * booksPerPage;
  const indexOfFirstBook: number = indexOfLastBook - booksPerPage;
  const currentBooks: BookT[] = books.slice(indexOfFirstBook, indexOfLastBook);

  const handleGetBooks = async () => {
    if (!loading) setLoading(true);

    const responseBooks = await getBooks();

    setBooks(responseBooks);
    setLoading(false);
  };

  const handleGetGenres = async () => {
    if (!loading) setLoading(true);

    const responseGenres = await getGenres();

    setGenres(responseGenres);
    setLoading(false);
  };

  useEffect(() => {
    handleGetBooks();
    handleGetGenres();
  }, []);

  if (loading) {
    return <h2>Loading</h2>;
  }

  return (
    <main className="main-app">
      <section className="filters-wrapper">
        <article className="filters">
          <button
            onClick={() => handleHide()}
            aria-label="filters"
            className="filters__btn"
          >
            Filters
          </button>

          {hide ? (
            <ul className="filters__menus">
              <li onClick={handleGetBooks} className="filters__show-all">
                Show All
              </li>
              {genres?.length > 0 && (
                <FilterMenu
                  genres={genres}
                  filterName="Genres"
                  setBooks={setBooks}
                ></FilterMenu>
              )}
            </ul>
          ) : null}
        </article>
      </section>

      <section className="books">
        {currentBooks.map((book) => (
          <Book key={book._id} {...book}></Book>
        ))}

        <AddBook
          books={books}
          genres={genres}
          setBooks={setBooks}
          setGenres={setGenres}
        ></AddBook>
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
