import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { FilterItemProps } from "@src/entities/props";

import { FilterItem } from "@src/components/FilterItem/FilterItem";

import { createServer } from "@tests/msw/server";
import { books, genres } from "@tests/jest.constants";

import { apiRouteBooks } from "@src/api/route";

type RenderComponent = {
  container: HTMLElement;
  genre: FilterItemProps["genre"];
  setBooks: jest.Mock;
};

const renderComponent = async (): Promise<RenderComponent> => {
  const genre = "terror";
  const setBooks = jest.fn();

  const { container } = render(
    <FilterItem genre={genre} setBooks={setBooks} />
  );

  await screen.findByRole("listitem");

  return {
    container: container,
    genre: genre,
    setBooks: setBooks,
  };
};

describe("FilterItem.tsx", () => {
  describe("General Tests.", () => {
    createServer([
      {
        path: `${apiRouteBooks}/genres`,
        method: "get",
        res: () => {
          return {
            message: "...",
            data: genres,
          };
        },
      },
      {
        path: `${apiRouteBooks}/:genre`,
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
      const { setBooks } = await renderComponent();

      const genreElement = screen.getByRole("listitem");

      await user.click(genreElement);

      expect(setBooks).toHaveBeenCalledTimes(1);
      expect(setBooks).toHaveBeenCalledWith(books);
    });
  });
});
