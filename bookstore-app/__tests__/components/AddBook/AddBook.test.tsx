import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { AddBookProps } from "@/types/props";

import AddBook from "@/components/AddBook/AddBook";

import bookService from "@/services/bookService";

import { mockBook, mockBooks } from "@tests/__mocks__/books.mock";
import { mockGenres } from "@tests/__mocks__/genres.mock";

jest.mock("@/services/bookService");

interface RenderComponent {
  container: HTMLElement;
  props: AddBookProps;
}

const mockSetBooks = jest.fn();
const mockSetGenres = jest.fn();

const renderComponent = (overrides?: Partial<AddBookProps>): RenderComponent => {
  const props: AddBookProps = {
    books: mockBooks,
    genres: mockGenres,
    setBooks: mockSetBooks,
    setGenres: mockSetGenres,
    ...overrides,
  };
  const { container } = render(<AddBook {...props} />);
  return { container, props };
};

describe("AddBook", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it("should render the article element", () => {
    const { container } = renderComponent();
    expect(container.querySelector<HTMLElement>("article.add-book")).toBeInTheDocument();
  });

  it("should render the toggle button with correct aria-label", () => {
    renderComponent();
    expect(screen.getByRole("button", { name: "Open add book form" })).toBeInTheDocument();
  });

  it("should not show the form initially", () => {
    renderComponent();
    expect(screen.queryByRole("form", { name: "Add new book form" })).not.toBeInTheDocument();
  });

  it("should show the form when the toggle button is clicked", async () => {
    const user = userEvent.setup();
    renderComponent();
    await user.click(screen.getByRole("button", { name: "Open add book form" }));
    expect(screen.getByRole("form", { name: "Add new book form" })).toBeInTheDocument();
  });

  it("should hide the form when the toggle button is clicked again", async () => {
    const user = userEvent.setup();
    renderComponent();
    const toggleBtn = screen.getByRole("button", { name: "Open add book form" });
    await user.click(toggleBtn);
    await user.click(toggleBtn);
    expect(screen.queryByRole("form", { name: "Add new book form" })).not.toBeInTheDocument();
  });

  it("should update the input value as the user types", async () => {
    const user = userEvent.setup();
    renderComponent();
    await user.click(screen.getByRole("button", { name: "Open add book form" }));
    const titleInput = screen.getByPlaceholderText("Set title");
    await user.type(titleInput, "New Book");
    expect(titleInput).toHaveValue("New Book");
  });

  it("should call bookService.add and setBooks on form submit", async () => {
    const user = userEvent.setup();
    (bookService.add as jest.Mock).mockResolvedValueOnce({
      message: "created",
      code: "201",
      data: mockBook,
    });
    renderComponent();
    await user.click(screen.getByRole("button", { name: "Open add book form" }));
    await user.click(screen.getByRole("button", { name: "Submit new book" }));
    await waitFor(() => {
      expect(bookService.add).toHaveBeenCalled();
      expect(mockSetBooks).toHaveBeenCalledWith([...mockBooks, { ...mockBook }]);
    });
  });

  it("should add new genre to genres list when it does not exist", async () => {
    const user = userEvent.setup();
    const newBook = { ...mockBook, genre: "Science Fiction" };
    (bookService.add as jest.Mock).mockResolvedValueOnce({
      message: "created",
      code: "201",
      data: newBook,
    });
    renderComponent({ genres: [] });
    await user.click(screen.getByRole("button", { name: "Open add book form" }));
    await user.click(screen.getByRole("button", { name: "Submit new book" }));
    await waitFor(() => {
      expect(mockSetGenres).toHaveBeenCalledWith(["Science Fiction"]);
    });
  });

  it("should not add genre when it already exists", async () => {
    const user = userEvent.setup();
    (bookService.add as jest.Mock).mockResolvedValueOnce({
      message: "created",
      code: "201",
      data: mockBook,
    });
    renderComponent();
    await user.click(screen.getByRole("button", { name: "Open add book form" }));
    await user.click(screen.getByRole("button", { name: "Submit new book" }));
    await waitFor(() => {
      expect(bookService.add).toHaveBeenCalled();
    });
    expect(mockSetGenres).not.toHaveBeenCalled();
  });
});
