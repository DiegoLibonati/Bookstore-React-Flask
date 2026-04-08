import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { PaginationProps } from "@/types/props";

import Pagination from "@/components/Pagination/Pagination";

interface RenderComponent {
  container: HTMLElement;
  props: PaginationProps;
}

const mockSetCurrentPage = jest.fn();

const renderComponent = (overrides?: Partial<PaginationProps>): RenderComponent => {
  const props: PaginationProps = {
    totalBooks: 14,
    booksPerPage: 7,
    setCurrentPage: mockSetCurrentPage,
    ...overrides,
  };
  const { container } = render(<Pagination {...props} />);
  return { container, props };
};

describe("Pagination", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it("should render the pagination list", () => {
    const { container } = renderComponent();
    expect(container.querySelector<HTMLUListElement>("ul.pagination-list")).toBeInTheDocument();
  });

  it("should render the correct number of page items", () => {
    renderComponent();
    expect(screen.getAllByRole("listitem")).toHaveLength(2);
  });

  it("should render no items when there are no books", () => {
    renderComponent({ totalBooks: 0 });
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });

  it("should call setCurrentPage with the correct page number when an item is clicked", async () => {
    const user = userEvent.setup();
    renderComponent();
    await user.click(screen.getAllByRole("listitem")[1]!);
    expect(mockSetCurrentPage).toHaveBeenCalledWith(2);
  });
});
