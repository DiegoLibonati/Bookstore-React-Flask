import type { Book } from "@/types/app";
import type { ResponseWithData } from "@/types/responses";

const genreService = {
  getAll: async (): Promise<ResponseWithData<Book["genre"][]>> => {
    const response = await fetch(`/api/v1/books/genres`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    return (await response.json()) as ResponseWithData<Book["genre"][]>;
  },
};

export default genreService;
