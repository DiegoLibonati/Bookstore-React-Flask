import { FilterMenuProps } from "../entities/entities";

import { FilterItem } from "./FilterItem";

import { useHide } from "../hooks/useHide";

export const FilterMenu = ({
  genres,
  filterName,
  setBooks,
}: FilterMenuProps): JSX.Element => {
  const { hide, handleHide } = useHide();

  return (
    <li onClick={handleHide}>
      {filterName}
      {hide ? (
        <ul>
          {genres.map((genre, index) => (
            <FilterItem
              key={index * 12}
              setBooks={setBooks}
              genre={genre}
            ></FilterItem>
          ))}
        </ul>
      ) : null}
    </li>
  );
};
