import { useState } from "react";

import { Book as BookT } from "@src/entities/entities";

import { Book } from "@src/components/Book/Book";
import { Pagination } from "@src/components/Pagination/Pagination";
import { FilterMenu } from "@src/components/FilterMenu/FilterMenu";
import { AddBook } from "@src/components/AddBook/AddBook";

import { useGetBooks } from "@src/hooks/useGetBooks";
import { useHide } from "@src/hooks/useHide";
import { useGetGenres } from "@src/hooks/useGetGenres";

import "@src/components/Main/Main.css";
import "@src/components/Main/Filters.css";
import "@src/components/Main/Books.css";
import "@src/components/Main/Pagination.css";

export const Main = (): JSX.Element => {
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [booksPerPage] = useState<number>(7);

  const { loading, books, handleBooks, setBooks } = useGetBooks();
  const { hide, handleHide } = useHide();
  const { genres, setGenres } = useGetGenres();

  const indexOfLastBook: number = currentPage * booksPerPage;
  const indexOfFirstBook: number = indexOfLastBook - booksPerPage;
  const currentBooks: BookT[] = books.slice(indexOfFirstBook, indexOfLastBook);

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
              <li onClick={() => handleBooks()} className="filters__show-all">
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
