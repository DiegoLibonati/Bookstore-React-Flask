import React from "react";
import { useHide } from "../hooks/useHide";
import { useState } from "react";
import { BsPlusCircle } from "react-icons/bs";
import { AddBookProps, FormBook } from "../entities/entities";
import { postBook } from "../api/postBook";

export const AddBook = ({
  books,
  genres,
  setBooks,
  setGenres,
}: AddBookProps): JSX.Element => {
  const { hide, handleHide } = useHide();

  const [form, setForm] = useState<FormBook>({
    title: "",
    author: "",
    genre: "",
    description: "",
    image: "",
  });

  const handleChangeInput: React.ChangeEventHandler<
    HTMLInputElement | HTMLTextAreaElement
  > = (e) => {
    const key = e.target.name as keyof FormBook;
    const value = e.target.value;
    setForm({ ...form, [key]: value });
  };

  const handleSubmit = async () => {
    const body = {
      title: form.title,
      author: form.author,
      description: form.description,
      image: form.image,
      genero: form.genre,
    };

    const result = await postBook(body);

    if (result.ok) {
      setBooks([...books, { ...body, _id: { $oid: body.image + "123" } }]);

      if (!genres.includes(body.genero)) {
        setGenres([...genres, body.genero]);
      }
    }
  };

  return (
    <article className="book_container">
      <BsPlusCircle id="IconPlus" onClick={() => handleHide()}></BsPlusCircle>

      {hide ? (
        <form
          className="book_container_information"
          onSubmit={() => handleSubmit()}
        >
          <input
            type="text"
            placeholder="Set title"
            value={form.title}
            onChange={(e) => handleChangeInput(e)}
          ></input>
          <input
            type="text"
            placeholder="Set author"
            value={form.author}
            onChange={(e) => handleChangeInput(e)}
          ></input>
          <input
            type="text"
            placeholder="Set genre"
            value={form.genre}
            onChange={(e) => handleChangeInput(e)}
          ></input>
          <textarea
            placeholder="Set description"
            value={form.description}
            onChange={(e) => handleChangeInput(e)}
          ></textarea>
          <input
            type="text"
            placeholder="Set image link"
            value={form.image}
            onChange={(e) => handleChangeInput(e)}
          ></input>
          <button type="submit">Submit</button>
        </form>
      ) : (
        <></>
      )}
    </article>
  );
};
