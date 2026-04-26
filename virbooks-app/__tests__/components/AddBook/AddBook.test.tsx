import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { RenderResult } from "@testing-library/react";
import type { AddBookProps } from "@/types/props";

import AddBook from "@/components/AddBook/AddBook";

import bookService from "@/services/bookService";

import { mockBook, mockBooks } from "@tests/__mocks__/books.mock";
import { mockGenres } from "@tests/__mocks__/genres.mock";

const mockSetBooks = jest.fn();
const mockSetGenres = jest.fn();

jest.mock("@/services/bookService", () => ({
  __esModule: true,
  default: {
    add: jest.fn(),
    getAll: jest.fn(),
    getAllByGenre: jest.fn(),
  },
}));

const renderComponent = (props: Partial<AddBookProps> = {}): RenderResult => {
  const defaultProps: AddBookProps = {
    books: mockBooks,
    genres: mockGenres,
    setBooks: mockSetBooks,
    setGenres: mockSetGenres,
    ...props,
  };
  return render(<AddBook {...defaultProps} />);
};

describe("AddBook", () => {
  describe("rendering", () => {
    it("should render the open form button", () => {
      renderComponent();
      expect(screen.getByRole("button", { name: "Open add book form" })).toBeInTheDocument();
    });

    it("should not render the form initially", () => {
      renderComponent();
      expect(screen.queryByRole("form", { name: "Add new book form" })).not.toBeInTheDocument();
    });
  });

  describe("behavior", () => {
    it("should show the form when the open button is clicked", async () => {
      const user = userEvent.setup();
      renderComponent();
      await user.click(screen.getByRole("button", { name: "Open add book form" }));
      expect(screen.getByRole("form", { name: "Add new book form" })).toBeInTheDocument();
    });

    it("should hide the form when the open button is clicked again", async () => {
      const user = userEvent.setup();
      renderComponent();
      const openBtn = screen.getByRole("button", { name: "Open add book form" });
      await user.click(openBtn);
      await user.click(openBtn);
      expect(screen.queryByRole("form", { name: "Add new book form" })).not.toBeInTheDocument();
    });

    it("should render all form fields when the form is open", async () => {
      const user = userEvent.setup();
      renderComponent();
      await user.click(screen.getByRole("button", { name: "Open add book form" }));
      expect(screen.getByLabelText("Title")).toBeInTheDocument();
      expect(screen.getByLabelText("Author")).toBeInTheDocument();
      expect(screen.getByLabelText("Genre")).toBeInTheDocument();
      expect(screen.getByLabelText("Description")).toBeInTheDocument();
      expect(screen.getByLabelText("Image")).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Submit new book" })).toBeInTheDocument();
    });

    it("should update the title input value when typed", async () => {
      const user = userEvent.setup();
      renderComponent();
      await user.click(screen.getByRole("button", { name: "Open add book form" }));
      const titleInput = screen.getByLabelText("Title");
      await user.type(titleInput, "My Book");
      expect(titleInput).toHaveValue("My Book");
    });

    it("should call bookService.add with the form data on submit", async () => {
      jest.mocked(bookService.add).mockResolvedValue({
        message: "ok",
        code: "200",
        data: mockBook,
      });
      const user = userEvent.setup();
      renderComponent();
      await user.click(screen.getByRole("button", { name: "Open add book form" }));
      await user.type(screen.getByLabelText("Title"), mockBook.title);
      await user.type(screen.getByLabelText("Author"), mockBook.author);
      await user.type(screen.getByLabelText("Genre"), mockBook.genre);
      await user.type(screen.getByLabelText("Description"), mockBook.description);
      await user.type(screen.getByLabelText("Image"), mockBook.image);
      await user.click(screen.getByRole("button", { name: "Submit new book" }));
      await waitFor(() => {
        expect(jest.mocked(bookService.add)).toHaveBeenCalledWith({
          title: mockBook.title,
          author: mockBook.author,
          genre: mockBook.genre,
          description: mockBook.description,
          image: mockBook.image,
        });
      });
    });

    it("should call setBooks with the updated list when submit succeeds", async () => {
      jest.mocked(bookService.add).mockResolvedValue({
        message: "ok",
        code: "200",
        data: mockBook,
      });
      const user = userEvent.setup();
      renderComponent();
      await user.click(screen.getByRole("button", { name: "Open add book form" }));
      await user.click(screen.getByRole("button", { name: "Submit new book" }));
      await waitFor(() => {
        expect(mockSetBooks).toHaveBeenCalledWith([...mockBooks, { ...mockBook }]);
      });
    });

    it("should call setGenres when the new book has a genre not in the list", async () => {
      const newBook = { ...mockBook, genre: "Science Fiction" };
      jest.mocked(bookService.add).mockResolvedValue({
        message: "ok",
        code: "200",
        data: newBook,
      });
      const user = userEvent.setup();
      renderComponent({ genres: mockGenres });
      await user.click(screen.getByRole("button", { name: "Open add book form" }));
      await user.click(screen.getByRole("button", { name: "Submit new book" }));
      await waitFor(() => {
        expect(mockSetGenres).toHaveBeenCalledWith([...mockGenres, "Science Fiction"]);
      });
    });

    it("should not call setGenres when the new book has an existing genre", async () => {
      jest.mocked(bookService.add).mockResolvedValue({
        message: "ok",
        code: "200",
        data: mockBook,
      });
      const user = userEvent.setup();
      renderComponent({ genres: [mockBook.genre] });
      await user.click(screen.getByRole("button", { name: "Open add book form" }));
      await user.click(screen.getByRole("button", { name: "Submit new book" }));
      await waitFor(() => {
        expect(mockSetBooks).toHaveBeenCalled();
      });
      expect(mockSetGenres).not.toHaveBeenCalled();
    });
  });
});
