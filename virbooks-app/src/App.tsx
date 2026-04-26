import { Fragment } from "react/jsx-runtime";

import type { JSX } from "react";

import Header from "@/components/Header/Header";

import BooksPage from "@/pages/BooksPage/BooksPage";

function App(): JSX.Element {
  return (
    <Fragment>
      <Header></Header>
      <BooksPage></BooksPage>
    </Fragment>
  );
}

export default App;
