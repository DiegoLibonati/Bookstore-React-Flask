import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { RenderResult } from "@testing-library/react";
import type { PaginationProps } from "@/types/props";

import Pagination from "@/components/Pagination/Pagination";

const mockSetCurrentPage = jest.fn();

const renderComponent = (props: Partial<PaginationProps> = {}): RenderResult => {
  const defaultProps: PaginationProps = {
    totalBooks: 14,
    booksPerPage: 7,
    setCurrentPage: mockSetCurrentPage,
    ...props,
  };
  return render(<Pagination {...defaultProps} />);
};

describe("Pagination", () => {
  describe("rendering", () => {
    it("should render the correct number of page items", () => {
      renderComponent({ totalBooks: 14, booksPerPage: 7 });
      expect(screen.getAllByRole("listitem")).toHaveLength(2);
    });

    it("should render page numbers starting from 1", () => {
      renderComponent({ totalBooks: 7, booksPerPage: 7 });
      expect(screen.getByText("1")).toBeInTheDocument();
    });

    it("should render no items when there are no books", () => {
      renderComponent({ totalBooks: 0, booksPerPage: 7 });
      expect(screen.queryAllByRole("listitem")).toHaveLength(0);
    });

    it("should ceil the page count for a partial last page", () => {
      renderComponent({ totalBooks: 8, booksPerPage: 7 });
      expect(screen.getAllByRole("listitem")).toHaveLength(2);
    });

    it("should render three pages for 21 books with 7 per page", () => {
      renderComponent({ totalBooks: 21, booksPerPage: 7 });
      expect(screen.getAllByRole("listitem")).toHaveLength(3);
    });
  });

  describe("behavior", () => {
    it("should call setCurrentPage with 1 when the first page item is clicked", async () => {
      const user = userEvent.setup();
      renderComponent({ totalBooks: 14, booksPerPage: 7 });
      await user.click(screen.getByText("1"));
      expect(mockSetCurrentPage).toHaveBeenCalledWith(1);
    });

    it("should call setCurrentPage with the correct page number when clicked", async () => {
      const user = userEvent.setup();
      renderComponent({ totalBooks: 14, booksPerPage: 7 });
      await user.click(screen.getByText("2"));
      expect(mockSetCurrentPage).toHaveBeenCalledWith(2);
    });

    it("should call setCurrentPage only once per click", async () => {
      const user = userEvent.setup();
      renderComponent({ totalBooks: 14, booksPerPage: 7 });
      await user.click(screen.getByText("1"));
      expect(mockSetCurrentPage).toHaveBeenCalledTimes(1);
    });
  });
});
