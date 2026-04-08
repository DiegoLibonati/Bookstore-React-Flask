import genreService from "@/services/genreService";

import { mockGenres } from "@tests/__mocks__/genres.mock";

describe("genreService", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  describe("getAll", () => {
    it("should return all genres", async () => {
      const mockedFetch = fetch as jest.MockedFunction<typeof fetch>;
      mockedFetch.mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue({ message: "ok", code: "200", data: mockGenres }),
      } as unknown as Response);

      const result = await genreService.getAll();

      expect(result.data).toEqual(mockGenres);
      expect(mockedFetch).toHaveBeenCalledWith("/api/v1/books/genres", {
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

      await expect(genreService.getAll()).rejects.toThrow("HTTP error! status: 500");
    });
  });
});
