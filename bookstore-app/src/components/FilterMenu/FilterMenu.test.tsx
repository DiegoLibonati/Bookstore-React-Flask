import { screen, render, within } from "@testing-library/react";
import user from "@testing-library/user-event";

import { FilterMenu } from "./FilterMenu";

import { createServer } from "../../tests/msw/server";
import { books } from "../../tests/jest.constants";

import { api_route_books } from "../../api/route";

const renderComponent = (): {
  container: HTMLElement;
  props: { genres: string[]; filterName: string; setBooks: jest.Mock };
} => {
  const genres = ["Novela", "Terror"];
  const filterName = "Genres";
  const mockSetBooks = jest.fn();

  const { container } = render(
    <FilterMenu
      genres={genres}
      filterName={filterName}
      setBooks={mockSetBooks}
    />
  );

  return {
    container: container,
    props: {
      genres: genres,
      filterName: filterName,
      setBooks: mockSetBooks,
    },
  };
};

describe("FilterMenu.tsx", () => {
  describe("General Tests.", () => {
    createServer([
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
