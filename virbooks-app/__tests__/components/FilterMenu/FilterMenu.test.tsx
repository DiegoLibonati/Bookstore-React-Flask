import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { RenderResult } from "@testing-library/react";
import type { FilterMenuProps } from "@/types/props";

import FilterMenu from "@/components/FilterMenu/FilterMenu";

import { mockGenres } from "@tests/__mocks__/genres.mock";

const mockSetBooks = jest.fn();

jest.mock("@/services/bookService", () => ({
  __esModule: true,
  default: {
    add: jest.fn(),
    getAll: jest.fn(),
    getAllByGenre: jest.fn(),
  },
}));

const renderComponent = (props: Partial<FilterMenuProps> = {}): RenderResult => {
  const defaultProps: FilterMenuProps = {
    genres: mockGenres,
    filterName: "Genres",
    setBooks: mockSetBooks,
    ...props,
  };
  return render(<FilterMenu {...defaultProps} />);
};

describe("FilterMenu", () => {
  describe("rendering", () => {
    it("should render the filter name", () => {
      renderComponent();
      expect(screen.getByText("Genres")).toBeInTheDocument();
    });

    it("should not render genre items initially", () => {
      renderComponent();
      mockGenres.forEach((genre) => {
        expect(screen.queryByText(genre)).not.toBeInTheDocument();
      });
    });

    it("should render a custom filter name when provided", () => {
      renderComponent({ filterName: "Categories" });
      expect(screen.getByText("Categories")).toBeInTheDocument();
    });
  });

  describe("behavior", () => {
    it("should show genre items when the filter menu is clicked", async () => {
      const user = userEvent.setup();
      renderComponent();
      await user.click(screen.getByText("Genres"));
      mockGenres.forEach((genre) => {
        expect(screen.getByText(genre)).toBeInTheDocument();
      });
    });

    it("should hide genre items when the filter menu is clicked again", async () => {
      const user = userEvent.setup();
      renderComponent();
      await user.click(screen.getByText("Genres"));
      await user.click(screen.getByText("Genres"));
      mockGenres.forEach((genre) => {
        expect(screen.queryByText(genre)).not.toBeInTheDocument();
      });
    });

    it("should render a FilterItem for each genre in the list", async () => {
      const user = userEvent.setup();
      const genres = ["Fantasy", "Horror", "Romance"];
      renderComponent({ genres });
      await user.click(screen.getByText("Genres"));
      genres.forEach((genre) => {
        expect(screen.getByText(genre)).toBeInTheDocument();
      });
    });

    it("should render no genre items when genres list is empty", async () => {
      const user = userEvent.setup();
      renderComponent({ genres: [] });
      await user.click(screen.getByText("Genres"));
      expect(screen.queryAllByRole("listitem")).toHaveLength(1);
    });
  });
});
