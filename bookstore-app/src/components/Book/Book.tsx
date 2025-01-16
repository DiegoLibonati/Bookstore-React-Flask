import { useHide } from "../../hooks/useHide";

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
      <img onClick={() => handleHide()} src={image} alt={title}></img>

      {hide ? (
        <div className="book__information">
          <h2>{title}</h2>
          <h3>{author}</h3>
          <p>{description}</p>
        </div>
      ) : null}
    </article>
  );
};
