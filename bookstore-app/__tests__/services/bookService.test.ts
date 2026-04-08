import bookService from "@/services/bookService";

import { mockBook, mockBooks } from "@tests/__mocks__/books.mock";

describe("bookService", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  describe("getAll", () => {
    it("should return all books", async () => {
      const mockedFetch = fetch as jest.MockedFunction<typeof fetch>;
      mockedFetch.mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue({ message: "ok", code: "200", data: mockBooks }),
      } as unknown as Response);

      const result = await bookService.getAll();

      expect(result.data).toEqual(mockBooks);
      expect(mockedFetch).toHaveBeenCalledWith("/api/v1/books/", {
        method: "GET",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
      });
    });

    it("should throw an error on non-ok response", async () => {
      const mockedFetch = fetch as jest.MockedFunction<typeof fetch>;
      mockedFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      } as unknown as Response);

      await expect(bookService.getAll()).rejects.toThrow("HTTP error! status: 500");
    });
  });

  describe("getAllByGenre", () => {
    it("should return books filtered by genre", async () => {
      const mockedFetch = fetch as jest.MockedFunction<typeof fetch>;
      mockedFetch.mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue({ message: "ok", code: "200", data: mockBooks }),
      } as unknown as Response);

      const result = await bookService.getAllByGenre("Novela");

      expect(result.data).toEqual(mockBooks);
      expect(mockedFetch).toHaveBeenCalledWith("/api/v1/books/Novela", {
        method: "GET",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
      });
    });

    it("should throw an error on non-ok response", async () => {
      const mockedFetch = fetch as jest.MockedFunction<typeof fetch>;
      mockedFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
      } as unknown as Response);

      await expect(bookService.getAllByGenre("Unknown")).rejects.toThrow("HTTP error! status: 404");
    });
  });

  describe("add", () => {
    it("should add a new book and return it", async () => {
      const mockedFetch = fetch as jest.MockedFunction<typeof fetch>;
      mockedFetch.mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue({ message: "created", code: "201", data: mockBook }),
      } as unknown as Response);

      const formData = {
        title: mockBook.title,
        author: mockBook.author,
        genre: mockBook.genre,
        description: mockBook.description,
        image: mockBook.image,
      };

      const result = await bookService.add(formData);

      expect(result.data).toEqual(mockBook);
      expect(mockedFetch).toHaveBeenCalledWith("/api/v1/books/", {
        method: "POST",
        body: JSON.stringify(formData),
        headers: { "Content-Type": "application/json", Accept: "application/json" },
      });
    });

    it("should throw an error on non-ok response", async () => {
      const mockedFetch = fetch as jest.MockedFunction<typeof fetch>;
      mockedFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
      } as unknown as Response);

      await expect(
        bookService.add({ title: "", author: "", genre: "", description: "", image: "" })
      ).rejects.toThrow("HTTP error! status: 400");
    });
  });
});
