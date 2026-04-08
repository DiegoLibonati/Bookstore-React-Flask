import type { JSX } from "react";
import type { FilterMenuProps } from "@/types/props";

import FilterItem from "@/components/FilterItem/FilterItem";

import { useHide } from "@/hooks/useHide";

import "@/components/FilterMenu/FilterMenu.css";

const FilterMenu = ({ genres, filterName, setBooks }: FilterMenuProps): JSX.Element => {
  const { hide, handleHide } = useHide();

  return (
    <li onClick={handleHide} className="filter-menu">
      {filterName}
      {hide ? (
        <ul className="filter-menu__items">
          {genres.map((genre, index) => (
            <FilterItem key={index * 12} setBooks={setBooks} genre={genre}></FilterItem>
          ))}
        </ul>
      ) : null}
    </li>
  );
};

export default FilterMenu;
