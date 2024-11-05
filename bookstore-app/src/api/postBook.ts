import { FormBook } from "../entities/entities";

import { api_route_books } from "./route";

export const postBook = async (body: FormBook): Promise<Response> => {
  return await fetch(`${api_route_books}/add`, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });
};
