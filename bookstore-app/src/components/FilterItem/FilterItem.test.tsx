import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { Book } from "../../entities/entities";

import { FilterItem } from "./FilterItem";

import { createServer } from "../../test/server";
import { api_route_books, api_route_genres } from "../../api/route";

const genres: string[] = ["Novela"];
const books: Book[] = [
  {
    _id: "asd123",
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
