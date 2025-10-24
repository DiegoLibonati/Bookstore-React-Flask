import { Fragment } from "react/jsx-runtime";

import { Header } from "@src/components/Header/Header";

import { BooksPage } from "@src/pages/BooksPage/BooksPage";

function App(): JSX.Element {
  return (
    <Fragment>
      <Header></Header>
      <BooksPage></BooksPage>
    </Fragment>
  );
}

export default App;
