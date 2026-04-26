import genreService from "@/services/genreService";

import { mockGenres } from "@tests/__mocks__/genres.mock";

const mockGenresResponse = { message: "ok", code: "200", data: mockGenres };

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

describe("genreService", () => {
  describe("getAll", () => {
    describe("when fetch succeeds", () => {
      it("should return the genres response", async () => {
        mockFetchSuccess(mockGenresResponse);
        const result = await genreService.getAll();
        expect(result).toEqual(mockGenresResponse);
      });

      it("should call fetch with the correct endpoint", async () => {
        mockFetchSuccess(mockGenresResponse);
        await genreService.getAll();
        expect(global.fetch).toHaveBeenCalledWith(
          "/api/v1/books/genres",
          expect.objectContaining({ method: "GET" })
        );
      });

      it("should call fetch with the correct headers", async () => {
        mockFetchSuccess(mockGenresResponse);
        await genreService.getAll();
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
        await expect(genreService.getAll()).rejects.toThrow("HTTP error! status: 500");
      });

      it("should throw an error with status 404", async () => {
        mockFetchError(404);
        await expect(genreService.getAll()).rejects.toThrow("HTTP error! status: 404");
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockFetchNetworkError("Failed to fetch");
        await expect(genreService.getAll()).rejects.toThrow("Failed to fetch");
      });
    });
  });
});
