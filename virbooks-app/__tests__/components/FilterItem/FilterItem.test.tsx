import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { RenderResult } from "@testing-library/react";
import type { FilterItemProps } from "@/types/props";

import FilterItem from "@/components/FilterItem/FilterItem";

import bookService from "@/services/bookService";

import { mockBooks } from "@tests/__mocks__/books.mock";
import { mockGenre } from "@tests/__mocks__/genres.mock";

const mockSetBooks = jest.fn();

jest.mock("@/services/bookService", () => ({
  __esModule: true,
  default: {
    add: jest.fn(),
    getAll: jest.fn(),
    getAllByGenre: jest.fn(),
  },
}));

const renderComponent = (props: Partial<FilterItemProps> = {}): RenderResult => {
  const defaultProps: FilterItemProps = {
    genre: mockGenre,
    setBooks: mockSetBooks,
    ...props,
  };
  return render(<FilterItem {...defaultProps} />);
};

describe("FilterItem", () => {
  describe("rendering", () => {
    it("should render the genre text", () => {
      renderComponent();
      expect(screen.getByText(mockGenre)).toBeInTheDocument();
    });

    it("should render a different genre when provided", () => {
      renderComponent({ genre: "Science Fiction" });
      expect(screen.getByText("Science Fiction")).toBeInTheDocument();
    });
  });

  describe("behavior", () => {
    it("should call bookService.getAllByGenre with the genre when clicked", async () => {
      jest.mocked(bookService.getAllByGenre).mockResolvedValue({
        message: "ok",
        code: "200",
        data: mockBooks,
      });
      const user = userEvent.setup();
      renderComponent();
      await user.click(screen.getByText(mockGenre));
      await waitFor(() => {
        expect(jest.mocked(bookService.getAllByGenre)).toHaveBeenCalledWith(mockGenre);
      });
    });

    it("should call setBooks with the fetched books after clicking", async () => {
      jest.mocked(bookService.getAllByGenre).mockResolvedValue({
        message: "ok",
        code: "200",
        data: mockBooks,
      });
      const user = userEvent.setup();
      renderComponent();
      await user.click(screen.getByText(mockGenre));
      await waitFor(() => {
        expect(mockSetBooks).toHaveBeenCalledWith(mockBooks);
      });
    });

    it("should call getAllByGenre with the correct genre when a different genre is provided", async () => {
      jest.mocked(bookService.getAllByGenre).mockResolvedValue({
        message: "ok",
        code: "200",
        data: mockBooks,
      });
      const user = userEvent.setup();
      renderComponent({ genre: "Fantasy" });
      await user.click(screen.getByText("Fantasy"));
      await waitFor(() => {
        expect(jest.mocked(bookService.getAllByGenre)).toHaveBeenCalledWith("Fantasy");
      });
    });
  });
});
