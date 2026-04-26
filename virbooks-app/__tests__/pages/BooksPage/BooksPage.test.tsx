import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { RenderResult } from "@testing-library/react";

import BooksPage from "@/pages/BooksPage/BooksPage";

import bookService from "@/services/bookService";
import genreService from "@/services/genreService";

import { mockBook, mockBooks } from "@tests/__mocks__/books.mock";
import { mockGenres } from "@tests/__mocks__/genres.mock";

const mockBooksResponse = { message: "ok", code: "200", data: mockBooks };
const mockGenresResponse = { message: "ok", code: "200", data: mockGenres };

jest.mock("@/services/bookService", () => ({
  __esModule: true,
  default: {
    add: jest.fn(),
    getAll: jest.fn(),
    getAllByGenre: jest.fn(),
  },
}));

jest.mock("@/services/genreService", () => ({
  __esModule: true,
  default: {
    getAll: jest.fn(),
  },
}));

const renderPage = (): RenderResult => render(<BooksPage />);

describe("BooksPage", () => {
  describe("rendering", () => {
    it("should show the loading state while data is being fetched", async () => {
      jest.mocked(bookService.getAll).mockReturnValue(
        new Promise(() => {
          // Empty fn
        })
      );
      jest.mocked(genreService.getAll).mockReturnValue(
        new Promise(() => {
          // Empty fn
        })
      );
      renderPage();
      await waitFor(() => {
        expect(screen.getByRole("heading", { name: "Loading" })).toBeInTheDocument();
      });
    });

    it("should render the filters button after data loads", async () => {
      jest.mocked(bookService.getAll).mockResolvedValue(mockBooksResponse);
      jest.mocked(genreService.getAll).mockResolvedValue(mockGenresResponse);
      renderPage();
      expect(
        await screen.findByRole("button", { name: "Toggle book filters" })
      ).toBeInTheDocument();
    });

    it("should render books after data loads", async () => {
      jest.mocked(bookService.getAll).mockResolvedValue(mockBooksResponse);
      jest.mocked(genreService.getAll).mockResolvedValue(mockGenresResponse);
      renderPage();
      expect(await screen.findByRole("img", { name: mockBook.title })).toBeInTheDocument();
    });

    it("should render the AddBook button after data loads", async () => {
      jest.mocked(bookService.getAll).mockResolvedValue(mockBooksResponse);
      jest.mocked(genreService.getAll).mockResolvedValue(mockGenresResponse);
      renderPage();
      expect(await screen.findByRole("button", { name: "Open add book form" })).toBeInTheDocument();
    });
  });

  describe("behavior", () => {
    it("should show the filters menu when the filters button is clicked", async () => {
      jest.mocked(bookService.getAll).mockResolvedValue(mockBooksResponse);
      jest.mocked(genreService.getAll).mockResolvedValue(mockGenresResponse);
      const user = userEvent.setup();
      renderPage();
      const filtersBtn = await screen.findByRole("button", { name: "Toggle book filters" });
      await user.click(filtersBtn);
      expect(screen.getByText("Show All")).toBeInTheDocument();
    });

    it("should hide the filters menu when the filters button is clicked again", async () => {
      jest.mocked(bookService.getAll).mockResolvedValue(mockBooksResponse);
      jest.mocked(genreService.getAll).mockResolvedValue(mockGenresResponse);
      const user = userEvent.setup();
      renderPage();
      const filtersBtn = await screen.findByRole("button", { name: "Toggle book filters" });
      await user.click(filtersBtn);
      await user.click(filtersBtn);
      expect(screen.queryByText("Show All")).not.toBeInTheDocument();
    });

    it("should show the Genres filter menu when genres are loaded and filters are open", async () => {
      jest.mocked(bookService.getAll).mockResolvedValue(mockBooksResponse);
      jest.mocked(genreService.getAll).mockResolvedValue(mockGenresResponse);
      const user = userEvent.setup();
      renderPage();
      const filtersBtn = await screen.findByRole("button", { name: "Toggle book filters" });
      await user.click(filtersBtn);
      expect(screen.getByText("Genres")).toBeInTheDocument();
    });

    it("should refetch all books when Show All is clicked", async () => {
      jest.mocked(bookService.getAll).mockResolvedValue(mockBooksResponse);
      jest.mocked(genreService.getAll).mockResolvedValue(mockGenresResponse);
      const user = userEvent.setup();
      renderPage();
      const filtersBtn = await screen.findByRole("button", { name: "Toggle book filters" });
      await user.click(filtersBtn);
      await user.click(screen.getByText("Show All"));
      await waitFor(() => {
        expect(jest.mocked(bookService.getAll)).toHaveBeenCalledTimes(2);
      });
    });
  });
});
