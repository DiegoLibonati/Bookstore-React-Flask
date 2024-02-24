import { useEffect } from "react";
import { useState } from "react";
import { Book, UseGetGenres } from "../entities/entities";
import { getGenres } from "../api/getGenres";

export const useGetGenres = (): UseGetGenres => {
  const [genres, setGenres] = useState<Book["genre"][]>([]);

  const handleGenres = async (): Promise<void> => {
    const genres = await getGenres();

    setGenres(genres);

    return
  };

  useEffect(() => {
    handleGenres();
  }, []);

  return {
    genres,
    setGenres,
  };
};
