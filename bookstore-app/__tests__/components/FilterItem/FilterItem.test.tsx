import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { FilterItemProps } from "@/types/props";

import FilterItem from "@/components/FilterItem/FilterItem";

import bookService from "@/services/bookService";

import { mockBooks } from "@tests/__mocks__/books.mock";
import { mockGenre } from "@tests/__mocks__/genres.mock";

jest.mock("@/services/bookService");

interface RenderComponent {
  container: HTMLElement;
  props: FilterItemProps;
}

const mockSetBooks = jest.fn();

const renderComponent = (overrides?: Partial<FilterItemProps>): RenderComponent => {
  const props: FilterItemProps = {
    genre: mockGenre,
    setBooks: mockSetBooks,
    ...overrides,
  };
  const { container } = render(
    <ul>
      <FilterItem {...props} />
    </ul>
  );
  return { container, props };
};

describe("FilterItem", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it("should render the genre text", () => {
    renderComponent();
    expect(screen.getByText(mockGenre)).toBeInTheDocument();
  });

  it("should call bookService.getAllByGenre and setBooks when clicked", async () => {
    const user = userEvent.setup();
    (bookService.getAllByGenre as jest.Mock).mockResolvedValueOnce({
      message: "ok",
      code: "200",
      data: mockBooks,
    });
    renderComponent();
    await user.click(screen.getByText(mockGenre));
    await waitFor(() => {
      expect(bookService.getAllByGenre).toHaveBeenCalledWith(mockGenre);
      expect(mockSetBooks).toHaveBeenCalledWith(mockBooks);
    });
  });
});
