import type { Book } from "@/types/app";
import type { BookAddPayload } from "@/types/payloads";
import type { ResponseWithData } from "@/types/responses";

const bookService = {
  getAll: async (): Promise<ResponseWithData<Book[]>> => {
    const response = await fetch(`/api/v1/books/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    return (await response.json()) as ResponseWithData<Book[]>;
  },
  getAllByGenre: async (genre: string): Promise<ResponseWithData<Book[]>> => {
    const response = await fetch(`/api/v1/books/${genre}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    return (await response.json()) as ResponseWithData<Book[]>;
  },
  add: async (body: BookAddPayload): Promise<ResponseWithData<Book>> => {
    const response = await fetch(`/api/v1/books/`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    return (await response.json()) as ResponseWithData<Book>;
  },
};

export default bookService;
