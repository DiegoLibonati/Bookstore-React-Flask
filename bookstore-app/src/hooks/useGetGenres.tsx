import { useEffect, useState } from "react";

import { Book } from "../entities/entities";

import { getGenres } from "../api/getGenres";

type UseGetGenres = {
  genres: Book["genre"][];
  setGenres: React.Dispatch<React.SetStateAction<string[]>>;
};

export const useGetGenres = (): UseGetGenres => {
  const [genres, setGenres] = useState<Book["genre"][]>([]);

  const handleGenres = async (): Promise<void> => {
    const genres = await getGenres();

    setGenres(genres);

    return;
  };

  useEffect(() => {
    handleGenres();
  }, []);

  return {
    genres,
    setGenres,
  };
};
