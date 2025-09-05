import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { Book } from "../../entities/entities";

import { Main } from "./Main";

import { createServer } from "../../../tests/msw/server";
import { books, genres } from "../../../tests/jest.constants";

import { api_route_books, api_route_genres } from "../../api/route";

const renderComponent = (): {
  container: HTMLElement;
} => {
  const { container } = render(<Main />);

  return {
    container: container,
  };
};

const renderComponentWithBooks = async (): Promise<{
  container: HTMLElement;
  book: Book;
  genre: string;
}> => {
  const book = books[0];
  const genre = genres[0];
  const { container } = render(<Main />);

  await screen.findByAltText(book.title);

  return {
    container: container,
    book: book,
    genre: genre,
  };
};

describe("Main.tsx", () => {
  describe("When making API calls.", () => {
    createServer([
      {
        path: api_route_books,
        method: "get",
        res: () => {
          return {
            message: "...",
            data: books,
          };
        },
      },
      {
        path: api_route_genres,
        method: "get",
        res: () => {
          return {
            message: "...",
            data: genres,
          };
        },
      },
    ]);

    test("A loading must be rendered when the books have not yet been rendered.", () => {
      renderComponent();

      const loadingElement = screen.getByRole("heading", {
        name: /loading/i,
      });

      expect(loadingElement).toBeInTheDocument();
    });
  });

  describe("When all API calls are terminated.", () => {
    createServer([
      {
        path: api_route_books,
        method: "get",
        res: () => {
          return {
            message: "...",
            data: books,
          };
        },
      },
      {
        path: api_route_genres,
        method: "get",
        res: () => {
          return {
            message: "...",
            data: genres,
          };
        },
      },
    ]);

    test("A Filters button must be rendered.", async () => {
      await renderComponentWithBooks();

      const filtersButton = screen.getByRole("button", {
        name: /filters/i,
      });

      expect(filtersButton).toBeInTheDocument();
    });

    test("A Show All button and a Genres button should be rendered as the main category.", async () => {
      await renderComponentWithBooks();

      const filtersButton = screen.getByRole("button", {
        name: /filters/i,
      });

      expect(filtersButton).toBeInTheDocument();

      await user.click(filtersButton);

      const listItemsElements = screen.getAllByRole("listitem");
      const showAllButton = listItemsElements.find(
        (item) => item.textContent === "Show All"
      );
      const genresButton = listItemsElements.find(
        (item) => item.textContent === "Genres"
      );

      expect(showAllButton).toBeInTheDocument();
      expect(genresButton).toBeInTheDocument();
    });

    test("The total number of books plus the add book card must be rendered.", async () => {
      const currentPage = 1;
      const booksPerPage = 7;

      const { container } = await renderComponentWithBooks();

      // eslint-disable-next-line
      const bookElements = container.querySelectorAll(".book");

      const indexOfLastBook: number = currentPage * booksPerPage;
      const indexOfFirstBook: number = indexOfLastBook - booksPerPage;
      const currentBooks: Book[] = books.slice(
        indexOfFirstBook,
        indexOfLastBook
      );

      expect(bookElements).toHaveLength(currentBooks.length);
    });

    test("The paging component must be rendered.", async () => {
      const { container } = await renderComponentWithBooks();

      // eslint-disable-next-line
      const paginationContainer = container.querySelector(".pagination");

      expect(paginationContainer).toBeInTheDocument();
    });
  });
});
