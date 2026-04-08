import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { FilterMenuProps } from "@/types/props";

import FilterMenu from "@/components/FilterMenu/FilterMenu";

import { mockGenres } from "@tests/__mocks__/genres.mock";

interface RenderComponent {
  container: HTMLElement;
  props: FilterMenuProps;
}

const mockSetBooks = jest.fn();

const renderComponent = (overrides?: Partial<FilterMenuProps>): RenderComponent => {
  const props: FilterMenuProps = {
    genres: mockGenres,
    filterName: "Genres",
    setBooks: mockSetBooks,
    ...overrides,
  };
  const { container } = render(
    <ul>
      <FilterMenu {...props} />
    </ul>
  );
  return { container, props };
};

describe("FilterMenu", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it("should render the filter menu with its name", () => {
    renderComponent();
    expect(screen.getByText("Genres")).toBeInTheDocument();
  });

  it("should not show genre items initially", () => {
    const { props } = renderComponent();
    expect(screen.queryByText(props.genres[0]!)).not.toBeInTheDocument();
  });

  it("should show genre items when clicked", async () => {
    const user = userEvent.setup();
    const { container, props } = renderComponent();
    await user.click(container.querySelector<HTMLLIElement>(".filter-menu")!);
    expect(screen.getByText(props.genres[0]!)).toBeInTheDocument();
  });

  it("should hide genre items when clicked again", async () => {
    const user = userEvent.setup();
    const { container, props } = renderComponent();
    const filterMenu = container.querySelector<HTMLLIElement>(".filter-menu")!;
    await user.click(filterMenu);
    await user.click(filterMenu);
    expect(screen.queryByText(props.genres[0]!)).not.toBeInTheDocument();
  });
});
