import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import BooksPage from "@/pages/BooksPage/BooksPage";

import bookService from "@/services/bookService";
import genreService from "@/services/genreService";

import { mockBooks } from "@tests/__mocks__/books.mock";
import { mockGenres } from "@tests/__mocks__/genres.mock";

jest.mock("@/services/bookService");
jest.mock("@/services/genreService");

interface RenderPage {
  container: HTMLElement;
}

const renderPage = (): RenderPage => {
  (bookService.getAll as jest.Mock).mockResolvedValue({
    message: "ok",
    code: "200",
    data: mockBooks,
  });
  (genreService.getAll as jest.Mock).mockResolvedValue({
    message: "ok",
    code: "200",
    data: mockGenres,
  });
  const { container } = render(<BooksPage />);
  return { container };
};

describe("BooksPage", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it("should render the main element", async () => {
    const { container } = renderPage();
    await waitFor(() => {
      expect(container.querySelector<HTMLElement>("main.main-app")).toBeInTheDocument();
    });
  });

  it("should fetch books and genres on mount", async () => {
    renderPage();
    await waitFor(() => {
      expect(bookService.getAll).toHaveBeenCalledTimes(1);
      expect(genreService.getAll).toHaveBeenCalledTimes(1);
    });
  });

  it("should render the filter toggle button", async () => {
    renderPage();
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Toggle book filters" })).toBeInTheDocument();
    });
  });

  it("should render books after fetching", async () => {
    renderPage();
    await waitFor(() => {
      expect(screen.getByAltText(mockBooks[0]!.title)).toBeInTheDocument();
    });
  });

  it("should show filter menu when the filter button is clicked", async () => {
    const user = userEvent.setup();
    renderPage();
    await waitFor(() => screen.getByRole("button", { name: "Toggle book filters" }));
    await user.click(screen.getByRole("button", { name: "Toggle book filters" }));
    expect(screen.getByText("Show All")).toBeInTheDocument();
  });

  it("should re-fetch books when Show All is clicked", async () => {
    const user = userEvent.setup();
    renderPage();
    await waitFor(() => screen.getByRole("button", { name: "Toggle book filters" }));
    await user.click(screen.getByRole("button", { name: "Toggle book filters" }));
    await user.click(screen.getByText("Show All"));
    await waitFor(() => {
      expect(bookService.getAll).toHaveBeenCalledTimes(2);
    });
  });
});
