import { http, HttpResponse } from "msw";

import type { BookAddPayload } from "@/types/payloads";

import bookService from "@/services/bookService";

import { mockBook, mockBooks } from "@tests/__mocks__/books.mock";
import { mockMswServer } from "@tests/__mocks__/mswServer.mock";

const mockBooksResponse = { message: "ok", code: "200", data: mockBooks };
const mockBookResponse = { message: "created", code: "201", data: mockBook };

const mockFormBook: BookAddPayload = {
  title: mockBook.title,
  author: mockBook.author,
  genre: mockBook.genre,
  description: mockBook.description,
  image: mockBook.image,
};

describe("bookService", () => {
  describe("getAll", () => {
    describe("when fetch succeeds", () => {
      it("should return the books response", async () => {
        mockMswServer.use(http.get("/api/v1/books/", () => HttpResponse.json(mockBooksResponse)));

        const result = await bookService.getAll();

        expect(result).toEqual(mockBooksResponse);
      });

      it("should send the request with JSON headers", async () => {
        let capturedHeaders: Headers | null = null;
        mockMswServer.use(
          http.get("/api/v1/books/", ({ request }) => {
            capturedHeaders = request.headers;
            return HttpResponse.json(mockBooksResponse);
          })
        );

        await bookService.getAll();

        expect(capturedHeaders!.get("Content-Type")).toBe("application/json");
        expect(capturedHeaders!.get("Accept")).toBe("application/json");
      });
    });

    describe("when the server returns an error", () => {
      it("should throw an error with status 500", async () => {
        mockMswServer.use(
          http.get("/api/v1/books/", () => new HttpResponse(null, { status: 500 }))
        );

        await expect(bookService.getAll()).rejects.toThrow("HTTP error! status: 500");
      });

      it("should throw an error with status 404", async () => {
        mockMswServer.use(
          http.get("/api/v1/books/", () => new HttpResponse(null, { status: 404 }))
        );

        await expect(bookService.getAll()).rejects.toThrow("HTTP error! status: 404");
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockMswServer.use(http.get("/api/v1/books/", () => HttpResponse.error()));

        await expect(bookService.getAll()).rejects.toThrow();
      });
    });
  });

  describe("getAllByGenre", () => {
    describe("when fetch succeeds", () => {
      it("should return the books response for the given genre", async () => {
        mockMswServer.use(
          http.get("/api/v1/books/:genre", () => HttpResponse.json(mockBooksResponse))
        );

        const result = await bookService.getAllByGenre("Novela");

        expect(result).toEqual(mockBooksResponse);
      });

      it("should hit the endpoint that includes the genre", async () => {
        let capturedGenre: string | undefined;
        mockMswServer.use(
          http.get("/api/v1/books/:genre", ({ params }) => {
            capturedGenre = params.genre as string;
            return HttpResponse.json(mockBooksResponse);
          })
        );

        await bookService.getAllByGenre("Fantasy");

        expect(capturedGenre).toBe("Fantasy");
      });
    });

    describe("when the server returns an error", () => {
      it("should throw an error with the HTTP status", async () => {
        mockMswServer.use(
          http.get("/api/v1/books/:genre", () => new HttpResponse(null, { status: 404 }))
        );

        await expect(bookService.getAllByGenre("Unknown")).rejects.toThrow(
          "HTTP error! status: 404"
        );
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockMswServer.use(http.get("/api/v1/books/:genre", () => HttpResponse.error()));

        await expect(bookService.getAllByGenre("Novela")).rejects.toThrow();
      });
    });
  });

  describe("add", () => {
    describe("when fetch succeeds", () => {
      it("should return the created book response", async () => {
        mockMswServer.use(
          http.post("/api/v1/books/", () => HttpResponse.json(mockBookResponse, { status: 201 }))
        );

        const result = await bookService.add(mockFormBook);

        expect(result).toEqual(mockBookResponse);
      });

      it("should send the request with the stringified body", async () => {
        let capturedBody: unknown;
        mockMswServer.use(
          http.post("/api/v1/books/", async ({ request }) => {
            capturedBody = await request.json();
            return HttpResponse.json(mockBookResponse, { status: 201 });
          })
        );

        await bookService.add(mockFormBook);

        expect(capturedBody).toEqual(mockFormBook);
      });

      it("should send the request with POST method and JSON headers", async () => {
        let capturedMethod: string | undefined;
        let capturedHeaders: Headers | null = null;
        mockMswServer.use(
          http.post("/api/v1/books/", ({ request }) => {
            capturedMethod = request.method;
            capturedHeaders = request.headers;
            return HttpResponse.json(mockBookResponse, { status: 201 });
          })
        );

        await bookService.add(mockFormBook);

        expect(capturedMethod).toBe("POST");
        expect(capturedHeaders!.get("Content-Type")).toBe("application/json");
        expect(capturedHeaders!.get("Accept")).toBe("application/json");
      });
    });

    describe("when the server returns an error", () => {
      it("should throw an error with the HTTP status", async () => {
        mockMswServer.use(
          http.post("/api/v1/books/", () => new HttpResponse(null, { status: 422 }))
        );

        await expect(bookService.add(mockFormBook)).rejects.toThrow("HTTP error! status: 422");
      });
    });

    describe("when there is a network error", () => {
      it("should propagate the network error", async () => {
        mockMswServer.use(http.post("/api/v1/books/", () => HttpResponse.error()));

        await expect(bookService.add(mockFormBook)).rejects.toThrow();
      });
    });
  });
});
