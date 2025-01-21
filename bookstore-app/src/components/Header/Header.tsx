import { images } from "../../assets/export";

import "./Header.css";

export const Header = (): JSX.Element => {
  return (
    <header className="header-wrapper">
      <img
        className="header-wrapper__logo"
        src={images.libraryLogo}
        alt="logo"
      ></img>
    </header>
  );
};
