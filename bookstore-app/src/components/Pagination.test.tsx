import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { Pagination } from "./Pagination";

const renderComponent = (): {
  container: HTMLElement;
  props: {
    totalBooks: number;
    booksPerPage: number;
    setCurrentPage: jest.Mock;
  };
} => {
  const totalBooks = 12;
  const booksPerPage = 6;
  const mockSetCurrentPage = jest.fn();

  const { container } = render(
    <Pagination
      totalBooks={totalBooks}
      booksPerPage={booksPerPage}
      setCurrentPage={mockSetCurrentPage}
    />
  );

  return {
    container: container,
    props: {
      totalBooks: totalBooks,
      booksPerPage: booksPerPage,
      setCurrentPage: mockSetCurrentPage,
    },
  };
};

test("The list containing the page buttons must be rendered.", () => {
  renderComponent();

  const listElement = screen.getByRole("list");

  expect(listElement).toBeInTheDocument();
});

test("The number of buttons should be rendered based on the total and the number of books per page.", () => {
  const { props } = renderComponent();

  const totalPaginatorButtons = Math.ceil(
    props.totalBooks / props.booksPerPage
  );

  expect(totalPaginatorButtons).toBeTruthy();

  const itemElements = screen.getAllByRole("listitem");

  expect(itemElements).toHaveLength(totalPaginatorButtons);
});

test("The setCurrentPage function must be executed once with the argument based on the page clicked.", async () => {
  const { props } = renderComponent();

  const totalPaginatorButtons = Math.ceil(
    props.totalBooks / props.booksPerPage
  );

  expect(totalPaginatorButtons).toBeTruthy();

  const itemElement = screen
    .getAllByRole("listitem")
    .find((item) => item.textContent === String(totalPaginatorButtons))!;

  await user.click(itemElement);

  expect(props.setCurrentPage).toHaveBeenCalledTimes(1);
  expect(props.setCurrentPage).toHaveBeenCalledWith(totalPaginatorButtons);
});
