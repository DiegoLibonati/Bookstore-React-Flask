import type { FormBook } from "@/types/forms";

import bookService from "@/services/bookService";

import { mockBook, mockBooks } from "@tests/__mocks__/books.mock";

const mockBooksResponse = { message: "ok", code: "200", data: mockBooks };
const mockBookResponse = { message: "created", code: "201", data: mockBook };

const mockFetchSuccess = (data: unknown): void => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => await data,
  } as Response);
};

const mockFetchError = (status: number): void => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: false,
    status,
  } as Response);
};

const mockFetchNetworkError = (message = "Network error"): void => {
  global.fetch = jest.fn().mockRejectedValue(new Error(message));
};

describe("bookService", () => {
  describe("getAll", () => {
    describe("when fetch succeeds", () => {
      it("should return the books response", async () => {
        mockFetchSuccess(mockBooksResponse);
        const result = await bookService.getAll();
        expect(result).toEqual(mockBooksResponse);
      });

      it("should call fetch with the correct endpoint", async () => {
        mockFetchSuccess(mockBooksResponse);
        await bookService.getAll();
        expect(global.fetch).toHaveBeenCalledWith(
          "/api/v1/books/",
          expect.objectContaining({ method: "GET" })
        );
      });

      it("should call fetch with the correct headers", async () => {
        mockFetchSuccess(mockBooksResponse);
        await bookService.getAll();
        expect(global.fetch).toHaveBeenCalledWith(
          expect.any(String),
          expect.objectContaining({
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
          })
        );
      });
    });

    describe("when the server returns an error", () => {
      it("should throw an error with status 500", async () => {
        mockFetchError(500);
        await expect(bookService.getAll()).rejects.toThrow("HTTP error! status: 500");
      });

      it("should throw an error with status 404", async () => {
        mockFetchError(404);
        await expect(bookService.getAll()).rejects.toThrow("HTTP error! status: 404");
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockFetchNetworkError("Failed to fetch");
        await expect(bookService.getAll()).rejects.toThrow("Failed to fetch");
      });
    });
  });

  describe("getAllByGenre", () => {
    describe("when fetch succeeds", () => {
      it("should return the books response for the given genre", async () => {
        mockFetchSuccess(mockBooksResponse);
        const result = await bookService.getAllByGenre("Novela");
        expect(result).toEqual(mockBooksResponse);
      });

      it("should call fetch with the endpoint that includes the genre", async () => {
        mockFetchSuccess(mockBooksResponse);
        await bookService.getAllByGenre("Fantasy");
        expect(global.fetch).toHaveBeenCalledWith(
          "/api/v1/books/Fantasy",
          expect.objectContaining({ method: "GET" })
        );
      });
    });

    describe("when the server returns an error", () => {
      it("should throw an error with the HTTP status", async () => {
        mockFetchError(404);
        await expect(bookService.getAllByGenre("Unknown")).rejects.toThrow(
          "HTTP error! status: 404"
        );
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockFetchNetworkError();
        await expect(bookService.getAllByGenre("Novela")).rejects.toThrow("Network error");
      });
    });
  });

  describe("add", () => {
    const mockFormBook: FormBook = {
      title: mockBook.title,
      author: mockBook.author,
      genre: mockBook.genre,
      description: mockBook.description,
      image: mockBook.image,
    };

    describe("when fetch succeeds", () => {
      it("should return the created book response", async () => {
        mockFetchSuccess(mockBookResponse);
        const result = await bookService.add(mockFormBook);
        expect(result).toEqual(mockBookResponse);
      });

      it("should call fetch with POST method and the correct endpoint", async () => {
        mockFetchSuccess(mockBookResponse);
        await bookService.add(mockFormBook);
        expect(global.fetch).toHaveBeenCalledWith(
          "/api/v1/books/",
          expect.objectContaining({ method: "POST" })
        );
      });

      it("should call fetch with the stringified body", async () => {
        mockFetchSuccess(mockBookResponse);
        await bookService.add(mockFormBook);
        expect(global.fetch).toHaveBeenCalledWith(
          expect.any(String),
          expect.objectContaining({ body: JSON.stringify(mockFormBook) })
        );
      });
    });

    describe("when the server returns an error", () => {
      it("should throw an error with the HTTP status", async () => {
        mockFetchError(422);
        await expect(bookService.add(mockFormBook)).rejects.toThrow("HTTP error! status: 422");
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockFetchNetworkError();
        await expect(bookService.add(mockFormBook)).rejects.toThrow("Network error");
      });
    });
  });
});
