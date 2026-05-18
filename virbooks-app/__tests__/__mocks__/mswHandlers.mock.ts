import { http, HttpResponse } from "msw";

import { mockBook, mockBooks } from "@tests/__mocks__/books.mock";
import { mockGenres } from "@tests/__mocks__/genres.mock";

export const mockMswHandlers = [
  http.get("/api/v1/books/", () => {
    return HttpResponse.json({ message: "ok", code: "200", data: mockBooks });
  }),
  http.get("/api/v1/books/genres", () => {
    return HttpResponse.json({ message: "ok", code: "200", data: mockGenres });
  }),
  http.get("/api/v1/books/:genre", ({ params }) => {
    return HttpResponse.json({
      message: "ok",
      code: "200",
      data: mockBooks.filter((book) => book.genre === params.genre),
    });
  }),
  http.post("/api/v1/books/", async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>;
    return HttpResponse.json(
      {
        message: "created",
        code: "201",
        data: { ...mockBook, ...body },
      },
      { status: 201 }
    );
  }),
];
