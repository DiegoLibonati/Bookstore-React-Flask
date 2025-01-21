import { useHide } from "../../hooks/useHide";

import "./Book.css";

interface BookProps {
  image: string;
  title: string;
  author: string;
  description: string;
}

export const Book = ({
  image,
  title,
  author,
  description,
}: BookProps): JSX.Element => {
  const { hide, handleHide } = useHide();

  return (
    <article className="book">
      <img
        onClick={() => handleHide()}
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
