import { http, HttpResponse } from "msw";

import genreService from "@/services/genreService";

import { mockGenres } from "@tests/__mocks__/genres.mock";
import { mockMswServer } from "@tests/__mocks__/mswServer.mock";

const mockGenresResponse = { message: "ok", code: "200", data: mockGenres };

describe("genreService", () => {
  describe("getAll", () => {
    describe("when fetch succeeds", () => {
      it("should return the genres response", async () => {
        mockMswServer.use(
          http.get("/api/v1/books/genres", () => HttpResponse.json(mockGenresResponse))
        );

        const result = await genreService.getAll();

        expect(result).toEqual(mockGenresResponse);
      });

      it("should send the request with JSON headers", async () => {
        let capturedHeaders: Headers | null = null;
        mockMswServer.use(
          http.get("/api/v1/books/genres", ({ request }) => {
            capturedHeaders = request.headers;
            return HttpResponse.json(mockGenresResponse);
          })
        );

        await genreService.getAll();

        expect(capturedHeaders!.get("Content-Type")).toBe("application/json");
        expect(capturedHeaders!.get("Accept")).toBe("application/json");
      });
    });

    describe("when the server returns an error", () => {
      it("should throw an error with status 500", async () => {
        mockMswServer.use(
          http.get("/api/v1/books/genres", () => new HttpResponse(null, { status: 500 }))
        );

        await expect(genreService.getAll()).rejects.toThrow("HTTP error! status: 500");
      });

      it("should throw an error with status 404", async () => {
        mockMswServer.use(
          http.get("/api/v1/books/genres", () => new HttpResponse(null, { status: 404 }))
        );

        await expect(genreService.getAll()).rejects.toThrow("HTTP error! status: 404");
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockMswServer.use(http.get("/api/v1/books/genres", () => HttpResponse.error()));

        await expect(genreService.getAll()).rejects.toThrow();
      });
    });
  });
});
