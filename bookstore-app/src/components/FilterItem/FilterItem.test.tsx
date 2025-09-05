import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { FilterItem } from "./FilterItem";

import { createServer } from "../../../tests/msw/server";
import { books, genres } from "../../../tests/jest.constants";

import { api_route_books, api_route_genres } from "../../api/route";

const renderComponent = async (): Promise<{
  container: HTMLElement;
  genre: string;
  mockSetBooks: jest.Mock;
}> => {
  const genre = "terror";
  const mockSetBooks = jest.fn();

  const { container } = render(
    <FilterItem genre={genre} setBooks={mockSetBooks} />
  );

  await screen.findByRole("listitem");

  return {
    container: container,
    genre: genre,
    mockSetBooks: mockSetBooks,
  };
};

describe("FilterItem.tsx", () => {
  describe("General Tests.", () => {
    createServer([
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
      {
        path: `${api_route_books}/:genre`,
        method: "get",
        res: () => {
          return {
            message: "...",
            data: books,
          };
        },
      },
    ]);

    test("A genre must be rendered.", async () => {
      await renderComponent();

      const genreElement = screen.getByRole("listitem");

      expect(genreElement).toBeInTheDocument();
    });

    test("The setBooks function must be executed only once with the books of the selected filter.", async () => {
      const { mockSetBooks } = await renderComponent();

      const genreElement = screen.getByRole("listitem");

      await user.click(genreElement);

      expect(mockSetBooks).toHaveBeenCalledTimes(1);
      expect(mockSetBooks).toHaveBeenCalledWith(books);
    });
  });
});
