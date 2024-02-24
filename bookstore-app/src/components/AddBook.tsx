import { useHide } from "../hooks/useHide";
import { BsPlusCircle } from "react-icons/bs";
import { AddBookProps, FormBook } from "../entities/entities";
import { postBook } from "../api/postBook";
import { useForm } from "../hooks/useForm";

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
      <BsPlusCircle id="IconPlus" onClick={() => handleHide()}></BsPlusCircle>

      {hide ? (
        <form
          className="book_container_information"
          onSubmit={(e) => handleSubmit(e)}
        >
          <input
            type="text"
            name="title"
            placeholder="Set title"
            value={formState.title}
            onChange={(e) => onInputChange(e)}
          ></input>
          <input
            type="text"
            name="author"
            placeholder="Set author"
            value={formState.author}
            onChange={(e) => onInputChange(e)}
          ></input>
          <input
            type="text"
            name="genre"
            placeholder="Set genre"
            value={formState.genre}
            onChange={(e) => onInputChange(e)}
          ></input>
          <textarea
            placeholder="Set description"
            name="description"
            value={formState.description}
            onChange={(e) => onInputChange(e)}
          ></textarea>
          <input
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
