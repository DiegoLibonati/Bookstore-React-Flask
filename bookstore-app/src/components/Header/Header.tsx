import assets from "@src/assets/export";

import "@src/components/Header/Header.css";

export const Header = (): JSX.Element => {
  return (
    <header className="header-wrapper">
      <img
        className="header-wrapper__logo"
        src={assets.images.libraryLogo}
        alt="logo"
      ></img>
    </header>
  );
};
