import { Book } from "@src/entities/entities";

import { apiRouteBooks } from "@src/api/route";

export const getGenres = async (): Promise<Book["genre"][]> => {
  const request = await fetch(`${apiRouteBooks}/genres`, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });
  const response: { code: string; message: string; data: Book["genre"][] } =
    await request.json();

  return response.data;
};
