import type { Book } from "@/types/app";

const genreService = {
  getAll: async (): Promise<{
    message: string;
    code: string;
    data: Book["genre"][];
  }> => {
    const response = await fetch(`/api/v1/books/genres`, {
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
      data: Book["genre"][];
    };
  },
};

export default genreService;
