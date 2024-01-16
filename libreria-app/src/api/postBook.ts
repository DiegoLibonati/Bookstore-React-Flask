import { FormBook } from "../entities/entities";

export const postBook = async (
  body: Omit<FormBook, "genre"> & { genero: string }
): Promise<Response> => {
  return await fetch("http://127.0.0.1:5000/libreria/crear", {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
    },
  });
};
