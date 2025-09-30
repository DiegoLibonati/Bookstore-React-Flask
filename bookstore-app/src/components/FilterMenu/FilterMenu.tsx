import { FilterMenuProps } from "@src/entities/props";

import { FilterItem } from "@src/components/FilterItem/FilterItem";

import { useHide } from "@src/hooks/useHide";

import "@src/components/FilterMenu/FilterMenu.css";

export const FilterMenu = ({
  genres,
  filterName,
  setBooks,
}: FilterMenuProps): JSX.Element => {
  const { hide, handleHide } = useHide();

  return (
    <li onClick={handleHide} className="filter-menu">
      {filterName}
      {hide ? (
        <ul className="filter-menu__items">
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
