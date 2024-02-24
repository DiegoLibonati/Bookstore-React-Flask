import { FormBook } from "../entities/entities";
import { api_route } from "./route";

export const postBook = async (
  body: FormBook
): Promise<Response> => {
  return await fetch(`${api_route}/add`, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });
};
