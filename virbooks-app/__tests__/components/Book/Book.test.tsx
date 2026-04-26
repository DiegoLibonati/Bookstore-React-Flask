import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { RenderResult } from "@testing-library/react";
import type { BookProps } from "@/types/props";

import Book from "@/components/Book/Book";

import { mockBook } from "@tests/__mocks__/books.mock";

const renderComponent = (props: Partial<BookProps> = {}): RenderResult => {
  const defaultProps: BookProps = {
    image: mockBook.image,
    title: mockBook.title,
    author: mockBook.author,
    description: mockBook.description,
    ...props,
  };
  return render(<Book {...defaultProps} />);
};

describe("Book", () => {
  describe("rendering", () => {
    it("should render the book image with the correct alt text", () => {
      renderComponent();
      expect(screen.getByRole("img", { name: mockBook.title })).toBeInTheDocument();
    });

    it("should render the book image with the correct src", () => {
      renderComponent();
      expect(screen.getByRole("img", { name: mockBook.title })).toHaveAttribute(
        "src",
        mockBook.image
      );
    });

    it("should not render book information initially", () => {
      renderComponent();
      expect(screen.queryByRole("heading", { name: mockBook.title })).not.toBeInTheDocument();
    });
  });

  describe("behavior", () => {
    it("should show book information when the image is clicked", async () => {
      const user = userEvent.setup();
      renderComponent();
      await user.click(screen.getByRole("img", { name: mockBook.title }));
      expect(screen.getByRole("heading", { name: mockBook.title })).toBeInTheDocument();
      expect(screen.getByText(mockBook.author)).toBeInTheDocument();
      expect(screen.getByText(mockBook.description)).toBeInTheDocument();
    });

    it("should render the title as an h2 when shown", async () => {
      const user = userEvent.setup();
      renderComponent();
      await user.click(screen.getByRole("img", { name: mockBook.title }));
      expect(screen.getByRole("heading", { name: mockBook.title, level: 2 })).toBeInTheDocument();
    });

    it("should hide book information when the image is clicked again", async () => {
      const user = userEvent.setup();
      renderComponent();
      const img = screen.getByRole("img", { name: mockBook.title });
      await user.click(img);
      await user.click(img);
      expect(screen.queryByRole("heading", { name: mockBook.title })).not.toBeInTheDocument();
    });

    it("should display the correct title when a different title is provided", async () => {
      const user = userEvent.setup();
      renderComponent({ title: "El Quijote" });
      await user.click(screen.getByRole("img", { name: "El Quijote" }));
      expect(screen.getByRole("heading", { name: "El Quijote", level: 2 })).toBeInTheDocument();
    });
  });
});
