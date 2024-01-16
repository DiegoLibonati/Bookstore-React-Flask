import { useState } from "react";
import { useGetBooks } from "../hooks/useGetBooks";
import { Book } from "./Book";
import { useHide } from "../hooks/useHide";
import { AddBook } from "./AddBook";
import { useGetGenres } from "../hooks/useGetGenres";
import { Pagination } from "./Pagination";
import { FilterMenu } from "./FilterMenu";
import { Book as BookT } from "../entities/entities";

import "../css/config.css";
import "../css/books_container.css";
import "../css/pagination_container.css";

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
  } else {
    return (
      <main className="main_container">
        <section className="config_container">
          <article className="filter_genero_container">
            <button onClick={() => handleHide()}>Filters</button>

            {hide ? (
              <ul className="filter_genero_container_list">
                <li onClick={() => handleBooks()}>Show All</li>
                <FilterMenu
                  genres={genres}
                  filterName="Genero"
                  setBooks={setBooks}
                ></FilterMenu>
              </ul>
            ) : null}
          </article>
        </section>

        <section className="books_container">
          {currentBooks.map((book) => (
            <Book key={book._id.$oid} {...book}></Book>
          ))}

          <AddBook
            books={books}
            genres={genres}
            setBooks={setBooks}
            setGenres={setGenres}
          ></AddBook>
        </section>

        <section className="pagination_container">
          <Pagination
            booksPerPage={booksPerPage}
            totalBooks={books.length}
            setCurrentPage={setCurrentPage}
          ></Pagination>
        </section>
      </main>
    );
  }
};
