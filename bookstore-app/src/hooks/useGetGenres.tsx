import { useEffect, useState } from "react";

import { Book } from "@src/entities/entities";
import { UseGetGenres } from "@src/entities/hooks";

import { getGenres } from "@src/api/getGenres";

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
