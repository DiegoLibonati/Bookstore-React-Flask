import { screen, render, within } from "@testing-library/react";
import user from "@testing-library/user-event";

import { FilterMenuProps } from "@src/entities/props";

import { FilterMenu } from "@src/components/FilterMenu/FilterMenu";

import { booksApi } from "@src/api/books";

import { createServer } from "@tests/msw/server";
import { books } from "@tests/jest.constants";

type RenderComponent = {
  container: HTMLElement;
  props: { setBooks: jest.Mock } & FilterMenuProps;
};

const renderComponent = (): RenderComponent => {
  const genres = ["Novela", "Terror"];
  const filterName = "Genres";
  const setBooks = jest.fn();

  const { container } = render(
    <FilterMenu genres={genres} filterName={filterName} setBooks={setBooks} />
  );

  return {
    container: container,
    props: {
      genres: genres,
      filterName: filterName,
      setBooks: setBooks,
    },
  };
};

describe("FilterMenu.tsx", () => {
  describe("General Tests.", () => {
    createServer([
      {
        path: `${booksApi}/:genre`,
        method: "get",
        res: () => {
          return {
            message: "...",
            data: books,
          };
        },
      },
    ]);

    test("The main category must be rendered.", () => {
      const { props } = renderComponent();

      const categoryElement = screen
        .getAllByRole("listitem")
        .find((item) => item.textContent === props.filterName);

      expect(categoryElement).toBeInTheDocument();
    });

    test("The list of genres should be rendered when you click on the category or filter.", async () => {
      const { props } = renderComponent();

      const categoryElement = screen
        .getAllByRole("listitem")
        .find((item) => item.textContent === props.filterName)!;

      await user.click(categoryElement);

      const genreFilterElements = within(screen.getByRole("list")).getAllByRole(
        "listitem"
      );

      expect(genreFilterElements).toHaveLength(props.genres.length);
    });
  });
});
