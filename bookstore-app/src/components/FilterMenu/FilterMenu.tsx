import { Book } from "../../entities/entities";

import { FilterItem } from "../FilterItem/FilterItem";

import { useHide } from "../../hooks/useHide";

import "./FilterMenu.css";

interface FilterMenuProps {
  genres: string[];
  filterName: string;
  setBooks: React.Dispatch<React.SetStateAction<Book[]>>;
}

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
