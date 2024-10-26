import { AddBookProps, FormBook } from "../entities/entities";

import { postBook } from "../api/postBook";
import { useForm } from "../hooks/useForm";
import { useHide } from "../hooks/useHide";

import { BsPlusCircle } from "react-icons/bs";

export const AddBook = ({
  books,
  genres,
  setBooks,
  setGenres,
}: AddBookProps): JSX.Element => {
  const { hide, handleHide } = useHide();

  const { formState, onInputChange } = useForm<FormBook>({
    title: "",
    author: "",
    genre: "",
    description: "",
    image: "",
  });

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();

    const result = await postBook(formState);

    if (result.ok) {
      setBooks([
        ...books,
        { ...formState, _id: { $oid: formState.image + "123" } },
      ]);

      if (!genres.includes(formState.genre)) {
        setGenres([...genres, formState.genre]);
      }
    }
  };

  return (
    <article className="book_container">
      <button
        type="button"
        aria-label="add book"
        className="add_book_button"
        onClick={() => handleHide()}
      >
        <BsPlusCircle id="IconPlus"></BsPlusCircle>
      </button>

      {hide ? (
        <form
          aria-label="form add book"
          className="book_container_information"
          onSubmit={(e) => handleSubmit(e)}
        >
          <label htmlFor="title" className="label_hide">
            Title
          </label>
          <input
            id="title"
            type="text"
            name="title"
            placeholder="Set title"
            value={formState.title}
            onChange={(e) => onInputChange(e)}
          ></input>
          <label htmlFor="author" className="label_hide">
            Author
          </label>
          <input
            id="author"
            type="text"
            name="author"
            placeholder="Set author"
            value={formState.author}
            onChange={(e) => onInputChange(e)}
          ></input>
          <label htmlFor="genre" className="label_hide">
            Genre
          </label>
          <input
            id="genre"
            type="text"
            name="genre"
            placeholder="Set genre"
            value={formState.genre}
            onChange={(e) => onInputChange(e)}
          ></input>
          <label htmlFor="description" className="label_hide">
            Description
          </label>
          <textarea
            id="description"
            placeholder="Set description"
            name="description"
            value={formState.description}
            onChange={(e) => onInputChange(e)}
          ></textarea>
          <label htmlFor="image" className="label_hide">
            Image
          </label>
          <input
            id="image"
            type="text"
            name="image"
            placeholder="Set image link"
            value={formState.image}
            onChange={(e) => onInputChange(e)}
          ></input>
          <button type="submit">Submit</button>
        </form>
      ) : null}
    </article>
  );
};
