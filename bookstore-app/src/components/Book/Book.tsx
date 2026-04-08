import type { JSX } from "react";
import type { BookProps } from "@/types/props";

import { useHide } from "@/hooks/useHide";

import "@/components/Book/Book.css";

const Book = ({ image, title, author, description }: BookProps): JSX.Element => {
  const { hide, handleHide } = useHide();

  return (
    <article className="book">
      <img
        onClick={() => {
          handleHide();
        }}
        src={image}
        alt={title}
        className="book__img"
      ></img>

      {hide ? (
        <div className="book__information">
          <h2 className="book__title">{title}</h2>
          <h3 className="book__author">{author}</h3>
          <p className="book__description">{description}</p>
        </div>
      ) : null}
    </article>
  );
};

export default Book;
