import { Book, FormBook } from "@src/entities/entities";

import { apiRouteBooks } from "@src/api/route";

export const postBook = async (body: FormBook): Promise<Book> => {
  const request = await fetch(`${apiRouteBooks}/`, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });

  const response: { code: string; message: string; data: Book } =
    await request.json();

  return response.data;
};
