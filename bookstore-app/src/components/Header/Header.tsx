import { images } from "../../assets/export";

import "../../css/header.css";

export const Header = (): JSX.Element => {
  return (
    <header className="header">
      <img className="header__logo" src={images.libraryLogo} alt="logo"></img>
    </header>
  );
};
