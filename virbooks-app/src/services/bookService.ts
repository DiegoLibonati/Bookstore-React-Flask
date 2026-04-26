import type { Book } from "@/types/app";
import type { FormBook } from "@/types/forms";

const bookService = {
  getAll: async (): Promise<{
    message: string;
    code: string;
    data: Book[];
  }> => {
    const response = await fetch(`/api/v1/books/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    return (await response.json()) as {
      message: string;
      code: string;
      data: Book[];
    };
  },
  getAllByGenre: async (
    genre: string
  ): Promise<{
    message: string;
    code: string;
    data: Book[];
  }> => {
    const response = await fetch(`/api/v1/books/${genre}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    return (await response.json()) as {
      message: string;
      code: string;
      data: Book[];
    };
  },
  add: async (
    body: FormBook
  ): Promise<{
    message: string;
    code: string;
    data: Book;
  }> => {
    const response = await fetch(`/api/v1/books/`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    return (await response.json()) as {
      message: string;
      code: string;
      data: Book;
    };
  },
};

export default bookService;
