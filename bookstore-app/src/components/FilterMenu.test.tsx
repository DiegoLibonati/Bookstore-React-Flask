import { screen, render, within } from "@testing-library/react";
import user from "@testing-library/user-event";

import { Book } from "../entities/entities";

import { FilterMenu } from "./FilterMenu";

import { createServer } from "../test/server";

const books: Book[] = [
  {
    _id: {
      $oid: "asd123",
    },
    author: "Bram Stoker",
    description:
      "Es una novela de fantasía gótica escrita por Bram Stoker, publicada en 1897.",
    genre: "Novela",
    image:
      "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Dracula-First-Edition-1897.jpg/220px-Dracula-First-Edition-1897.jpg",
    title: "Drácula",
  },
];

createServer([
  {
    path: "/api/v1/bookstore/:genre",
    method: "get",
    res: () => {
      return books;
    },
  },
]);

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
