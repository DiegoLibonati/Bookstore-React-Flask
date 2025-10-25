import { BsPlusCircle } from "react-icons/bs";

import { FormBook } from "@src/entities/forms";
import { AddBookProps } from "@src/entities/props";

import { useForm } from "@src/hooks/useForm";
import { useHide } from "@src/hooks/useHide";

import { postBook } from "@src/api/post/postBook";

import "@src/components/AddBook/AddBook.css";

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

    const response = await postBook(formState);
    const newBook = response.data;

    if (newBook) {
      setBooks([...books, { ...newBook }]);

      if (!genres.includes(newBook.genre)) {
        setGenres([...genres, newBook.genre]);
      }
    }
  };

  return (
    <article className="add-book">
      <button
        type="button"
        aria-label="add book"
        className="add-book__btn"
        onClick={() => handleHide()}
      >
        <BsPlusCircle
          id="AddBookIconPlus"
          className="add-book__btn-icon"
        ></BsPlusCircle>
      </button>

      {hide ? (
        <form
          aria-label="form add book"
          className="add-book__form"
          onSubmit={(e) => handleSubmit(e)}
        >
          <label
            htmlFor="title"
            className="add-book__form-label add-book__form-label--hide"
          >
            Title
          </label>
          <input
            id="title"
            type="text"
            name="title"
            placeholder="Set title"
            className="add-book__form-input"
            value={formState.title}
            onChange={(e) => onInputChange(e)}
          ></input>
          <label
            htmlFor="author"
            className="add-book__form-label add-book__form-label--hide"
          >
            Author
          </label>
          <input
            id="author"
            type="text"
            name="author"
            placeholder="Set author"
            className="add-book__form-input"
            value={formState.author}
            onChange={(e) => onInputChange(e)}
          ></input>
          <label
            htmlFor="genre"
            className="add-book__form-label add-book__form-label--hide"
          >
            Genre
          </label>
          <input
            id="genre"
            type="text"
            name="genre"
            placeholder="Set genre"
            className="add-book__form-input"
            value={formState.genre}
            onChange={(e) => onInputChange(e)}
          ></input>
          <label
            htmlFor="description"
            className="add-book__form-label add-book__form-label--hide"
          >
            Description
          </label>
          <textarea
            id="description"
            placeholder="Set description"
            name="description"
            className="add-book__form-textarea"
            value={formState.description}
            onChange={(e) => onInputChange(e)}
          ></textarea>
          <label
            htmlFor="image"
            className="add-book__form-label add-book__form-label--hide"
          >
            Image
          </label>
          <input
            id="image"
            type="text"
            name="image"
            placeholder="Set image link"
            className="add-book__form-input"
            value={formState.image}
            onChange={(e) => onInputChange(e)}
          ></input>
          <button
            type="submit"
            aria-label="submit"
            className="add-book__form-submit"
          >
            Submit
          </button>
        </form>
      ) : null}
    </article>
  );
};
